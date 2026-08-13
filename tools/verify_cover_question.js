/* Reproduce the user's exact complaint: open a book, sit on page 1 (wordless
 * cover) and ask "what is this book about?" then "Test me on this".
 *   node tools/verify_cover_question.js "Humanities" 7
 */
const BASE = "http://127.0.0.1:5173";
const SUBJ = process.argv[2] || "Humanities";
const YEAR = parseInt(process.argv[3] || "7", 10);

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
  await page.waitForTimeout(2500);

  const p1 = await page.evaluate(() => window.PBReading.pageText(1));
  const dig = await page.evaluate(() => window.PBReading.digest(3));
  console.log(`page 1: ${p1.length} chars (wordless cover)`);
  console.log("digest gives the model pages: " + dig.map((d) => d.page).join(", ") +
    " (" + dig.map((d) => d.text.length + "ch").join(", ") + ")");
  console.log("panel: " + (await page.textContent(".pbc-where")));

  async function ask(q) {
    const before = await page.evaluate(
      () => document.querySelectorAll("#pbChat .pbc-assistant .pbc-body").length,
    );
    await page.fill(".pbc-input", q);
    await page.click(".pbc-send");
    await page.waitForFunction(
      (n) => {
        const b = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
        return b.length > n && b[b.length - 1].textContent.trim().length > 60 &&
          !document.querySelector(".pbc-status.on");
      },
      before,
      { timeout: 240000 },
    );
    await page.waitForTimeout(1200);
    return page.evaluate(() => {
      const b = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      return b[b.length - 1].textContent.trim();
    });
  }

  console.log("\n--- Q: what is this book about? ---");
  console.log(await ask("what is this book about?"));
  console.log("\n--- Q: Test me on this ---");
  console.log(await ask("Test me on this"));
  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  await browser.close();
})();
