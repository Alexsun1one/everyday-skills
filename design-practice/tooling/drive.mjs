// Drive a LIVE app through an interaction sequence and capture each step,
// so the felt interaction (states, flow, transitions) can be judged — not just static look.
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
const url = process.argv[2], out = process.argv[3] || '/tmp/drive';
mkdirSync(out, { recursive: true });
const b = await chromium.launch({ channel: 'chrome' });
const c = await b.newContext({ viewport: { width: 1440, height: 900 } });
const p = await c.newPage();
const log = [];
await p.goto(url, { waitUntil: 'load' });
await p.waitForTimeout(1500);
const shot = async (n) => { await p.screenshot({ path: `${out}/${n}.png` }); log.push('ok ' + n); };
await shot('1-default');
// hover the primary action button
try {
  const btn = p.getByRole('button', { name: /new issue|new deal|new invoice|new/i }).first();
  await btn.hover(); await p.waitForTimeout(250); await shot('2-primary-hover');
} catch (e) { log.push('btn-hover FAIL ' + e.message.slice(0, 60)); }
// open the command palette (⌘K)
try {
  await p.keyboard.press('Meta+k'); await p.waitForTimeout(450); await shot('3-cmdk');
  await p.keyboard.press('Escape'); await p.waitForTimeout(250);
} catch (e) { log.push('cmdk FAIL ' + e.message.slice(0, 60)); }
// click the first data row to open the detail drawer (try several selectors)
let opened = false;
for (const sel of ['tbody tr', '[role="row"]', '.issue-row', '.row', '.deal-row', 'li[role="button"]']) {
  try {
    const row = p.locator(sel).filter({ hasText: /.+/ }).first();
    if (await row.count()) { await row.click({ timeout: 1500 }); await p.waitForTimeout(600); await shot('4-detail-drawer'); opened = true; break; }
  } catch (e) { /* try next */ }
}
if (!opened) log.push('row-click: no drawer opened');
console.log(log.join('\n'));
await b.close();
