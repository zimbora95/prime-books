/* Does a book's conversation RESUME after switching books and after a reload?
 *
 * The user's requirement: first visit to book X starts a session; going to book
 * Y and back to X, or closing the tab and returning to X, resumes X's session.
 *
 *   node tools/verify_session_resume.js
 */
const BASE = "http://127.0.0.1:5173";

async function openBook(page, pick) {
  const bk = await page.evaluate(async (p) => {
    let rows = await fetch("/books-manifest.local.json")
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null);
    if (!Array.isArray(rows) || !rows.length)
      rows = await fetch("/books-manifest.json").then((r) => r.json());
    return rows.find((x) => x.year === p.year && x.subject.startsWith(p.subject));
  }, pick);
  await page.evaluate(
    (t) =>
      window.PBReading.openBook(
        { title: t.subject, band: "Year " + t.year, yearNum: t.year },
        t.pdf,
      ),
    bk,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });
  await page.waitForTimeout(2000);
  return bk;
}

async function ask(page, q) {
  const before = await page.evaluate(
    () => document.querySelectorAll("#pbChat .pbc-assistant .pbc-body").length,
  );
  await page.fill(".pbc-input", q);
  await page.click(".pbc-send");
  let stable = 0,
    last = -1;
  const t0 = Date.now();
  for (;;) {
    if (Date.now() - t0 > 420000) break;
    const st = await page.evaluate((m) => {
      const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      return {
        n: x.length,
        len: x.length > m ? x[x.length - 1].textContent.trim().length : 0,
        busy: !!document.querySelector(".pbc-status.on"),
      };
    }, before);
    if (st.n > before && !st.busy && st.len > 0 && st.len === last) stable++;
    else stable = 0;
    last = st.len;
    if (stable >= 3) break;
    await page.waitForTimeout(1500);
  }
  return page.evaluate(() => {
    const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
    return x.length ? x[x.length - 1].textContent.trim() : "";
  });
}

const sid = (page) =>
  page.evaluate(() => {
    try {
      return JSON.parse(localStorage.getItem("pb.tutor.sessions.v1") || "{}");
    } catch (e) {
      return {};
    }
  });

(async () => {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  let page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", (e) => errs.push(e.message));
  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForTimeout(2500);

  let pass = 0,
    fail = 0;
  const ok = (m) => { console.log("  ok   " + m); pass++; };
  const bad = (m) => { console.log("  FAIL " + m); fail++; };

  console.log("=== 1. book X: say something memorable ===");
  const X = await openBook(page, { year: 7, subject: "Humanities" });
  console.log("  X = " + X.subject);
  await ask(page, "Remember this codeword for later: ELEPHANT-42. Just confirm you have it.");
  const mapA = await sid(page);
  const sidX = mapA[Object.keys(mapA)[0]];
  console.log("  session for X: " + sidX);
  sidX ? ok("session recorded in localStorage") : bad("no session stored");

  console.log("\n=== 2. switch to book Y: must be a DIFFERENT session ===");
  const Y = await openBook(page, { year: 2, subject: "Mathematics" });
  console.log("  Y = " + Y.subject);
  await ask(page, "What is 2 plus 2?");
  const mapB = await sid(page);
  const keys = Object.keys(mapB);
  console.log("  sessions now: " + keys.length);
  keys.length === 2 ? ok("book Y minted its own session") : bad("expected 2 sessions, got " + keys.length);

  console.log("\n=== 3. RELOAD the page (simulates closing the tab) ===");
  await page.reload({ waitUntil: "load" });
  await page.waitForTimeout(2500);
  const mapC = await sid(page);
  Object.keys(mapC).length === Object.keys(mapB).length
    ? ok("session map survived the reload (localStorage)")
    : bad("session map lost on reload: " + JSON.stringify(mapC));

  console.log("\n=== 4. return to book X: does it REMEMBER the codeword? ===");
  await openBook(page, { year: 7, subject: "Humanities" });
  await page.waitForTimeout(3000);
  const restored = await page.evaluate(
    () => document.querySelectorAll("#pbChat .pbc-msg").length,
  );
  console.log("  messages repainted in the panel: " + restored);
  restored > 1
    ? ok("panel restored the earlier transcript from the server")
    : bad("panel came back empty (history verb not working?)");

  const a = await ask(page, "What codeword did I ask you to remember?");
  console.log("  ANSWER: " + a.slice(0, 200));
  /ELEPHANT-42/i.test(a)
    ? ok("SESSION RESUMED: it recalled ELEPHANT-42")
    : bad("did not recall the codeword: session did not resume");

  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  console.log(`\npassed ${pass}, failed ${fail}`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
