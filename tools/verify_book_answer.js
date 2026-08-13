/* Ask the reading assistant a real question about a real page in a specific
 * book, driving the actual UI. Proves the synced masters have a text layer the
 * AI can read.
 *   node tools/verify_book_answer.js "Mathematics" 3 [page]
 */
const BASE = "http://127.0.0.1:5173";
const SUBJ = process.argv[2] || "Mathematics";
const YEAR = parseInt(process.argv[3] || "3", 10);
const WANT = parseInt(process.argv[4] || "0", 10);

(async () => {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on("pageerror", (e) => errs.push(e.message));
  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForTimeout(2000);

  const book = await page.evaluate(
    async ([s, y]) => {
      const rows = await fetch("/books-manifest.json").then((r) => r.json());
      return rows.find((r) => r.year === y && r.subject.includes(s));
    },
    [SUBJ, YEAR],
  );
  if (!book) {
    console.log("no manifest entry for", SUBJ, YEAR);
    await browser.close();
    return;
  }
  console.log(`BOOK: Year ${book.year} ${book.subject} — ${book.pages}pp`);
  await page.evaluate(
    (t) =>
      window.PBReading.openBook(
        { title: t.subject, band: "Year " + t.year, yearNum: t.year },
        t.pdf,
      ),
    book,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });

  /* page 1 first: this is the page that reported "no text" before the resync */
  const p1 = await page.evaluate(() => window.PBReading.pageText(1));
  console.log(`page 1 text: ${p1.length} chars ${p1.length ? "(readable)" : "(NO TEXT LAYER)"}`);
  if (p1.length) console.log("   " + p1.slice(0, 140).replace(/\s+/g, " "));

  const target =
    WANT ||
    (await page.evaluate(async () => {
      const R = window.PBReading;
      for (let p = 4; p < Math.min(60, 200); p++) {
        const t = await R.pageText(p);
        if (t && t.length > 500) return p;
      }
      return 1;
    }));
  await page.evaluate((p) => window.PBReading.goToPage(p), target);
  await page.waitForTimeout(2500);
  console.log("panel: " + (await page.textContent(".pbc-where")));

  await page.fill(".pbc-input", "What is on this page? Answer in two sentences, only from the page.");
  await page.click(".pbc-send");
  await page.waitForFunction(
    () => {
      const b = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      const last = b[b.length - 1];
      return last && last.textContent.trim().length > 40 &&
        !document.querySelector(".pbc-status.on");
    },
    { timeout: 240000 },
  );
  const ans = await page.evaluate(() => {
    const b = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
    return b[b.length - 1].textContent.trim();
  });
  console.log("\nANSWER: " + ans.slice(0, 420));
  const src = await page.evaluate((p) => window.PBReading.pageText(p), target);
  console.log("\n(source page " + target + ", " + src.length + " chars): " +
    src.slice(0, 200).replace(/\s+/g, " "));
  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  await browser.close();
})();
