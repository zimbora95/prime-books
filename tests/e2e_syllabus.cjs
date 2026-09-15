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
      tiles: ["t-books", "t-units", "t-subs", "t-table", "t-book", "t-none"]
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

  /* THE regression this page was fixed for: a title with no input table, whose
     reader Sections list the teacher CAN see, must show that list inline here
     too — the same labels, in the same order, not a link off the page. */
  const fromBook = data.years.flatMap((y) => y.books).filter((b) => b.source === "book");
  const english = fromBook.find((b) => b.slug === "y01-english");
  ok("a PDF-input title now carries a unit list instead of a dead link",
    !!english && english.units.length === 9, english && JSON.stringify(english.units.length));
  const inline = await page.evaluate((slug) => {
    const card = document.getElementById(slug);
    const units = Array.from(card.querySelectorAll(".unit .u")).map((e) => e.textContent.trim());
    const li = card.querySelector(".unit .u").getBoundingClientRect();
    return { units, visible: li.height > 0, text: card.textContent };
  }, "y01-english");
  ok("every unit the reader lists is on the page, in order",
    english && inline.units.length === english.units.length &&
    inline.units.every((t, i) => t.startsWith(english.units[i].title)),
    JSON.stringify(inline.units.slice(0, 3)));
  ok("the book-read units are visible without any click", inline.visible);
  ok("the block names its source honestly",
    /input is a PDF document/.test(inline.text) &&
    /contents page/.test(inline.text) &&
    /Sections/.test(inline.text));
  const bookTitles = fromBook.filter((b) => b.units.length);
  ok("every from-the-book title renders its units",
    await page.evaluate((slugs) => slugs.every((s) => {
      const c = document.getElementById(s);
      return c && /No list to read/.test(c.textContent) === false;
    }), bookTitles.map((b) => b.slug)),
    bookTitles.length + " titles");

  /* THE TITLE STANDARD - the shapes the teacher asked for, on the page. */
  const cardOf = (slug) => page.evaluate((s) => {
    const c = document.getElementById(s);
    return {
      units: Array.from(c.querySelectorAll(".unit .u")).map((e) => e.textContent.trim()),
      terms: Array.from(c.querySelectorAll(".term")).map((e) => e.textContent.trim()),
      furn: Array.from(c.querySelectorAll(".furn")).map((e) => e.textContent.trim()),
      meta: c.querySelector(".meta").textContent,
      text: c.textContent,
    };
  }, slug);

  const en = await cardOf("y01-english");
  ok("'Stop N' becomes 'Unit N'", en.units[0].startsWith("Unit 1 · Going places"), en.units[0]);
  ok("a fused label is repaired to the book's own words",
    en.units.some((t) => t.startsWith("Unit 8 · How I feel")), JSON.stringify(en.units[7]));
  ok("the repaired title is not SHOUTED anywhere",
    await page.evaluate(() =>
      Array.from(document.querySelectorAll(".unit .u, ul.subs li")).every((e) => {
        const t = e.textContent.replace(/×\d+$/, "").replace(/p\.\d+$/, "").trim();
        const own = t.split("·").slice(1).join("·").trim() || t;
        return own !== own.toUpperCase() || !/[A-Z]{3}/.test(own);
      })));

  const m3 = await cardOf("y03-mathematics");
  ok("terms are dividers, not units",
    m3.terms.length === 3 && /^Term 1/.test(m3.terms[0]) && /^Term 2/.test(m3.terms[1]),
    JSON.stringify(m3.terms));
  ok("the unit numbers under a term are 1..N in the book's order",
    m3.units.length === 8 && m3.units[1].startsWith("Unit 2 · Tally charts and frequency tables") &&
    m3.units[2].startsWith("Unit 3 · Angles and movement") && !/Unit 4 · Tally/.test(m3.text),
    JSON.stringify(m3.units.slice(0, 4)));

  const pt = await cardOf("y04-portuguese");
  ok("a Portuguese fused label is repaired too",
    pt.units.some((t) => t.startsWith("Unit 7 · A gota e o jardim")),
    JSON.stringify(pt.units[6]));

  const pe13 = await cardOf("y13-physical-education");
  ok("unusable numbers are renumbered 1..N",
    pe13.units.length === 4 &&
    pe13.units.map((t) => (t.match(/^Unit (\d+)/) || [])[1]).join(",") === "1,2,3,4" &&
    !/Unit 12|Unit 14/.test(pe13.text), JSON.stringify(pe13.units));

  const pe7 = await cardOf("y07-physical-education");
  ok("a SHOUTED spreadsheet row is Title Cased on the page",
    pe7.units[0].startsWith("Unit 1 · Futsal") && pe7.units[1].startsWith("Unit 2 · Cross Country"),
    JSON.stringify(pe7.units.slice(0, 2)));

  /* ...and the spreadsheet itself was corrected, not just the page: the JSON
     the Input panel renders is generated FROM the .xlsx. */
  const xlsxJson = await fetch(BASE + "/inputs/y07-physical-education.json").then((r) => r.json());
  const titles = xlsxJson.rows.map((r) => String(r.Title || ""));
  ok("the correction is written into the input spreadsheet",
    titles.includes("Unit 1 · Futsal") && titles.includes("Unit 2 · Cross Country") &&
    !titles.some((t) => t === t.toUpperCase() && /[A-Z]{3}/.test(t)),
    JSON.stringify(titles.slice(0, 3)));

  const pt8 = await cardOf("y08-portuguese-2nd");
  ok("a contents-page row is marked, not counted as a unit",
    pt8.furn.length === 1 && /Índice/.test(pt8.furn[0]) && !/Unit 2 · Índice/.test(pt8.units.join()),
    JSON.stringify(pt8.furn));
  ok("the header count excludes non-unit rows",
    pt8.meta.includes("7 units") && pt8.meta.includes("1 other row"), pt8.meta);

  /* whole-catalogue sweep: nothing SHOUTED, nothing fused-camel, no stray " . " */
  const bad = [];
  data.years.flatMap((y) => y.books).forEach((b) => {
    (b.units || []).forEach((u) => {
      const own = (u.title.split("·")[1] || u.title).trim();
      if (/[A-Z]{3}/.test(own) && own === own.toUpperCase()) bad.push(b.slug + ": " + u.title);
      if (/[a-z][A-Z]/.test(u.title)) bad.push(b.slug + ": " + u.title);
      if (/ \./.test(u.title) || /,[^\s]/.test(u.title)) bad.push(b.slug + ": " + u.title);
    });
  });
  ok("no SHOUTED, fused or badly spaced unit label survives anywhere", bad.length === 0,
    bad.slice(0, 6).join(" | "));

  /* honest gaps: the titles where even the book yields nothing say so */
  const blank = data.years.flatMap((y) => y.books).find((b) => b.source === "pdf");
  const noBook = data.years.flatMap((y) => y.books).find((b) => b.source === "none");
  const pdfText = await page.evaluate((s) => document.getElementById(s).textContent, blank.slug);
  const noText = await page.evaluate((s) => document.getElementById(s).textContent, noBook.slug);
  ok("a title with a PDF input and no readable list says so",
    /No list to read/.test(pdfText) && pdfText.includes(blank.input.file));
  ok("a title with nothing on disk says so", /No list to read/.test(noText));

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

  await page.click('.chip[data-f="book"]');
  await page.waitForTimeout(150);
  const bookOnly = await page.evaluate(() =>
    document.querySelectorAll(".subj").length);
  ok("the from-the-book chip shows exactly those titles",
    bookOnly === data.totals.withBook, bookOnly + " vs " + data.totals.withBook);
  await page.click('.chip[data-f="none"]');
  await page.waitForTimeout(150);
  const none = await page.evaluate(() => ({
    n: document.querySelectorAll(".subj").length,
    all: Array.from(document.querySelectorAll(".subj")).every((c) =>
      /No list to read|Contents page unreadable/.test(c.textContent)),
  }));
  ok("the no-list chip shows only titles with nothing to read",
    none.n === data.totals.nothing && none.all, JSON.stringify(none));
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
