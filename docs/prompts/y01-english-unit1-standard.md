# Prompt — English Year 1: Unit 1 in the standardised edition

Paste everything below the rule into the worker (a fresh session on this checkout,
or a kanban card body). It is written to be self-contained: it names the master,
the engine, the standard, the look, the gate and the evidence, and it stops at
Unit 1 for the teacher's verdict.

---

## Your job

Build the **standardised edition of English Year 1** at
`public/library/y01-english-standard/`, following the house standard, and make it
a top-tier Year 1 book a six-year-old wants to open. **This round is Unit 1 only**
— pages 8–16 of the new book. Then stop, attach your evidence and wait for the
teacher's verdict. Units 2–6 are a separate round with the same treatment.

The master (`public/library/y01-english/`) is the **input to follow**: its
teaching sequence and its cast are the material. Its wording is not — see the
copyright rule below.

## Where everything is (paths verified in this checkout)

| what | where |
|---|---|
| the master — the input | `public/library/y01-english/book.pdf` · 186 pp · 210×270 mm · front matter, six units, back matter |
| the engine to work in | `work/y01-english-book/` — `build_book.py` (page-type engine; `--plan` prints the plan and the rhythm audit), `content/*.json` (the words), `art/` (71 plates), `gen_art.py`, `identity.json` (this book's own identity), `master-186pp.pdf`, `master-inventory.txt` (page-by-page inventory of the master), `qa_pages.py`, `make_evidence.py` |
| the standard | `public/standards/primary-standard.md` · `public/standards/years-1-4.json` |
| the brief every card follows | `docs/year-1-book-brief.md` — read it end to end first |
| the look of the finished thing | `/book/y01-art-and-design`, pages 8–16 — that is the unit language |
| the newest worked example | `public/library/y01-physical-education-standard/book.pdf` (71 pp, gate-clean) and its engine `work/y01-pe-book/build_book.py` |
| the gate | `tools/standards_check.py <slug>` |
| craft notes, read before touching anything | `prime-books-book-builder` skill references: `fresh-standard-edition-from-a-master.md`, `standard-edition-from-master-build.md`, `standard-edition-engine-pitfalls.md`, `standard-edition-single-line-fit.md`, `print-parity-and-gutter.md`, `drawn-furniture-and-masks.md`; and `prime-books-site`: `publishing-a-standard-edition.md` |

## Unit 1 as the plan already has it

Nine pages, pages 8–16, unit colour **violet**:

1. opener (full-bleed, the unit's colour)
2. hook — *Before you start*
3. model — *Five vowels, one at a time*
4. response — *Write the five vowels*
5. breath — *Look up*
6. steps — *Make the letter with your finger first*
7. signature — *Our sound hunt*
8. wordbank — *The sounds we know*
9. check

The master's Unit 1 (its pages 8–22 and 30) holds: the five vowels one at a time,
each with its sound, its picture words and its letter hunt; how each letter is
made with a pencil; the four first sounds b, m, s and t; the sound-hunt game; the
unit's own check lines.

**Keep the teaching sequence whole.** If nine pages cannot carry it honestly,
extend the unit's pages (the plan audit allows more D pages) — never drop a beat,
never pad.

## Rules that are verdicts, not taste

- **612×792 pt** (US Letter); trim 216×279 mm; 3 mm bleed.
- **Mirrored margins, on the print parity.** A `-standard` page keeps **20 mm
  (56.7 pt) on its binding edge and 15 mm (42.5 pt) on the outer edge**. The pack
  prints *its* page 1 on a right-hand page and starts at master page 2, so a
  master **even** page is a recto; the engine and the gate mirror accordingly.
  The gate fails text outside that box. Every page must end exactly 20.0 mm off
  its gutter.
- Nothing below **y 741** (the folio-badge zone), nothing above y 12.
- Every interior page carries the running-head band and the folio badge (24 pt,
  centred at 550, 758); the badge mirrors with the page.
- **Every page reaches its foot**: `build_book.py` must print
  `fill: every page reaches its foot`. A half-blank page is a defect.
- **Dynamic pages**: no page type twice in a row, no two spreads reading as the
  same spread with different words, exactly one signature page and at least one
  breath page in the unit.
- Year 1 reading load: **16 pt on 21 pt leading, never smaller**; ≤80 words a
  page; instructions ≤7 words; one idea a page.
- No emojis in shipping text — drawn furniture instead (`arrow()`, `arc()`,
  `spiral()`, drawn faces, chalk lines).
- Fonts embedded, from `/root/pbfonts`: Fredoka (display), Andika (reading),
  Caveat (accent).
- Plates placed as **JPEG** at 300 DPI; **no lettering of any kind inside a
  picture**.

## The art lock and this book's cast

The illustration direction is locked in the standard: an original **Beatrix
Potter** direction — fine ink contours, transparent watercolour, warm muted
pigments, lightly textured cream paper. **Music & Drama Year 1 is the on-model
book**: put every new plate beside its plates and regenerate until the light, the
pigments and the weight of the line match. Never photorealistic, never flat
vector, never a modern object.

This book's own cast and place are declared in `identity.json` — **Pippin Hollow**,
a village at the foot of a hill with one lane, a green with a pond, a shop with a
bell, a school with a reading tree, and a bus over the hill to market — and its
friends: **Wren** (a wren in a red knitted bobble hat), **Bramble** (a hedgehog in
a mustard-yellow scarf), **Otis** (a young otter in a blue fisherman's jumper),
**Sorrel** (a rabbit in a green pinafore), **Nell** (a nanny goat in a patchwork
apron) and **Barto** (a badger in a long brown coat). They are consistent across
every plate and nothing is copied from another Prime Book — not a sentence, not an
animal, not a plate. (The master's own friends — Leo, Mia, Sofia, Pip and Hoot —
stay in the master; if the teacher wants them for continuity with the book the
children already know, that is one decision to confirm **before** plates are
painted, and two names to check against the other Year 1 titles: Bramble and
Sorrel also live in PE Year 1.) Plates route
through `tools/pb_image_gen.py` (model `openai/gpt-image-2.5-sunburst`, medium
quality) with a prompt written per plate — the character, the object, the place.
**Look at every plate yourself before you place it.**

## What "top tier" means for these nine pages

Take the teaching you keep and make each page a place the child wants to stay:
pictures that **fill and crop** like a printed book (no letterboxing, no white
dome over an arch); the opener full-bleed in the unit's colour with the arched
window; one wide teaching band for the vowels with the letters chipped onto it;
a printed chalk line with a start dot and the unit's character showing the stroke
order; activity cards with **drawn** icons; a hand-drawn trail joining the sound
hunt; three drawn faces on the check page; the unit's colour present on every
page. The teacher's words for the failure mode: *"not the same structure with
different words"*.

## The copyright rule

The master is the source of **sequence and pedagogy**, not of wording. Write
every sentence fresh in the house voice. Where a picture word, rhyme or reader in
the master echoes a published reading scheme, choose our own words for the same
sound, on our own cast and props. Never copy text from any third-party published
book, and never lift a line from the master verbatim: keep the progression, and
re-express it.

## The process

1. Read `docs/year-1-book-brief.md` and the craft notes above, then read the
   master's Unit 1 pages.
2. `cd work/y01-english-book && /root/prime-books/.venv/bin/python build_book.py --plan`
   — confirm the plan and the rhythm audit before drawing anything.
3. Recompose the nine pages in the engine's page types; keep the words in
   `content/unit1.json`; generate or regenerate plates as needed.
4. `/root/prime-books/.venv/bin/python build_book.py` → `y01-english-new.pdf`.
   **Render and look at every page yourself**, one at a time; fix; rebuild.
5. Place the interior at `public/library/y01-english-standard/book.pdf` (with
   the master's `cover.webp` as the edition's cover), then gate it:
   `/root/prime-books/.venv/bin/python tools/standards_check.py y01-english-standard`
   — **0 failures** required.
6. Evidence: before/after renders (master page | your page) for all nine pages,
   plus a contact sheet, plus the gate's output pasted into your comment.
7. **Never touch `public/library/y01-english/`** — that is the teacher's master.
   Do not commit, do not push, do not write `public/library.json`: the publisher
   lands the row and the deploy.
8. Stop and report. Wait for the teacher's verdict before Units 2–6.

## Traps that have already cost a rebuild

- PyMuPDF has no page-level arc — draw it as a polyline.
- A long heading or band label runs out of its box: shrink-then-trim, never
  overflow.
- Pictures must be cropped to their frame, not letterboxed.
- A footer reading *Prime School Press · English · Year 1* is **not** part of the
  standard: the running head is the band, the folio is the badge.
- The pack builder is incremental — a geometry change needs `--force`, and never
  run two pack builds for the same slug at once.
- Copy the PE book's **method**, never its words, cast or plates.
