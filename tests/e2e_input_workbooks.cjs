/* E2E for editable input workbooks in master and finished readers. */
const { chromium } = require("/tmp/node_modules/playwright-core");
const BASE = process.env.PB_BASE || "http://127.0.0.1:8645";
const CHROME = process.env.PB_CHROME ||
  "/root/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome";
const slugs = ["y04-portuguese", "y05-portuguese", "y06-portuguese",
  "y08-portuguese-1st", "y10-portuguese-1st", "y11-portuguese-1st"];
const expectedSubunit = "Unidade 2.4 - Texto Narrativo - Literaturas de Língua Portuguesa";

async function waitForInputButton(page) {
  await page.waitForFunction(() => {
    const button = document.getElementById("fbInputBtn");
    return button && getComputedStyle(button).display !== "none";
  }, null, { timeout: 60000 });
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const failures = [];

  for (const slug of slugs) {
    const response = await page.goto(BASE + "/book/" + slug,
      { waitUntil: "domcontentloaded", timeout: 45000 });
    if (!response || response.status() !== 200)
      throw new Error(`${slug}: route status ${response && response.status()}`);
    await waitForInputButton(page);
    await page.click("#fbInputBtn");
    await page.waitForFunction(() => {
      const panel = document.getElementById("fbInputPanel");
      return panel && panel.classList.contains("spreadsheet") &&
        panel.querySelectorAll(".fb-input-sheet tbody tr").length >= 1;
    }, null, { timeout: 30000 });
    const state = await page.evaluate(() => {
      const panel = document.getElementById("fbInputPanel");
      const link = panel.querySelector("#fbInputNote a");
      const rows = Array.from(panel.querySelectorAll(".fb-input-sheet tbody tr"));
      return {
        panel: panel.className,
        heading: document.getElementById("fbInputHead").textContent,
        note: document.getElementById("fbInputNote").textContent,
        href: link ? decodeURIComponent(new URL(link.href).pathname) : "",
        download: link && link.getAttribute("download"),
        units: rows.filter((r) => r.classList.contains("unit")).length,
        subunits: rows.filter((r) => r.classList.contains("subunit")).length,
        labels: rows.map((r) => r.cells[1]?.textContent.trim() || ""),
      };
    });
    const expectedPath = `/inputs/${slug} - input.xlsx`;
    const file = await page.request.get(BASE + "/inputs/" + encodeURIComponent(`${slug} - input.xlsx`));
    const workbookBytes = await file.body();
    if (slug === "y04-portuguese" && process.env.PB_SHOT)
      await page.screenshot({ path: process.env.PB_SHOT, fullPage: false });
    const ok = state.panel.includes("spreadsheet") && state.heading === "Excel workbook input" &&
      state.href === expectedPath && state.download === `${slug} - input.xlsx` &&
      state.units === 8 && state.subunits === 13 &&
      (slug !== "y04-portuguese" || state.labels.includes(expectedSubunit)) &&
      file.status() === 200 && workbookBytes.subarray(0, 2).toString() === "PK";
    console.log(`${ok ? "PASS" : "FAIL"} ${slug}: ${state.units} units, ${state.subunits} subunits, workbook HTTP ${file.status()}`);
    if (!ok) failures.push(slug);
  }

  /* An existing finished edition must inherit its master's editable workbook. */
  await page.goto(BASE + "/finished/book/y01-physical-education-standard",
    { waitUntil: "domcontentloaded", timeout: 45000 });
  await waitForInputButton(page);
  await page.click("#fbInputBtn");
  await page.waitForFunction(() => {
    const panel = document.getElementById("fbInputPanel");
    return panel && panel.classList.contains("spreadsheet") &&
      panel.querySelectorAll(".fb-input-sheet tbody tr").length > 0;
  }, null, { timeout: 30000 });
  const finished = await page.evaluate(() => ({
    heading: document.getElementById("fbInputHead").textContent,
    href: decodeURIComponent(new URL(document.querySelector("#fbInputNote a").href).pathname),
    rows: document.querySelectorAll(".fb-input-sheet tbody tr").length,
  }));
  const finishedOk = finished.heading === "Excel workbook input" &&
    finished.href === "/inputs/y01-physical-education - input.xlsx" && finished.rows > 0;
  console.log(`${finishedOk ? "PASS" : "FAIL"} finished reader inherits master's workbook: ${finished.rows} rows`);
  if (!finishedOk) failures.push("finished-workbook-inheritance");

  /* Keep the existing PDF reader treatment intact for books that genuinely use PDFs. */
  await page.goto(BASE + "/book/y01-english", { waitUntil: "domcontentloaded", timeout: 45000 });
  await waitForInputButton(page);
  await page.click("#fbInputBtn");
  await page.waitForSelector("#fbInputPanel.viewer iframe", { timeout: 30000 });
  const pdfPath = await page.evaluate(() =>
    decodeURIComponent(new URL(document.querySelector("#fbInputBody iframe").src).pathname));
  const pdfOk = pdfPath === "/inputs/y01-english - input.pdf";
  console.log(`${pdfOk ? "PASS" : "FAIL"} existing PDF source still uses the document viewer`);
  if (!pdfOk) failures.push("pdf-viewer-regression");

  await browser.close();
  console.log(`${slugs.length + 2 - failures.length}/${slugs.length + 2} input-source checks passed`);
  process.exit(failures.length ? 1 : 0);
})().catch((error) => { console.error(error); process.exit(2); });
