import { chromium } from 'playwright';
const b = await chromium.launch({ channel: 'chrome' });
const c = await b.newContext({ viewport: { width: 390, height: 844 } });
const p = await c.newPage();
const failed = [];
p.on('response', (r) => { if (r.status() === 404) failed.push(r.url()); });
await p.goto('http://localhost:8799/index.html', { waitUntil: 'load' });
await p.waitForTimeout(1500);
const over = await p.evaluate(() => {
  const vw = document.documentElement.clientWidth;
  const out = [];
  for (const el of document.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    // only near-edge offenders that extend the PAGE (ignore far-scrolled content inside overflow rails)
    if (r.right > vw + 1 && r.right < vw + 120 && r.width <= vw + 120) {
      out.push({ tag: el.tagName.toLowerCase(), cls: (el.className && el.className.toString().slice(0, 44)) || '', right: Math.round(r.right), w: Math.round(r.width) });
    }
  }
  return { vw, docScrollW: document.documentElement.scrollWidth, items: out.sort((a, b) => b.right - a.right).slice(0, 12) };
});
console.log('404s:', JSON.stringify([...new Set(failed)]));
console.log(JSON.stringify(over, null, 1));
await b.close();
