// Record a MOTION video of the live UI's interactions — the only way to judge 呼吸感.
import { chromium } from 'playwright';
const url = process.argv[2], dir = process.argv[3] || '/tmp/rec';
const b = await chromium.launch({ channel: 'chrome' });
const c = await b.newContext({ viewport: { width: 1440, height: 900 }, recordVideo: { dir, size: { width: 1440, height: 900 } } });
const p = await c.newPage();
await p.goto(url, { waitUntil: 'load' });
await p.waitForTimeout(1200);
const safe = async (fn) => { try { await fn(); } catch (_) {} };
// 1) hover sweep — shows hover micro-feedback
for (const sel of ['.workspace-tab', '.small-tab', '.preset-tab', '.icon-btn', '.transport-btn', '.tiny-btn']) {
  const els = await p.$$(sel);
  for (const e of els.slice(0, 4)) { await safe(async () => { await e.hover({ timeout: 600 }); await p.waitForTimeout(240); }); }
}
await p.mouse.move(700, 450); await p.waitForTimeout(200);
// 2) click tabs/tools — active-state transitions
for (const sel of ['.workspace-tab', '.preset-tab', '.small-tab']) {
  const els = await p.$$(sel);
  for (const e of els.slice(0, 3)) { await safe(async () => { await e.click({ timeout: 700 }); await p.waitForTimeout(380); }); }
}
// 3) drag a slider / open a custom dropdown if present
await safe(async () => {
  const r = await p.$('input[type=range], [role="slider"]');
  if (r) { const box = await r.boundingBox(); if (box) { await p.mouse.move(box.x + box.width * 0.3, box.y + box.height / 2); await p.mouse.down(); await p.mouse.move(box.x + box.width * 0.85, box.y + box.height / 2, { steps: 12 }); await p.mouse.up(); await p.waitForTimeout(400); } }
});
await safe(async () => { const d = await p.$('[aria-haspopup="listbox"], .dropdown-trigger'); if (d) { await d.click(); await p.waitForTimeout(500); await p.keyboard.press('Escape'); } });
// 4) transport play — playhead motion
await safe(async () => { const play = await p.$('.transport-btn.play, .transport-btn'); if (play) { await play.click(); await p.waitForTimeout(1800); } });
await p.waitForTimeout(400);
await c.close(); await b.close();
console.log('video dir:', dir);
