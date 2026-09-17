# English Year 1 — standardise Unit 1 · prompt for a fresh Hermes session

Open a new Hermes session and paste everything below the rule as its first
message. It assumes the session runs on the machine that holds the checkout at
`/root/prime-books` (if yours is elsewhere, say so in the first line and stop).

---

You are standardising **English Year 1** for Prime Books — the school's own
Cambridge-pathway textbooks. One book, one job: build the **standardised edition**
of English Year 1 at `public/library/y01-english-standard/`, and **only Unit 1
this round** (pages 8–16 of the new book). Then stop and report, so the teacher
can judge Unit 1 before the rest is done.

A master already exists — `public/library/y01-english/`, 186 pages, written and
placed by the teacher — and an engine already builds a 71-page plan of it in the
standard's shape. This is **not** authoring from nothing: it is recomposing the
master's teaching into the house standard and making each page something a
six-year-old wants to open.

## 1. Load the doctrine before you touch anything

- `skill_view(name='prime-books-standard')` — the specification.
- `skill_view(name='prime-books-book-builder')` — the craft: PDF page authoring,
  plates, print file.
- `skill_view(name='prime-books-site')` — the publishing lane.
- `docs/year-1-book-brief.md` — the brief every card follows; read it end to end.
- From `prime-books-book-builder`'s references: `fresh-standard-edition-from-a-master.md`,
  `standard-edition-from-master-build.md`, `standard-edition-engine-pitfalls.md`,
  `standard-edition-single-line-fit.md`, `print-parity-and-gutter.md`,
  `drawn-furniture-and-masks.md`.

The newest worked example is **Physical Education Year 1**:
`public/library/y01-physical-education-standard/book.pdf` (71 pages, gate-clean)
and its engine `work/y01-pe-book/`. Copy its **method**, never its words, its cast
or its plates.

## 2. Where the material is

| what | where |
|---|---|
| the master — the input to follow | `public/library/y01-english/book.pdf` · 186 pp · 210×270 mm |
| the engine | `work/y01-english-book/` — `build_book.py` (`--plan` prints the page plan and the rhythm audit), `content/*.json` (the words), `art/` (71 plates), `gen_art.py`, `identity.json`, `master-186pp.pdf`, `master-inventory.txt` (an inventory of every master page), `qa_pages.py`, `make_evidence.py` |
| the standard | `public/standards/primary-standard.md` · `public/standards/years-1-4.json` |
| the look of the finished thing | `/book/y01-art-and-design`, pages 8–16 |
| the gate | `tools/standards_check.py` (run everything through `/root/prime-books/.venv/bin/python`) |

## 3. Unit 1 as the plan already has it

Pages 8–16, nine pages, unit colour **violet**: opener (full-bleed, the unit's
colour) · hook *Before you start* · model *Five vowels, one at a time* · response
*Write the five vowels* · breath *Look up* · steps *Make the letter with your
finger first* · signature *Our sound hunt* · wordbank *The sounds we know* · check.

The master's Unit 1 (its pages 8–22 and 30) holds: the five vowels one at a time,
each with its sound, its picture words and its letter hunt; how each letter is
made with a pencil; the four first sounds b, m, s and t; the sound-hunt game; the
unit's own check lines. **Keep the teaching sequence whole** — if nine pages
cannot carry it honestly, extend the unit's pages (the audit allows more D pages);
never drop a beat, never pad.

## 4. The rules that are verdicts, not taste

- **612×792 pt** (US Letter); trim 216×279 mm; 3 mm bleed.
- **Mirrored margins, on the print parity.** 20 mm (56.7 pt) on the binding edge,
  15 mm (42.5 pt) on the outer. The printer's text file prints *its* page 1 on a
  right-hand page and starts at master page 2, so a master **even** page is a
  recto; the engine, the badge and the gate mirror with it. Every page must end
  exactly 20.0 mm off its gutter.
- Nothing below y 741 (the folio-badge zone), nothing above y 12.
- The running-head band and the folio badge (24 pt, centred 550, 758) on every
  interior page.
- **Every page reaches its foot.** `build_book.py` must print
  `fill: every page reaches its foot`; a half-blank page is a defect, not a
  matter of taste. No blank pages.
- **Dynamic pages.** No page type twice in a row, and no two spreads that read as
  the same spread with different words; exactly one signature page and at least
  one breath page in the unit.
- Year 1 reading load: **16 pt on 21 pt leading, never smaller**; ≤80 words a
  page; instructions of seven words or fewer; one idea a page.
- No emojis in shipping text — drawn furniture instead (`arrow()`, `arc()`,
  `spiral()`, drawn faces, chalk lines).
- Fonts embedded, from `/root/pbfonts`: Fredoka (display), Andika (reading),
  Caveat (accent). Plates placed as **JPEG** at 300 DPI.
- **No lettering of any kind inside a picture.**

## 5. The art lock, the place and the cast

The illustration direction is locked in the standard: an original **Beatrix
Potter** direction — fine ink contours, transparent watercolour, warm muted
pigments, lightly textured cream paper. **Music & Drama Year 1 is the on-model
book**: put each new plate beside its plates and regenerate until the light, the
pigments and the weight of the line match. Never photorealistic, never flat vector,
never a modern object.

This book's own place and cast are declared in `identity.json`: **Pippin Hollow** —
a village at the foot of a hill, one lane, a green with a pond, a shop with a bell
over its door, a school with a reading tree on the wall, and a bus that goes over
the hill to market — and **Wren** (a wren in a red knitted bobble hat), **Bramble**
(a hedgehog in a mustard-yellow scarf), **Otis** (a young otter in a blue
fisherman's jumper), **Sorrel** (a rabbit in a green pinafore), **Nell** (a nanny
goat in a patchwork apron), **Barto** (a badger in a long brown coat). Keep them
consistent across every plate, and copy nothing from another Prime Book.

One decision to confirm **before** any plate is painted: the master's own friends
are Leo, Mia, Sofia, Pip and Hoot. If the teacher wants those five for continuity
with the book the children already know, that replaces the cast above and every
plate is painted to match. Ask, and note that Bramble and Sorrel also live in PE
Year 1. Plates route through `tools/pb_image_gen.py` (model
`openai/gpt-image-2.5-sunburst`, medium quality) with a prompt written per plate —
the character, the object, the place.

## 6. What "top tier" looks like on these nine pages

Make each page a place the child wants to stay: pictures that **fill and crop**
like a printed book (no letterboxing, no white dome over an arch); the opener
full-bleed in the unit's colour with the arched window; one wide teaching band for
the vowels with the letters chipped onto it; a printed chalk line with a start dot
and the unit's character showing the stroke order; activity cards with **drawn**
icons; a hand-drawn trail joining the sound hunt; three drawn faces on the check
page; the unit's colour present on every page. The failure mode the teacher named
in his own words: *"not the same structure with different words"*.

## 7. The copyright rule

The master is the source of **sequence and pedagogy**, not of wording. Write every
sentence fresh in the house voice (the voice is declared in `identity.json`:
short second-person sentences, seven-word instructions, no child ever called
"clever", every invitation with a way out). Where a picture word, rhyme or reader
in the master echoes a published reading scheme, choose our own words for the same
sound, on our own cast and props. Never copy from a third-party published book and
never lift a line from the master verbatim: keep the progression, re-express it.

## 8. Method

1. `cd work/y01-english-book && /root/prime-books/.venv/bin/python build_book.py --plan`
   — read the plan and the rhythm audit before drawing anything.
2. Recompose the nine pages in the engine's page types; the words live in
   `content/unit1.json`; generate or regenerate plates as needed.
3. Build: `/root/prime-books/.venv/bin/python build_book.py` → `y01-english-new.pdf`.
4. **Render every page you changed and look at each one** — `vision_analyze` on
   the rendered PNG, one page at a time, at full size, and on every plate before
   you place it. Text-first inspection misses what the teacher sees; this is what
   he means by "refresh to see it". Fix, rebuild, look again.
5. Place the interior at `public/library/y01-english-standard/book.pdf` (the
   master's `cover.webp` serves as the edition's cover — the cover, the imprint
   page and the back cover are the standardised face and are already decided),
   then gate it:
   `/root/prime-books/.venv/bin/python tools/standards_check.py y01-english-standard`
   — **0 failures** required.

## 9. Evidence and boundaries

- Attach before/after renders (master page | your page) for all nine pages, plus a
  contact sheet, plus the gate's own output pasted verbatim. A summary claiming
  the checks pass is not evidence.
- **Never write `public/library/y01-english/`** — that is the teacher's master.
  Restore it with `git checkout HEAD -- public/library/y01-english/` if it changed.
- Touch only English Year 1's files: neighbours are working other books in the
  same checkout.
- Do **not** commit, do **not** push, do **not** write `public/library.json` and
  never write `public/standardized.json` — the publisher lands the row and the
  deploy.
- Nothing is deleted without the teacher's permission, and nothing moves off the
  page he placed it on without a question.

## 10. When to stop and ask

If the work needs a judgement you cannot make — teaching that is not in the master,
a picture that would have to be licensed, a code that would have to be tested,
anything that would have to be **removed**, or the cast decision above — ask **one**
precise question naming the page and the exact text. A block is a good outcome,
not a failure.

## 11. Traps that have already cost a rebuild

- PyMuPDF has no page-level arc — draw it as a polyline.
- A long heading or band label runs out of its box: shrink-then-trim, never
  overflow (one gate failure was a card head reaching x1 576.5 pt).
- Pictures must be cropped to their frame, not letterboxed; an arch needs its
  plate masked into the arch or it shows a white dome.
- A footer reading *Prime School Press · English · Year 1* is **not** part of the
  standard: the running head is the band, the folio is the badge.
- The pack builder is incremental — a geometry change needs `--force`, and never
  run two pack builds for the same slug at once.
- The gate's measured verdict is the truth, not the code's intention: measure the
  rendered page.

## 12. Finish by reporting

Lead with what changed, page by page; give the gate's verdict, the fill line, the
measured margin, and the evidence paths. Then **stop and ask for the teacher's
verdict on Unit 1**. Units 2–6 are a separate round with the same treatment once
Unit 1 is approved.
