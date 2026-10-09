# PROMPT — NEW PRIME BOOK · UNIT 1
(Fill in the [BRACKETS]. Send this once. Then /queue the "UNIT N" prompt below for each next unit.)

Build a premium ("top tier pro") Prime Book from scratch: **[SUBJECT] · [YEAR LABEL, e.g. 6.º Ano]**,
experiment slug **[SLUG, e.g. y06-portuguese-anthropic]**, language **[pt-PT / en-GB / …]**.
Inputs: `public/inputs/[MASTER-SLUG].json` + `public/markdown/[MASTER-SLUG].md` (unit list and specs).
Cover source: the master book `public/library/[MASTER-SLUG]/book.pdf` (page 1 + last page).
This message covers **UNIT 1 ONLY**. Finish it, check it, publish it, then stop. I will queue the next units.
Before starting, read `prime-books-book-builder/references/new-book-unit-by-unit-lessons.md`.

## Fixed decisions (do not revisit)
1. **Format.** US Letter 216 × 279 mm, HTML → Chromium PDF, one folder per unit
   (`experiments/[SLUG]/u1/`, `u2/`, …), own `build.py`, `metrics.py`, `src/`, `art/`.
   - Live text ≥ 5 mm from every trim edge (headers, folios and tab labels too) and ≥ 20 mm from the gutter.
   - Design odd/even furniture for PRINT parity: the printed interior starts at book p. 2 on a right-hand page.
2. **Fonts.** Static TTF instances only, no variable fonts. Use `*{font-synthesis:none}`.
   - Any symbol the fonts lack is an inline SVG with explicit width/height.
   - Gate: zero Type3, zero fallback fonts (DejaVu/Liberation) in `get_fonts`/spans.
3. **No self-recorded audio and no TTS. No QR code or URL to `*.vercel.app` or any of our own hosting.**
   - Every QR goes to a stable PUBLIC site: RTP Ensina / RTP Arquivos / RTP Play, PNL, DGE, museums,
     municipalities, Priberam, Infopédia, Ciência Viva, Wikipédia.
   - Verify each URL (HTTP 200) and read what it really contains. Questions must be answerable from it.
     Never invent the content of a video you did not verify.
   - If no public resource fits, design a different activity (paired reading aloud, dramatisation,
     teacher reads a text printed in the teacher section).
   - Generate QR codes with `segno`, with a `viewBox` and a 4-module quiet zone.
4. **Solutions and teacher read-aloud texts** go in the book's back matter. Write them per unit to
   `uN/site/solucoes.md` and `uN/site/textos-professor.md`. Never on a web page.
5. **Language.** Every label in the book's language, including the year: «6.º Ano», never «Year 6».
   - Applies everywhere: openers, running headers, imprint, tests, covers.
   - pt-PT under AO90, polished register for the age group.
6. **Copyright.** Copyrighted literary works: short attributed extracts (≤ 4 lines), plus our own
   summaries and activities. The full book is read in class.
7. **Art.** One style for the whole book: [e.g. gouache + coloured pencil, mid-century European picture book;
   palette …].
   - Pure white backgrounds for spot art. No text in images.
   - Use multi-panel sheets (2×2 / 3×3) cropped for character consistency.
   - Vision-review every image before use.
8. **Continuity.** Folios and activity numbers run continuously across the whole book. Unit 1 starts at folio 1
   (front matter is roman, i–viii) and activity 1. Record the last folio and last activity number in
   `experiments/[SLUG]/continuity.json`.
9. **Page count.** Each unit has an even page count and no blank pages. Unit 1 = [24] pages.
10. **Background work.** Long work runs as detached `hermes chat -Q --query-file` jobs, never in-chat
    subagents. Venv in `/root/.venvs/`. Tell me the cost estimate before launching more than one job.

## Unit 1 content
[Unit 1 title + subunits from the inputs, plus any teacher notes.] Each subunit gets:
- a text or extract;
- comprehension at three levels (bronze / prata / ouro);
- grammar or vocabulary in context;
- a writing or oral task.

Plus a full-bleed illustrated opener, a unit-plan page and a closing self-check page.

## QA gate (all must pass before you report)
- `metrics.py`: no overflow or collision, content bottom ≤ 270 mm, nothing past the right margin.
- Every page rendered at ≥ 130 dpi and reviewed one by one with vision as a strict print art director.
  Settle every claimed defect with a DOM or pixel measurement before editing.
- Proof-read all text once more.
- Decode every QR from the PDF (tiled cv2, 200 dpi). Zero contain "vercel" and all return HTTP 200.
- Grep printed text for "vercel", "Year ", "faixa", "áudio gravado": zero hits.
- Fonts gate passes (Type3 = 0, no fallbacks). Page count exact and even.
- Before/after PNGs of every reworked page in `u1/qa-evidence/`.

## Publish Unit 1
1. Copy to `public/library/[SLUG]/` (book.pdf, cover.webp from page 1, preview/).
2. Add or patch ONE row in `public/library.json` (surgical, origin/main + my row only, original formatting).
3. Regenerate `public/markdown/[SLUG].md` for this slug only.
4. Commit only this slug's files and push. Verify the live PDF md5 matches the local file.
5. Report: page list, QR list (page → URL), checks output, cost of this unit, and honest leftovers.
   Do not build covers, front matter or the BookVault pack yet. That comes after the last unit.
