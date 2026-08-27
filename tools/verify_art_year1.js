/* The user's scenario, exactly: open ART AND DESIGN YEAR 1 in the site and talk
 * to it as if it were a fresh Hermes session on localhost with that PDF attached.
 *   node tools/verify_art_year1.js
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
    /* Prefer the local manifest: it is the one carrying the MEGA paths that the
       authoring assistant needs, and the one index.html itself uses on
       localhost. Reading the public manifest here reports markdown=undefined. */
    let rows = await fetch("/library.local.json")
      .then((x) => (x.ok ? x.json() : null))
      .catch(() => null);
    if (!Array.isArray(rows) || !rows.length)
      rows = await fetch("/library.json").then((x) => x.json());
    return rows.find((x) => x.year === 1 && x.subject.indexOf("Art") === 0);
  });
  console.log("BOOK: Year " + bk.year + " " + bk.subject + " (" + bk.pages + "pp)");
  console.log("  master : " + bk.src);
  console.log("  markdown: " + bk.markdown);
  console.log("  buildable: " + bk.buildable);

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

  async function ask(q, label) {
    const n = await page.evaluate(
      () => document.querySelectorAll("#pbChat .pbc-assistant .pbc-body").length,
    );
    await page.fill(".pbc-input", q);
    await page.click(".pbc-send");
    const seen = new Set();
    const t0 = Date.now();
    let stable = 0;
    let lastLen = -1;
    for (;;) {
      if (Date.now() - t0 > 760000) { console.log("   (timeout)"); break; }
      const s = await page.evaluate(() => {
        const e = document.querySelector(".pbc-status");
        return e && e.classList.contains("on") ? e.textContent : "";
      });
      if (s && !seen.has(s)) { seen.add(s); console.log("   [" + s + "]"); }
      /* An agent turn interleaves prose and tool calls, so the bubble grows,
         pauses while a tool runs, then grows again. Waiting for "non-empty and
         no status" catches the FIRST paragraph and reports a false failure.
         Require the text to stop growing for several consecutive polls with no
         status chip showing. */
      const st = await page.evaluate((m) => {
        const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
        const busy = !!document.querySelector(".pbc-status.on");
        return {
          n: x.length,
          len: x.length > m ? x[x.length - 1].textContent.trim().length : 0,
          busy: busy,
        };
      }, n);
      if (st.n > n && !st.busy && st.len > 0 && st.len === lastLen) stable++;
      else stable = 0;
      lastLen = st.len;
      if (stable >= 4) break;
      await page.waitForTimeout(1500);
    }
    const a = await page.evaluate(() => {
      const x = document.querySelectorAll("#pbChat .pbc-assistant .pbc-body");
      return x[x.length - 1].textContent.trim();
    });
    console.log("\n" + label + ":\n" + a.slice(0, 900));
    return a;
  }

  console.log("\n================ Q1: does it know it has the files? ================");
  const a1 = await ask(
    "Which book is attached to this session, and what files of it can you actually open on this machine? List the real paths.",
    "A1",
  );
  const okPaths = /MEGA/.test(a1) && /MARKDOWN|Art & Design/.test(a1);
  console.log(okPaths ? "   ok   names the real MEGA paths" : "   FAIL no real paths named");

  console.log("\n================ Q2: make it USE the files ================");
  const a2 = await ask(
    "Open this book's manuscript and list its four unit names, exactly as written in the files.",
    "A2",
  );
  const units = ["mark room", "thread room", "clay room", "paint room"];
  const hit = units.filter((u) => a2.toLowerCase().includes(u));
  console.log("   units found: " + hit.length + "/4 -> " + hit.join(", "));
  console.log(hit.length === 4 ? "   ok   read the real manuscript" : "   FAIL did not read all four");

  console.log("\n================ Q3: rebuild honesty ================");
  const a3 = await ask("Can you rebuild this book's PDF right now?", "A3");
  if (bk.buildable) {
    const claims = /yes|i can|build\.py|rightsize/i.test(a3);
    console.log(
      claims
        ? "   ok   book IS buildable and it says so"
        : "   FAIL book is buildable but it denied it",
    );
  } else {
    const honest = /\bno\b|cannot|can't|no build engine/i.test(a3);
    console.log(
      honest
        ? "   ok   honest that it cannot rebuild"
        : "   FAIL claimed it can rebuild a non-buildable book",
    );
  }

  console.log(errs.length ? "\nJS errors: " + errs.join(" | ") : "\nno JS errors");
  await browser.close();
})();
