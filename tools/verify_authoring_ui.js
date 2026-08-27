/* Drive the real UI end to end: a factual question that needs no tools, then an
 * authoring question that must use them. Prints the status chips as they change,
 * so a long tool-running turn is visibly alive.
 *   node tools/verify_authoring_ui.js
 */
const BASE = "http://127.0.0.1:5173";

(async () => {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on("pageerror", (e) => errs.push(e.message));
  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForTimeout(2500);

  const bk = await page.evaluate(async () => {
    const r = await fetch("/books-manifest.json").then((x) => x.json());
    return r.find((x) => x.year === 7 && x.subject.includes("Humanities"));
  });
  console.log("manifest carries markdown path:", !!bk.markdown, "| buildable:", bk.buildable);
  await page.evaluate(
    (t) => window.PBReading.openBook({ title: t.subject, band: "Year " + t.year }, t.pdf),
    bk,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });
  await page.waitForTimeout(2000);
  const meta = await page.evaluate(() => window.PBReading.meta);
  console.log("meta.markdownDir:", meta.markdownDir || "(EMPTY)");
  console.log("meta.buildable:", meta.buildable,
    "| pageCount:", await page.evaluate(() => window.PBReading.pageCount));

  async function ask(q, label) {
    const n = await page.evaluate(
      () => document.querySelectorAll("#pbChat .pbc-assistant .pbc-body").length,
    );
    await page.fill(".pbc-input", q);
    await page.click(".pbc-send");
    const seen = new Set();
    const t0 = Date.now();
    for (;;) {
      if (Date.now() - t0 > 780000) { console.log("   (timed out waiting)"); break; }
      const s = await page.evaluate(() => {
        const e = document.querySelector(".pbc-status");
        return e && e.classList.contains("on") ? e.textContent : "";
      });
      if (s && !seen.has(s)) { seen.add(s); console.log("   [status] " + s); }
      const done = await page.evaluate((m) => {
        const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
        return x.length > m && x[x.length - 1].textContent.trim().length > 40 &&
          !document.querySelector(".pbc-status.on");
      }, n);
      if (done) break;
      await page.waitForTimeout(1500);
    }
    const a = await page.evaluate(() => {
      const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      return x[x.length - 1].textContent.trim();
    });
    console.log(label + ": " + a.slice(0, 420));
    return a;
  }

  console.log("\n--- Q1 (needs no tools): how many pages this pdf has? ---");
  const a1 = await ask("how many pages this pdf has?", "A1");
  console.log(/194/.test(a1) ? "   ok   says 194" : "   FAIL does not say 194");

  console.log("\n--- Q2 (must use tools): read the scheme map ---");
  const a2 = await ask(
    "Using your tools, read this book's 06-SCHEME-MAP.md and tell me the name of Unit 3.",
    "A2",
  );
  console.log(/unit 3/i.test(a2) ? "   ok   answered about Unit 3" : "   check the answer above");

  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  await browser.close();
})();
