import { chromium } from 'playwright';
const b = await chromium.launch({ channel: 'chrome' });
const c = await b.newContext({ viewport: { width: 1440, height: 900 } });
const p = await c.newPage();
await p.goto(process.argv[2], { waitUntil: 'load' });
await p.waitForTimeout(2000);
await p.screenshot({ path: process.argv[3], fullPage: process.argv[4] !== 'viewport' });
await b.close();
console.log('shot saved:', process.argv[3]);
