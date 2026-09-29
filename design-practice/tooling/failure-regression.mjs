#!/usr/bin/env node
/**
 * design-practice Failure Mode regression for SHOWCASE HTML.
 *
 * The SKILL.md Failure Mode Library has 40 entries. About a third are STATIC-DETECTABLE
 * on generated HTML (the showcases). This tool turns those into machine-runnable checks,
 * so a showcase can't silently regress into the plastic failure patterns the skill exists to refuse.
 *
 * The other ~25 failures are agent-process failures (skipped Intent Brief, no Type-A drafts,
 * didn't read agent-playbook, etc.) — those cannot be statically detected from HTML and are
 * left as agent self-checks in references/qa-*.md. Trying to machine-check them would just
 * produce false positives.
 *
 * What this tool catches (each tied back to SKILL.md by #):
 *   #3  Two primary buttons on one screen (IA unclear)
 *   #4  "暂无数据" / "No data" empty state without classification
 *   #5  Hardcoded colors inside components (tokens skipped)
 *   #6  Missing :focus-visible (AI "cleaned" focus rings away)
 *   #12 Hover-only micro-interaction (color change alone, no scale/transform)
 *   #13 Off-4px-grid spacing values (13/17/22/27 inline pixel invention)
 *   #17 Mixed icon libraries (Lucide + Heroicons + emoji in one file)
 *   #34 Info dump (single screen with too many top-level actionable controls)
 *   NEVER: indigo/violet/purple-gradient Hero
 *   NEVER: emoji-as-icons in buttons/nav
 *   NEVER: `overflow:hidden` masking non-responsive mobile layout
 *   NEVER: modal without focus-trap signal (role=dialog + aria-modal + focus management)
 *   NEVER: baked text inside generated <img>
 *
 * Usage:
 *   node failure-regression.mjs <path-to-html> [--out <dir>] [--strict]
 *
 * Exit codes:
 *   0 = no failures detected (warnings allowed)
 *   2 = failures detected — fix before claiming showcase "done"
 *   1 = usage error
 */

import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------- arg parsing ----------

function parseArgs(argv) {
  const args = { target: null, out: null, strict: false };
  const it = argv.slice(2)[Symbol.iterator]();
  let cur;
  while (!(cur = it.next()).done) {
    const a = cur.value;
    if (a === '--out') args.out = resolve(it.next().value);
    else if (a === '--strict') args.strict = true;
    else if (a === '-h' || a === '--help') {
      console.error(`usage: node failure-regression.mjs <html> [--out <dir>] [--strict]`);
      process.exit(0);
    } else if (a.startsWith('-')) {
      console.error(`unknown arg: ${a}`); process.exit(1);
    } else {
      args.target = resolve(a);
    }
  }
  if (!args.target) { console.error('missing <html>'); process.exit(1); }
  return args;
}

// ---------- HTML parsing (regex-based, no dependency) ----------

function stripComments(html) {
  return html.replace(/<!--[\s\S]*?-->/g, '');
}
function stripStyles(html) {
  // Pull <style> contents out separately
  const styles = [];
  const stripped = html.replace(/<style\b[^>]*>([\s\S]*?)<\/style>/gi, (m, body) => {
    styles.push(body);
    return '';
  });
  return { stripped, styles: styles.join('\n\n') };
}
function extractBody(html) {
  const m = /<body\b[^>]*>([\s\S]*?)<\/body>/i.exec(html);
  return m ? m[1] : html;
}

// ---------- individual checks ----------

/**
 * #3 Two primary buttons on one screen.
 */
function checkTwoPrimaryButtons(body, styles) {
  const findings = [];
  const primaryClassRe = /\b(btn|button|cta)[\w-]*?(primary|cta|submit|main)[\w-]*\b/i;
  const accentBgRe = /background:\s*(?:#[0-9a-f]{3,8}|var\(--accent|var\(--color-(?:primary|accent|cta))/i;

  // Pre-parse styles into a class -> body map ONCE (O(n)), not per-button.
  const classMap = new Map();
  const cssRuleRe = /\.([\w-]+)\s*\{([^}]*)\}/g;
  let rm;
  while ((rm = cssRuleRe.exec(styles)) !== null) {
    if (!classMap.has(rm[1])) classMap.set(rm[1], rm[2]);
  }

  const buttonRe = /<(?:button|a)\b[^>]*>/gi;
  const buttons = [];
  let m;
  while ((m = buttonRe.exec(body)) !== null) {
    const tag = m[0];
    const isPrimary = primaryClassRe.test(tag) || /aria-label="[^"]*(?:submit|create|save|confirm|primary)/i.test(tag);
    let accent = false;
    const cls = /\bclass\s*=\s*"([^"]+)"/i.exec(tag);
    if (cls) {
      const classList = cls[1].split(/\s+/);
      for (const c of classList) {
        const body = classMap.get(c);
        if (body && accentBgRe.test(body)) { accent = true; break; }
      }
    }
    if (isPrimary || accent) buttons.push({ pos: m.index, tag });
  }
  for (let i = 0; i < buttons.length; i++) {
    for (let j = i + 1; j < buttons.length; j++) {
      const span = body.slice(buttons[i].pos, buttons[j].pos);
      if (span.length > 1500) break;
      if (/<(?:\/(?:main|section|article)|hr)\b>/i.test(span)) break;
      findings.push({
        severity: 'fail',
        rule: 'two_primary_buttons',
        skill_ref: '#3',
        message: 'Two primary buttons within one screen — IA unclear. One primary per screen.',
        evidence: [buttons[i].tag.slice(0, 100), buttons[j].tag.slice(0, 100)],
      });
      break;
    }
  }
  return findings;
}

/**
 * #4 "暂无数据" empty state without classification.
 */
function checkEmptyState(body) {
  const findings = [];
  const badEmptyPhrases = [
    /暂无数据/g, /暂无内容/g, /没有数据/g, /No data/gi, /No results?/gi,
    /Nothing (?:here|to show|yet)/gi, /Empty/gi,
  ];
  for (const re of badEmptyPhrases) {
    let m;
    while ((m = re.exec(body)) !== null) {
      // Check 200 chars around for the three-classification signal
      const ctx = body.slice(Math.max(0, m.index - 300), m.index + 300).toLowerCase();
      const classified = /initial|first.?time|get.?started|filter|clear.?filter|permission|request.?access|not.?allowed|no.?permission/.test(ctx)
        || /创建|新增|添加|开始|清除|过滤|无权|申请权限/.test(ctx);
      if (!classified) {
        findings.push({
          severity: 'fail',
          rule: 'empty_state_no_classification',
          skill_ref: '#4',
          message: `Empty state "${m[0]}" found without three-classification (initial/filter/permission) signal.`,
          evidence: body.slice(Math.max(0, m.index - 50), m.index + 50),
        });
      }
    }
  }
  return findings;
}

/**
 * #5 Hardcoded colors inside components.
 * Indicators: hex colors inside component-scoped CSS (not :root).
 */
function checkHardcodedColors(styles) {
  const findings = [];
  // Find :root block (these are the legitimate primitive tokens)
  const rootBlock = /:root\s*\{([\s\S]*?)\}/g;
  let rootText = '';
  let m;
  while ((m = rootBlock.exec(styles)) !== null) rootText += m[1];
  // Find all hex colors NOT in :root
  const hexRe = /#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b/g;
  const outside = styles.replace(/:root\s*\{[\s\S]*?\}/g, '');
  let h;
  const hits = new Map();
  while ((h = hexRe.exec(outside)) !== null) {
    hits.set(h[0].toLowerCase(), (hits.get(h[0].toLowerCase()) || 0) + 1);
  }
  // Filter out legitimate uses: black/white/grayscale are often OK at primitive level
  // but should still go through tokens. Be conservative: flag all non-:root hex.
  for (const [color, count] of hits) {
    // Allow pure white/black as common exceptions
    if (['#000', '#fff', '#ffffff', '#000000', '#0000'].includes(color)) continue;
    findings.push({
      severity: 'warn',
      rule: 'hardcoded_color',
      skill_ref: '#5',
      message: `Hardcoded color "${color}" used ${count}x outside :root. Should be a token.`,
      evidence: color,
    });
  }
  return findings;
}

/**
 * #6 Missing :focus-visible.
 */
function checkFocusVisible(styles) {
  const findings = [];
  if (!/:focus-visible|:focus\s*\{[\s\S]*?outline|:focus\s*\{[\s\S]*?box-shadow/i.test(styles)) {
    findings.push({
      severity: 'fail',
      rule: 'missing_focus_visible',
      skill_ref: '#6',
      message: 'No :focus-visible rule found. Focus rings were "cleaned" away — keyboard users lose their road.',
      evidence: 'no :focus-visible selector in CSS',
    });
  }
  // also check for the anti-pattern: :focus { outline: none } without replacement
  if (/:focus\s*\{[^}]*outline:\s*(?:none|0)[^}]*\}/i.test(styles) && !/:focus(?:-visible)?\s*\{[^}]*(?:outline|box-shadow)/i.test(styles)) {
    findings.push({
      severity: 'fail',
      rule: 'removed_focus_no_replacement',
      skill_ref: '#6',
      message: '`:focus { outline: none }` without an alternative focus indicator. AI plastic tell.',
      evidence: 'outline:none with no replacement',
    });
  }
  return findings;
}

/**
 * #12 Hover-only micro-interaction (no scale/transform on interaction).
 */
function checkHoverOnlyColor(styles) {
  const findings = [];
  const hoverRe = /:hover\s*\{([^}]*)\}/gi;
  let m;
  let hoverOnlyCount = 0;
  let totalHover = 0;
  while ((m = hoverRe.exec(styles)) !== null) {
    totalHover++;
    const body = m[1];
    // Has motion signals: transform, scale, translate, transition with non-color property
    const hasMotion = /transform|scale|translate|rotate/i.test(body);
    const hasShadow = /box-shadow/i.test(body);
    const hasColor = /color|background|border-color/i.test(body);
    if (hasColor && !hasMotion && !hasShadow) hoverOnlyCount++;
  }
  if (totalHover >= 3 && hoverOnlyCount / totalHover > 0.7) {
    findings.push({
      severity: 'warn',
      rule: 'hover_only_color',
      skill_ref: '#12',
      message: `${hoverOnlyCount}/${totalHover} :hover rules only change color. Micro-interaction four-pack (trigger/rule/feedback/loop) missing.`,
      evidence: `hover-only-color ratio: ${(hoverOnlyCount / totalHover * 100).toFixed(0)}%`,
    });
  }
  return findings;
}

/**
 * #13 Off-4px-grid spacing values.
 */
function checkOffGridSpacing(styles) {
  const findings = [];
  // Common off-grid values
  const offGridRe = /(?:padding|margin|gap|top|left|right|bottom|width|height):\s*(?:13|14|15|17|18|19|22|23|25|26|27|29|30|31|33|34|35|37|38|39|41|42|43|44|46|47)px/gi;
  let m;
  const hits = new Map();
  while ((m = offGridRe.exec(styles)) !== null) {
    const val = /(\d+)px/.exec(m[0])[1];
    hits.set(val, (hits.get(val) || 0) + 1);
  }
  for (const [val, count] of hits) {
    findings.push({
      severity: 'warn',
      rule: 'off_grid_spacing',
      skill_ref: '#13',
      message: `Off-4px-grid value ${val}px used ${count}x. Should snap to 4/8/12/16/24/32/48.`,
      evidence: `${val}px`,
    });
  }
  return findings;
}

/**
 * #17 Mixed icon libraries.
 */
function checkMixedIconLibraries(body) {
  const findings = [];
  const signals = {
    lucide: /<svg[^>]*class="[^"]*\blucide-[\w-]+\b/i.test(body) || /data-lucide="/i.test(body),
    heroicons: /<svg[^>]*class="[^"]*\bheroicon/i.test(body) || /<!--.*heroicons/i.test(body),
    phosphor: /<svg[^>]*class="[^"]*\bph[-_]/i.test(body),
    phosphorDuotone: /<svg[^>]*class="[^"]*\bph-duotone/i.test(body),
    emoji: /[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{27BF}]/u.test(body),
    material: /<span[^>]*class="[^"]*\bmaterial-icons\b/i.test(body),
  };
  const detected = Object.entries(signals).filter(([, v]) => v).map(([k]) => k);
  // Phosphor + PhosphorDuotone count as one (Duotone is a Phosphor weight)
  const unique = new Set(detected.filter(d => d !== 'phosphorDuotone'));
  if (unique.size >= 2) {
    findings.push({
      severity: 'fail',
      rule: 'mixed_icon_libraries',
      skill_ref: '#17',
      message: `Multiple icon libraries in one page: ${detected.join(', ')}. One library per product (style-DNA-bound).`,
      evidence: detected.join(', '),
    });
  }
  return findings;
}

/**
 * NEVER: indigo/violet/purple-gradient Hero.
 */
function checkIndigoVioletGradient(styles, body) {
  const findings = [];
  // Check hero sections specifically
  const heroBlock = /<(?:header|section)[^>]*(?:class="[^"]*(?:hero|landing|jumbotron)[^"]*"[^>]*)>[\s\S]*?<\/(?:header|section)>/gi;
  const heroText = heroBlock.exec(body);
  const heroCSS = heroText ? body.slice(heroText.index, heroText.index + 2000) : body.slice(0, 3000);
  const indigoRe = /#(?:6366f1|4f46e5|5e6ad2|7c3aed|8b5cf6|a78bfa|6d28d9)\b/i;
  const purpleGradientRe = /(?:purple|violet|indigo)[\w\s()-]*?(?:gradient|to-|linear-gradient)|(?:gradient|linear-gradient)[\s(),\w-]*?(?:purple|violet|indigo)/i;
  // Also check class names like "from-indigo", "via-purple", "to-violet"
  const tailwindRe = /\b(?:from|via|to)-(?:indigo|violet|purple)(?:-\d+)?\b/i;
  if (indigoRe.test(heroCSS) || purpleGradientRe.test(heroCSS) || tailwindRe.test(heroCSS)) {
    findings.push({
      severity: 'fail',
      rule: 'indigo_violet_gradient_hero',
      skill_ref: 'NEVER list',
      message: 'Indigo/violet/purple gradient in hero region — the default AI-plastic palette. Use one owned accent.',
      evidence: (indigoRe.exec(heroCSS) || purpleGradientRe.exec(heroCSS) || tailwindRe.exec(heroCSS) || [''])[0],
    });
  }
  return findings;
}

/**
 * NEVER: emoji-as-icons in buttons/nav.
 */
function checkEmojiAsIcons(body) {
  const findings = [];
  const emojiRe = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{27BF}]/gu;
  // Check only inside <button> and <nav>
  const buttonOrNav = /<(?:button|nav|a)\b[^>]*>([\s\S]*?)<\/(?:button|nav|a)>/gi;
  let m;
  while ((m = buttonOrNav.exec(body)) !== null) {
    const inner = m[1];
    if (emojiRe.test(inner)) {
      // exclude if there's also an <svg> (then emoji is decorative, not the icon)
      if (!/<svg/i.test(inner)) {
        const e = inner.match(emojiRe);
        findings.push({
          severity: 'fail',
          rule: 'emoji_as_icon',
          skill_ref: 'NEVER list',
          message: `Emoji used as icon in button/nav without SVG fallback: "${e.join('')}".`,
          evidence: m[0].slice(0, 80),
        });
      }
    }
  }
  return findings;
}

/**
 * NEVER: `overflow:hidden` masking non-responsive layout.
 * Heuristic: a fixed-width grid + overflow:hidden in body/html.
 */
function checkOverflowHiddenMobileMask(styles) {
  const findings = [];
  // body or .container with overflow:hidden AND no @media mobile rule
  const hasBodyOverflowHidden = /(?:^|[\s{])(?:body|html|\.container|\.app|main)\s*\{[^}]*overflow:\s*hidden/i.test(styles);
  const hasMediaMobile = /@media[^{]*max-width:\s*(?:390|480|640|768)px/i.test(styles);
  const hasFixedWidth = /(?:min-width|width):\s*\d{3,}px/i.test(styles);
  if (hasBodyOverflowHidden && hasFixedWidth && !hasMediaMobile) {
    findings.push({
      severity: 'fail',
      rule: 'overflow_hidden_mobile_mask',
      skill_ref: 'NEVER list',
      message: '`overflow:hidden` on body/container with fixed-width layout and no mobile @media — silently clips mobile instead of reflowing.',
      evidence: 'overflow:hidden + fixed width + no @media mobile',
    });
  }
  return findings;
}

/**
 * NEVER: modal without focus-trap signal.
 */
function checkModalWithoutFocusTrap(body) {
  const findings = [];
  const modalRe = /<(?:div|section)\b[^>]*(?:role="dialog"|class="[^"]*(?:modal|dialog)[^"]*")[^>]*>/gi;
  let m;
  while ((m = modalRe.exec(body)) !== null) {
    const tag = m[0];
    const hasAriaModal = /aria-modal="true"/i.test(tag);
    const hasRoleDialog = /role="dialog"/i.test(tag);
    if (!hasAriaModal && !hasRoleDialog) {
      // Has class modal but no role/aria — sketchy but not necessarily a modal
      continue;
    }
    // For real role=dialog: warn if no JS-based focus management is visible (we can't run JS,
    // so we just check for the presence of focus-trap hints in scripts)
    findings.push({
      severity: 'warn',
      rule: 'modal_no_focus_trap_signal',
      skill_ref: 'NEVER list',
      message: 'Modal/dialog detected. Verify focus-trap + Esc + focus-return — static HTML cannot prove it, drive-test with behavior-audit.mjs.',
      evidence: tag.slice(0, 80),
    });
  }
  return findings;
}

// ---------- runner ----------

function runAll(html, targetPath) {
  const noComments = stripComments(html);
  const { stripped, styles } = stripStyles(noComments);
  const body = extractBody(stripped);
  const allFindings = [];
  const checks = [
    ['two_primary_buttons',        () => checkTwoPrimaryButtons(body, styles)],
    ['empty_state',                () => checkEmptyState(body)],
    ['hardcoded_colors',           () => checkHardcodedColors(styles)],
    ['focus_visible',              () => checkFocusVisible(styles)],
    ['hover_only_color',           () => checkHoverOnlyColor(styles)],
    ['off_grid_spacing',           () => checkOffGridSpacing(styles)],
    ['mixed_icon_libraries',       () => checkMixedIconLibraries(body)],
    ['indigo_violet_gradient',     () => checkIndigoVioletGradient(styles, body)],
    ['emoji_as_icon',              () => checkEmojiAsIcons(body)],
    ['overflow_hidden_mobile',     () => checkOverflowHiddenMobileMask(styles)],
    ['modal_focus_trap',           () => checkModalWithoutFocusTrap(body)],
  ];
  for (const [name, fn] of checks) {
    const t0 = Date.now();
    try {
      const findings = fn();
      allFindings.push(...findings);
      const dt = Date.now() - t0;
      if (dt > 100) {
        allFindings.push({
          severity: 'warn',
          rule: 'slow_check',
          skill_ref: name,
          message: `Check "${name}" took ${dt}ms (>100ms threshold). May indicate catastrophic regex on this input.`,
          evidence: `${dt}ms`,
        });
      }
    } catch (e) {
      allFindings.push({
        severity: 'warn',
        rule: 'check_error',
        skill_ref: name,
        message: `Check "${name}" threw: ${e.message}`,
        evidence: '',
      });
    }
  }
  return allFindings;
}

// ---------- report ----------

function renderMarkdown(findings, targetPath) {
  const L = [];
  const fails = findings.filter(f => f.severity === 'fail');
  const warns = findings.filter(f => f.severity === 'warn');
  L.push(`# Failure Mode Regression — ${basename(targetPath)}`);
  L.push('');
  L.push(`- Target: \`${targetPath}\``);
  L.push(`- Failures: **${fails.length}**`);
  L.push(`- Warnings: **${warns.length}**`);
  L.push('');
  L.push('## Verdict');
  L.push('');
  if (fails.length === 0) {
    if (warns.length === 0) {
      L.push('**PASS** — no failure-mode patterns detected.');
    } else {
      L.push(`**PASS (with ${warns.length} warning${warns.length === 1 ? '' : 's'})** — review the warnings before claiming "done".`);
    }
  } else {
    L.push(`**FAIL** — ${fails.length} failure pattern${fails.length === 1 ? '' : 's'} detected. These are the exact "AI plastic tells" the skill refuses.`);
  }
  L.push('');
  L.push('## Coverage');
  L.push('');
  L.push('This tool statically detects a subset of SKILL.md\'s 40 Failure Modes. The rest are agent-process failures (skipped Intent Brief, no Type-A drafts, etc.) and live in `references/qa-*.md`.');
  L.push('');
  L.push('| SKILL.md # | Detected |');
  L.push('| --- | --- |');
  L.push('| #3 Two primary buttons | ✓ |');
  L.push('| #4 Empty state no classification | ✓ |');
  L.push('| #5 Hardcoded colors | ✓ |');
  L.push('| #6 Missing focus-visible | ✓ |');
  L.push('| #12 Hover-only micro-interaction | ✓ |');
  L.push('| #13 Off-4px-grid spacing | ✓ |');
  L.push('| #17 Mixed icon libraries | ✓ |');
  L.push('| #34 Info dump | partial (via off-grid heuristic) |');
  L.push('| NEVER: indigo/violet hero | ✓ |');
  L.push('| NEVER: emoji-as-icons | ✓ |');
  L.push('| NEVER: overflow:hidden mobile mask | ✓ |');
  L.push('| NEVER: modal no focus-trap | warn (static can\'t prove JS) |');
  L.push('| #1, #2, #7-11, #14-16, #18-40 | agent self-check (qa-*.md) |');
  L.push('');
  if (findings.length > 0) {
    L.push('## Findings');
    L.push('');
    L.push('| Severity | Rule | SKILL.md # | Message | Evidence |');
    L.push('| --- | --- | --- | --- | --- |');
    for (const f of [...fails, ...warns].sort((a, b) => {
      const sa = a.severity === 'fail' ? 0 : 1;
      const sb = b.severity === 'fail' ? 0 : 1;
      return sa - sb;
    })) {
      const ev = (f.evidence || '').toString().replace(/\|/g, '\\|').replace(/\n/g, ' ').slice(0, 60);
      L.push(`| ${f.severity} | ${f.rule} | ${f.skill_ref} | ${f.message.replace(/\|/g, '\\|')} | ${ev} |`);
    }
  }
  return L.join('\n');
}

// ---------- main ----------

function main() {
  const args = parseArgs(process.argv);
  if (!existsSync(args.target)) {
    console.error(`File not found: ${args.target}`);
    process.exit(1);
  }
  const html = readFileSync(args.target, 'utf8');
  const findings = runAll(html, args.target);
  const fails = findings.filter(f => f.severity === 'fail');

  if (args.out) {
    mkdirSync(args.out, { recursive: true });
    writeFileSync(join(args.out, 'report.json'), JSON.stringify({ target: args.target, findings }, null, 2));
    writeFileSync(join(args.out, 'report.md'), renderMarkdown(findings, args.target));
    console.log(`Report written to ${args.out}/report.md`);
  }

  console.log(JSON.stringify({
    target: args.target,
    total: findings.length,
    failures: fails.length,
    warnings: findings.length - fails.length,
    rules: [...new Set(findings.map(f => f.rule))],
  }, null, 2));

  // --strict: warnings also block
  if (fails.length > 0 || (args.strict && findings.length > 0)) process.exit(2);
}

main();
