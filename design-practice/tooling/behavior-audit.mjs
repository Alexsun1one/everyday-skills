// BEHAVIOR AUDIT — the thing the static harness is blind to.
// Drives the LIVE app: are the controls REAL, or a static facade?
//   1) naked native controls (select/checkbox/radio/range not restyled)
//   2) dead buttons (click → ZERO DOM mutation) — EXCLUDING the cases where no-op is correct:
//      disabled, already-active toggles, and file-dialog triggers (open a native picker, no DOM change)
//   3) hover-feedback (cursor → does the element respond?)
//   4) a11yDepth — keyboard focus-visible, dialog trap/Esc, ARIA semantics
// Usage: node behavior-audit.mjs <url> [--max=44]
import { chromium } from 'playwright';

const url = process.argv[2];
const max = Number((process.argv.find((a) => a.startsWith('--max=')) || '--max=44').split('=')[1]);
if (!url) { console.error('usage: node behavior-audit.mjs <url>'); process.exit(2); }

const browser = await chromium.launch({ channel: 'chrome' });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(1200);

// 1) naked native form controls
const nativeControls = await page.evaluate(() => {
  const out = [];
  for (const el of document.querySelectorAll('select, input[type=checkbox], input[type=radio], input[type=range]')) {
    const cs = getComputedStyle(el);
    const ap = cs.appearance || cs.webkitAppearance || '';
    if (ap && ap !== 'none') {
      out.push({ tag: el.tagName.toLowerCase(), type: el.getAttribute('type') || '', appearance: ap,
        sel: el.id ? '#' + el.id : (el.className ? '.' + String(el.className).split(' ')[0] : el.tagName.toLowerCase()) });
    }
  }
  return out;
});

const interactiveCount = await page.evaluate(() =>
  document.querySelectorAll('button, [role="button"], a[href], input, select, textarea, [tabindex]:not([tabindex="-1"]), [onclick]').length);
const buttonCount = await page.evaluate(() => document.querySelectorAll('button, [role="button"]').length);

// 2) dead-button test — reload before each click for a clean state, observe DOM mutations.
// EXCLUDE controls where "no DOM change" is EXPECTED (disabled / already-active / opens a file dialog).
let live = 0, dead = 0, skipped = 0, fileDialog = 0;
const deadSample = [];
const n = Math.min(buttonCount, max);
for (let i = 0; i < n; i++) {
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(350);
  const r = await page.evaluate(async (idx) => {
    const btns = document.querySelectorAll('button, [role="button"]');
    const el = btns[idx];
    if (!el) return { skip: 'none' };
    const label = (el.getAttribute('aria-label') || el.textContent || el.className || 'btn').replace(/\s+/g, ' ').trim().slice(0, 34) || '(icon)';
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') return { skip: 'disabled', label };
    if (['aria-pressed', 'aria-selected', 'aria-checked'].some((a) => el.getAttribute(a) === 'true')) return { skip: 'active', label };
    const isFileDialog = !!el.querySelector('input[type=file]')
      || !!(el.parentElement && el.parentElement.querySelector('input[type=file]'))
      || /上传|upload|导入|import|选择文件|choose file|browse|浏览/i.test(label);
    let mutations = 0;
    const obs = new MutationObserver((ms) => { mutations += ms.length; });
    obs.observe(document.documentElement, { subtree: true, childList: true, attributes: true, characterData: true });
    const urlBefore = location.href;
    try { el.click(); } catch (_) {}
    await new Promise((res) => setTimeout(res, 380));
    obs.disconnect();
    return { label, mutations, navigated: location.href !== urlBefore, isFileDialog };
  }, i);
  if (r.skip === 'none') continue;
  if (r.skip) { skipped++; continue; }
  if (r.mutations > 0 || r.navigated) live++;
  else if (r.isFileDialog) fileDialog++;          // opens a native picker — not dead
  else { dead++; deadSample.push(r.label); }
}
const tested = live + dead;
const liveRatio = tested ? Math.round((live / tested) * 100) : 100;

// 3) HOVER-FEEDBACK — do interactive elements respond to the cursor? ("鼠标移上去有个轻微变化")
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(700);
let hoverResp = 0, hoverStatic = 0; const hStatic = [];
const sig = (el) => { const c = getComputedStyle(el); return [c.backgroundColor, c.borderColor, c.color, c.transform, c.boxShadow, c.opacity].join('|'); };
const handles = await page.$$('button:not([aria-pressed="true"]):not([aria-selected="true"]), [role="button"], tbody tr, [role="row"], a[href], .card, .row, .nav__link, .day-tab, .tab, .tier');
for (const h of handles.slice(0, 18)) {
  try {
    const before = await h.evaluate(sig);
    await h.hover({ timeout: 700 });
    await page.waitForTimeout(150);
    const after = await h.evaluate(sig);
    if (before !== after) hoverResp++;
    else { hoverStatic++; const lbl = await h.evaluate((el) => (el.getAttribute('aria-label') || el.textContent || el.className || el.tagName).replace(/\s+/g, ' ').trim().slice(0, 26)); hStatic.push(lbl || '(el)'); }
    await page.mouse.move(2, 2);
  } catch (_) {}
}
const hoverTested = hoverResp + hoverStatic;
const hoverRatio = hoverTested ? Math.round((hoverResp / hoverTested) * 100) : 0;

// 4) A11Y DEPTH — keyboard focus-visible, dialog trap/Esc, ARIA semantics
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(700);

/** @param {import('playwright').Page} pg */
async function auditFocusVisible(pg) {
  const focusable = await pg.evaluate(() => {
    const sel =
      'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
    return Array.from(document.querySelectorAll(sel))
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) return false;
        const cs = getComputedStyle(el);
        return cs.display !== 'none' && cs.visibility !== 'hidden';
      })
      .slice(0, 24)
      .map((el) => {
        const id = el.id;
        const cls = el.className?.toString?.()?.trim();
        let selector = el.tagName.toLowerCase();
        if (id) selector = `#${id}`;
        else if (cls) selector = `${el.tagName.toLowerCase()}.${cls.split(/\s+/)[0]}`;
        const label = (el.getAttribute('aria-label') || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40);
        return { selector, label, tag: el.tagName.toLowerCase() };
      });
  });

  let focusVisible = 0;
  let noFocusRing = [];
  let reached = 0;

  await pg.evaluate(() => {
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
    document.body.setAttribute('tabindex', '-1');
    document.body.focus();
  });

  for (const item of focusable) {
    const result = await pg.evaluate((selector) => {
      const el = document.querySelector(selector);
      if (!(el instanceof HTMLElement)) return null;

      function styleSig(node) {
        const cs = getComputedStyle(node);
        return {
          outlineWidth: cs.outlineWidth,
          outlineStyle: cs.outlineStyle,
          outlineColor: cs.outlineColor,
          boxShadow: cs.boxShadow,
          borderColor: cs.borderColor,
          borderWidth: cs.borderWidth,
          backgroundColor: cs.backgroundColor,
        };
      }

      if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
      const before = styleSig(el);
      el.focus();
      const focused = styleSig(el);
      const isFocused = document.activeElement === el;

      const outlineVisible =
        focused.outlineStyle !== 'none' &&
        parseFloat(focused.outlineWidth) > 0 &&
        focused.outlineColor !== 'rgba(0, 0, 0, 0)';

      const changed =
        focused.boxShadow !== before.boxShadow ||
        focused.borderColor !== before.borderColor ||
        focused.borderWidth !== before.borderWidth ||
        focused.backgroundColor !== before.backgroundColor ||
        focused.outlineWidth !== before.outlineWidth ||
        focused.outlineStyle !== before.outlineStyle;

      return { isFocused, hasVisibleFocus: outlineVisible || changed };
    }, item.selector);

    if (!result?.isFocused) continue;
    reached++;
    if (result.hasVisibleFocus) focusVisible++;
    else noFocusRing.push(item);
  }

  const focusVisibleRatio = reached ? Math.round((focusVisible / reached) * 100) / 100 : 1;
  return { focusableCount: focusable.length, reachedCount: reached, focusVisibleCount: focusVisible, focusVisibleRatio, noFocusRingSample: noFocusRing.slice(0, 8) };
}

/** @param {import('playwright').Page} pg */
async function auditDialogs(pg) {
  const dialogMeta = await pg.evaluate(() => {
    const open = Array.from(document.querySelectorAll('[role="dialog"], [aria-modal="true"]'))
      .filter((el) => {
        const cs = getComputedStyle(el);
        return cs.display !== 'none' && cs.visibility !== 'hidden';
      })
      .map((el) => ({
        selector: el.id ? `#${el.id}` : `[role="${el.getAttribute('role')}"]`,
        hasAccessibleName: !!(el.getAttribute('aria-label') || el.getAttribute('aria-labelledby')),
        label: el.getAttribute('aria-label') || null,
      }));

    const triggers = Array.from(document.querySelectorAll(
      'button, [role="button"], a[href]',
    ))
      .filter((el) => {
        const t = (el.textContent || el.getAttribute('aria-label') || '').toLowerCase();
        return /modal|dialog|open|settings|menu|drawer|详情|设置|弹窗|抽屉/.test(t);
      })
      .slice(0, 6)
      .map((el) => ({
        selector: el.id ? `#${el.id}` : el.tagName.toLowerCase(),
        label: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40),
      }));

    return { open, triggers };
  });

  const results = [];

  async function testDialogState(selector, label, openedByClick) {
    const trapped = await pg.evaluate((sel) => {
      const dialog = document.querySelector(sel);
      if (!dialog) return false;
      const focusables = dialog.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])',
      );
      if (!focusables.length) return false;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (!(first instanceof HTMLElement) || !(last instanceof HTMLElement)) return false;
      last.focus();
      const ev = new KeyboardEvent('keydown', { key: 'Tab', bubbles: true, cancelable: true });
      last.dispatchEvent(ev);
      // After trap, focus should stay inside dialog (wrap to first or remain in dialog)
      return dialog.contains(document.activeElement);
    }, selector);

    let escCloses = false;
    await pg.keyboard.press('Escape');
    await pg.waitForTimeout(250);
    escCloses = await pg.evaluate((sel) => {
      const dialog = document.querySelector(sel);
      if (!dialog) return true;
      const cs = getComputedStyle(dialog);
      return cs.display === 'none' || cs.visibility === 'hidden' || dialog.getAttribute('aria-hidden') === 'true';
    }, selector);

    const hasAccessibleName = await pg.evaluate((sel) => {
      const dialog = document.querySelector(sel);
      if (!dialog) return false;
      return !!(dialog.getAttribute('aria-label') || dialog.getAttribute('aria-labelledby'));
    }, selector);

    results.push({ selector, label, openedByClick, trapped, escCloses, hasAccessibleName });
  }

  for (const d of dialogMeta.open) {
    await testDialogState(d.selector, d.label || d.selector, false);
  }

  for (const tr of dialogMeta.triggers) {
    await pg.goto(url, { waitUntil: 'load' });
    await pg.waitForTimeout(500);
    try {
      await pg.click(tr.selector, { timeout: 2000 });
      await pg.waitForTimeout(400);
      const opened = await pg.evaluate(() =>
        Array.from(document.querySelectorAll('[role="dialog"], [aria-modal="true"]')).find((el) => {
          const cs = getComputedStyle(el);
          return cs.display !== 'none' && cs.visibility !== 'hidden';
        }),
      );
      if (opened) {
        const sel = await pg.evaluate((el) => (el.id ? `#${el.id}` : '[role="dialog"]'), opened);
        await testDialogState(sel, tr.label, true);
      }
    } catch (_) {}
  }

  return results;
}

/** @param {import('playwright').Page} pg */
async function auditAriaSemantics(pg) {
  return pg.evaluate(() => {
    const violations = [];

    for (const dialog of document.querySelectorAll('[role="dialog"]')) {
      if (!dialog.getAttribute('aria-label') && !dialog.getAttribute('aria-labelledby')) {
        violations.push({
          rule: 'dialog-accessible-name',
          selector: dialog.id ? `#${dialog.id}` : '[role="dialog"]',
          detail: 'role=dialog missing aria-label and aria-labelledby',
        });
      }
    }

    for (const tablist of document.querySelectorAll('[role="tablist"]')) {
      const tabs = tablist.querySelectorAll('[role="tab"]');
      const tabIndices = Array.from(tabs).map((t) => t.getAttribute('tabindex'));
      const hasRoving = tabIndices.some((v) => v === '0') && tabIndices.filter((v) => v === '-1').length >= tabs.length - 1;
      if (tabs.length > 1 && !hasRoving && !tabIndices.every((v) => v === '0' || v === null)) {
        violations.push({
          rule: 'tablist-roving-tabindex',
          selector: tablist.id ? `#${tablist.id}` : '[role="tablist"]',
          detail: `tablist with ${tabs.length} tabs lacks roving tabindex (expected one tabindex=0, rest -1)`,
        });
      }
    }

    for (const btn of document.querySelectorAll('button, [role="button"]')) {
      const isToggle =
        btn.hasAttribute('aria-pressed') ||
        btn.hasAttribute('aria-checked') ||
        btn.hasAttribute('aria-expanded') ||
        /toggle|switch|tab/i.test(btn.className?.toString?.() ?? '') ||
        /toggle|switch/i.test(btn.getAttribute('aria-label') ?? '');
      const hasState =
        btn.hasAttribute('aria-pressed') ||
        btn.hasAttribute('aria-checked') ||
        btn.hasAttribute('aria-expanded');
      if (isToggle && !hasState) {
        violations.push({
          rule: 'toggle-missing-aria-state',
          selector: btn.id ? `#${btn.id}` : 'button',
          detail: 'toggle-like button missing aria-pressed/aria-checked/aria-expanded',
          label: (btn.textContent || btn.getAttribute('aria-label') || '').trim().slice(0, 40),
        });
      }
    }

    return violations.slice(0, 20);
  });
}

const focusAudit = await auditFocusVisible(page);
const ariaViolations = await auditAriaSemantics(page);
const dialogAudits = await auditDialogs(page);

let a11yDepthScore = 5;
if (focusAudit.reachedCount === 0 && focusAudit.focusableCount > 0) a11yDepthScore = Math.min(a11yDepthScore, 2);
else if (focusAudit.focusVisibleRatio < 0.35) a11yDepthScore = 1;
else if (focusAudit.focusVisibleRatio < 0.55) a11yDepthScore = Math.min(a11yDepthScore, 2);
else if (focusAudit.focusVisibleRatio < 0.75) a11yDepthScore = Math.min(a11yDepthScore, 3);
else if (focusAudit.focusVisibleRatio < 0.9) a11yDepthScore = Math.min(a11yDepthScore, 4);

for (const d of dialogAudits) {
  if (!d.hasAccessibleName) a11yDepthScore = Math.min(a11yDepthScore, 2);
  if (d.openedByClick && !d.trapped) a11yDepthScore = Math.min(a11yDepthScore, 2);
  if (d.openedByClick && !d.escCloses) a11yDepthScore = Math.min(a11yDepthScore, 3);
}

if (ariaViolations.length > 5) a11yDepthScore = Math.min(a11yDepthScore, 1);
else if (ariaViolations.length > 2) a11yDepthScore = Math.min(a11yDepthScore, 2);
else if (ariaViolations.length > 0) a11yDepthScore = Math.min(a11yDepthScore, 3);

const a11yDepth = {
  a11yDepthScore,
  focusVisibleRatio: focusAudit.focusVisibleRatio,
  focusableCount: focusAudit.focusableCount,
  reachedCount: focusAudit.reachedCount,
  focusVisibleCount: focusAudit.focusVisibleCount,
  noFocusRingSample: focusAudit.noFocusRingSample,
  dialogAudits,
  ariaViolations,
  ariaViolationCount: ariaViolations.length,
};

let score = 5;
if (nativeControls.length) score = Math.min(score, 2);
if (liveRatio < 30) score = 1;
else if (liveRatio < 50) score = Math.min(score, 2);
else if (liveRatio < 70) score = Math.min(score, 3);
else if (liveRatio < 85) score = Math.min(score, 4);
if (hoverRatio < 40) score = Math.min(score, 2);
else if (hoverRatio < 65) score = Math.min(score, 3);
if (a11yDepthScore <= 2) score = Math.min(score, a11yDepthScore);
else if (a11yDepthScore <= 3) score = Math.min(score, 4);

console.log(JSON.stringify({
  url,
  behaviorScore: score,
  nakedNativeControls: nativeControls.length,
  nativeDetail: nativeControls.slice(0, 6),
  interactiveCount, buttonsTested: tested, live, dead, liveRatio: liveRatio + '%',
  skipped, fileDialog,                                   // excluded from dead (no-op is correct here)
  hoverResponsiveRatio: hoverRatio + '%', hoverStaticSample: hStatic.slice(0, 10),
  deadSample: deadSample.slice(0, 12),
  a11yDepth,
}, null, 1));
await browser.close();
