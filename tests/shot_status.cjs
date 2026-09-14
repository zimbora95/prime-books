#!/usr/bin/env node
/* Screenshot /status (full page + first screen) for visual review. */
const { chromium } = require('/tmp/node_modules/playwright-core');
const BASE = process.env.PB_BASE || 'http://127.0.0.1:8645';
const EXE = '/root/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome';
(async () => {
  const b = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1180, height: 900 } });
  await p.goto(BASE + '/status', { waitUntil: 'domcontentloaded' });
  await p.waitForSelector('#years table tbody tr', { timeout: 15000 });
  await p.waitForFunction(() => document.getElementById('t-books').textContent !== '–');
  await p.waitForTimeout(400);
  await p.screenshot({ path: '/root/status-top.png' });
  await p.screenshot({ path: '/root/status-full.png', fullPage: true });
  console.log('wrote /root/status-top.png and /root/status-full.png');
  await b.close();
})();
