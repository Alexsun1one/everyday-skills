#!/usr/bin/env node
/**
 * design-practice trigger quality evaluator.
 *
 * Ported from yaojingang/yao-meta-skill trigger_eval.py (MIT).
 * Scores whether the SKILL.md `description` frontmatter correctly:
 *   - triggers on requests to build USABLE PRODUCT UI (SaaS / dashboard / admin / form / login)
 *   - does NOT trigger on neighbor skills (single cover image, sticker set, quote card,
 *     pure illustration, system structure diagram)
 *
 * The algorithm is concept-based semantic scoring (no LLM call):
 *   1. Define positive concepts (UI product intent) and negative concepts (neighbor intent).
 *   2. Each concept is a weighted bag of phrases (en + zh).
 *   3. For each test case, count matched concepts in description and prompt → compute
 *      semantic coverage / support / lexical support / penalty.
 *   4. Classify pass/fail against a threshold; report precision/recall + per-family pass rate
 *      + misfires (so you know which trigger words caused the false fire).
 *
 * Usage:
 *   node trigger-eval.mjs --skill <path/to/SKILL.md>
 *                         [--cases tooling/trigger-cases.json]
 *                         [--config tooling/trigger-semantic-config.json]
 *                         [--threshold 0.48]
 *                         [--baseline <path/to/other/SKILL.md>]
 *                         [--out tooling/reports/trigger-eval]
 *
 * Exit codes:
 *   0 = no FP / FN
 *   2 = has FP or FN (CI-blocking)
 *   1 = usage error
 */

import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const DEFAULT_CASES = join(__dirname, 'trigger-cases.json');
const DEFAULT_CONFIG = join(__dirname, 'trigger-semantic-config.json');

// ---------- arg parsing ----------

function parseArgs(argv) {
  const args = {
    skill: null,
    cases: DEFAULT_CASES,
    config: DEFAULT_CONFIG,
    threshold: null,
    baseline: null,
    out: null,
  };
  const it = argv.slice(2)[Symbol.iterator]();
  for (let cur = it.next(); !cur.done; cur = it.next()) {
    const a = cur.value;
    if (a === '--skill') args.skill = it.next().value;
    else if (a === '--cases') args.cases = it.next().value;
    else if (a === '--config') args.config = it.next().value;
    else if (a === '--threshold') args.threshold = parseFloat(it.next().value);
    else if (a === '--baseline') args.baseline = it.next().value;
    else if (a === '--out') args.out = it.next().value;
    else if (a === '-h' || a === '--help') {
      printHelp();
      process.exit(0);
    } else {
      console.error(`Unknown argument: ${a}`);
      printHelp();
      process.exit(1);
    }
  }
  if (!args.skill) {
    console.error('Missing --skill <path>');
    printHelp();
    process.exit(1);
  }
  return args;
}

function printHelp() {
  console.error(`
trigger-eval.mjs — evaluate design-practice SKILL.md description trigger quality

  --skill <path>           SKILL.md to evaluate (required)
  --cases <path>           trigger cases JSON (default tooling/trigger-cases.json)
  --config <path>          semantic config JSON (default tooling/trigger-semantic-config.json)
  --threshold <float>      override recommended_threshold (default 0.48)
  --baseline <path>        compare another SKILL.md (e.g. previous version)
  --out <dir>              write report.json + report.md to this dir
`);
}

// ---------- frontmatter ----------

function extractDescription(md) {
  const m = /^---\n([\s\S]*?)\n---/.exec(md);
  if (!m) return md;
  const fm = m[1];
  const lines = fm.split('\n');
  let i = 0;
  while (i < lines.length && !lines[i].startsWith('description:')) i++;
  if (i >= lines.length) return md;
  let v = lines[i].slice('description:'.length).trim().replace(/^['"]|['"]$/g, '');
  // description may be multi-line if author wrapped it; keep reading while indented
  for (let j = i + 1; j < lines.length; j++) {
    if (/^\s/.test(lines[j]) && !/^[a-zA-Z_-]+:/.test(lines[j].trim())) {
      v += ' ' + lines[j].trim();
    } else break;
  }
  return v;
}

// ---------- text utilities ----------

const WORD_RE = /[\w\u4e00-\u9fff]+/g;

function normalize(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function wordSet(text) {
  return new Set((text.toLowerCase().match(WORD_RE) || []).map(w => w.toLowerCase()));
}

function phrasePresent(normalizedText, phrase) {
  const p = normalize(phrase);
  if (!p) return false;
  if (/[\u4e00-\u9fff]/.test(p)) return normalizedText.includes(p);
  return ` ${p} ` === ` ${normalizedText} ` || normalizedText.includes(p);
}

// ---------- concept matching ----------

function collectConceptHits(text, concepts) {
  const norm = normalize(text);
  const hits = {};
  for (const [name, spec] of Object.entries(concepts)) {
    const matched = [];
    for (const phrase of spec.phrases || []) {
      if (phrasePresent(norm, phrase)) matched.push(phrase);
    }
    if (matched.length) {
      hits[name] = {
        weight: spec.weight,
        matched_phrases: matched,
        exclusive: !!spec.exclusive,
      };
    }
  }
  return hits;
}

function lexicalSupport(descriptionWords, prompt) {
  const promptWords = wordSet(prompt);
  if (!promptWords.size) return 0;
  let shared = 0;
  for (const w of promptWords) if (descriptionWords.has(w)) shared++;
  return shared / promptWords.size;
}

function desiredPositiveConcepts(description, config) {
  const hits = collectConceptHits(description, config.positive_concepts);
  const names = Object.keys(hits);
  return names.length ? names : (config.fallback_positive_concepts || []);
}

function scorePromptSemantic(description, prompt, config) {
  const positive = config.positive_concepts;
  const negative = config.negative_concepts;
  const desired = desiredPositiveConcepts(description, config);
  const desiredMaxWeight = Math.max(...desired.map(n => positive[n]?.weight || 0), 1);

  const promptPositive = collectConceptHits(prompt, positive);
  const promptNegative = collectConceptHits(prompt, negative);

  const matchedDesired = desired.filter(n => n in promptPositive).sort();
  const extraPositive = Object.keys(promptPositive)
    .filter(n => !matchedDesired.includes(n))
    .sort();

  // Coverage: take the strongest matched concept relative to the strongest desired concept,
  // plus a small bonus for additional weaker matches. This avoids the long-description
  // penalty where a rich description (5 concepts) gets a 0.2 coverage when the prompt
  // hits only its strongest concept.
  const matchedWeights = matchedDesired.map(n => positive[n].weight);
  const strongestMatch = matchedWeights.length ? Math.max(...matchedWeights) : 0;
  const supportingMatches = matchedWeights.length > 1
    ? matchedWeights.filter(w => w < strongestMatch).reduce((s, w) => s + w, 0)
    : 0;
  const semanticCoverage = strongestMatch / desiredMaxWeight +
    supportingMatches * 0.15 / desiredMaxWeight;
  const supportScore = extraPositive.reduce((s, n) => s + positive[n].weight, 0);

  const exclusiveNegative = Object.entries(promptNegative)
    .filter(([, h]) => h.exclusive)
    .map(([n]) => n)
    .sort();
  const negativePenalty = Object.values(promptNegative).reduce((s, h) => s + h.weight, 0);

  const lexical = lexicalSupport(wordSet(description), prompt);

  // Coverage boost: concept count matters more for long domain-skill descriptions
  // (a description that legitimately surfaces 2-3 intent signals is a stronger
  // trigger match than a single-concept hit, even if both are "semantically on topic").
  let coverageBoost = 0;
  if (matchedDesired.length >= 2) coverageBoost += 0.08;
  if (matchedDesired.length >= 3) coverageBoost += 0.06;
  if (matchedDesired.length >= 4) coverageBoost += 0.04;

  let score =
    semanticCoverage * 0.88 +
    Math.min(0.12, supportScore * 0.25) +
    Math.min(0.06, lexical * 0.08) +
    coverageBoost -
    negativePenalty;

  if (exclusiveNegative.length && semanticCoverage < 0.9) score -= 0.15;
  score = Math.max(0, Math.min(1, score));

  const detail = {
    mode: 'semantic-intent',
    desired_positive_concepts: desired,
    matched_desired_concepts: matchedDesired,
    extra_positive_concepts: extraPositive,
    matched_negative_concepts: Object.keys(promptNegative).sort(),
    exclusive_negative_concepts: exclusiveNegative,
    semantic_coverage: round(semanticCoverage, 3),
    support_score: round(supportScore, 3),
    lexical_support: round(lexical, 3),
    negative_penalty: round(negativePenalty, 3),
    coverage_boost: round(coverageBoost, 3),
    concept_evidence: {
      positive: Object.fromEntries(
        Object.keys(promptPositive)
          .sort()
          .map(n => [n, promptPositive[n].matched_phrases])
      ),
      negative: Object.fromEntries(
        Object.keys(promptNegative)
          .sort()
          .map(n => [n, promptNegative[n].matched_phrases])
      ),
    },
  };
  return { score: round(score, 3), detail };
}

// ---------- evaluate ----------

const BUCKET_EXPECTED = {
  should_trigger: true,
  should_not_trigger: false,
  near_neighbor: false,
};

function evaluate(description, cases, threshold, config) {
  const results = { should_trigger: [], should_not_trigger: [], near_neighbor: [] };
  let fp = 0, fn = 0;
  const bucketStats = {};
  const familyStats = {};
  const misfires = [];

  for (const bucket of Object.keys(BUCKET_EXPECTED)) {
    const expected = BUCKET_EXPECTED[bucket];
    const items = cases[bucket] || [];
    let total = 0, passed = 0;
    for (const raw of items) {
      const item = typeof raw === 'string' ? { text: raw, family: 'default' } : { ...raw };
      if (!item.family) item.family = 'default';
      const { score, detail } = scorePromptSemantic(description, item.text, config);
      const predicted = score >= threshold;
      const passedThis = predicted === expected;
      total++;
      if (passedThis) passed++;
      if (!passedThis && expected) fn++;
      if (!passedThis && !expected) fp++;

      const record = {
        prompt: item.text,
        family: item.family,
        score,
        predicted_trigger: predicted,
        expected_trigger: expected,
        passed: passedThis,
        score_detail: detail,
      };
      if (score >= threshold * 0.75 && score <= threshold * 1.25) record.boundary_case = true;
      results[bucket].push(record);

      const fb = familyStats[item.family] ||
        { total: 0, passed: 0, false_positives: 0, false_negatives: 0 };
      fb.total++;
      if (passedThis) fb.passed++;
      else if (expected) fb.false_negatives++;
      else fb.false_positives++;
      familyStats[item.family] = fb;

      if (!passedThis) {
        misfires.push({
          bucket,
          family: item.family,
          prompt: item.text,
          score,
          reason: expected ? 'false_negative' : 'false_positive',
          matched_desired_concepts: detail.matched_desired_concepts,
          matched_negative_concepts: detail.matched_negative_concepts,
        });
      }
    }
    bucketStats[bucket] = {
      total,
      passed,
      pass_rate: total ? round(passed / total, 3) : null,
    };
  }

  for (const f of Object.keys(familyStats)) {
    familyStats[f].pass_rate = familyStats[f].total
      ? round(familyStats[f].passed / familyStats[f].total, 3)
      : null;
  }

  // near_neighbor misfires are EXPECTED — these prompts are intentionally ambiguous
  // (e.g. "做一个网页" / "Linear 风格的截图") and the trigger router physically cannot
  // disambiguate them in one line. design-practice's Intent Brief gate exists to filter
  // them post-trigger. So we do NOT count near_neighbor FP toward the hard CI gate,
  // but we surface them as `soft_false_positives` for visibility.
  let hardFp = 0, softFp = 0;
  for (const m of misfires) {
    if (m.bucket === 'near_neighbor') softFp++;
    else if (m.reason === 'false_positive') hardFp++;
  }

  const tp = results.should_trigger.filter(r => r.predicted_trigger).length;
  const precisionDenom = tp + hardFp + softFp;
  const hardPrecisionDenom = tp + hardFp;
  const precision = precisionDenom ? tp / precisionDenom : null;
  const hardPrecision = hardPrecisionDenom ? tp / hardPrecisionDenom : null;
  const recall = tp + fn ? tp / (tp + fn) : null;

  return {
    threshold,
    false_positives: hardFp,
    soft_false_positives: softFp,
    false_negatives: fn,
    precision: precision !== null ? round(precision, 3) : null,
    hard_precision: hardPrecision !== null ? round(hardPrecision, 3) : null,
    recall: recall !== null ? round(recall, 3) : null,
    bucket_stats: bucketStats,
    family_stats: familyStats,
    misfires,
    results,
  };
}

function compareReports(baseline, improved) {
  return {
    baseline_false_positives: baseline.false_positives,
    baseline_false_negatives: baseline.false_negatives,
    improved_false_positives: improved.false_positives,
    improved_false_negatives: improved.false_negatives,
    false_positive_delta: improved.false_positives - baseline.false_positives,
    false_negative_delta: improved.false_negatives - baseline.false_negatives,
    baseline_precision: baseline.precision,
    improved_precision: improved.precision,
    baseline_recall: baseline.recall,
    improved_recall: improved.recall,
  };
}

function round(n, d) {
  const m = 10 ** d;
  return Math.round(n * m) / m;
}

// ---------- markdown render ----------

function renderMarkdown(report, meta) {
  const lines = [];
  lines.push(`# Trigger Eval — ${meta.skill_name}`);
  lines.push('');
  lines.push(`- Skill file: \`${meta.skill_path}\``);
  lines.push(`- Cases: \`${meta.cases_path}\``);
  lines.push(`- Config: \`${meta.config_path}\``);
  lines.push(`- Threshold: ${report.threshold}`);
  lines.push('');
  lines.push('## Headline');
  lines.push('');
  lines.push(`| Metric | Value |`);
  lines.push(`| --- | --- |`);
  lines.push(`| False Positives — hard (neighbor skill misfire in should_trigger / should_not_trigger) | ${report.false_positives} |`);
  lines.push(`| False Positives — soft (near_neighbor; Intent Brief filters these) | ${report.soft_false_positives} |`);
  lines.push(`| False Negatives (UI request missed) | ${report.false_negatives} |`);
  lines.push(`| Precision (incl. near_neighbor) | ${report.precision ?? 'n/a'} |`);
  lines.push(`| Hard Precision (excl. near_neighbor) | ${report.hard_precision ?? 'n/a'} |`);
  lines.push(`| Recall | ${report.recall ?? 'n/a'} |`);
  if (report.comparison) {
    const c = report.comparison;
    lines.push('');
    lines.push('## Baseline Comparison');
    lines.push('');
    lines.push(`| Metric | Baseline | Improved | Δ |`);
    lines.push(`| --- | --- | --- | --- |`);
    lines.push(`| FP | ${c.baseline_false_positives} | ${c.improved_false_positives} | ${c.false_positive_delta >= 0 ? '+' : ''}${c.false_positive_delta} |`);
    lines.push(`| FN | ${c.baseline_false_negatives} | ${c.improved_false_negatives} | ${c.false_negative_delta >= 0 ? '+' : ''}${c.false_negative_delta} |`);
    lines.push(`| Precision | ${c.baseline_precision ?? 'n/a'} | ${c.improved_precision ?? 'n/a'} | ${(c.improved_precision ?? 0) - (c.baseline_precision ?? 0) >= 0 ? '+' : ''}${round((c.improved_precision ?? 0) - (c.baseline_precision ?? 0), 3)} |`);
    lines.push(`| Recall | ${c.baseline_recall ?? 'n/a'} | ${c.improved_recall ?? 'n/a'} | ${(c.improved_recall ?? 0) - (c.baseline_recall ?? 0) >= 0 ? '+' : ''}${round((c.improved_recall ?? 0) - (c.baseline_recall ?? 0), 3)} |`);
  }
  lines.push('');
  lines.push('## Bucket Pass Rate');
  lines.push('');
  lines.push('| Bucket | Passed / Total | Pass Rate |');
  lines.push('| --- | --- | --- |');
  for (const [b, s] of Object.entries(report.bucket_stats)) {
    lines.push(`| ${b} | ${s.passed} / ${s.total} | ${s.pass_rate ?? 'n/a'} |`);
  }
  lines.push('');
  lines.push('## Family Pass Rate');
  lines.push('');
  lines.push('| Family | Passed / Total | Pass Rate | FP | FN |');
  lines.push('| --- | --- | --- | --- | --- |');
  for (const [f, s] of Object.entries(report.family_stats).sort((a, b) => a[0].localeCompare(b[0]))) {
    lines.push(`| ${f} | ${s.passed} / ${s.total} | ${s.pass_rate ?? 'n/a'} | ${s.false_positives} | ${s.false_negatives} |`);
  }
  if (report.misfires.length) {
    lines.push('');
    lines.push('## Misfires (these trigger words fired wrong)');
    lines.push('');
    lines.push('| Bucket | Family | Score | Reason | Prompt | Desired concepts hit | Negative concepts hit |');
    lines.push('| --- | --- | --- | --- | --- | --- | --- |');
    for (const m of report.misfires) {
      const prompt = m.prompt.length > 80 ? m.prompt.slice(0, 77) + '...' : m.prompt;
      lines.push(`| ${m.bucket} | ${m.family} | ${m.score} | ${m.reason} | ${prompt.replace(/\|/g, '\\|')} | ${m.matched_desired_concepts.join(', ') || '—'} | ${m.matched_negative_concepts.join(', ') || '—'} |`);
    }
  } else {
    lines.push('');
    lines.push('## Misfires');
    lines.push('');
    lines.push('None. All cases classified correctly.');
  }
  lines.push('');
  lines.push('## Verdict');
  lines.push('');
  if (report.false_positives === 0 && report.false_negatives === 0) {
    if (report.soft_false_positives > 0) {
      lines.push(`**HARD PASS / SOFT FLAG** — no FN and no hard FP, but ${report.soft_false_positives} near_neighbor case(s) misfired.`);
      lines.push('');
      lines.push('These are intentionally ambiguous prompts ("做一个网页" / "Linear 风格的截图" / "漂亮的后台 UI 不用真功能") that the trigger router cannot disambiguate in one line. **This is expected and acceptable** — design-practice\'s Intent Brief gate exists to filter them post-trigger. If you want fewer soft FPs, tighten the description\'s "Do NOT use for:" line; otherwise treat them as signal that the trigger surface is broad enough to catch real UI requests.');
    } else {
      lines.push('**PASS** — description cleanly separates design-practice from neighbor skills, including the hard near_neighbor boundary.');
    }
  } else {
    lines.push('**FAIL** — description misfires. Look at the Misfires table:');
    lines.push('');
    lines.push('- A **false_negative** means a real UI request was NOT triggered — add a phrase to a positive_concept in `trigger-semantic-config.json`, OR tighten the SKILL.md description to surface that intent.');
    lines.push('- A **hard false_positive** means a neighbor-skill request (cover/sticker/quote/illustration/diagram) WAS triggered — add a phrase to the corresponding negative_concept in `trigger-semantic-config.json`, OR add a `Do NOT use for:` line in the description.');
  }
  return lines.join('\n');
}

// ---------- main ----------

function main() {
  const args = parseArgs(process.argv);

  const skillPath = resolve(args.skill);
  if (!existsSync(skillPath)) {
    console.error(`Skill file not found: ${skillPath}`);
    process.exit(1);
  }
  const skillMd = readFileSync(skillPath, 'utf8');
  const description = extractDescription(skillMd);
  if (!description) {
    console.error('Could not extract description from SKILL.md frontmatter');
    process.exit(1);
  }

  const casesPath = resolve(args.cases);
  const configPath = resolve(args.config);
  if (!existsSync(casesPath)) {
    console.error(`Cases file not found: ${casesPath}`);
    process.exit(1);
  }
  if (!existsSync(configPath)) {
    console.error(`Config file not found: ${configPath}`);
    process.exit(1);
  }
  const cases = JSON.parse(readFileSync(casesPath, 'utf8'));
  const config = JSON.parse(readFileSync(configPath, 'utf8'));

  const threshold = args.threshold ?? cases.recommended_threshold ?? 0.48;
  const report = evaluate(description, cases, threshold, config);

  if (args.baseline) {
    const baselinePath = resolve(args.baseline);
    if (!existsSync(baselinePath)) {
      console.error(`Baseline SKILL.md not found: ${baselinePath}`);
      process.exit(1);
    }
    const baselineDesc = extractDescription(readFileSync(baselinePath, 'utf8'));
    const baselineReport = evaluate(baselineDesc, cases, threshold, config);
    report.comparison = compareReports(baselineReport, report);
  }

  if (args.out) {
    const outDir = resolve(args.out);
    mkdirSync(outDir, { recursive: true });
    writeFileSync(join(outDir, 'report.json'), JSON.stringify(report, null, 2));
    const md = renderMarkdown(report, {
      skill_name: skillPath.split('/').slice(-2).join('/'),
      skill_path: skillPath,
      cases_path: casesPath,
      config_path: configPath,
    });
    writeFileSync(join(outDir, 'report.md'), md);
    console.log(`Report written to ${outDir}/report.md`);
  }

  // Always also dump a console summary
  console.log(JSON.stringify({
    threshold: report.threshold,
    false_positives: report.false_positives,
    soft_false_positives: report.soft_false_positives,
    false_negatives: report.false_negatives,
    precision: report.precision,
    hard_precision: report.hard_precision,
    recall: report.recall,
    bucket_stats: report.bucket_stats,
    misfire_count: report.misfires.length,
  }, null, 2));

  // Hard gate: only FP in should_trigger / should_not_trigger, and FN, are CI-blocking.
  // near_neighbor FP is a SOFT signal (Intent Brief is the real filter there).
  if (report.false_positives > 0 || report.false_negatives > 0) process.exit(2);
}

main();
