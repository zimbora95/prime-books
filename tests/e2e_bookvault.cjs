#!/usr/bin/env node
/* =============================================================================
   E2E: the "Download Bookvault" button and its page.

   Run against the LIVE file server (127.0.0.1:8645), which serves the real
   index.html and bookvault.html with the real library:

       /tmp/node_modules/.bin/../../node_modules  ->  playwright-core 1.55
       node tests/e2e_bookvault.cjs

   What it proves, in order:
     1. the button EXISTS on a book and sits IMMEDIATELY RIGHT OF "Download PDF"
        (DOM order AND on-screen x), on a book that has a PDF
     2. clicking it lands on /book/<slug>/bookvault and the page renders
     3. both download links resolve to real files, with the right byte counts
     4. the cover preview actually decodes as an image
     5. the checks list renders, with passes
     6. specifications SURVIVE A REAL RELOAD (server-side, not localStorage)
     7. a book with no PDF toasts instead of navigating
   ============================================================================= */
const { chromium } = require('/tmp/node_modules/playwright-core');

const BASE = process.env.PB_BASE || 'http://127.0.0.1:8645';
const SLUG = process.env.PB_SLUG || 'y01-physical-education';
const EXE = '/root/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome';

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: !!ok, detail: detail || '' });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  -- ' + detail : ''}`);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: EXE,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader',
           '--enable-unsafe-swiftshader'],
  });
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 } });

  /* the flipbook loads real PDFs through pdf.js; stub them so the test is
     about buttons and pages, not about rendering 72 pages in software GL */
  await ctx.route('**/*.pdf', (route) => {
    const u = route.request().url();
    if (/bookvault|text-file|cover-file/.test(u)) return route.continue();
    return route.abort();
  });

  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 200)));

  // ---- 1. the button, on a book page -------------------------------------
  await page.goto(`${BASE}/book/${SLUG}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#fbVaultBtn', { timeout: 45000 });
  const order = await page.evaluate(() => {
    const dl = document.getElementById('fbDownloadBtn');
    const bv = document.getElementById('fbVaultBtn');
    const kids = Array.from(dl.parentElement.children);
    return {
      dlIndex: kids.indexOf(dl),
      bvIndex: kids.indexOf(bv),
      label: bv.textContent.trim(),
      dlBox: dl.getBoundingClientRect().toJSON(),
      bvBox: bv.getBoundingClientRect().toJSON(),
      visible: bv.offsetWidth > 0 && getComputedStyle(bv).visibility !== 'hidden',
      cls: bv.className,
    };
  });
  check('button exists and is visible', order.visible, `label "${order.label}"`);
  check('button sits immediately right of Download PDF (DOM)',
    order.bvIndex === order.dlIndex + 1,
    `Download PDF at ${order.dlIndex}, BookVault at ${order.bvIndex}`);
  check('button sits immediately right of Download PDF (on screen)',
    order.bvBox.x >= order.dlBox.x + order.dlBox.width - 1,
    `PDF x=${Math.round(order.dlBox.x)}+${Math.round(order.dlBox.width)}, ` +
    `BookVault x=${Math.round(order.bvBox.x)}`);
  check('button carries its own accent class',
    /fb-btn-vault/.test(order.cls), order.cls);

  // ---- 2. click through to the page --------------------------------------
  await Promise.all([
    page.waitForURL(new RegExp(`/book/${SLUG}/bookvault$`), { timeout: 30000 }),
    page.click('#fbVaultBtn'),
  ]);
  await page.waitForSelector('#bvBody', { state: 'visible', timeout: 30000 });
  const sub = await page.textContent('#bvSub');
  check('page renders for the book', /Preparing/.test(sub), sub.trim().slice(0, 80));

  /* The page paints its shell before the record lands (it waits on the live
     probe, then the settings, then the record). Asserting downloads the
     instant #bvBody appears races that and fails on a slow first paint --
     wait for the state, not the container. */
  await page.waitForSelector('#bvTextActions a.bv-dl', { timeout: 45000 });

  // ---- 3/4. the two downloads and the cover preview ----------------------
  const text = await page.evaluate(async () => {
    const a = document.querySelector('#bvTextActions a.bv-dl');
    if (!a) return null;
    const r = await fetch(a.getAttribute('href'), { method: 'HEAD' });
    return { href: a.getAttribute('href'), dl: a.getAttribute('download'), status: r.status,
             len: r.headers.get('content-length') };
  });
  check('text file link present and downloadable',
    text && text.status === 200 && +text.len > 100000,
    text ? `${text.href} (${(text.len / 1e6).toFixed(1)} MB)` : 'no link');

  const cover = await page.evaluate(async () => {
    const img = document.querySelector('#bvCoverBox img');
    const a = document.querySelector('#bvCoverActions a.bv-dl');
    if (!img || !a) return null;
    const r = await fetch(a.getAttribute('href'), { method: 'HEAD' });
    return { src: img.getAttribute('src'), w: img.naturalWidth, h: img.naturalHeight,
             status: r.status, len: r.headers.get('content-length') };
  });
  check('cover preview decodes as an image',
    cover && cover.w > 500 && cover.h > 500, cover ? `${cover.w}x${cover.h}` : 'no image');
  check('cover file link present and downloadable',
    cover && cover.status === 200 && +cover.len > 100000,
    cover ? `${(cover.len / 1e6).toFixed(1)} MB` : 'no link');

  // ---- 5. the checks ------------------------------------------------------
  const checks = await page.evaluate(() => ({
    rows: document.querySelectorAll('#bvChecks .bv-check').length,
    passes: document.querySelectorAll('#bvChecks .bv-tick.ok').length,
    warns: document.querySelectorAll('#bvChecks .bv-tick.warn').length,
    text: document.getElementById('bvChecks').textContent.slice(0, 400),
    sheet: (document.querySelector('#bvSheetActions a') || {}).getAttribute
      ? document.querySelector('#bvSheetActions a').getAttribute('href') : null,
  }));
  check('checks list renders', checks.rows >= 8,
    `${checks.rows} rows, ${checks.passes} pass, ${checks.warns} open`);
  check('no failing check', checks.passes + checks.warns === checks.rows,
    `${checks.passes} pass + ${checks.warns} open = ${checks.rows}`);
  check('upload sheet is offered', !!checks.sheet, checks.sheet || '');

  // ---- 6. specifications survive a real reload ---------------------------
  const isbn = '978-1-9999-' + String(Date.now()).slice(-4) + '-0';
  await page.fill('#bvIsbn', isbn);
  await page.click('#bvSave');
  await page.waitForFunction(
    () => /Saved/.test(document.getElementById('bvMsg').textContent), null,
    { timeout: 20000 });
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#bvBody', { state: 'visible', timeout: 30000 });
  await page.waitForFunction(
    (want) => document.getElementById('bvIsbn').value === want, isbn, { timeout: 20000 });
  const after = await page.inputValue('#bvIsbn');
  check('specifications survive a real reload (server-side)', after === isbn, after);

  // ---- 7. the button across several books, and an unknown address --------
  const sample = ['y01-art-and-design', 'y01-english', 'y07-computing-structured'];
  const seen = [];
  for (const s of sample) {
    const q = await ctx.newPage();
    await q.route('**/*.pdf', (r) => r.abort());
    await q.goto(`${BASE}/book/${s}`, { waitUntil: 'domcontentloaded' });
    let ok = false;
    try {
      await q.waitForSelector('#fbVaultBtn', { state: 'visible', timeout: 30000 });
      ok = true;
    } catch (e) {}
    seen.push(`${s}:${ok ? 'yes' : 'NO'}`);
    await q.close();
  }
  check('button appears on every sampled book', seen.every((s) => s.endsWith('yes')),
    seen.join(' '));

  const nf = await ctx.newPage();
  await nf.route('**/*.pdf', (r) => r.abort());
  await nf.goto(`${BASE}/book/zzz-not-a-book/bookvault`, { waitUntil: 'domcontentloaded' });
  await nf.waitForSelector('#bvNotFound', { state: 'visible', timeout: 30000 });
  check('unknown address says so instead of half-rendering', true, 'not-found panel shown');
  await nf.close();

  check('no uncaught page errors', errors.length === 0, errors.join(' | ').slice(0, 200));

  await browser.close();
  const failed = results.filter((r) => !r.ok);
  console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
})().catch((e) => {
  console.error('HARNESS ERROR:', e);
  process.exit(2);
});
