#!/usr/bin/env node
/**
 * design-practice context budget + resource boundary audit.
 *
 * Adapted from yaojingang/yao-meta-skill context_sizer.py + resource_boundary_check.py (MIT).
 *
 * The YAO thresholds (1000-1300 token initial budget, 80% skill-body ratio) are tuned
 * for small conversational skills. design-practice is a DEEP DOMAIN skill — its SKILL.md
 * alone legitimately runs 8-10k tokens, and its references/ library is supposed to be
 * large (the whole point is per-stage on-demand depth, not initial load).
 *
 * So this tool asks the questions that actually matter for THIS skill:
 *
 *   1. INITIAL LOAD — what does an agent eat if it reads SKILL.md + AGENTS.md + the
 *      few files SKILL.md explicitly points to as "read FIRST"? That's the real
 *      initial load, not "SKILL.md alone".
 *   2. ON-DEMAND DEPTH — what's the per-stage budget? When the agent enters Stage 0,
 *      how much does it eat? Stage 1? Stage 2? Stage 3? Each stage should fit in
 *      a reasonable context window so the agent can actually do its job.
 *   3. DECORATIVE FILES — files that exist but aren't referenced by SKILL.md, the
 *      stage playbooks, or any other entry path. These are dead weight.
 *   4. TOP-HEAVY FILES — individual files >4k tokens. Candidates for splitting.
 *   5. SHOWCASE DEBT — showcase directories with no index.html (the live samples
 *      the skill is supposed to produce; missing = the skill's claim is unverified).
 *
 * Usage:
 *   node context-budget.mjs [--root <path>] [--out <dir>] [--json]
 *
 * Exit codes:
 *   0 = budget pass (within thresholds, no decorative files)
 *   2 = budget fail (initial load > threshold, or decorative files found)
 *   1 = usage error
 */

import { readFileSync, existsSync, statSync, readdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, relative, join, dirname, basename, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------- config ----------

const TEXT_EXTS = new Set(['.md', '.json', '.yaml', '.yml', '.js', '.mjs', '.ts', '.css', '.html', '.txt']);
const IGNORED_DIRS = new Set([
  'node_modules',
  '.git',
  'reports',        // tooling output
  '.DS_Store',
  '_extract',       // raw scraped token data — asset, not agent context
  '.playwright-mcp',
  '.omx',
]);
const IGNORED_FILES = new Set([
  'source-full.md',           // full article source — reference asset, not agent context
  'COMMERCIALIZATION.md',     // business notes, not skill content
  'demo-crm.html',            // superseded by showcase-crm
  'demo-crm-v2.html',
  'demo-crm-v3.html',
  'full2x2-replay.png',
]);
const IGNORED_REPORT_SUBDIR = 'tooling/reports';

// design-practice specific: the "real" initial load isn't just SKILL.md, it's
// SKILL.md + the files it explicitly points agents to read FIRST.
const INITIAL_LOAD_FILES = [
  'SKILL.md',
  'AGENTS.md',
];
const INITIAL_LOAD_DIRS_REFERENCED = [
  // Files SKILL.md explicitly tells agents to read first (from the Executable Core + Depth Layers)
  'references/agent-playbook.md',
  'references/intent-reading.md',
  'references/fast-path.md',
];

// Stage-specific reference bundles. When the agent enters a stage, it reads these.
const STAGE_BUNDLES = {
  'Stage 0 — Judgment': [
    'design-judgment/README.md',
    'design-judgment/00-principles.md',
    'design-judgment/01-task-field.md',
    'design-judgment/02-complexity-conservation.md',
    'design-judgment/03-true-vs-empty-simple.md',
    'design-judgment/04-visual-hierarchy.md',
    'design-judgment/05-task-network.md',
  ],
  'Stage 0.5 — Patterns': [
    'patterns/README.md',
    'patterns/01-list-detail.md',
    'patterns/02-complex-flow.md',
    'patterns/03-container-decision.md',
    'patterns/04-feedback-decision.md',
    'patterns/05-design-system-governance.md',
    'patterns/06-progressive-disclosure.md',
    'patterns/07-case-dissection-dictionary.md',
  ],
  'Stage 1 — Drafts': [
    'references/stage1-five-layer.md',
    'references/stage1-intent-routing.md',
    'references/stage1-task-card.md',
    'references/stage1-divergence.md',
    'references/stage1-output-formats.md',
    'references/stage1-state-variants.md',
    'references/stage1-object-state-permission.md',
    'references/stage1-tradeoff.md',
    'references/stage1-wireframe-rules.md',
    'references/stage1-ia-containers.md',
    'references/variation-engine.md',
  ],
  'Stage 2 — Restore': [
    'references/stage2-design-tokens.md',
    'references/stage2-button-8-states.md',
    'references/stage2-microinteractions.md',
    'references/stage2-motion-discipline.md',
    'references/stage2-fidelity-restore.md',
    'references/anti-plastic-fix-guide.md',
  ],
  'Stage 3 — Render Loop': [
    'references/rubric-10d.md',
    'references/stage3-render-refine-loop.md',
    'references/craft-details-invisible.md',
    'references/micro-interactions-liveness.md',
    'references/quality-landscape.md',
    'tooling/README.md',
  ],
  'Workflow': [
    'workflow/README.md',
    'workflow/01-ten-step-flow.md',
    'workflow/02-design-task-brief.md',
    'workflow/03-ai-collaboration-roles.md',
    'workflow/04-p0p1p2-review.md',
    'workflow/05-eight-step-project.md',
  ],
  'Components (pixel layer)': null, // computed: max single component file (agent reads per-need, not all 14)
  'Visual Language (skin layer)': null, // computed: all visual-language/*.md (agent picks ONE style DNA)
  'QA (self-inspection)': [
    'references/qa-page-five-questions.md',
    'references/qa-state-acceptance.md',
    'references/qa-a11y.md',
    'references/qa-responsive.md',
    'references/qa-bad-data.md',
    'references/qa-three-gates.md',
    'references/qa-p0p1p2.md',
    'references/qa-restore-fidelity.md',
    'references/qa-mosaic-check.md',
  ],
};

// Thresholds calibrated for design-practice (NOT YAO's small-skill defaults).
const THRESHOLDS = {
  initial_load_warn: 15000,   // tokens — agent can handle this in a focused session
  initial_load_fail: 30000,   // tokens — too much, agent will lose the thread
  stage_bundle_warn: 12000,   // per stage
  stage_bundle_fail: 25000,   // per stage — agent can't hold this much in working memory
  file_split_threshold: 4000, // individual file at this size is a split candidate
  showcase_required: ['showcase'], // these dirs MUST have an index.html (skill's claim of "live samples")
};

// ---------- helpers ----------

function estimateTokens(text) {
  // 4 chars/token is the standard rough heuristic; CJK is denser (~2-3 chars/token for pure CJK),
  // but mixed CJK+latin averages out close to 4. YAO uses 4 too.
  return Math.max(1, Math.round(text.length / 4));
}

function isText(p) {
  return TEXT_EXTS.has(extname(p).toLowerCase());
}

function walkDir(root, out = []) {
  const entries = readdirSync(root, { withFileTypes: true });
  for (const e of entries) {
    if (IGNORED_DIRS.has(e.name)) continue;
    const full = join(root, e.name);
    if (e.isDirectory()) walkDir(full, out);
    else if (e.isFile() && isText(e.name) && !IGNORED_FILES.has(e.name)) out.push(full);
  }
  return out;
}

function readText(p) {
  try {
    return readFileSync(p, 'utf8');
  } catch {
    try {
      return readFileSync(p, 'utf8');
    } catch {
      return '';
    }
  }
}

function rel(p, root) {
  return relative(root, p);
}

// ---------- core analysis ----------

function scanAllFiles(root) {
  const all = [];
  const entries = readdirSync(root, { withFileTypes: true });
  for (const e of entries) {
    if (IGNORED_DIRS.has(e.name)) continue;
    const full = join(root, e.name);
    if (e.isDirectory()) {
      walkDir(full, all);
    } else if (e.isFile() && isText(e.name) && !IGNORED_FILES.has(e.name)) {
      all.push(full);
    }
  }
  // Exclude tooling/reports subtree explicitly (already ignored by IGNORED_DIRS check on 'reports',
  // but the dir is named 'reports' under tooling/ — handle that).
  return all.filter(p => {
    const r = rel(p, root);
    if (r.startsWith(join('tooling', 'reports'))) return false;
    // Exclude any path that contains an ignored dir anywhere
    const parts = r.split('/');
    if (parts.some(seg => IGNORED_DIRS.has(seg))) return false;
    if (IGNORED_FILES.has(basename(r))) return false;
    return true;
  });
}

function fileSize(p) {
  return readText(p).length;
}

function tokensFor(p) {
  return estimateTokens(readText(p));
}

function resolveBundle(root, bundle) {
  if (!bundle) return [];
  return bundle
    .map(f => join(root, f))
    .filter(p => existsSync(p))
    .map(p => ({ path: rel(p, root), tokens: tokensFor(p) }));
}

function resolveDirBundle(root, dir) {
  const dirPath = join(root, dir);
  if (!existsSync(dirPath)) return [];
  return walkDir(dirPath)
    .map(p => ({ path: rel(p, root), tokens: tokensFor(p) }));
}

function findDecorativeFiles(root, allFiles, referencedSet) {
  // A file is "decorative" if it's a .md file NOT in the referenced set AND
  // NOT referenced by name from any other .md file.
  // Conservative: only flag .md files (the primary knowledge medium).
  const mdFiles = allFiles.filter(p => p.endsWith('.md'));
  const decorative = [];
  for (const p of mdFiles) {
    const r = rel(p, root);
    if (referencedSet.has(r)) continue;
    // Check if the basename is mentioned anywhere else
    const base = basename(p);
    let mentioned = false;
    for (const other of mdFiles) {
      if (other === p) continue;
      const otherText = readText(other);
      if (otherText.includes(base) || otherText.includes(r)) {
        mentioned = true;
        break;
      }
    }
    if (!mentioned) decorative.push({ path: r, tokens: tokensFor(p) });
  }
  return decorative;
}

function findTopHeavyFiles(root, allFiles) {
  const threshold = THRESHOLDS.file_split_threshold;
  return allFiles
    .map(p => ({ path: rel(p, root), tokens: tokensFor(p) }))
    .filter(f => f.tokens >= threshold)
    .sort((a, b) => b.tokens - a.tokens);
}

function findShowcaseDebt(root) {
  // Showcase dirs that should have an index.html but don't
  const debt = [];
  const required = THRESHOLDS.showcase_required;
  for (const dir of required) {
    const idx = join(root, dir, 'index.html');
    if (!existsSync(idx)) {
      // count what IS in the dir, if anything
      const dirPath = join(root, dir);
      let extras = [];
      if (existsSync(dirPath)) {
        extras = readdirSync(dirPath).filter(f => !f.startsWith('.'));
      }
      debt.push({ dir, missing: 'index.html', present: extras });
    }
  }
  // also check showcase-* dirs declared in AGENTS.md
  const all = readdirSync(root, { withFileTypes: true });
  for (const e of all) {
    if (e.isDirectory() && e.name.startsWith('showcase-')) {
      const idx = join(root, e.name, 'index.html');
      if (!existsSync(idx)) {
        const present = readdirSync(join(root, e.name)).filter(f => !f.startsWith('.'));
        debt.push({ dir: e.name, missing: 'index.html', present });
      }
    }
  }
  return debt;
}

function computeInitialLoad(root) {
  const files = [];
  let total = 0;
  for (const f of INITIAL_LOAD_FILES) {
    const p = join(root, f);
    if (existsSync(p)) {
      const t = tokensFor(p);
      files.push({ path: f, tokens: t });
      total += t;
    }
  }
  for (const f of INITIAL_LOAD_DIRS_REFERENCED) {
    const p = join(root, f);
    if (existsSync(p)) {
      const t = tokensFor(p);
      files.push({ path: f, tokens: t });
      total += t;
    }
  }
  return { files, total };
}

function computeStageBundles(root) {
  const out = {};
  for (const [name, bundle] of Object.entries(STAGE_BUNDLES)) {
    let files;
    let mode = 'sum';
    if (name.startsWith('Components')) {
      // Agent reads components per-need (SKILL.md E6): "list components the page contains,
      // open each file". So measure MAX single file, not SUM — a typical page pulls 4-6 components.
      const all = resolveDirBundle(root, 'components');
      const max = all.length ? Math.max(...all.map(f => f.tokens)) : 0;
      out[name] = {
        files: all,
        total: max,
        mode: 'max-single-file',
        typical_pull: Math.round(all.sort((a, b) => b.tokens - a.tokens).slice(0, 5).reduce((s, f) => s + f.tokens, 0)),
        note: 'Agent reads per-need; shown value is the largest single component file. "Typical pull" = top 5 components sum (a dense page).',
      };
    } else if (name.startsWith('Visual Language')) {
      // Agent picks ONE style DNA based on Intent Brief — not all five at once.
      const all = resolveDirBundle(root, 'visual-language').filter(f => !f.path.endsWith('README.md') && !f.path.endsWith('icon-systems.md'));
      const max = all.length ? Math.max(...all.map(f => f.tokens)) : 0;
      out[name] = {
        files: all,
        total: max + (existsSync(join(root, 'visual-language/README.md')) ? tokensFor(join(root, 'visual-language/README.md')) : 0),
        mode: 'max-single-style + README',
        note: 'Agent reads README.md (selector) + ONE style file based on Intent Brief. Shown value = README + largest style file.',
      };
    } else {
      files = resolveBundle(root, bundle);
      const total = files.reduce((s, f) => s + f.tokens, 0);
      out[name] = { files, total, mode: 'sum' };
    }
  }
  return out;
}

function buildReferencedSet(root) {
  // Union of all files mentioned in initial load + all stage bundles
  const set = new Set();
  for (const f of INITIAL_LOAD_FILES) set.add(f);
  for (const f of INITIAL_LOAD_DIRS_REFERENCED) set.add(f);
  for (const [, bundle] of Object.entries(STAGE_BUNDLES)) {
    if (!bundle) continue;
    for (const f of bundle) set.add(f);
  }
  // Add all components + visual-language (always part of the contract)
  for (const d of ['components', 'visual-language']) {
    const dirPath = join(root, d);
    if (existsSync(dirPath)) {
      for (const p of walkDir(dirPath)) set.add(rel(p, root));
    }
  }
  // Add SKILL.md references that look like file paths
  const skillText = existsSync(join(root, 'SKILL.md')) ? readText(join(root, 'SKILL.md')) : '';
  const refMatches = [...skillText.matchAll(/[`\b]([a-zA-Z0-9_-]+\/[a-zA-Z0-9_./-]+\.md|[a-zA-Z0-9_-]+\/[a-zA-Z0-9_./-]+\.(?:json|mjs|html))[`\b]/g)];
  for (const m of refMatches) set.add(m[1]);
  return set;
}

function analyze(root) {
  const allFiles = scanAllFiles(root);
  const initialLoad = computeInitialLoad(root);
  const stageBundles = computeStageBundles(root);
  const referencedSet = buildReferencedSet(root);
  const decorative = findDecorativeFiles(root, allFiles, referencedSet);
  const topHeavy = findTopHeavyFiles(root, allFiles);
  const showcaseDebt = findShowcaseDebt(root);

  const totalTextTokens = allFiles.reduce((s, p) => s + tokensFor(p), 0);

  // per-directory breakdown
  const dirBreakdown = {};
  for (const p of allFiles) {
    const r = rel(p, root);
    const topDir = r.includes('/') ? r.slice(0, r.indexOf('/')) : r;
    if (!dirBreakdown[topDir]) dirBreakdown[topDir] = { files: 0, tokens: 0 };
    dirBreakdown[topDir].files++;
    dirBreakdown[topDir].tokens += tokensFor(p);
  }

  // verdict
  const failures = [];
  const warnings = [];
  if (initialLoad.total > THRESHOLDS.initial_load_fail) {
    failures.push(`Initial load ${initialLoad.total}t > ${THRESHOLDS.initial_load_fail}t — agent will lose the thread before doing any work.`);
  } else if (initialLoad.total > THRESHOLDS.initial_load_warn) {
    warnings.push(`Initial load ${initialLoad.total}t > ${THRESHOLDS.initial_load_warn}t — heavy, consider trimming.`);
  }
  for (const [name, b] of Object.entries(stageBundles)) {
    if (b.total > THRESHOLDS.stage_bundle_fail) {
      failures.push(`${name} bundle ${b.total}t > ${THRESHOLDS.stage_bundle_fail}t — agent can't hold this in working memory.`);
    } else if (b.total > THRESHOLDS.stage_bundle_warn) {
      warnings.push(`${name} bundle ${b.total}t > ${THRESHOLDS.stage_bundle_warn}t — heavy, may need sub-staging.`);
    }
  }
  if (decorative.length > 0) {
    warnings.push(`${decorative.length} decorative .md file(s) — not in any entry path, not referenced by name elsewhere.`);
  }
  if (showcaseDebt.length > 0) {
    warnings.push(`${showcaseDebt.length} showcase dir(s) missing index.html — skill's "live sample" claim is unverified for these.`);
  }

  return {
    ok: failures.length === 0,
    failures,
    warnings,
    stats: {
      total_text_tokens: totalTextTokens,
      total_files: allFiles.length,
      initial_load: initialLoad,
      stage_bundles: Object.fromEntries(
        Object.entries(stageBundles).map(([k, v]) => [k, {
          total: v.total,
          file_count: v.files.length,
          mode: v.mode || 'sum',
          note: v.note,
          typical_pull: v.typical_pull,
        }])
      ),
      dir_breakdown: dirBreakdown,
      decorative_files: decorative,
      top_heavy_files: topHeavy,
      showcase_debt: showcaseDebt,
    },
    thresholds: THRESHOLDS,
  };
}

// ---------- markdown render ----------

function renderMarkdown(report, rootPath) {
  const L = [];
  const s = report.stats;
  L.push(`# Context Budget — ${rootPath}`);
  L.push('');
  L.push('## Headline');
  L.push('');
  L.push('| Metric | Value | Threshold |');
  L.push('| --- | --- | --- |');
  L.push(`| Initial-load tokens | ${s.initial_load.total} | warn ${THRESHOLDS.initial_load_warn} / fail ${THRESHOLDS.initial_load_fail} |`);
  L.push(`| Total text tokens (whole repo, excl node_modules) | ${s.total_text_tokens} | — |`);
  L.push(`| Decorative .md files (not in any entry path) | ${s.decorative_files.length} | 0 ideal |`);
  L.push(`| Top-heavy files (≥${THRESHOLDS.file_split_threshold}t) | ${s.top_heavy_files.length} | split candidates |`);
  L.push(`| Showcase dirs missing index.html | ${s.showcase_debt.length} | 0 required |`);
  L.push('');
  L.push('## Verdict');
  L.push('');
  if (report.ok) {
    if (report.warnings.length === 0) {
      L.push('**PASS** — initial load and every stage bundle within budget; no decorative files.');
    } else {
      L.push('**PASS (with warnings)** — within budget, but address these to keep the skill healthy:');
      for (const w of report.warnings) L.push(`- ${w}`);
    }
  } else {
    L.push('**FAIL**:');
    for (const f of report.failures) L.push(`- ${f}`);
    for (const w of report.warnings) L.push(`- (warn) ${w}`);
  }
  L.push('');
  L.push('## Initial Load (what an agent reads to start)');
  L.push('');
  L.push('| File | Tokens |');
  L.push('| --- | --- |');
  for (const f of s.initial_load.files) L.push(`| ${f.path} | ${f.tokens} |`);
  L.push(`| **TOTAL** | **${s.initial_load.total}** |`);
  L.push('');
  L.push('## Per-Stage Bundle Size');
  L.push('');
  L.push('When the agent enters each stage, this is what it eats.');
  L.push('');
  L.push('| Stage | Files | Tokens | Threshold |');
  L.push('| --- | --- | --- | --- |');
  for (const [name, b] of Object.entries(s.stage_bundles)) {
    const t = b.total;
    const mode = b.mode || 'sum';
    const flag = t > THRESHOLDS.stage_bundle_fail ? '❌ FAIL'
      : t > THRESHOLDS.stage_bundle_warn ? '⚠ warn'
      : '✓';
    const modeTag = mode === 'sum' ? '' : ` _(${mode})_`;
    L.push(`| ${name} | ${b.file_count} | ${t} | ${flag}${modeTag} |`);
    if (b.note) L.push(`|   | | _${b.note}_ | |`);
  }
  L.push('');
  L.push('## Directory Breakdown');
  L.push('');
  L.push('| Directory | Files | Tokens | % of total |');
  L.push('| --- | --- | --- | --- |');
  const dirEntries = Object.entries(s.dir_breakdown).sort((a, b) => b[1].tokens - a[1].tokens);
  for (const [dir, info] of dirEntries) {
    const pct = ((info.tokens / s.total_text_tokens) * 100).toFixed(1);
    L.push(`| ${dir}/ | ${info.files} | ${info.tokens} | ${pct}% |`);
  }
  if (s.decorative_files.length > 0) {
    L.push('');
    L.push('## Decorative Files (consider archiving or wiring into an entry path)');
    L.push('');
    L.push('| File | Tokens |');
    L.push('| --- | --- |');
    for (const f of s.decorative_files.sort((a, b) => b.tokens - a.tokens)) {
      L.push(`| ${f.path} | ${f.tokens} |`);
    }
  }
  if (s.top_heavy_files.length > 0) {
    L.push('');
    L.push(`## Top-Heavy Files (≥${THRESHOLDS.file_split_threshold}t — split candidates)`);
    L.push('');
    L.push('| File | Tokens |');
    L.push('| --- | --- |');
    for (const f of s.top_heavy_files.slice(0, 15)) {
      L.push(`| ${f.path} | ${f.tokens} |`);
    }
    if (s.top_heavy_files.length > 15) L.push(`| ...and ${s.top_heavy_files.length - 15} more | |`);
  }
  if (s.showcase_debt.length > 0) {
    L.push('');
    L.push('## Showcase Debt (live samples missing)');
    L.push('');
    L.push('| Dir | Missing | Present |');
    L.push('| --- | --- | --- |');
    for (const d of s.showcase_debt) {
      L.push(`| ${d.dir}/ | ${d.missing} | ${d.present.length ? d.present.join(', ') : '(empty)'} |`);
    }
  }
  return L.join('\n');
}

// ---------- main ----------

function main() {
  const argv = process.argv.slice(2);
  let root = process.cwd();
  let outDir = null;
  let jsonOnly = false;
  const it = argv[Symbol.iterator]();
  let cur;
  while (!(cur = it.next()).done) {
    const a = cur.value;
    if (a === '--root') root = resolve(it.next().value);
    else if (a === '--out') outDir = resolve(it.next().value);
    else if (a === '--json') jsonOnly = true;
    else if (a === '-h' || a === '--help') {
      console.error(`
context-budget.mjs — design-practice context budget + resource boundary audit

  --root <path>   skill root (default cwd)
  --out <dir>     write report.json + report.md to this dir
  --json          dump JSON to stdout instead of summary
`);
      process.exit(0);
    } else {
      console.error(`Unknown arg: ${a}`);
      process.exit(1);
    }
  }

  if (!existsSync(join(root, 'SKILL.md'))) {
    console.error(`Not a skill root (no SKILL.md): ${root}`);
    process.exit(1);
  }

  const report = analyze(root);

  if (outDir) {
    mkdirSync(outDir, { recursive: true });
    writeFileSync(join(outDir, 'report.json'), JSON.stringify(report, null, 2));
    writeFileSync(join(outDir, 'report.md'), renderMarkdown(report, root));
    console.log(`Report written to ${outDir}/report.md`);
  }

  if (jsonOnly) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(JSON.stringify({
      ok: report.ok,
      failures: report.failures,
      warnings: report.warnings,
      initial_load_tokens: report.stats.initial_load.total,
      total_text_tokens: report.stats.total_text_tokens,
      stage_bundle_tokens: Object.fromEntries(
        Object.entries(report.stats.stage_bundles).map(([k, v]) => [k, v.total])
      ),
      stage_bundle_modes: Object.fromEntries(
        Object.entries(report.stats.stage_bundles).map(([k, v]) => [k, v.mode || 'sum'])
      ),
      decorative_files: report.stats.decorative_files.length,
      top_heavy_files: report.stats.top_heavy_files.length,
      showcase_debt: report.stats.showcase_debt.length,
    }, null, 2));
  }

  if (!report.ok) process.exit(2);
}

main();
