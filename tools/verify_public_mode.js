/* Prove the PUBLIC (remote-Hermes) mode without deploying.
 *
 * Serves dist/ + public/ on 127.0.0.1 but visits it as http://[::1] so
 * location.hostname is NOT localhost... which is still local. So instead we
 * assert the two things that actually differ in remote mode, by stubbing
 * hostname detection the way a deployed page would see it:
 *   1. the PUBLIC manifest carries no disk paths (so BOOK_ROWS has none)
 *   2. the reading context/briefing offer a public https URL and DROP the
 *      manuscript paths, buildable flag and the authoring section
 *
 * Run the dev server first (npm run dev), then: node tools/verify_public_mode.js
 */
const BASE = "http://127.0.0.1:5173";

(async () => {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
  const errs = [];
  page.on("pageerror", (e) => errs.push(e.message));

  /* Force the module to believe it is deployed, before it loads. */
  await page.addInitScript(() => {
    window.__PB_FORCE_REMOTE = true;
  });
  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForTimeout(2500);

  console.log("=== 1. public manifest must carry no disk paths ===");
  const pub = await page.evaluate(() =>
    fetch("/books-manifest.json").then((r) => r.json()),
  );
  const fields = Object.keys(pub[0]).sort();
  console.log("   public fields: " + fields.join(", "));
  const leaks = pub.filter((r) =>
    Object.values(r).some((v) => String(v).includes("Users")),
  );
  console.log(
    leaks.length === 0
      ? "   ok   no absolute disk path in the deployed manifest"
      : "   FAIL " + leaks.length + " rows leak a disk path",
  );
  const hasAuthoring = ["src", "markdown", "book_dir", "buildable"].filter((k) =>
    fields.includes(k),
  );
  console.log(
    hasAuthoring.length === 0
      ? "   ok   no authoring fields deployed"
      : "   FAIL deployed manifest exposes: " + hasAuthoring.join(", "),
  );

  console.log("\n=== 2. remote briefing must not promise authoring ===");
  const remote = await page.evaluate(() => !!window.__PB_REMOTE);
  console.log("   module in REMOTE mode: " + remote);
  /* Open a book so the briefing has real metadata to describe. */
  const bk = await page.evaluate(async () => {
    const rows = await fetch("/books-manifest.json").then((r) => r.json());
    return rows.find((x) => x.year === 7 && x.subject.includes("Humanities"));
  });
  await page.evaluate(
    (t) => window.PBReading.openBook({ title: t.subject, band: "Year " + t.year }, t.pdf),
    bk,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });
  await page.waitForTimeout(1500);
  const b = await page.evaluate(() =>
    window.__pbBriefingForTest ? window.__pbBriefingForTest() : "",
  );
  if (!b) {
    console.log("   (no test hook; skipping briefing assertions)");
  } else {
    const bad = ["MARKDOWN", "WORKSTATION", "AUTHORING", "build.py"].filter((s) =>
      b.includes(s),
    );
    console.log(
      bad.length === 0
        ? "   ok   briefing has no manuscript/build instructions"
        : "   FAIL briefing still mentions: " + bad.join(", "),
    );
    console.log(
      /public URL: https?:\/\//.test(b)
        ? "   ok   briefing offers a fetchable public URL"
        : "   FAIL no public URL offered to the remote agent",
    );
  }

  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  await browser.close();
})();
