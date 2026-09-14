#!/usr/bin/env node
/* =============================================================================
   E2E: the /status point-of-situation page.

   Run against the LIVE file server (127.0.0.1:8645):

       node tests/e2e_status.cjs

   What it proves, in order:
     1. /status serves the status document (not the catalogue)
     2. status.json loads and the summary tiles carry the real totals
     3. every year is rendered, and every title appears exactly once
     4. a title links to its own /book/<slug> page
     5. the "Missing input" filter shows ONLY titles with no input file
     6. the "Has input" filter shows ONLY titles that have one
     7. the search box filters across the whole list
     8. Standardised reads as none (the flag store is deliberately empty)
   ============================================================================= */
const { chromium } = require('/tmp/node_modules/playwright-core');

const BASE = process.env.PB_BASE || 'http://127.0.0.1:8645';
const EXE = '/root/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome';

let pass = 0, fail = 0;
function ok(label, cond, extra) {
  if (cond) { pass++; console.log(`  PASS  ${label}`); }
  else { fail++; console.log(`  FAIL  ${label}${extra ? "  <- " + extra : ""}`); }
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  const errors = [];
  const bad404 = [];
  // /favicon.ico 404s on every page of this site (no favicon is shipped): a
  // browser convenience request, not a defect this page can introduce.
  const ignorable = (t) => /favicon\.ico/.test(t);
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('response', (r) => {
    if (r.status() === 404 && !ignorable(r.url())) bad404.push(r.url());
  });

  console.log(`\n== /status E2E == ${BASE}/status\n`);
  const resp = await page.goto(BASE + '/status', { waitUntil: 'domcontentloaded' });
  ok('/status answers 200', resp.status() === 200, 'got ' + resp.status());
  ok('serves the status document', /Point of Situation/.test(await page.title()),
     await page.title());

  await page.waitForSelector('#years table tbody tr', { timeout: 15000 });
  await page.waitForFunction(() => document.getElementById('t-books').textContent !== '–',
                             null, { timeout: 15000 });

  const totals = await page.evaluate(() => ({
    books: +document.getElementById('t-books').textContent,
    pages: document.getElementById('t-pages').textContent,
    withInput: +document.getElementById('t-with').textContent,
    noInput: +document.getElementById('t-without').textContent,
    std: +document.getElementById('t-std').textContent,
    stdHint: document.getElementById('t-std-hint').textContent,
    gen: document.getElementById('gen').textContent,
    years: document.querySelectorAll('.yearblock').length,
    rows: document.querySelectorAll('#years tbody tr').length,
  }));
  console.log('  totals:', JSON.stringify(totals));

  ok('tiles loaded real totals', totals.books > 100 && totals.gen !== '–');
  ok('withInput + noInput === books', totals.withInput + totals.noInput === totals.books,
     `${totals.withInput}+${totals.noInput} vs ${totals.books}`);
  ok('a title with no input is not counted as standardised',
     totals.std === 0 && /none yet/.test(totals.stdHint));
  ok('all years rendered', totals.years >= 13, 'years=' + totals.years);
  ok('every title listed exactly once', totals.rows === totals.books,
     `${totals.rows} rows vs ${totals.books} books`);

  const firstLink = await page.getAttribute('#years tbody tr td.subject a', 'href');
  ok('a title links to its own book page', /^\/book\/[a-z0-9-]+$/.test(firstLink || ''),
     String(firstLink));

  /* --- filters ------------------------------------------------------------ */
  const kindOf = () => page.$$eval('#years tbody tr', (rows) =>
    rows.map((r) => r.querySelector('td.input .kind').textContent.trim()));

  await page.click('.chip[data-f="missing"]');
  let kinds = await kindOf();
  let shown = await page.textContent('#shown');
  ok('"Missing input" shows only titles without an input',
     kinds.length > 0 && kinds.every((k) => k === '—'),
     kinds.filter((k) => k !== '—').slice(0, 3).join(', '));
  ok('"Missing input" count matches the tile',
     shown === `${totals.noInput} of ${totals.books} titles shown`, shown);

  await page.click('.chip[data-f="input"]');
  kinds = await kindOf();
  shown = await page.textContent('#shown');
  ok('"Has input" shows only titles WITH an input',
     kinds.length > 0 && kinds.every((k) => /✓/.test(k)),
     kinds.filter((k) => !/✓/.test(k)).slice(0, 3).join(', '));
  ok('"Has input" count matches the tile',
     shown === `${totals.withInput} of ${totals.books} titles shown`, shown);

  await page.click('.chip[data-f="std"]');
  ok('"Standardised" is empty, as the flag store is',
     (await page.textContent('#shown')) === `0 of ${totals.books} titles shown`,
     await page.textContent('#shown'));

  await page.click('.chip[data-f="all"]');
  await page.fill('#q', 'computing');
  await page.waitForTimeout(120);
  const hits = await page.$$eval('#years tbody tr', (rows) =>
    rows.length && rows.every((r) => /computing/i.test(r.textContent)));
  ok('search filters the whole list', hits);
  const searchCount = await page.textContent('#shown');
  ok('search count is smaller than the catalogue',
     parseInt(searchCount, 10) < totals.books, searchCount);

  await page.fill('#q', 'zzzznotasubject');
  await page.waitForTimeout(120);
  ok('a search with no hits says so',
     /Nothing matches/.test(await page.textContent('#years')));

  /* --- the sign-off: server-side and permanent, or honestly refused -------- */
  const IS_LOCAL = /127\.0\.0\.1|localhost/.test(BASE);
  await page.fill('#q', '');          /* the previous case left a no-hits query */
  await page.click('.chip[data-f="all"]');
  await page.waitForSelector('#years tbody tr button.stamp', { timeout: 10000 });
  const slug = await page.getAttribute('#years tbody tr button.stamp', 'data-slug');
  ok('every row carries a sign-off button', /^[a-z0-9-]+$/.test(slug || ''), String(slug));

  await page.click('#years tbody tr button.stamp');
  if (IS_LOCAL) {
    await page.waitForFunction(
      (s) => {
        const b = document.querySelector('button.stamp[data-slug="' + s + '"]');
        return b && b.dataset.on === '1';
      }, slug, { timeout: 10000 });
    ok('clicking signs a title off', true);
    ok('the Standardised tile counts it',
       (await page.textContent('#t-std')) === '1', await page.textContent('#t-std'));
    ok('the year roll-up counts it',
       /standardised 1\//.test(await page.textContent('.yearhead .bar')),
       await page.textContent('.yearhead .bar'));

    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#years tbody tr button.stamp', { timeout: 15000 });
    await page.waitForFunction(() => document.getElementById('t-books').textContent !== '–',
                               null, { timeout: 15000 });
    ok('the sign-off survives a real reload (not localStorage)',
       (await page.getAttribute(`button.stamp[data-slug="${slug}"]`, 'data-on')) === '1');

    const store = await (await fetch(BASE + '/standardized.json?cb=' + Date.now())).json();
    ok('the flag store on disk agrees', store[slug] === true, JSON.stringify(store));

    /* leave the store exactly as we found it */
    await page.click(`button.stamp[data-slug="${slug}"]`);
    await page.waitForFunction(
      (s) => {
        const b = document.querySelector('button.stamp[data-slug="' + s + '"]');
        return b && b.dataset.on === '0';
      }, slug, { timeout: 10000 });
    const after = await (await fetch(BASE + '/standardized.json?cb=' + Date.now())).json();
    ok('undoing removes it (store left empty)', Object.keys(after).length === 0,
       JSON.stringify(after));
    ok('the tile goes back to none yet',
       (await page.textContent('#t-std')) === '0' &&
       /none yet/.test(await page.textContent('#t-std-hint')));
  } else {
    await page.waitForTimeout(600);
    ok('on the static deploy, a click says so instead of pretending to save',
       /read-only|Could not save/.test(await page.textContent('#toast')),
       await page.textContent('#toast'));
    const store = await (await fetch(BASE + '/standardized.json?cb=' + Date.now())).json();
    ok('the deployed build cannot write the flag store',
       Object.keys(store).length === 0, JSON.stringify(store));
  }

  ok('no page errors', errors.length === 0, errors.slice(0, 2).join(' | '));
  ok('nothing on the page 404s', bad404.length === 0, bad404.slice(0, 3).join(' | '));

  await browser.close();
  console.log(`\n${pass} passed, ${fail} failed\n`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error('HARNESS ERROR', e); process.exit(2); });
