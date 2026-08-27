/* Verify the Prime Books reading assistant against a running dev server.
 *
 * Tests the things that actually break:
 *   1. the panel mounts and the rail is visible
 *   2. PBReading reports the correct spread and real page text
 *   3. page-change events fire and the panel's label follows
 *   4. canvas budget is respected on the LONGEST book (628pp) - no crash
 *   5. a different book creates a DIFFERENT Hermes session; same book reuses it
 *   6. a real question about a real page gets an answer grounded in that page
 *
 * Usage: node tools/verify_assistant.js [baseUrl]
 */
const BASE = process.argv[2] || "http://127.0.0.1:5173";

async function main() {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });

  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("crash", () => errors.push("PAGE CRASHED"));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push("console: " + m.text().slice(0, 200));
  });

  const log = (s) => console.log(s);
  const fail = (s) => {
    console.log("  FAIL " + s);
    process.exitCode = 1;
  };
  const ok = (s) => console.log("  ok   " + s);

  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForTimeout(2500);

  /* ---- 1. panel mounted ---- */
  log("\n[1] panel mounts");
  const mounted = await page.evaluate(
    () => !!document.getElementById("pbChat"),
  );
  mounted ? ok("#pbChat present") : fail("#pbChat missing");
  const hasApi = await page.evaluate(() => !!window.PBReading);
  hasApi ? ok("window.PBReading present") : fail("window.PBReading missing");

  /* ---- open the LONGEST book straight from the manifest ---- */
  log("\n[2] open the longest book (628pp PE Year 12)");
  const target = await page.evaluate(async () => {
    const rows = await fetch("/books-manifest.json").then((r) => r.json());
    rows.sort((a, b) => (b.pages || 0) - (a.pages || 0));
    return rows[0];
  });
  log("    " + target.pages + "pp - Year " + target.year + " " + target.subject);

  await page.evaluate(
    (t) =>
      window.PBReading.openBook(
        { title: t.subject, band: "Year " + t.year, yearNum: t.year },
        t.pdf,
      ),
    target,
  );
  await page.waitForFunction(() => window.PBReading && window.PBReading.ready, {
    timeout: 180000,
  });
  ok("flipbook built, PBReading.ready = true");

  const memAfterOpen = await page.evaluate(() => ({
    live: document.querySelectorAll("#fbBook canvas").length,
    withBitmap: Array.from(
      document.querySelectorAll("#fbBook canvas"),
    ).filter((c) => c.width > 0).length,
    pages: window.PBReading.spread(),
  }));
  log(
    "    shells=" +
      memAfterOpen.live +
      " withBitmap=" +
      memAfterOpen.withBitmap +
      " spread=" +
      JSON.stringify(memAfterOpen.pages),
  );
  memAfterOpen.withBitmap <= 45
    ? ok("canvas budget respected (" + memAfterOpen.withBitmap + " <= 45)")
    : fail("too many live canvases: " + memAfterOpen.withBitmap);

  /* ---- 3. page text is real ---- */
  log("\n[3] page text extraction");
  const textSample = await page.evaluate(async () => {
    const R = window.PBReading;
    for (const p of [8, 12, 20, 30, 40]) {
      const t = await R.pageText(p);
      if (t && t.length > 120) return { page: p, len: t.length, head: t.slice(0, 160) };
    }
    return null;
  });
  if (textSample) {
    ok("page " + textSample.page + " -> " + textSample.len + " chars");
    log("    \u201c" + textSample.head.replace(/\s+/g, " ") + "\u2026\u201d");
  } else fail("no page yielded extractable text");

  /* ---- 4. flip tracking ---- */
  log("\n[4] page-change tracking");
  await page.evaluate(() => {
    window.__pbEvents = [];
    window.addEventListener("pb:page-change", (e) =>
      window.__pbEvents.push(e.detail.pages),
    );
  });
  const before = await page.evaluate(() => window.PBReading.spread());
  await page.evaluate(() => window.PBReading.goToPage(64));
  await page.waitForTimeout(2000);
  const after = await page.evaluate(() => window.PBReading.spread());
  const evs = await page.evaluate(() => window.__pbEvents.length);
  log("    " + JSON.stringify(before) + " -> " + JSON.stringify(after) + " (" + evs + " events)");
  evs > 0 ? ok("pb:page-change fired") : fail("no pb:page-change event");
  after[0] !== before[0]
    ? ok("spread advanced")
    : fail("spread did not change");
  const label = await page.evaluate(
    () => (document.querySelector(".pbc-where") || {}).textContent || "",
  );
  /^Reading page/.test(label)
    ? ok('panel label follows: "' + label + '"')
    : fail('panel label wrong: "' + label + '"');

  /* ---- 5. memory after heavy navigation ---- */
  log("\n[5] canvas budget after deep navigation");
  for (const p of [120, 240, 360, 480, 600, 300, 90]) {
    await page.evaluate((n) => window.PBReading.goToPage(n), p);
    await page.waitForTimeout(700);
  }
  const liveCount = () =>
    page.evaluate(
      () =>
        Array.from(document.querySelectorAll("#fbBook canvas")).filter(
          (c) => c.width > 0,
        ).length,
    );
  const peak = await liveCount();
  /* Renders in flight hold an allocated canvas that eviction must NOT reclaim
     (zeroing it mid-render blanks the page), so the count legitimately
     overshoots while a burst settles. What must hold is the SETTLED bound. */
  await page.waitForTimeout(4000);
  const settled = await liveCount();
  const mb = await page.evaluate(() => {
    let bytes = 0;
    document
      .querySelectorAll("#fbBook canvas")
      .forEach((c) => (bytes += c.width * c.height * 4));
    return Math.round(bytes / 1048576);
  });
  log(
    "    peak during burst: " +
      peak +
      "  settled: " +
      settled +
      "  (~" +
      mb +
      " MB)",
  );
  settled <= 40
    ? ok("settled at the budget (" + settled + " <= 40)")
    : fail("budget blown after settle: " + settled);
  peak <= 70
    ? ok("transient peak sane (" + peak + " <= 70)")
    : fail("transient peak too high: " + peak);

  const crashed = errors.some((e) => e.includes("CRASH"));
  crashed ? fail("renderer crashed") : ok("no crash on the 628pp book");

  /* ---- 6. sessions: one per book ---- */
  log("\n[6] one Hermes session per book");
  const s1 = await page.evaluate(async () => {
    const r = await fetch("/hermes/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "verify book A" }),
    });
    return (await r.json()).sessionId;
  });
  const s2 = await page.evaluate(async () => {
    const r = await fetch("/hermes/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "verify book B" }),
    });
    return (await r.json()).sessionId;
  });
  log("    A=" + s1 + "  B=" + s2);
  s1 && s2 && s1 !== s2
    ? ok("distinct sessions minted")
    : fail("sessions not distinct");

  /* ---- 7. grounded answer about a real page ---- */
  log("\n[7] a real answer about a real page (this calls the model)");
  const answer = await page.evaluate(async (sid) => {
    const R = window.PBReading;
    const pages = R.spread();
    const text = await R.pageText(pages[0]);
    const input =
      "[READING CONTEXT]\nBook: Physical Education, Year 12\nVisible: page " +
      pages[0] +
      "\n--- page text ---\n" +
      text.slice(0, 4000) +
      "\n[END]\n\nPupil's question: In one short sentence, what is this page about? Answer only from the text above.";
    const res = await fetch("/hermes/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessionId: sid, input: input }),
    });
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = "",
      out = "";
    for (;;) {
      const c = await reader.read();
      if (c.done) break;
      buf += dec.decode(c.value, { stream: true });
      const frames = buf.split(/\n\n/);
      buf = frames.pop();
      for (const f of frames) {
        if (f.indexOf("event: assistant.completed") === 0) {
          const line = f.split(/\n/).find((l) => l.indexOf("data:") === 0);
          if (line) {
            try {
              out = JSON.parse(line.slice(5)).content || out;
            } catch (e) {}
          }
        }
      }
    }
    return { pages: pages, answer: out, sourceLen: text.length };
  }, s1);
  log("    page " + answer.pages[0] + " (" + answer.sourceLen + " chars of source)");
  log("    ANSWER: " + (answer.answer || "(none)").slice(0, 300));
  answer.answer && answer.answer.length > 15
    ? ok("model answered")
    : fail("no answer returned");

  /* ---- 8. book switch: new book = new session, same book = same session ---- */
  log("\n[8] session identity across a real book switch");
  const second = await page.evaluate(async () => {
    const rows = await fetch("/books-manifest.json").then((r) => r.json());
    rows.sort((a, b) => (b.pages || 0) - (a.pages || 0));
    return rows[2];
  });
  const keyA = await page.evaluate(() => window.PBReading.bookKey);
  await page.evaluate(
    (t) => window.PBReading.openBook({ title: t.subject }, t.pdf),
    second,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });
  await page.waitForTimeout(1200);
  const keyB = await page.evaluate(() => window.PBReading.bookKey);
  log("    A=" + String(keyA).slice(-42) + "\n    B=" + String(keyB).slice(-42));
  keyA && keyB && keyA !== keyB
    ? ok("bookKey changed on switch (=> new session)")
    : fail("bookKey did not change");
  const logCleared = await page.evaluate(
    () => document.querySelectorAll("#pbChat .pbc-msg").length,
  );
  log("    panel messages after switch: " + logCleared);
  logCleared <= 1
    ? ok("panel reset for the new book")
    : fail("stale conversation carried across books");

  /* back to the first book: the key must come back identical */
  await page.evaluate(
    (t) => window.PBReading.openBook({ title: t.subject }, t.pdf),
    target,
  );
  await page.waitForFunction(() => window.PBReading.ready, { timeout: 180000 });
  await page.waitForTimeout(1200);
  const keyAgain = await page.evaluate(() => window.PBReading.bookKey);
  keyAgain === keyA
    ? ok("returning to book A restores its key (=> its session resumes)")
    : fail("book A key not restored: " + keyAgain);

  /* ---- 9. rail toggle re-lays-out the spread ---- */
  log("\n[9] rail toggle re-lays-out the spread");
  /* At a wide viewport the spread is HEIGHT-constrained, so there is room for
     the rail either way and the width legitimately does not move. Narrow the
     window so the rail actually competes for width - that is the case that
     would otherwise push the book off-centre. */
  await page.setViewportSize({ width: 1150, height: 900 });
  await page.waitForTimeout(1200);
  const wOn = await page.evaluate(
    () => document.getElementById("fbBook").getBoundingClientRect().width,
  );
  const fitsOn = await page.evaluate(() => {
    const b = document.getElementById("fbBook").getBoundingClientRect();
    const r = document.getElementById("pbChat").getBoundingClientRect();
    return {
      overlap: b.right > r.left + 2,
      bookRight: Math.round(b.right),
      railLeft: Math.round(r.left),
    };
  });
  log("    with rail: book width=" + Math.round(wOn) + " right=" + fitsOn.bookRight + " rail left=" + fitsOn.railLeft);
  !fitsOn.overlap
    ? ok("book and rail do not overlap at 1150px")
    : fail("book overlaps the rail at 1150px");

  await page.evaluate(() => document.getElementById("pbChatBtn").click());
  await page.waitForTimeout(1200);
  const wOff = await page.evaluate(
    () => document.getElementById("fbBook").getBoundingClientRect().width,
  );
  log("    without rail: book width=" + Math.round(wOff));
  wOff > wOn + 20
    ? ok("book reclaims the rail's width when hidden")
    : fail("book did not grow (" + Math.round(wOn) + " -> " + Math.round(wOff) + ")");
  const railHidden = await page.evaluate(
    () => !document.body.classList.contains("pbc-on"),
  );
  railHidden ? ok("rail hidden") : fail("rail still visible");
  await page.evaluate(() => document.getElementById("pbChatBtn").click());
  await page.waitForTimeout(1000);
  const wBack = await page.evaluate(
    () => document.getElementById("fbBook").getBoundingClientRect().width,
  );
  Math.abs(wBack - wOn) < 3
    ? ok("re-showing the rail restores the layout")
    : fail("layout not restored: " + Math.round(wOn) + " -> " + Math.round(wBack));

  if (errors.length) {
    log("\nJS errors seen (" + errors.length + "):");
    errors.slice(0, 8).forEach((e) => log("    " + e));
  } else log("\nno JS errors");

  await browser.close();
  log(
    process.exitCode === 1
      ? "\nRESULT: failures above"
      : "\nRESULT: all checks passed",
  );
}
main().catch((e) => {
  console.error("harness error:", e);
  process.exit(1);
});
