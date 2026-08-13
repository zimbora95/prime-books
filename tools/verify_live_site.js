/* Drive the DEPLOYED site end to end against the real backend.
 *
 * Opens a book on the live site, asks a question whose answer exists only on the
 * page in front of the reader, and checks the reply against that page's actual
 * text. This is the only test that proves the whole chain: browser -> Vercel
 * function -> GCP Hermes -> model -> back.
 *
 *   node tools/verify_live_site.js [https://prime-books-pi.vercel.app]
 */
const SITE = process.argv[2] || "https://prime-books-pi.vercel.app";

(async () => {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on("pageerror", (e) => errs.push(e.message));

  console.log("site: " + SITE);
  await page.goto(SITE, { waitUntil: "load", timeout: 90000 });
  await page.waitForTimeout(3000);

  const health = await page.evaluate(() =>
    fetch("/hermes/health").then((r) => r.json()),
  );
  console.log("hermes health: " + JSON.stringify(health));
  if (!health.configured) {
    console.log("FAIL not configured: set the env vars in Vercel and redeploy");
    await browser.close();
    process.exit(1);
  }

  const bk = await page.evaluate(async () => {
    const rows = await fetch("/books-manifest.json").then((r) => r.json());
    return rows.find((x) => x.year === 7 && x.subject.includes("Humanities"));
  });
  console.log(`book: Year ${bk.year} ${bk.subject} (${bk.pages}pp)`);

  await page.evaluate(
    (t) =>
      window.PBReading.openBook(
        { title: t.subject, band: "Year " + t.year, yearNum: t.year },
        t.pdf,
      ),
    bk,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });
  await page.waitForTimeout(2500);

  /* Land on a spread of real body text, not the contents list: a contents page
     can be summarised from the book's structure alone, so it does not prove the
     page text reached the model. */
  await page.evaluate(() => window.PBReading.goToPage(99));
  await page.waitForTimeout(3000);
  const spread = await page.evaluate(() => window.PBReading.spread());
  /* Grade against the text the model was actually given: a spread's left page is
     often blank (art, or a section break), so reading only spread[0] scored an
     accurate answer as ungrounded. Concatenate every visible page. */
  const parts = [];
  for (const p of spread) {
    parts.push(await page.evaluate((n) => window.PBReading.pageText(n), p));
  }
  const src = parts.join("\n");
  console.log(
    `spread ${spread.join("-")}, source text ${src.length} chars ` +
      `(per page: ${parts.map((t) => t.length).join(", ")})`,
  );
  console.log("source opens: " + JSON.stringify(src.slice(0, 120)));

  const before = await page.evaluate(
    () => document.querySelectorAll("#pbChat .pbc-assistant .pbc-body").length,
  );
  await page.fill(".pbc-input", "In one sentence, what are these two pages about?");
  await page.click(".pbc-send");

  const seen = new Set();
  let stable = 0,
    lastLen = -1;
  const t0 = Date.now();
  for (;;) {
    if (Date.now() - t0 > 300000) {
      console.log("   (timed out waiting for the answer)");
      break;
    }
    const s = await page.evaluate(() => {
      const e = document.querySelector(".pbc-status");
      return e && e.classList.contains("on") ? e.textContent : "";
    });
    if (s && !seen.has(s)) {
      seen.add(s);
      console.log("   [" + s + "]");
    }
    const st = await page.evaluate((m) => {
      const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      return {
        n: x.length,
        len: x.length > m ? x[x.length - 1].textContent.trim().length : 0,
        busy: !!document.querySelector(".pbc-status.on"),
      };
    }, before);
    if (st.n > before && !st.busy && st.len > 0 && st.len === lastLen) stable++;
    else stable = 0;
    lastLen = st.len;
    if (stable >= 3) break;
    await page.waitForTimeout(1500);
  }

  const answer = await page.evaluate(() => {
    const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
    return x.length ? x[x.length - 1].textContent.trim() : "";
  });
  console.log("\nANSWER: " + answer.slice(0, 500));

  /* Prime PDFs set headings with wide letter-spacing, so pdf.js returns
     "P A R T  T W O · T H E  P L A Y E R S". Collapse runs of single letters
     before comparing, or a correct answer scores as ungrounded. */
  const normalise = (s) =>
    s
      .toLowerCase()
      .replace(/(?:\b[a-z]\s){2,}\b[a-z]\b/g, (m) => m.replace(/\s+/g, ""))
      .replace(/\s+/g, " ");
  const stop = new Set(
    ("the a an and or of to in on for with is are was were this that these those " +
      "you your it its as at by from be been about page pages book year one two " +
      "part unit units topic topics number numbers list listing every")
      .split(" "),
  );
  const pageWords = new Set(
    (normalise(src).match(/[a-z]{5,}/g) || []).filter((w) => !stop.has(w)),
  );
  const answerWords = (normalise(answer).match(/[a-z]{5,}/g) || []).filter(
    (w) => !stop.has(w),
  );
  const overlap = [...new Set(answerWords.filter((w) => pageWords.has(w)))];
  console.log(
    `\ngrounding: ${overlap.length} distinctive words shared with the real page`,
  );
  console.log("  " + overlap.slice(0, 14).join(", "));
  console.log(
    overlap.length >= 2
      ? "  ok   the answer reuses this page's own vocabulary"
      : "  CHECK low overlap: read the answer against the page yourself",
  );
  console.log(
    "  (advisory only: a correct paraphrase can legitimately score low)",
  );
  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  await browser.close();
})();
