#!/usr/bin/env node
/**
 * design-practice Stage 3 harness
 * render → collect signals → emit report.json + report.md
 *
 * Usage: node render-critique.mjs <path-to-html-or-url> [--out <dir>]
 */

import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFileSync, mkdirSync, writeFileSync, statSync, existsSync } from 'node:fs';
import { resolve, dirname, basename, extname, join } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { createReadStream } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const axeSource = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const __dirname = dirname(fileURLToPath(import.meta.url));

const VIEWPORTS = [
  { id: 'desktop', width: 1440, height: 900, label: 'Desktop 1440×900' },
  { id: 'tablet', width: 768, height: 1024, label: 'Tablet 768×1024' },
  { id: 'mobile', width: 390, height: 844, label: 'Mobile 390×844' },
  { id: 'mobile360', width: 360, height: 780, label: 'Mobile 360×780' },
];

const RESPONSIVE_MOBILE_IDS = new Set(['mobile', 'mobile360']);

const RUBRIC = [
  { id: 'hierarchy', name: 'Hierarchy (视觉层级)', visual: true },
  { id: 'spacing', name: 'Spacing & rhythm (间距节奏)', visual: false },
  { id: 'typography', name: 'Typography (字体)', visual: true },
  { id: 'contrast_a11y', name: 'Contrast & a11y (对比可访问性)', visual: false },
  { id: 'color_tokens', name: 'Color & token discipline (色彩token纪律)', visual: false },
  { id: 'state_coverage', name: 'State coverage (状态完整)', visual: false },
  { id: 'motion', name: 'Motion (动效)', visual: false },
  { id: 'performance', name: 'Performance (性能)', visual: false },
  { id: 'responsive', name: 'Responsive integrity (响应式)', visual: false },
  { id: 'restraint', name: 'Restraint & originality (克制与原创)', visual: true },
];

const INDIGO_PATTERNS = [
  /#6366f1/i,
  /#4f46e5/i,
  /#5e6ad2/i,
  /indigo-\d+/i,
  /violet-\d+/i,
  /purple.*gradient|gradient.*purple/i,
];

const VITALS_INIT_SCRIPT = `
(() => {
  if (window.__critiqueVitals) return;
  window.__critiqueVitals = {
    lcpMs: null,
    lcpElement: null,
    cls: 0,
    layoutShiftCount: 0,
    inpMs: null,
    inpEvent: null,
  };
  try {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        window.__critiqueVitals.lcpMs = Math.round(entry.startTime);
        const el = entry.element;
        window.__critiqueVitals.lcpElement = el
          ? {
              tag: el.tagName?.toLowerCase?.() ?? 'unknown',
              id: el.id || null,
              className: el.className?.toString?.() ?? null,
              text: (el.textContent ?? '').trim().slice(0, 80) || null,
            }
          : null;
      }
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (_) {}
  try {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          window.__critiqueVitals.cls += entry.value;
          window.__critiqueVitals.layoutShiftCount++;
        }
      }
    }).observe({ type: 'layout-shift', buffered: true });
  } catch (_) {}
  try {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.interactionId && entry.duration > (window.__critiqueVitals.inpMs ?? 0)) {
          window.__critiqueVitals.inpMs = Math.round(entry.duration);
          window.__critiqueVitals.inpEvent = entry.name;
        }
      }
    }).observe({ type: 'event', buffered: true, durationThreshold: 16 });
  } catch (_) {}
})();
`;

/** @param {string[]} argv */
function parseArgs(argv) {
  const positional = [];
  let outDir = join(__dirname, 'reports');

  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--out' && argv[i + 1]) {
      outDir = resolve(argv[++i]);
    } else if (!argv[i].startsWith('--')) {
      positional.push(argv[i]);
    }
  }

  if (positional.length === 0) {
    console.error('Usage: node render-critique.mjs <path-to-html-or-url> [--out <dir>]');
    process.exit(2);
  }

  return { target: positional[0], outDir };
}

function isUrl(input) {
  return /^https?:\/\//i.test(input);
}

/**
 * Serve a single local HTML file on an ephemeral localhost port.
 * @param {string} filePath
 */
function serveHtml(filePath) {
  const abs = resolve(filePath);
  const content = readFileSync(abs, 'utf8');
  const dir = dirname(abs);

  const server = createServer((req, res) => {
    const urlPath = req.url?.split('?')[0] ?? '/';
    if (urlPath === '/' || urlPath === `/${basename(abs)}`) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(content);
      return;
    }

    const rel = urlPath.replace(/^\//, '');
    const candidate = resolve(dir, rel);
    if (!candidate.startsWith(dir)) {
      res.writeHead(403).end('Forbidden');
      return;
    }
    try {
      const st = statSync(candidate);
      if (!st.isFile()) {
        res.writeHead(404).end('Not found');
        return;
      }
      res.writeHead(200);
      createReadStream(candidate).pipe(res);
    } catch {
      res.writeHead(404).end('Not found');
    }
  });

  return new Promise((resolvePromise, reject) => {
    server.listen(0, '127.0.0.1', () => {
      const addr = server.address();
      if (!addr || typeof addr === 'string') {
        reject(new Error('Failed to bind temp server'));
        return;
      }
      resolvePromise({
        url: `http://127.0.0.1:${addr.port}/${basename(abs)}`,
        close: () =>
          new Promise((r) => {
            server.close(() => r());
          }),
      });
    });
    server.on('error', reject);
  });
}


/**
 * Injected into the page to collect layout, token-drift, motion, and state heuristics.
 * Must be self-contained (no closure deps).
 */
function collectDomSignals() {
  const INDIGO = [/#6366f1/i, /#4f46e5/i, /#5e6ad2/i, /indigo-\d+/i, /violet-\d+/i];

  function gcd(a, b) {
    let x = Math.abs(a);
    let y = Math.abs(b);
    while (y) {
      const t = y;
      y = x % y;
      x = t;
    }
    return x || 1;
  }

  function gcdList(nums) {
    return nums.reduce((acc, n) => gcd(acc, n), nums[0] ?? 1);
  }

  function mode(nums) {
    const freq = new Map();
    for (const n of nums) freq.set(n, (freq.get(n) ?? 0) + 1);
    let best = nums[0] ?? 4;
    let bestCount = 0;
    for (const [n, c] of freq) {
      if (c > bestCount) {
        best = n;
        bestCount = c;
      }
    }
    return best;
  }

  let allCss = '';
  const authoredRules = [];

  for (const sheet of Array.from(document.styleSheets)) {
    try {
      for (const rule of Array.from(sheet.cssRules)) {
        allCss += rule.cssText + '\n';
        if (rule.type === CSSRule.STYLE_RULE && rule.selectorText) {
          authoredRules.push({ selector: rule.selectorText, cssText: rule.style.cssText });
        }
      }
    } catch {
      // cross-origin stylesheet — skip
    }
  }
  for (const el of document.querySelectorAll('style')) {
    const text = el.textContent ?? '';
    allCss += text;
    const ruleRe = /([^{]+)\{([^}]+)\}/g;
    let m;
    while ((m = ruleRe.exec(text))) {
      authoredRules.push({ selector: m[1].trim(), cssText: m[2] });
    }
  }

  const rootFontPx = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;

  /** @param {string} raw @param {number} base */
  function toPx(raw, base = rootFontPx) {
    const v = raw.trim().toLowerCase();
    if (v.endsWith('px')) return parseFloat(v);
    if (v.endsWith('rem')) return parseFloat(v) * base;
    if (v.endsWith('em')) return parseFloat(v) * base;
    if (v.endsWith('%')) return null;
    const n = parseFloat(v);
    return Number.isFinite(n) ? n : null;
  }

  /** @param {string} css @returns {string|null} */
  function rgbToHex(css) {
    if (!css) return null;
    const t = css.trim();
    if (/^#[0-9a-f]{3,8}$/i.test(t)) {
      if (t.length === 4) {
        return `#${t[1]}${t[1]}${t[2]}${t[2]}${t[3]}${t[3]}`.toLowerCase();
      }
      return t.toLowerCase();
    }
    const m = t.match(/rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)/i);
    if (!m) return null;
    const r = Math.round(Number(m[1]));
    const g = Math.round(Number(m[2]));
    const b = Math.round(Number(m[3]));
    return `#${[r, g, b].map((x) => x.toString(16).padStart(2, '0')).join('')}`;
  }

  /** @param {string} val */
  function normalizeColor(val) {
    const t = val.trim();
    if (!t || /^(inherit|initial|unset|revert|currentcolor|transparent|none|auto|content-box|border-box)$/i.test(t)) {
      return null;
    }
    const hex = rgbToHex(t);
    if (hex) return hex;
    if (/^var\(--[^)]+\)$/.test(t)) return t;
    if (/^color-mix\(/.test(t)) return t.slice(0, 48);
    if (/^(linear|radial|conic)-gradient\(/.test(t)) return t.slice(0, 48);
    if (/^color\(/.test(t)) {
      const inner = t.match(/color\([^)]+\)/);
      return inner ? inner[0].slice(0, 40) : null;
    }
    return null;
  }

  const spacingPropRe = /^(margin(?:-(?:top|right|bottom|left))?|padding(?:-(?:top|right|bottom|left))?|gap|row-gap|column-gap)$/i;
  const spacingValuesPx = [];
  const authoredSpacing = [];

  for (const rule of authoredRules) {
    const decls = rule.cssText.split(';').map((d) => d.trim()).filter(Boolean);
    for (const decl of decls) {
      const idx = decl.indexOf(':');
      if (idx < 0) continue;
      const prop = decl.slice(0, idx).trim();
      const val = decl.slice(idx + 1).trim();
      if (!spacingPropRe.test(prop)) continue;

      const parts = val.split(/\s+/);
      for (const part of parts) {
        if (part === '0' || part === 'auto' || part === 'inherit' || part === 'initial') continue;
        const px = toPx(part);
        if (px == null || px <= 0 || px > 192) continue;
        spacingValuesPx.push(px);
        authoredSpacing.push({ prop, value: part, px: Math.round(px * 100) / 100, selector: rule.selector });
      }
    }
  }

  const roundedSpacing = spacingValuesPx.map((v) => Math.round(v));
  const detectedScale = roundedSpacing.length ? mode(roundedSpacing.filter((v) => v > 0 && v <= 32)) : 4;
  const gcdScale = roundedSpacing.length ? gcdList(roundedSpacing.filter((v) => v > 0)) : detectedScale;
  const baseUnit = [4, 8].includes(gcdScale) ? gcdScale : [4, 8].includes(detectedScale) ? detectedScale : gcdScale <= 2 ? 4 : gcdScale;

  const offScaleMap = new Map();
  for (const item of authoredSpacing) {
    const px = item.px;
    if (Math.abs(px % baseUnit) <= 0.01) continue;
    const key = `${item.prop}:${item.value}`;
    if (!offScaleMap.has(key)) {
      offScaleMap.set(key, { prop: item.prop, value: item.value, px: item.px, selectors: [] });
    }
    const entry = offScaleMap.get(key);
    if (entry.selectors.length < 5 && !entry.selectors.includes(item.selector)) {
      entry.selectors.push(item.selector);
    }
  }
  const authoredOffScale = Array.from(offScaleMap.values()).sort((a, b) => a.px - b.px);

  const fontFamilies = new Set();
  const fontSizes = new Set();
  const colors = new Set();
  const hexColors = [];
  const cssVarColors = [];
  let centerAlignCount = 0;
  let textAlignTotal = 0;
  let dropShadowCount = 0;
  let indigoHits = 0;
  const radiusValues = new Set();
  const easingCurves = new Set();

  for (const rule of authoredRules) {
    const decls = rule.cssText.split(';').map((d) => d.trim()).filter(Boolean);
    for (const decl of decls) {
      const idx = decl.indexOf(':');
      if (idx < 0) continue;
      const prop = decl.slice(0, idx).trim().toLowerCase();
      const val = decl.slice(idx + 1).trim();
      if (prop === 'font-size') {
        const px = toPx(val);
        if (px != null) fontSizes.add(Math.round(px * 10) / 10);
      }
      if (prop === 'border-radius' || prop.startsWith('border-') && prop.endsWith('-radius')) {
        val.split(/\s+/).forEach((part) => {
          const px = toPx(part);
          if (px != null) radiusValues.add(Math.round(px * 10) / 10);
          else if (part === '50%' || part === '9999px') radiusValues.add(part);
        });
      }
      if (prop === 'transition-timing-function' || prop === 'animation-timing-function') {
        easingCurves.add(val);
      }
      if (/^color$|^background|^border.*color|^fill$|^stroke$/.test(prop)) {
        const norm = normalizeColor(val);
        if (norm) colors.add(norm);
      }
    }
  }

  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    fontFamilies.add(cs.fontFamily);
    const fs = parseFloat(cs.fontSize);
    if (fs) fontSizes.add(Math.round(fs * 10) / 10);

    const ta = cs.textAlign;
    if (ta) {
      textAlignTotal++;
      if (ta === 'center') centerAlignCount++;
    }

    const shadow = cs.boxShadow;
    const filter = cs.filter;
    if ((shadow && shadow !== 'none') || (filter && filter.includes('drop-shadow'))) {
      dropShadowCount++;
    }

    for (const prop of ['color', 'background-color', 'border-color']) {
      const c = cs.getPropertyValue(prop);
      if (!c || c === 'transparent' || c === 'rgba(0, 0, 0, 0)') continue;
      const norm = normalizeColor(c);
      if (norm) colors.add(norm);
      if (/^#[0-9a-f]{3,8}$/i.test(c.trim())) hexColors.push(c.trim());
      if (c.includes('var(--')) cssVarColors.push(c);
    }

    const br = cs.borderRadius;
    if (br && br !== '0px') {
      br.split(/\s+/).forEach((part) => {
        const px = parseFloat(part);
        if (Number.isFinite(px)) radiusValues.add(Math.round(px * 10) / 10);
      });
    }
  }

  const hexInCss = (allCss.match(/#[0-9a-fA-F]{3,8}\b/g) ?? []).length;
  const varInCss = (allCss.match(/var\(--[^)]+\)/g) ?? []).length;

  for (const pat of INDIGO) {
    if (pat.test(allCss)) indigoHits++;
  }

  const stateFlags = {
    hover: /:hover\b/.test(allCss),
    focus: /:focus\b/.test(allCss),
    focusVisible: /:focus-visible\b/.test(allCss),
    active: /:active\b/.test(allCss),
    disabled: /:disabled\b|\[disabled\]|\[aria-disabled/.test(allCss),
    loading: /loading|is-loading|skeleton|aria-busy/i.test(allCss + document.body.innerHTML),
    empty: /empty|is-empty|no-data|暂无|没有数据/i.test(allCss + document.body.innerHTML),
    error: /error|is-error|invalid|danger|aria-invalid/i.test(allCss + document.body.innerHTML),
    permission: /permission|forbidden|403|denied|无权/i.test(allCss + document.body.innerHTML),
  };

  const motionIssues = [];
  const motionRules = allCss.match(/(transition|animation)[^;{]+/gi) ?? [];
  let hasReducedMotion = /@media\s*\([^)]*prefers-reduced-motion/i.test(allCss);

  for (const rule of motionRules) {
    const isTransition = /^\s*transition/i.test(rule);
    if (isTransition && /\b(width|height|top|left|right|bottom|margin|padding|inset)\b/i.test(rule)) {
      motionIssues.push(`non-composited transition (animates layout prop): ${rule.slice(0, 80)}`);
    }
    if (isTransition) {
      const durMatch = rule.match(/(\d*\.?\d+)\s*(ms|s)\b/i);
      if (durMatch) {
        const ms = durMatch[2].toLowerCase() === 's' ? parseFloat(durMatch[1]) * 1000 : parseFloat(durMatch[1]);
        if (ms > 500) motionIssues.push(`transition ${ms}ms > 500ms (sluggish feedback): ${rule.slice(0, 80)}`);
      }
      const easeMatch = rule.match(/(?:ease|linear|cubic-bezier\([^)]+\)|steps\([^)]+\))/i);
      if (easeMatch) easingCurves.add(easeMatch[0]);
    }
    if (/^\s*animation/i.test(rule)) {
      const easeMatch = rule.match(/(?:ease|linear|cubic-bezier\([^)]+\)|steps\([^)]+\))/i);
      if (easeMatch) easingCurves.add(easeMatch[0]);
    }
  }

  const overflowX = document.documentElement.scrollWidth > document.documentElement.clientWidth;
  const overflowY = document.documentElement.scrollHeight > document.documentElement.clientHeight;
  const domNodeCount = document.getElementsByTagName('*').length;

  const vitals = window.__critiqueVitals ?? {};
  let lcpMs = vitals.lcpMs ?? null;
  let lcpElement = vitals.lcpElement ?? null;
  let cls = vitals.cls ?? 0;
  let layoutShiftCount = vitals.layoutShiftCount ?? 0;
  let inpMs = vitals.inpMs ?? null;
  let inpEvent = vitals.inpEvent ?? null;

  if (lcpMs == null) {
    const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
    if (lcpEntries.length > 0) {
      const last = lcpEntries[lcpEntries.length - 1];
      lcpMs = Math.round(last.startTime);
      lcpElement = {
        tag: last.element?.tagName?.toLowerCase() ?? 'unknown',
        id: last.element?.id ?? null,
        className: last.element?.className?.toString?.() ?? null,
        text: (last.element?.textContent ?? '').trim().slice(0, 80) || null,
      };
    }
  }

  if (!layoutShiftCount) {
    for (const entry of performance.getEntriesByType('layout-shift')) {
      if (!entry.hadRecentInput) {
        cls += entry.value;
        layoutShiftCount++;
      }
    }
  }

  if (inpMs == null) {
    const events = performance.getEntriesByType('event');
    for (const entry of events) {
      if (entry.duration > (inpMs ?? 0)) {
        inpMs = Math.round(entry.duration);
        inpEvent = entry.name;
      }
    }
    const fi = performance.getEntriesByType('first-input');
    if (fi.length && (inpMs == null || fi[0].processingStart - fi[0].startTime > inpMs)) {
      inpMs = Math.round(fi[0].processingStart - fi[0].startTime);
      inpEvent = fi[0].name;
    }
  }

  const centerRatio = textAlignTotal > 0 ? centerAlignCount / textAlignTotal : 0;
  const typeScale = Array.from(fontSizes).sort((a, b) => a - b);
  const palette = Array.from(colors).sort();
  const radiusScale = Array.from(radiusValues).sort((a, b) => {
    if (typeof a === 'string') return 1;
    if (typeof b === 'string') return -1;
    return a - b;
  });
  const easings = Array.from(easingCurves).sort();

  return {
    fontFamilyCount: fontFamilies.size,
    fontFamilies: Array.from(fontFamilies).slice(0, 12),
    distinctColorCount: colors.size,
    spacing: {
      baseUnit,
      detectedScale,
      authoredValueCount: spacingValuesPx.length,
      offScaleCount: authoredOffScale.length,
      offScale: authoredOffScale.slice(0, 30),
    },
    hexColorCount: hexColors.length,
    cssVarColorUsage: cssVarColors.length,
    hexInCss,
    varInCss,
    indigoPaletteHits: indigoHits,
    centerAlignRatio: Math.round(centerRatio * 100) / 100,
    dropShadowElementCount: dropShadowCount,
    hasFocusVisibleRules: stateFlags.focusVisible,
    stateFlags,
    motionIssues: motionIssues.slice(0, 20),
    hasReducedMotion,
    overflow: { horizontal: overflowX, vertical: overflowY },
    domNodeCount,
    performance: {
      lcpMs,
      cls: Math.round(cls * 1000) / 1000,
      layoutShiftCount,
      inpMs,
      inpEvent,
      lcpElement,
    },
    designSystem: {
      typeScale,
      palette,
      radiusScale,
      easings,
    },
    cssLength: allCss.length,
  };
}

/**
 * Mobile-focused responsive integrity signals — detects clipping, fixed widths,
 * inner scroll overflow, touch targets, and tiny body text.
 * Self-contained for page.evaluate().
 */
function collectResponsiveSignals() {
  const viewportWidth = window.innerWidth;
  const TOLERANCE = 4;
  const interactiveSel =
    'button, a[href], [role="button"], input:not([type="hidden"]), select, textarea, [role="link"]';

  function elDesc(el) {
    const tag = el.tagName.toLowerCase();
    const cls = el.className?.toString?.()?.trim();
    const id = el.id;
    let sel = tag;
    if (id) sel = `#${id}`;
    else if (cls) sel = `${tag}.${cls.split(/\s+/).slice(0, 2).join('.')}`;
    return { tag, className: cls?.slice(0, 80) || null, selector: sel };
  }

  function isVisible(el) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
    const rect = el.getBoundingClientRect();
    return rect.width >= 1 && rect.height >= 1;
  }

  /** @param {string} cols */
  function sumFixedGridTracks(cols) {
    if (!cols || cols === 'none') return null;
    let sum = 0;
    let fixedCount = 0;
    for (const part of cols.split(/\s+/)) {
      const t = part.trim();
      if (!t || t === 'auto' || t.endsWith('fr') || t.endsWith('%')) continue;
      const px = parseFloat(t);
      if (Number.isFinite(px)) {
        sum += px;
        fixedCount++;
      }
    }
    return fixedCount > 0 ? sum : null;
  }

  function visibleWidthInViewport(rect) {
    const left = Math.max(0, rect.left);
    const right = Math.min(viewportWidth, rect.right);
    return Math.max(0, right - left);
  }

  function isAriaHidden(el) {
    let node = el;
    while (node) {
      if (node.getAttribute?.('aria-hidden') === 'true' || node.hasAttribute?.('hidden')) return true;
      node = node.parentElement;
    }
    return false;
  }

  // An element scrolled out of view inside a user-scrollable ancestor (overflow-x:auto/scroll) that
  // ITSELF fits the viewport is legit contained-scroll (tabs / carousels / wide-table wrappers) — NOT a
  // clip failure. (overflow:hidden is deliberately NOT exempt — that masks content the user can't reach,
  // which is exactly the fixed-desktop-grid failure we must still catch.)
  function inContainedScroller(el) {
    let node = el.parentElement;
    while (node && node !== document.body) {
      const cs = getComputedStyle(node);
      if (['auto', 'scroll'].includes(cs.overflowX) || ['auto', 'scroll'].includes(cs.overflow)) {
        if (node.getBoundingClientRect().right <= viewportWidth + TOLERANCE + 1) return true;
      }
      node = node.parentElement;
    }
    return false;
  }

  // (a) Clipped / overflowing content beyond viewport (even under overflow:hidden)
  const clipped = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!(el instanceof HTMLElement) || !isVisible(el) || isAriaHidden(el)) continue;
    if (inContainedScroller(el)) continue;
    const rect = el.getBoundingClientRect();
    const overflowRight = rect.right > viewportWidth + TOLERANCE ? Math.round(rect.right - viewportWidth) : 0;
    const overflowLeft = rect.left < -TOLERANCE ? Math.round(-rect.left) : 0;
    const maxOverflow = Math.max(overflowRight, overflowLeft);
    if (maxOverflow <= 0) continue;
    const visibleW = visibleWidthInViewport(rect);
    // Off-canvas panels (drawers, sidebars) fully outside viewport — not a responsive failure.
    if (visibleW < 8) continue;
    if (maxOverflow <= 2 && rect.width >= viewportWidth * 0.95) continue;
    clipped.push({ ...elDesc(el), overflowRight, overflowLeft, maxOverflow, visibleW: Math.round(visibleW) });
  }
  clipped.sort((a, b) => b.maxOverflow - a.maxOverflow);

  // (b) Fixed/min widths exceeding viewport; grid/flex track sums
  const fixedWidth = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!(el instanceof HTMLElement) || !isVisible(el) || isAriaHidden(el)) continue;
    if (inContainedScroller(el)) continue;   // min-width inside a contained scroller (wide-table wrapper) is legit
    const rect = el.getBoundingClientRect();
    if (visibleWidthInViewport(rect) < 8) continue;
    const cs = getComputedStyle(el);
    const minW = parseFloat(cs.minWidth);
    const w = parseFloat(cs.width);
    if (Number.isFinite(minW) && minW > viewportWidth + TOLERANCE) {
      fixedWidth.push({ ...elDesc(el), kind: 'min-width', px: Math.round(minW) });
    }
    if (cs.width.endsWith('px') && Number.isFinite(w) && w > viewportWidth + TOLERANCE) {
      fixedWidth.push({ ...elDesc(el), kind: 'width', px: Math.round(w) });
    }
    const gridSum = sumFixedGridTracks(cs.gridTemplateColumns);
    if (gridSum != null && gridSum > viewportWidth + TOLERANCE) {
      fixedWidth.push({ ...elDesc(el), kind: 'grid-columns-sum', px: Math.round(gridSum) });
    }
    // Only ROW flex stacks children horizontally — a column flex's children sum vertically, so summing
    // their widths is meaningless (it would false-flag every stacked card).
    if (cs.display === 'flex' && cs.flexWrap === 'nowrap' && (cs.flexDirection === 'row' || cs.flexDirection === 'row-reverse')) {
      let childSum = 0;
      let visibleChildren = 0;
      for (const child of el.children) {
        if (!(child instanceof HTMLElement)) continue;
        const crect = child.getBoundingClientRect();
        if (visibleWidthInViewport(crect) < 4) continue;
        visibleChildren++;
        childSum += crect.width;
      }
      if (visibleChildren >= 2 && childSum > viewportWidth + TOLERANCE) {
        fixedWidth.push({ ...elDesc(el), kind: 'flex-nowrap-children-sum', px: Math.round(childSum) });
      }
    }
  }

  const strictFixedWidth = fixedWidth.filter((f) => f.kind !== 'flex-nowrap-children-sum');

  // (c) Horizontal scroll on root or inner containers
  const horizontalScroll = [];
  const rootEls = [
    { label: 'documentElement', el: document.documentElement },
    { label: 'body', el: document.body },
  ];
  for (const { label, el } of rootEls) {
    if (el.scrollWidth > el.clientWidth + TOLERANCE) {
      horizontalScroll.push({
        label,
        isRoot: true,
        overflowPx: el.scrollWidth - el.clientWidth,
      });
    }
  }
  for (const el of document.querySelectorAll('body *')) {
    if (!(el instanceof HTMLElement) || !isVisible(el)) continue;
    const cs = getComputedStyle(el);
    const ox = cs.overflowX;
    const o = cs.overflow;
    if (!['auto', 'scroll', 'overlay'].includes(ox) && !['auto', 'scroll', 'overlay'].includes(o)) continue;
    if (el.scrollWidth > el.clientWidth + TOLERANCE) {
      horizontalScroll.push({
        ...elDesc(el),
        isRoot: false,
        overflowPx: el.scrollWidth - el.clientWidth,
      });
    }
  }

  // (d) Touch targets smaller than 44×44 (hard-flag <24)
  const touchSmall = [];
  const touchHardSmall = [];
  for (const el of document.querySelectorAll(interactiveSel)) {
    if (!(el instanceof HTMLElement) || !isVisible(el)) continue;
    // WCAG 2.2 SC 2.5.8 exempts inline links (in a sentence / text run) from target-size — don't penalize them.
    if (el.tagName === 'A' && getComputedStyle(el).display.startsWith('inline')) continue;
    const rect = el.getBoundingClientRect();
    const w = Math.round(rect.width);
    const h = Math.round(rect.height);
    const entry = { ...elDesc(el), width: w, height: h };
    if (w < 24 || h < 24) touchHardSmall.push(entry);
    else if (w < 44 || h < 44) touchSmall.push(entry);
  }

  // (e) Body text < 12px — primary copy only (skip meta/caption/badge utility classes)
  const smallText = [];
  const metaClassRe = /\b(meta|caption|hint|badge|label|axis|val|target|delta|spark|unit|chip|pill|tag|stamp|crumb|pct|sub|fine-print|overline|kicker|eyebrow|mono|tnum)\b/i;
  for (const el of document.querySelectorAll('p, span, li, td, th, label, a, button, h1, h2, h3, h4, h5, h6')) {
    if (!(el instanceof HTMLElement) || !isVisible(el) || isAriaHidden(el)) continue;
    const text = (el.textContent ?? '').trim();
    if (text.length < 4) continue;                       // values / chips / units / short tokens — not body copy
    const cs0 = getComputedStyle(el);
    if (cs0.textTransform === 'uppercase' && parseFloat(cs0.letterSpacing) > 0.2) continue;  // an eyebrow/micro-label, not primary copy
    const cls = el.className?.toString?.() ?? '';
    if (metaClassRe.test(cls)) continue;
    const directText = Array.from(el.childNodes)
      .filter((n) => n.nodeType === Node.TEXT_NODE)
      .map((n) => n.textContent?.trim() ?? '')
      .join('');
    if (!directText && el.children.length > 1) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (Number.isFinite(fs) && fs < 12) {
      smallText.push({ ...elDesc(el), fontSizePx: Math.round(fs * 10) / 10, textSample: text.slice(0, 48) });
    }
  }

  return {
    viewportWidth,
    clipped: { count: clipped.length, maxOverflow: clipped[0]?.maxOverflow ?? 0, sample: clipped.slice(0, 8) },
    fixedWidth: { count: fixedWidth.length, strictCount: strictFixedWidth.length, sample: fixedWidth.slice(0, 8) },
    horizontalScroll: { count: horizontalScroll.length, rootCount: horizontalScroll.filter((h) => h.isRoot).length, sample: horizontalScroll.slice(0, 8) },
    touchTargets: {
      below44Count: touchSmall.length,
      below24Count: touchHardSmall.length,
      sample: [...touchHardSmall, ...touchSmall].slice(0, 8),
    },
    smallText: { count: smallText.length, sample: smallText.slice(0, 8) },
  };
}

/**
 * Aggregate mobile responsive signals (worst viewport wins per metric).
 * @param {Array<{ id: string, responsive?: object }>} viewports
 */
function aggregateResponsiveDetail(viewports) {
  const mobile = viewports.filter((v) => RESPONSIVE_MOBILE_IDS.has(v.id) && v.responsive);
  if (!mobile.length) return null;

  const worst = {
    clippedCount: 0,
    clippedMaxOverflow: 0,
    fixedWidthCount: 0,
    strictFixedWidthCount: 0,
    flexNowrapCount: 0,
    horizontalScrollCount: 0,
    horizontalRootScrollCount: 0,
    touchBelow44: 0,
    touchBelow24: 0,
    smallTextCount: 0,
    perViewport: {},
    samples: {
      clipped: [],
      fixedWidth: [],
      horizontalScroll: [],
      touchTargets: [],
      smallText: [],
    },
  };

  for (const vp of mobile) {
    const r = vp.responsive;
    worst.perViewport[vp.id] = r;
    worst.clippedCount = Math.max(worst.clippedCount, r.clipped.count);
    worst.clippedMaxOverflow = Math.max(worst.clippedMaxOverflow, r.clipped.maxOverflow);
    worst.fixedWidthCount = Math.max(worst.fixedWidthCount, r.fixedWidth.count);
    worst.strictFixedWidthCount = Math.max(worst.strictFixedWidthCount, r.fixedWidth.strictCount ?? 0);
    worst.flexNowrapCount = Math.max(
      worst.flexNowrapCount,
      r.fixedWidth.count - (r.fixedWidth.strictCount ?? 0),
    );
    worst.horizontalScrollCount = Math.max(worst.horizontalScrollCount, r.horizontalScroll.count);
    worst.horizontalRootScrollCount = Math.max(worst.horizontalRootScrollCount, r.horizontalScroll.rootCount ?? 0);
    worst.touchBelow44 = Math.max(worst.touchBelow44, r.touchTargets.below44Count);
    worst.touchBelow24 = Math.max(worst.touchBelow24, r.touchTargets.below24Count);
    worst.smallTextCount = Math.max(worst.smallTextCount, r.smallText.count);

    if (r.clipped.maxOverflow >= worst.clippedMaxOverflow) worst.samples.clipped = r.clipped.sample;
    if (r.fixedWidth.count >= worst.fixedWidthCount) worst.samples.fixedWidth = r.fixedWidth.sample;
    if (r.horizontalScroll.count >= worst.horizontalScrollCount) {
      worst.samples.horizontalScroll = r.horizontalScroll.sample;
    }
    if (r.touchTargets.below24Count + r.touchTargets.below44Count >= worst.touchBelow44 + worst.touchBelow24) {
      worst.samples.touchTargets = r.touchTargets.sample;
    }
    if (r.smallText.count >= worst.smallTextCount) worst.samples.smallText = r.smallText.sample;
  }

  return worst;
}

/**
 * Score responsive integrity 1–5 from aggregated mobile detail.
 * @param {ReturnType<typeof aggregateResponsiveDetail>} detail
 */
function scoreResponsive(detail) {
  if (!detail) return { score: 5, summary: 'No mobile responsive audit data.' };

  let score = 5;
  const flags = [];

  const severeClip =
    detail.clippedCount >= 6 &&
    detail.clippedMaxOverflow >= 48 &&
    (detail.strictFixedWidthCount >= 1 || detail.clippedMaxOverflow >= 120);
  const moderateClip =
    (detail.clippedCount >= 4 && detail.clippedMaxOverflow >= 32) ||
    detail.strictFixedWidthCount >= 2 ||
    (detail.clippedCount >= 2 && detail.clippedMaxOverflow >= 48 && detail.flexNowrapCount >= 1);

  if (severeClip) {
    score = Math.min(score, 1);
    flags.push(`clipped content (${detail.clippedCount} els, max ${detail.clippedMaxOverflow}px)`);
  } else if (moderateClip) {
    score = Math.min(score, 2);
    flags.push(
      `layout overflow/clipping (${detail.clippedCount} clipped, ${detail.strictFixedWidthCount} strict fixed-width)`,
    );
  } else if (detail.clippedCount >= 1 || detail.strictFixedWidthCount >= 1 || detail.flexNowrapCount >= 2) {
    score = Math.min(score, 3);
    flags.push(
      `minor clipping (${detail.clippedCount}) / flex-nowrap (${detail.flexNowrapCount}) / fixed-width (${detail.strictFixedWidthCount})`,
    );
  }

  // Only the PAGE panning sideways is a real failure. An inner overflow-x:auto wrapper that scrolls
  // is the RECOMMENDED "contain wide content" pattern (see responsive-adaptive-mastery.md) — never penalize it.
  if (detail.horizontalRootScrollCount > 0) {
    score = Math.min(score, detail.horizontalRootScrollCount > 1 ? 1 : 2);
    flags.push(`page scrolls horizontally (${detail.horizontalRootScrollCount} root)`);
  } else if (detail.horizontalScrollCount > 3) {
    score = Math.min(score, 4);
    flags.push(`${detail.horizontalScrollCount} inner scroll containers (verify each is intentional)`);
  }

  if (detail.touchBelow24 > 10) {
    score = Math.min(score, 2);
    flags.push(`${detail.touchBelow24} touch targets <24px`);
  } else if (detail.touchBelow24 > 4) {
    score = Math.min(score, 3);
    flags.push(`${detail.touchBelow24} touch targets <24px`);
  } else if (detail.touchBelow24 > 0) {
    score = Math.min(score, 4);
    flags.push(`${detail.touchBelow24} touch targets <24px`);
  } else if (detail.touchBelow44 > 15) {
    score = Math.min(score, 3);
    flags.push(`${detail.touchBelow44} touch targets <44px`);
  } else if (detail.touchBelow44 > 6) {
    score = Math.min(score, 4);
    flags.push(`${detail.touchBelow44} touch targets <44px`);
  }

  if (detail.smallTextCount > 20) {
    score = Math.min(score, 2);
    flags.push(`${detail.smallTextCount} primary text nodes <12px`);
  } else if (detail.smallTextCount > 8) {
    score = Math.min(score, 3);
    flags.push(`${detail.smallTextCount} primary text nodes <12px`);
  } else if (detail.smallTextCount > 2) {
    score = Math.min(score, 4);
    flags.push(`${detail.smallTextCount} primary text nodes <12px`);
  }

  const summary =
    flags.length === 0
      ? 'Clean mobile reflow at 390px and 360px — no clipping, fixed-width, scroll, touch, or text-size issues.'
      : flags.join('; ');

  return { score: clampScore(score), summary, flags };
}

/**
 * Wait for LCP / layout-shift / event timing to populate, then simulate interaction for INP.
 * @param {import('playwright').Page} page
 */
async function waitForWebVitals(page) {
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    const btn =
      document.querySelector('button:not([disabled])') ??
      document.querySelector('[role="button"]') ??
      document.querySelector('a');
    if (btn instanceof HTMLElement) btn.click();
    else document.body.click();
  });
  await page.waitForTimeout(500);
}

/**
 * @param {import('playwright').Page} page
 */
async function runAxeScan(page) {
  await page.addScriptTag({ content: typeof axeSource === 'string' ? axeSource : String(axeSource) });
  return page.evaluate(async () => {
    // @ts-expect-error axe injected
    const results = await window.axe.run(document, {
      runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] },
    });

    /** @param {object} node */
    function summarizeNode(node) {
      const checks = [...(node.any ?? []), ...(node.all ?? []), ...(node.none ?? [])];
      const contrast = checks.find((c) => c.id === 'color-contrast' && c.data);
      const out = {
        target: node.target,
        html: node.html?.slice(0, 120) ?? null,
        failureSummary: node.failureSummary ?? null,
      };
      if (contrast?.data) {
        out.colorContrast = {
          foreground: contrast.data.fgColor ?? contrast.data.foregroundColor ?? null,
          background: contrast.data.bgColor ?? contrast.data.backgroundColor ?? null,
          contrastRatio: contrast.data.contrastRatio ?? null,
          required: contrast.data.expectedContrastRatio ?? contrast.data.requiredContrastRatio ?? null,
          fontSize: contrast.data.fontSize ?? null,
          fontWeight: contrast.data.fontWeight ?? null,
        };
      }
      return out;
    }

    return {
      violations: results.violations.map((v) => ({
        id: v.id,
        impact: v.impact,
        help: v.help,
        description: v.description,
        helpUrl: v.helpUrl,
        nodeCount: v.nodes.length,
        nodes: v.nodes.slice(0, 15).map(summarizeNode),
      })),
      incomplete: results.incomplete.length,
      passes: results.passes.length,
    };
  });
}

/**
 * Find representative interactive elements and capture default/hover/focus states.
 * @param {import('playwright').Page} page
 * @param {string} runDir
 */
async function captureInteractionStates(page, runDir) {
  const targets = await page.evaluate(() => {
    /** @param {string} role @param {string} label */
    function pick(role, label) {
      const candidates = [];
      if (role === 'primary-button') {
        candidates.push(
          ...Array.from(document.querySelectorAll('button.btn-primary, button.primary, button[type="submit"]')),
          ...Array.from(document.querySelectorAll('button')).filter((b) => {
            const cs = getComputedStyle(b);
            return cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
          }),
        );
      } else if (role === 'nav-link') {
        candidates.push(
          ...Array.from(document.querySelectorAll('nav a, [role="navigation"] a, header a')),
          ...Array.from(document.querySelectorAll('a')),
        );
      } else if (role === 'table-row') {
        candidates.push(
          ...Array.from(document.querySelectorAll('tbody tr, tr[data-row], table tr')),
        );
      } else if (role === 'input') {
        candidates.push(
          ...Array.from(document.querySelectorAll('input:not([type="hidden"]), textarea, select')),
        );
      }
      for (const el of candidates) {
        if (!(el instanceof HTMLElement)) continue;
        const rect = el.getBoundingClientRect();
        if (rect.width < 8 || rect.height < 8) continue;
        if (rect.bottom < 0 || rect.top > innerHeight) continue;
        const sel =
          el.id ? `#${el.id}` :
          el.tagName.toLowerCase() + (el.className ? `.${String(el.className).trim().split(/\s+/).slice(0, 2).join('.')}` : '');
        return { role, label, selector: sel };
      }
      return null;
    }
    return ['primary-button', 'nav-link', 'table-row', 'input'].map((r) => pick(r, r)).filter(Boolean);
  });

  const captures = [];
  const cellW = 320;
  const cellH = 120;
  const cols = 3;
  const rows = targets.length;

  for (const target of targets) {
    const loc = page.locator(target.selector).first();
    const visible = await loc.isVisible().catch(() => false);
    if (!visible) continue;

    const base = join(runDir, `state-${target.role}`);
    const paths = { role: target.role, selector: target.selector, default: null, hover: null, focus: null };

    try {
      await loc.scrollIntoViewIfNeeded();
      paths.default = `${base}-default.png`;
      await loc.screenshot({ path: paths.default });
      captures.push({ ...target, state: 'default', path: paths.default });

      await loc.hover({ force: true });
      await page.waitForTimeout(150);
      paths.hover = `${base}-hover.png`;
      await loc.screenshot({ path: paths.hover });
      captures.push({ ...target, state: 'hover', path: paths.hover });

      await page.keyboard.press('Tab').catch(() => {});
      await loc.focus();
      await page.waitForTimeout(100);
      paths.focus = `${base}-focus.png`;
      await loc.screenshot({ path: paths.focus });
      captures.push({ ...target, state: 'focus', path: paths.focus });
    } catch {
      // skip element if not interactable
    }
  }

  let contactSheetPath = null;
  if (captures.length > 0) {
    contactSheetPath = join(runDir, 'desktop-states.png');
    const dataUrls = [];
    for (const cap of captures) {
      const buf = readFileSync(cap.path);
      dataUrls.push({ label: `${cap.role} / ${cap.state}`, data: `data:image/png;base64,${buf.toString('base64')}` });
    }

    await page.evaluate(
      async ({ items, cellW, cellH, cols, rows }) => {
        const canvas = document.createElement('canvas');
        canvas.width = cols * cellW;
        canvas.height = Math.max(1, rows) * cellH;
        const ctx = canvas.getContext('2d');
        if (!ctx) return null;
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < items.length; i++) {
          const col = i % cols;
          const row = Math.floor(i / cols);
          const x = col * cellW;
          const y = row * cellH;
          const img = new Image();
          await new Promise((res, rej) => {
            img.onload = () => res();
            img.onerror = rej;
            img.src = items[i].data;
          });
          const scale = Math.min((cellW - 16) / img.width, (cellH - 28) / img.height, 1);
          const dw = img.width * scale;
          const dh = img.height * scale;
          ctx.fillStyle = '#888';
          ctx.font = '11px system-ui,sans-serif';
          ctx.fillText(items[i].label, x + 8, y + 14);
          ctx.drawImage(img, x + (cellW - dw) / 2, y + 20, dw, dh);
        }

        document.body.appendChild(canvas);
        canvas.id = '__critique_contact_sheet';
        return canvas.toDataURL('image/png');
      },
      { items: dataUrls, cellW, cellH, cols, rows: Math.ceil(captures.length / cols) },
    );

    const sheetEl = page.locator('#__critique_contact_sheet');
    if (await sheetEl.count()) {
      await sheetEl.screenshot({ path: contactSheetPath });
      await page.evaluate(() => document.getElementById('__critique_contact_sheet')?.remove());
    }
  }

  return { targets, captures, contactSheetPath };
}

/** Score helpers — 0 (bad) to 5 (excellent) */
function clampScore(n) {
  return Math.max(0, Math.min(5, Math.round(n)));
}

/**
 * Build rubric entries from aggregated signals.
 * @param {object} agg
 * @param {string[]} screenshotPaths
 */
function buildRubric(agg, screenshotPaths) {
  const { signals, axe, consoleErrors, viewports } = agg;
  const mobile = viewports.find((v) => v.id === 'mobile') ?? viewports[0];
  const desktop = viewports.find((v) => v.id === 'desktop') ?? viewports[0];
  const perf = desktop.signals.performance ?? {};
  const spacing = desktop.signals.spacing ?? { offScaleCount: 0, baseUnit: 4, offScale: [] };

  const rubric = {};

  rubric.hierarchy = {
    score: null,
    status: 'needs_visual_judgment',
    reason: 'Primary action clarity requires looking at screenshots — harness cannot score hierarchy from DOM alone.',
    evidence: {
      screenshots: screenshotPaths,
      hint: 'In 1 second at desktop, is the primary action unmistakable? Compare accent usage vs body text weight.',
    },
  };

  const offScale = spacing.offScaleCount ?? 0;
  const totalAuthored = spacing.authoredValueCount ?? (offScale + 40);
  // Score by RATIO, not absolute count: a dense/complex app authors far more spacing values and
  // would unfairly fail a fixed threshold. What matters is the % of values off the detected grid.
  const offRatio = totalAuthored > 0 ? offScale / totalAuthored : 0;
  let spacingScore = 5;
  if (offRatio >= 0.35) spacingScore = 1;
  else if (offRatio >= 0.20) spacingScore = 2;
  else if (offRatio >= 0.10) spacingScore = 3;
  else if (offRatio >= 0.05) spacingScore = 4;
  rubric.spacing = {
    score: clampScore(spacingScore),
    status: 'auto_scored',
    reason: `${offScale}/${totalAuthored} authored spacing values (${Math.round(offRatio * 100)}%) off the ${spacing.baseUnit}px scale.`,
    evidence: { spacing },
  };

  rubric.typography = {
    score: null,
    status: 'needs_visual_judgment',
    reason: 'Type scale, optical alignment, and line-length need screenshot review; harness extracts scale snapshot.',
    evidence: {
      screenshots: screenshotPaths,
      fontFamilyCount: desktop.signals.fontFamilyCount,
      fontFamilies: desktop.signals.fontFamilies,
      typeScale: desktop.signals.designSystem?.typeScale ?? [],
    },
  };

  const serious = axe.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
  const moderate = axe.violations.filter((v) => v.impact === 'moderate');
  let a11yScore = 5;
  if (serious.length > 0) a11yScore = 1;
  else if (moderate.length > 3) a11yScore = 2;
  else if (moderate.length > 0) a11yScore = 3;
  else if (!desktop.signals.hasFocusVisibleRules) a11yScore = 3;
  else if (axe.violations.length > 0) a11yScore = 4;
  rubric.contrast_a11y = {
    score: clampScore(a11yScore),
    status: 'auto_scored',
    reason: `${serious.length} serious/critical axe violations; focus-visible rules: ${desktop.signals.hasFocusVisibleRules ? 'yes' : 'no'}.`,
    evidence: { axeViolations: axe.violations, hasFocusVisibleRules: desktop.signals.hasFocusVisibleRules },
  };

  const hexRatio = desktop.signals.hexInCss / Math.max(1, desktop.signals.hexInCss + desktop.signals.varInCss);
  let colorScore = 5;
  if (desktop.signals.indigoPaletteHits > 0) colorScore -= 2;
  if (hexRatio > 0.7) colorScore -= 2;
  else if (hexRatio > 0.4) colorScore -= 1;
  if (desktop.signals.distinctColorCount > 25) colorScore -= 1;
  rubric.color_tokens = {
    score: clampScore(colorScore),
    status: 'auto_scored',
    reason: `${desktop.signals.hexInCss} hardcoded hex in CSS vs ${desktop.signals.varInCss} var() uses; indigo-default hits: ${desktop.signals.indigoPaletteHits}; ${desktop.signals.distinctColorCount} distinct colors.`,
    evidence: {
      hexInCss: desktop.signals.hexInCss,
      varInCss: desktop.signals.varInCss,
      indigoPaletteHits: desktop.signals.indigoPaletteHits,
      palette: desktop.signals.designSystem?.palette ?? [],
    },
  };

  const sf = desktop.signals.stateFlags;
  const stateKeys = Object.keys(sf);
  const covered = stateKeys.filter((k) => sf[k]).length;
  let stateScore = Math.round((covered / stateKeys.length) * 5);
  rubric.state_coverage = {
    score: clampScore(stateScore),
    status: 'auto_scored',
    reason: `Static CSS/HTML signals cover ${covered}/${stateKeys.length} state categories; interaction screenshots captured for hover/focus review.`,
    evidence: { stateFlags: sf, interactionStates: agg.interactionStates ?? null },
  };

  const motionProblems = desktop.signals.motionIssues.length;
  let motionScore = 5;
  if (motionProblems > 5) motionScore = 1;
  else if (motionProblems > 2) motionScore = 2;
  else if (motionProblems > 0) motionScore = 3;
  if (!desktop.signals.hasReducedMotion) motionScore = Math.min(motionScore, 3);
  rubric.motion = {
    score: clampScore(motionScore),
    status: 'auto_scored',
    reason: `${motionProblems} motion rule issues; prefers-reduced-motion: ${desktop.signals.hasReducedMotion ? 'present' : 'missing'}.`,
    evidence: {
      motionIssues: desktop.signals.motionIssues,
      hasReducedMotion: desktop.signals.hasReducedMotion,
      easings: desktop.signals.designSystem?.easings ?? [],
    },
  };

  const lcp = perf.lcpMs;
  const cls = perf.cls ?? 0;
  const inp = perf.inpMs;
  let perfScore = 5;
  if (lcp != null && lcp > 4000) perfScore = 1;
  else if (lcp != null && lcp > 2500) perfScore = 2;
  else if (lcp != null && lcp > 1800) perfScore = 3;
  if (cls > 0.25) perfScore = Math.min(perfScore, 1);
  else if (cls > 0.1) perfScore = Math.min(perfScore, 2);
  else if (cls > 0.05) perfScore = Math.min(perfScore, 3);
  if (inp != null && inp > 500) perfScore = Math.min(perfScore, 2);
  else if (inp != null && inp > 200) perfScore = Math.min(perfScore, 3);
  rubric.performance = {
    score: clampScore(perfScore),
    status: 'auto_scored',
    reason: `LCP ${lcp ?? 'pending'} ms, CLS ${cls}, INP ~${inp ?? 'pending'} ms, ${desktop.signals.domNodeCount} DOM nodes.`,
    evidence: { performance: perf, domNodeCount: desktop.signals.domNodeCount },
  };

  // Responsive integrity: mobile audits at 390 + 360 detect clipping/fixed grids, not just page scroll.
  const responsiveDetail = aggregateResponsiveDetail(viewports);
  const { score: respScore, summary: respSummary } = scoreResponsive(responsiveDetail);
  rubric.responsive = {
    score: respScore,
    status: 'auto_scored',
    reason: respSummary,
    evidence: {
      detail: responsiveDetail,
      perViewport: viewports.map((v) => ({
        id: v.id,
        overflow: v.signals.overflow,
        responsive: v.responsive ?? null,
      })),
    },
  };

  rubric.restraint = {
    score: null,
    status: 'needs_visual_judgment',
    reason: 'Anti-AI-median judgment (card tiling, signature, removables) requires screenshot review.',
    evidence: {
      screenshots: screenshotPaths,
      centerAlignRatio: desktop.signals.centerAlignRatio,
      dropShadowElementCount: desktop.signals.dropShadowElementCount,
      hint: 'Could anything be removed? Is this 3-card hero tiling? Any signature element?',
    },
  };

  const scored = Object.entries(rubric).filter(([, v]) => v.score != null);
  let weakest = scored[0];
  for (const entry of scored) {
    if (entry[1].score < weakest[1].score) weakest = entry;
  }

  const visualDims = Object.entries(rubric).filter(([, v]) => v.status === 'needs_visual_judgment');
  const nextWorkItem = weakest
    ? { dimension: weakest[0], score: weakest[1].score, source: 'harness_auto' }
    : { dimension: visualDims[0]?.[0] ?? 'hierarchy', score: null, source: 'agent_visual' };

  return { rubric, nextWorkItem };
}

/**
 * @param {object} report
 */
function renderMarkdown(report) {
  const lines = [];
  lines.push(`# Render Critique Report`);
  lines.push('');
  lines.push(`- **Target:** ${report.meta.target}`);
  lines.push(`- **URL:** ${report.meta.url}`);
  lines.push(`- **Generated:** ${report.meta.timestamp}`);
  lines.push(`- **Gate:** ${report.gate.passed ? 'PASS' : 'FAIL'}`);
  if (report.gate.reasons.length) {
    lines.push(`- **Gate failures:** ${report.gate.reasons.join('; ')}`);
  }
  lines.push('');

  lines.push('## Screenshots');
  for (const vp of report.viewports) {
    lines.push(`- **${vp.label}:** \`${vp.screenshot}\``);
  }
  if (report.interactionStates?.contactSheetPath) {
    lines.push(`- **Interaction states (contact sheet):** \`${report.interactionStates.contactSheetPath}\``);
  }
  lines.push('');

  lines.push('## Performance (Core Web Vitals)');
  const perf = report.viewports.find((v) => v.id === 'desktop')?.signals?.performance ?? {};
  lines.push(`- **LCP:** ${perf.lcpMs ?? 'pending'} ms`);
  if (perf.lcpElement) {
    const el = perf.lcpElement;
    lines.push(`- **LCP element:** \`<${el.tag}${el.id ? ` id="${el.id}"` : ''}${el.className ? ` class="${String(el.className).slice(0, 60)}"` : ''}>\`${el.text ? ` — "${el.text}"` : ''}`);
  }
  lines.push(`- **CLS:** ${perf.cls ?? 0} (${perf.layoutShiftCount ?? 0} shifts)`);
  lines.push(`- **INP (approx):** ${perf.inpMs ?? 'pending'} ms${perf.inpEvent ? ` (${perf.inpEvent})` : ''}`);
  lines.push(`- **DOM nodes:** ${report.viewports.find((v) => v.id === 'desktop')?.signals?.domNodeCount ?? 'n/a'}`);
  lines.push('');

  lines.push('## Design system snapshot');
  const ds = report.viewports.find((v) => v.id === 'desktop')?.signals?.designSystem ?? {};
  lines.push(`- **Type scale (px):** ${(ds.typeScale ?? []).join(', ') || 'none detected'}`);
  lines.push(`- **Palette:** ${(ds.palette ?? []).map((c) => `\`${c}\``).join(' ') || 'none detected'}`);
  lines.push(`- **Radius scale (px):** ${(ds.radiusScale ?? []).join(', ') || 'none detected'}`);
  lines.push(`- **Easing curves:** ${(ds.easings ?? []).join(', ') || 'none detected'}`);
  lines.push('');

  lines.push('## Spacing rhythm (authored CSS)');
  const sp = report.viewports.find((v) => v.id === 'desktop')?.signals?.spacing ?? {};
  lines.push(`- **Detected base unit:** ${sp.baseUnit ?? 4}px (mode ${sp.detectedScale ?? 'n/a'}, ${sp.authoredValueCount ?? 0} authored values scanned)`);
  lines.push(`- **Off-scale authored values:** ${sp.offScaleCount ?? 0}`);
  for (const item of sp.offScale ?? []) {
    lines.push(`  - \`${item.prop}: ${item.value}\` (${item.px}px) — e.g. ${item.selectors.slice(0, 2).join(', ')}`);
  }
  lines.push('');

  lines.push('## Accessibility (axe — actionable)');
  if (report.axe.violations.length === 0) {
    lines.push('- No violations.');
  } else {
    for (const v of report.axe.violations) {
      lines.push(`### ${v.id} (${v.impact})`);
      lines.push(`- **Help:** ${v.help}`);
      lines.push(`- **Nodes:** ${v.nodeCount} total (showing ${v.nodes.length})`);
      for (const node of v.nodes) {
        const sel = Array.isArray(node.target) ? node.target.join(' › ') : String(node.target);
        lines.push(`- **Target:** \`${sel}\``);
        if (node.failureSummary) lines.push(`  - ${node.failureSummary.replace(/\n/g, ' ')}`);
        if (node.colorContrast) {
          const cc = node.colorContrast;
          lines.push(`  - **Contrast:** fg \`${cc.foreground}\` on bg \`${cc.background}\` → ratio **${cc.contrastRatio}** (required **${cc.required}**)`);
        }
      }
      lines.push('');
    }
  }
  lines.push('');

  lines.push('## Responsive integrity (mobile 390 + 360)');
  const rd = report.rubric.responsive?.evidence?.detail;
  if (rd) {
    lines.push(`- **Clipped elements:** ${rd.clippedCount} (max overflow ${rd.clippedMaxOverflow}px)`);
    for (const c of rd.samples.clipped ?? []) {
      lines.push(`  - \`${c.selector}\` overflows ${c.maxOverflow}px`);
    }
    lines.push(`- **Fixed-width violations:** ${rd.fixedWidthCount}`);
    for (const f of rd.samples.fixedWidth ?? []) {
      lines.push(`  - \`${f.selector}\` ${f.kind} ${f.px}px`);
    }
    lines.push(`- **Horizontal scroll containers:** ${rd.horizontalScrollCount}`);
    lines.push(`- **Touch targets <44px:** ${rd.touchBelow44} (<24px: ${rd.touchBelow24})`);
    lines.push(`- **Text nodes <12px:** ${rd.smallTextCount}`);
  } else {
    lines.push('- No mobile responsive audit data.');
  }
  lines.push('');

  lines.push('## Interaction state captures');
  if (!report.interactionStates?.captures?.length) {
    lines.push('- No interactive elements captured.');
  } else {
    for (const cap of report.interactionStates.captures) {
      lines.push(`- **${cap.role} / ${cap.state}** (\`${cap.selector}\`): \`${cap.path}\``);
    }
  }
  lines.push('');

  lines.push('## 10-Dimension Rubric');
  lines.push('');
  lines.push('| # | Dimension | Score | Status | Reason |');
  lines.push('|---|-----------|-------|--------|--------|');
  RUBRIC.forEach((dim, i) => {
    const r = report.rubric[dim.id];
    const score = r.score == null ? '—' : String(r.score);
    lines.push(`| ${i + 1} | ${dim.name} | ${score}/5 | ${r.status} | ${r.reason} |`);
  });
  lines.push('');

  lines.push('## Next Work Item (single weakest dimension)');
  lines.push('');
  lines.push(`**${report.nextWorkItem.dimension}** (score ${report.nextWorkItem.score ?? 'visual review'}/5, source: ${report.nextWorkItem.source})`);
  lines.push('');

  lines.push('## Console & Network');
  lines.push('');
  if (report.console.errors.length === 0) lines.push('- No console errors.');
  else report.console.errors.forEach((e) => lines.push(`- ERROR: ${e}`));
  if (report.console.warnings.length) {
    report.console.warnings.slice(0, 10).forEach((w) => lines.push(`- WARN: ${w}`));
  }
  if (report.pageErrors.length) {
    report.pageErrors.forEach((e) => lines.push(`- PAGE ERROR: ${e}`));
  }
  if (report.failedRequests.length) {
    lines.push('');
    lines.push('### Failed network requests');
    report.failedRequests.forEach((r) => lines.push(`- ${r.status ?? 'failed'} ${r.url}`));
  }
  lines.push('');

  lines.push('## Token-drift heuristics (desktop)');
  const s = report.viewports.find((v) => v.id === 'desktop')?.signals;
  if (s) {
    lines.push(`- Font families: ${s.fontFamilyCount}`);
    lines.push(`- Distinct colors: ${s.distinctColorCount}`);
    lines.push(`- Hex in CSS: ${s.hexInCss} / var(): ${s.varInCss}`);
    lines.push(`- Indigo-default hits: ${s.indigoPaletteHits}`);
    lines.push(`- text-align:center ratio: ${s.centerAlignRatio}`);
    lines.push(`- Elements with shadow/drop-shadow: ${s.dropShadowElementCount}`);
    lines.push(`- :focus-visible rules: ${s.hasFocusVisibleRules ? 'yes' : 'no'}`);
  }
  lines.push('');

  lines.push('## Agent visual review checklist');
  lines.push('');
  lines.push('Dimensions marked `needs_visual_judgment` — open screenshots + `desktop-states.png` and score 0–5:');
  lines.push('1. **Hierarchy** — primary action in 1s?');
  lines.push('3. **Typography** — real scale, not Inter-default mush?');
  lines.push('10. **Restraint** — signature vs AI-median card pile?');
  lines.push('');

  return lines.join('\n');
}

/** Resolve a usable Chromium binary (bundled full build, headless shell, or system Chrome). */
function resolveChromiumLaunchOptions() {
  const caches = [
    process.env.PLAYWRIGHT_BROWSERS_PATH,
    join(homedir(), 'Library/Caches/ms-playwright'),
    join(homedir(), '.cache', 'ms-playwright'),
  ].filter(Boolean);

  const builds = ['1148', '1228', '1223'];
  const platformPaths = (root, ver) => {
    if (process.platform === 'darwin') {
      return join(root, `chromium-${ver}`, 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium');
    }
    if (process.platform === 'linux') {
      return join(root, `chromium-${ver}`, 'chrome-linux', 'chrome');
    }
    if (process.platform === 'win32') {
      return join(root, `chromium-${ver}`, 'chrome-win', 'chrome.exe');
    }
    return null;
  };

  for (const root of caches) {
    for (const ver of builds) {
      const full = platformPaths(root, ver);
      if (full && existsSync(full)) return { executablePath: full, headless: true };
    }
  }

  return { headless: true };
}

/** Launch Chromium with fallback to system Chrome if bundled browser missing. */
async function launchBrowser() {
  const opts = resolveChromiumLaunchOptions();
  try {
    return await chromium.launch(opts);
  } catch {
    console.warn('Bundled Chromium unavailable, falling back to channel=chrome');
    return chromium.launch({ channel: 'chrome', headless: true });
  }
}

async function main() {
  const { target, outDir } = parseArgs(process.argv.slice(2));
  mkdirSync(outDir, { recursive: true });

  let url = target;
  let serverClose = async () => {};

  if (!isUrl(target)) {
    const abs = resolve(target);
    if (extname(abs).toLowerCase() !== '.html' && extname(abs).toLowerCase() !== '.htm') {
      console.error('Local target must be a .html file or a full http(s) URL');
      process.exit(2);
    }
    const served = await serveHtml(abs);
    url = served.url;
    serverClose = served.close;
  }

  const runId = new Date().toISOString().replace(/[:.]/g, '-');
  const runDir = join(outDir, runId);
  mkdirSync(runDir, { recursive: true });

  const consoleErrors = [];
  const consoleWarnings = [];
  const pageErrors = [];
  const failedRequests = [];

  const browser = await launchBrowser();
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.addInitScript(VITALS_INIT_SCRIPT);

  page.on('console', (msg) => {
    const text = msg.text();
    if (msg.type() === 'error') consoleErrors.push(text);
    else if (msg.type() === 'warning') consoleWarnings.push(text);
  });
  page.on('pageerror', (err) => pageErrors.push(err.message));
  page.on('requestfailed', (req) => {
    failedRequests.push({ url: req.url(), failure: req.failure()?.errorText ?? 'unknown' });
  });
  page.on('response', (res) => {
    const status = res.status();
    if (status >= 400) {
      failedRequests.push({ url: res.url(), status });
    }
  });

  const viewportResults = [];
  const screenshotPaths = [];
  let axeResults = { violations: [], incomplete: 0, passes: 0 };
  let interactionStates = null;

  for (const vp of VIEWPORTS) {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });

    if (vp.id === 'desktop') {
      await waitForWebVitals(page);
      axeResults = await runAxeScan(page);
      interactionStates = await captureInteractionStates(page, runDir);
    } else {
      await page.waitForTimeout(800);
    }

    const signals = await page.evaluate(collectDomSignals);
    let responsive = null;
    if (RESPONSIVE_MOBILE_IDS.has(vp.id)) {
      responsive = await page.evaluate(collectResponsiveSignals);
    }

    const screenshotFile = `${vp.id}-${vp.width}x${vp.height}.png`;
    const screenshotPath = join(runDir, screenshotFile);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    screenshotPaths.push(screenshotPath);

    viewportResults.push({
      id: vp.id,
      label: vp.label,
      width: vp.width,
      height: vp.height,
      screenshot: screenshotPath,
      signals,
      responsive,
    });
  }

  await browser.close();
  await serverClose();

  const responsiveDetail = aggregateResponsiveDetail(viewportResults);
  const { score: responsiveScore } = scoreResponsive(responsiveDetail);
  const seriousAxe = axeResults.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');

  const gateReasons = [];
  if (consoleErrors.length) gateReasons.push(`${consoleErrors.length} console error(s)`);
  if (pageErrors.length) gateReasons.push(`${pageErrors.length} uncaught exception(s)`);
  if (seriousAxe.length) gateReasons.push(`${seriousAxe.length} critical/serious axe violation(s)`);
  // Gate fails on actual mobile LAYOUT BREAKAGE (clipping past viewport / fixed-width grid that won't adapt /
  // page panning sideways) — per the rubric's documented gate. A low responsive score driven ONLY by small text
  // or touch-target size is a quality issue (it lowers dim 9), not "unshippable", so it does NOT fail the gate.
  const layoutBreakage = !!responsiveDetail && (
    (responsiveDetail.clippedCount ?? 0) >= 4 ||            // systemic clipping
    (responsiveDetail.clippedMaxOverflow ?? 0) >= 48 ||     // content meaningfully cut off (not a minor nudge)
    (responsiveDetail.strictFixedWidthCount ?? 0) >= 1 ||   // a fixed/min-width grid that won't adapt
    (responsiveDetail.horizontalRootScrollCount ?? 0) >= 1  // the page itself pans sideways
  );
  if (layoutBreakage) {
    gateReasons.push(`mobile layout breakage — responsive ${responsiveScore}/5 (clipping/fixed-width/page-scroll at 360/390)`);
  }

  const agg = {
    signals: viewportResults.find((v) => v.id === 'desktop')?.signals,
    axe: axeResults,
    consoleErrors,
    viewports: viewportResults,
    interactionStates,
  };
  const { rubric, nextWorkItem } = buildRubric(agg, screenshotPaths);

  const report = {
    meta: {
      target,
      url,
      timestamp: new Date().toISOString(),
      runDir,
      viewports: VIEWPORTS.map((v) => v.label),
    },
    viewports: viewportResults,
    console: { errors: consoleErrors, warnings: consoleWarnings },
    pageErrors,
    failedRequests,
    axe: axeResults,
    interactionStates,
    rubric,
    nextWorkItem,
    gate: { passed: gateReasons.length === 0, reasons: gateReasons },
  };

  const jsonPath = join(runDir, 'report.json');
  const mdPath = join(runDir, 'report.md');
  writeFileSync(jsonPath, JSON.stringify(report, null, 2), 'utf8');
  writeFileSync(mdPath, renderMarkdown(report), 'utf8');

  console.log(`Report written:`);
  console.log(`  ${jsonPath}`);
  console.log(`  ${mdPath}`);
  console.log(`Gate: ${report.gate.passed ? 'PASS' : 'FAIL'}`);
  if (gateReasons.length) console.log(`  Reasons: ${gateReasons.join('; ')}`);
  console.log(`Weakest auto-scored dimension: ${nextWorkItem.dimension} (${nextWorkItem.score}/5)`);

  process.exit(report.gate.passed ? 0 : 1);
}

main().catch((err) => {
  console.error(err);
  process.exit(2);
});
