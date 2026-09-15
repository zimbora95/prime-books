/* Capture what the READER actually shows under Sections, for every title whose
 * input is not a spreadsheet - and write it to public/reader-sections.json.
 *
 * WHY THE READER, AND NOT A REIMPLEMENTATION: /syllabus says "the same list you
 * see under Sections in the reader". A pymupdf reimplementation of the reader's
 * buildSections() was tried first and it DISAGREED on real titles (Y2 Maths: the
 * page listed 3 units the reader does not show at all; Y8 English: the reader
 * shows 2 units, the parse found 1; Y9 Humanities: the parse invented bare
 * numbers as unit names where the reader shows nothing). A page that contradicts
 * the reader is exactly the defect this file exists to kill, so the reader is
 * driven for real and its rows are stored.
 *
 * The rows are the panel's own buttons: label, the reader's page number (or no
 * page), and whether the row is a unit or a subunit. The panel's source line is
 * kept too ("contents page" / "unit openings" / "scheme of work"), because the
 * page has to say where the list came from.
 *
 * Slow (the reader renders a flipbook: ~30 s a book, minutes for a 700-page
 * one), but incremental - every book is appended to the output as it finishes,
 * so an interrupted run loses nothing and `--again` resumes over the captured
 * slugs only.
 *
 *   node tools/capture_reader_sections.cjs                  # local :8645
 *   PB_BASE=https://prime-books-pi.vercel.app node tools/capture_reader_sections.cjs
 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("/tmp/node_modules/playwright-core");

const REPO = path.resolve(__dirname, "..");
const OUT = path.join(REPO, "public", "reader-sections.json");
const BASE = process.env.PB_BASE || "http://127.0.0.1:8645";
const CHROME =
  process.env.PB_CHROME ||
  "/root/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome";
const INPUTS = path.join(REPO, "public", "inputs");

function tableSlugs() {
  const out = new Set();
  for (const name of fs.readdirSync(INPUTS)) {
    const m = /^([a-z0-9-]+) - input\.([a-z0-9]+)$/i.exec(name);
    if (m && m[2].toLowerCase() !== "pdf") out.add(m[1]);
  }
  return out;
}

function load() {
  try {
    return JSON.parse(fs.readFileSync(OUT, "utf8"));
  } catch (e) {
    return { note: "Reader Sections panel, captured row by row.", books: {} };
  }
}

function save(state) {
  state.generated = new Date().toISOString().replace(/\.\d+Z$/, "Z");
  fs.writeFileSync(OUT + ".tmp", JSON.stringify(state, null, 1) + "\n");
  fs.renameSync(OUT + ".tmp", OUT);
}

(async () => {
  const again = process.argv.includes("--again");
  const only = process.argv.slice(2).filter((a) => a.startsWith("y"));
  const lib = JSON.parse(fs.readFileSync(path.join(REPO, "public", "library.json"), "utf8"));
  const haveTable = tableSlugs();
  const state = load();
  const todo = lib
    .map((b) => b.slug)
    .filter((s) => (only.length ? only.includes(s) : !haveTable.has(s)))
    .filter((s) => again || !state.books[s]);

  const browser = await chromium.launch({ executablePath: CHROME, args: ["--no-sandbox"] });
  let n = 0;
  for (const slug of todo) {
    const t0 = Date.now();
    /* A small viewport: the reader renders a flipbook and the canvas is what
       costs the time; the sections list does not care how big the book is drawn. */
    const page = await browser.newPage({
      viewport: { width: 900, height: 700 },
      deviceScaleFactor: 0.3,
    });
    let rows = [], src = "";
    try {
      /* pb:book-open fires TWICE: once when the book opens (the Sections panel
         still holds its "no sections" placeholder), then again right after
         loadSections() has rendered the real list. Reading on the first event
         captures the placeholder - which is how a first run of this script
         recorded nine English stops as "none". So wait for the second. */
      await page.addInitScript(() => {
        window.__pbOpens = 0;
        window.addEventListener("pb:book-open", () => { window.__pbOpens++; });
      });
      await page.goto(BASE + "/book/" + slug + "#sections", { waitUntil: "domcontentloaded" });
      const deadline = Date.now() + 240000;
      for (;;) {
        const st = await page.evaluate(() => ({
          rows: document.querySelectorAll("#fbTocList .toc-it").length,
          opens: window.__pbOpens || 0,
        })).catch(() => ({ rows: 0, opens: 0 }));
        if (st.rows > 0) break;
        if (st.opens >= 2) break;
        if (Date.now() > deadline) break;
        await page.waitForTimeout(2000);
      }
      const got = await page.evaluate(() => {
        const list = document.getElementById("fbTocList");
        return {
          src: (document.getElementById("fbTocSrc") || {}).textContent || "",
          rows: Array.from(list.querySelectorAll(".toc-it")).map((b) => ({
            label: b.querySelector(".toc-name").textContent.trim(),
            unit: b.classList.contains("unit"),
            page: b.classList.contains("flat")
              ? null
              : parseInt(((b.querySelector("i") || {}).textContent || "").replace(/\D/g, ""), 10) || null,
          })),
          empty: /No sections found/.test(list.textContent),
        };
      });
      src = got.src;
      rows = got.rows;
      if (got.empty) src = "none";
    } catch (e) {
      src = "error: " + String(e.message).slice(0, 80);
    }
    state.books[slug] = { src: src, rows: rows };
    n++;
    save(state);
    console.log(
      "  " + slug.padEnd(34) + String(rows.length).padStart(4) + " rows  " +
      ((Date.now() - t0) / 1000).toFixed(0) + "s  " + JSON.stringify(src).slice(0, 60),
    );
    await page.close();
  }
  await browser.close();
  const withRows = Object.values(state.books).filter((b) => b.rows.length).length;
  console.log(`captured ${n} this run; ${Object.keys(state.books).length} in ${OUT}, ${withRows} with rows`);
})().catch((e) => {
  console.error("harness error:", e);
  process.exit(2);
});
