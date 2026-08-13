/* End-to-end as a pupil: type into the real input, read the real bubble, then
 * turn the page and ask a follow-up in the SAME session.
 * Usage: node tools/verify_pupil_flow.js [baseUrl] */
const BASE = process.argv[2] || "http://127.0.0.1:5173";

(async () => {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on("pageerror", (e) => errs.push(e.message));
  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForTimeout(2000);

  /* a mid-sized real book */
  const book = await page.evaluate(async () => {
    const rows = await fetch("/books-manifest.json").then((r) => r.json());
    return rows.find((r) => r.pages > 80 && r.pages < 220) || rows[0];
  });
  console.log("book: Year " + book.year + " " + book.subject + " (" + book.pages + "pp)");
  await page.evaluate(
    (t) => window.PBReading.openBook({ title: t.subject, band: "Year " + t.year }, t.pdf),
    book,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });

  /* land on a text-bearing page */
  const landed = await page.evaluate(async () => {
    const R = window.PBReading;
    for (const p of [14, 18, 22, 26, 30, 34, 40]) {
      const t = await R.pageText(p);
      if (t && t.length > 400) {
        R.goToPage(p);
        return { page: p, len: t.length };
      }
    }
    return null;
  });
  console.log("landed on page " + landed.page + " (" + landed.len + " chars)");
  await page.waitForTimeout(2500);
  console.log("panel says: " + (await page.textContent(".pbc-where")));

  async function ask(q) {
    await page.fill(".pbc-input", q);
    await page.click(".pbc-send");
    await page.waitForFunction(
      () => {
        const b = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
        const last = b[b.length - 1];
        return last && last.textContent.trim().length > 30 &&
          !document.querySelector(".pbc-status.on");
      },
      { timeout: 240000 },
    );
    return page.evaluate(() => {
      const b = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      return b[b.length - 1].textContent.trim();
    });
  }

  console.log("\n--- Q1 (typed into the real box) ---");
  const a1 = await ask("What is this page about? Two sentences.");
  console.log("A1: " + a1.slice(0, 400));

  console.log("\n--- turn the page, then a follow-up in the SAME session ---");
  await page.evaluate((p) => window.PBReading.goToPage(p + 4), landed.page);
  await page.waitForTimeout(2500);
  console.log("panel says: " + (await page.textContent(".pbc-where")));
  const a2 = await ask("What page am I on now, and did we speak about a different page before?");
  console.log("A2: " + a2.slice(0, 500));

  const sessions = await page.evaluate(() =>
    JSON.parse(sessionStorage.getItem("pb.tutor.sessions.v1") || "{}"),
  );
  const keys = Object.keys(sessions);
  console.log("\nsessions held: " + keys.length + " -> " + JSON.stringify(Object.values(sessions)));
  console.log(keys.length === 1 ? "ok   one session for one book" : "FAIL expected exactly 1");
  console.log(errs.length ? "JS errors: " + errs.join(" | ") : "no JS errors");
  await browser.close();
})();
