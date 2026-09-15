/* E2E for /syllabus — the mega overview page.
 *
 * What it proves, against whatever PB_BASE serves:
 *   1. the route serves the syllabus document (not index.html, not a 404);
 *   2. every title in syllabus.json is on the page, grouped by year, with the
 *      unit and subunit counts the JSON claims — nothing dropped in render;
 *   3. units and subunits are VISIBLE without a click (the whole point): the
 *      first book's subunit text is in the DOM and has a non-zero box;
 *   4. the search box and the chips filter honestly, and clearing restores;
 *   5. no console error / no failed request beyond /favicon.ico, which 404s on
 *      every page of this site.
 *
 *   node tests/e2e_syllabus.cjs                                   # :8645
 *   PB_BASE=https://prime-books-pi.vercel.app node tests/e2e_syllabus.cjs
 */
const path = require("path");
const { chromium } = require("/tmp/node_modules/playwright-core");

const BASE = process.env.PB_BASE || "http://127.0.0.1:8645";
const CHROME =
  process.env.PB_CHROME ||
  "/root/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome";
const SHOT = process.env.PB_SHOT || "/root/prime-books/tests/syllabus.png";

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log("  ok   " + name); }
  else { fail++; console.log("  FAIL " + name + (extra ? "  -> " + extra : "")); }
}

(async () => {
  const data = await fetch(BASE + "/syllabus.json").then((r) => r.json());
  console.log("syllabus.json:", JSON.stringify(data.totals));

  const browser = await chromium.launch({ executablePath: CHROME, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  const errors = [], badRequests = [];
  /* /favicon.ico 404s on EVERY page of this site (no favicon is shipped), and
     the console text does not carry the URL — so filter it by location. */
  page.on("console", (m) => {
    if (m.type() !== "error") return;
    const url = (m.location() && m.location().url) || "";
    const text = m.text();
    if (/favicon/.test(url) || /favicon/i.test(text)) return;
    errors.push(text + (url ? " @ " + url : ""));
  });
  page.on("requestfailed", (r) => badRequests.push(r.url() + " " + r.failure().errorText));
  page.on("response", (r) => {
    if (r.status() >= 400 && !/favicon\.ico/.test(r.url()))
      badRequests.push(r.status() + " " + r.url());
  });

  const res = await page.goto(BASE + "/syllabus", { waitUntil: "domcontentloaded" });
  ok("route serves the syllabus document", res.status() === 200, "HTTP " + res.status());
  ok("document is syllabus.html",
    /Prime School Books — Syllabus/.test(await page.title()), await page.title());

  await page.waitForSelector(".subj", { timeout: 20000 });

  /* 2. counts */
  const dom = await page.evaluate(() => {
    const books = Array.from(document.querySelectorAll(".subj"));
    const years = Array.from(document.querySelectorAll(".yearblock"));
    return {
      books: books.length,
      years: years.length,
      yearIds: years.map((y) => y.id),
      subjects: books.map((b) => b.querySelector("a.subject").textContent.trim()),
      units: document.querySelectorAll(".unit").length,
      subs: document.querySelectorAll("ul.subs li").length,
      shown: document.getElementById("shown").textContent,
      tiles: ["t-books", "t-units", "t-subs", "t-table", "t-pdf", "t-none"]
        .map((id) => document.getElementById(id).textContent),
      jump: document.querySelectorAll("#jump a").length,
    };
  });
  ok("every title is on the page", dom.books === data.totals.books,
    dom.books + " vs " + data.totals.books + " in the json");
  ok("every year is on the page", dom.years === data.totals.years,
    dom.years + " vs " + data.totals.years);
  ok("unit count matches the json", dom.units === data.totals.units,
    dom.units + " vs " + data.totals.units);
  ok("subunit count matches the json", dom.subs === data.totals.subunits,
    dom.subs + " vs " + data.totals.subunits);
  ok("jump list covers every year", dom.jump === data.totals.years);
  ok("tiles read the json totals",
    dom.tiles[0] === String(data.totals.books) &&
    dom.tiles[1] === data.totals.units.toLocaleString() &&
    dom.tiles[2] === data.totals.subunits.toLocaleString(),
    dom.tiles.join(" / "));
  ok("shown counter covers the whole page",
    dom.shown === data.totals.books + " of " + data.totals.books + " titles · " +
      data.totals.units + " units shown", dom.shown);

  /* the first book that has an input table: its subunits must be on the page,
     expanded, with a real box — no click, no accordion. */
  const first = data.years[0].books.find((b) => b.source === "input" && b.units.length);
  const vis = await page.evaluate((slug) => {
    const card = document.getElementById(slug);
    if (!card) return null;
    const sub = card.querySelector("ul.subs li");
    const unit = card.querySelector(".unit .u");
    const box = sub && sub.getBoundingClientRect();
    const ubox = unit && unit.getBoundingClientRect();
    return {
      subText: sub ? sub.textContent.trim() : null,
      subVisible: !!(box && box.width > 0 && box.height > 0 &&
        getComputedStyle(sub).visibility !== "hidden"),
      unitText: unit ? unit.textContent.trim() : null,
      unitVisible: !!(ubox && ubox.height > 0),
      subs: card.querySelectorAll("ul.subs li").length,
    };
  }, first.slug);
  ok("first input title has its subunits in the DOM",
    vis && vis.subs === first.units.reduce((n, u) => n + u.subs.length, 0),
    JSON.stringify(vis));
  ok("subunits are visible without any click", vis && vis.subVisible, JSON.stringify(vis));
  ok("unit headings are visible", vis && vis.unitVisible, JSON.stringify(vis));
  ok("a subunit carries the input's own wording",
    vis && first.units.some((u) => u.subs.some((s) => vis.subText.startsWith(s.title))),
    vis && vis.subText);

  /* honest gaps: a PDF-only title and a title with no input say so */
  const pdfBook = data.years.flatMap((y) => y.books).find((b) => b.source === "pdf");
  const noBook = data.years.flatMap((y) => y.books).find((b) => b.source === "none");
  const pdfText = await page.evaluate((s) => document.getElementById(s).textContent, pdfBook.slug);
  const noText = await page.evaluate((s) => document.getElementById(s).textContent, noBook.slug);
  ok("a PDF-only title states there is no unit table",
    /No unit table on disk/.test(pdfText) && pdfText.includes(pdfBook.input.file));
  ok("a title with no input says so", /No input file/.test(noText));

  /* 4. filters */
  const before = await page.textContent("#shown");
  await page.fill("#q", "printing");
  await page.waitForTimeout(150);
  const q = await page.evaluate(() => ({
    books: document.querySelectorAll(".subj").length,
    marks: document.querySelectorAll("mark").length,
    shown: document.getElementById("shown").textContent,
  }));
  ok("search narrows the page", q.books > 0 && q.books < data.totals.books,
    JSON.stringify(q));
  ok("search highlights what it matched", q.marks > 0);
  await page.fill("#q", "");
  await page.waitForTimeout(150);
  ok("clearing the search restores the page",
    (await page.textContent("#shown")) === before);

  await page.click('.chip[data-f="pdf"]');
  await page.waitForTimeout(150);
  const pdfOnly = await page.evaluate(() =>
    Array.from(document.querySelectorAll(".subj")).every((c) =>
      /No unit table on disk/.test(c.textContent)));
  ok("the PDF chip shows only PDF-input titles", pdfOnly);
  await page.click('.chip[data-f="none"]');
  await page.waitForTimeout(150);
  const none = await page.evaluate(() => ({
    n: document.querySelectorAll(".subj").length,
    all: Array.from(document.querySelectorAll(".subj")).every((c) =>
      /No input file|No unit table on disk/.test(c.textContent)),
  }));
  ok("the no-input chip shows only titles with no input file",
    none.n === data.totals.noInput && none.all, JSON.stringify(none));
  await page.click('.chip[data-f="all"]');
  await page.waitForTimeout(150);

  await page.screenshot({ path: SHOT });
  await page.screenshot({
    path: SHOT.replace(/\.png$/, "-mid.png"),
    fullPage: true,
    clip: { x: 0, y: 1200, width: 1400, height: 2600 },
  });

  ok("no console errors", errors.length === 0, errors.join(" | "));
  ok("no failed requests", badRequests.length === 0, badRequests.join(" | "));

  await browser.close();
  console.log("\n" + pass + " passed, " + fail + " failed · screenshots: " + SHOT);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error("harness error:", e); process.exit(2); });
