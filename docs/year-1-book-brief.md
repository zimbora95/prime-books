# Year 1 Prime Book — the authoring brief every card follows

One card = one book. This is the brief that card is worked to, and the shape of
the finished thing is fixed by the reference edition below. Read it end to end
before you touch anything; it is short, and every line of it is a rule that has
already cost a rebuilt book.

## The reference edition

**Physical Education Year 1** — `public/library/y01-physical-education-standard/book.pdf`,
71 pages, built from nothing but the standard, the school's own programme and the
teacher's brief. It is machine-clean (`tools/standards_check.py`: 0 failures,
0 warnings) and it is the model for every Year 1 book on the shelf. Open it. Its
source tree is `work/y01-pe-book/` (`build_book.py` is the page-type engine,
`gen_art.py` the plate prompts, `content/*.json` the words, `identity.json` the
book's declared identity).

Copy its **method**, never its content: a new book has its own cast, its own
place, its own words and its own plates. Nothing is copied from another Prime
Book — not a sentence, not an animal, not a plate.

## The shape

| pages | what |
|---|---|
| 1–7 | front matter: cover, imprint, contents, welcome, how to use this book, what we use, safety/before-you-start |
| 8–… | the six units, nine pages each |
| …–(n-1) | back matter: the I-can record, the illustrated glossary (3 pp), what good looks like, sources, codes written out, every word of the year (2 pp), the page for the grown-up, the closing page |
| n | the back cover, its lower band kept clear for BookVault's production barcode |

A Year 1 book is **71 pages** (7 + 54 + 9 + 1) — a legal BookVault extent (12n − 1).
If your subject genuinely needs more, the next legal counts are 83 and 95; more
pages mean more units' worth of teaching, never padding.

## The page-type engine, not a template

Every page is one of the standard's page types, and the plan of the book is
audited before a single page is drawn:

- **E** opener (full-bleed in the unit's colour), hook
- **D** model, steps, wordbank, glossary, reference cards
- **R** response, check, reflect, portfolio
- **B** breath (one large picture, the unit's rest beat)
- **S** signature (the page in every unit where the child does the moving)

A unit's rhythm is a string of these weights. The audit refuses: the same page
type twice in a row, two dense pages in a row, three response pages in a row,
more than two of any type in a unit, a unit with fewer than four distinct page
types, and a unit without exactly one signature page and at least one breath
page. **No two spreads may read as the same spread with different words** — this
is the teacher's first rule for these books, and the audit exists to enforce it.

## The rules that have already been paid for

1. **No half-blank pages.** Every page's ink must reach the foot of the type area
   (y 726 pt). A page that stops two thirds of the way down reads as an unfinished
   print file and is a defect, not a matter of taste. `build_book.py` measures it
   and prints `half-blank pages (n)`; it must print `fill: every page reaches its foot`.
2. **Full-bleed unit openers** in the unit's own palette colour, to the trim on
   all four sides. The house gate fails a book with no full-bleed opener.
3. **The imprint on the last page** reads `P R I M E  S C H O O L  P R E S S`
   (letter-spaced); the gate matches that literal string.
4. **Text inside the box.** Nothing outside the safe area: x 42 → 570 pt,
   no text below y 725 (folio/badge zone) and none above y 12.
5. **The year ladder's size**, never smaller: Year 1 body text is 16 pt on 21 pt
   leading. If it does not fit, the page is designed again, not shrunk.
6. **Year 1 reading load**: 80 words a page at most, instructions of seven words
   or fewer, one idea a page.
7. **Fonts embedded, never embedded-by-reference**; plates at 300 DPI; plates are
   placed as JPEG (the same watercolour is 3.7 MB as PNG and 0.4 MB as JPEG — the
   interior is shipped over the web as well as printed).
8. **Evidence is part of the job.** Render the pages you changed before and after
   and attach them to the card: `hermes kanban attach <task id> before.png after.png`.
   A completion summary without attached renders is not accepted.

## The art

The illustration direction is locked in the standard
(`public/standards/years-1-4.json` → `illustration`): an original Beatrix Potter
direction — fine ink contours, transparent watercolour, warm muted pigments,
lightly textured cream paper. **Music & Drama Year 1 is the on-model book**: put a
new plate beside its plates before you place it, and regenerate until the light,
the pigments and the weight of the line match. Never photorealistic, never flat
vector, never a modern object, and **no lettering of any kind inside a picture**.

**Every plate is painted, and a photograph is a failure.** A Year 1 Prime Book has
no stock photography and no documentary photo spreads: a picture of a real object
is drawn in the house direction, like every other plate. A book that arrives with
studio photographs has not followed the standard, however good the photography is.

**Look at every plate before you place it**, one plate at a time, at full size. A
plate that fails the direction is generated again; it is never placed "for now".

Route plates through `tools/pb_image_gen.py` (model `openai/gpt-image-2.5-sunburst`,
medium quality) with prompts written per plate, not templated: each prompt names
the cast member, the object and the place. This book invents its own cast (named
animals, each with one trait, each of whom gets something wrong) and its own
place, and keeps them consistent across every plate.

## The gate

`tools/standards_check.py <slug>` must report **0 failures**. Warnings are for the
teacher to judge, not for the worker to ignore. Before you claim a book is done:

```
.venv/bin/python tools/standards_check.py <slug>          # 0 failures
.venv/bin/python tools/md_sync.py --check                 # ALL SYNCED
```

## Publishing — not yours

Workers **never commit, never push, never write `public/standardized.json`** and
never touch another book's folder: neighbours are working other books in the same
checkout. Publish the interior into `public/library/<slug>-standard/` — the title's
**standardised edition**, a folder of its own, with the same six files every
standardised edition has (`book.pdf`, `cover.webp`, `preview/01.webp`,
`preview/02.webp`, `preview/last.webp`, `bookvault/`).

**Never publish over a master.** `public/library/<year>-<subject>/` holds the
teacher's own placed book — the cover, the imprint page, the back cover and every
page of teaching that was put there by hand. Overwriting it replaces a master with
a worker's build and takes the book off the shelf as the teacher knows it. A
master is read, never written. If your slug's master folder changes on disk, you
have made a mistake: restore it with `git checkout HEAD -- public/library/<slug>/`
before anything else.

The standardised edition's slug is the master's slug with `-standard` appended, so
its reader URL is `/finished/book/<year>-<subject>-standard`. The publisher lands
the commit and the manifest row; you leave `public/library.json` alone.

## Evidence is not optional

Attach before/after renders to this card — `hermes kanban attach <task id>
before.png after.png` — and a contact sheet of all your pages. A completion summary
without attached renders is not accepted, and the publisher will not ship the book.
Claiming the machine checks pass is not evidence: run them and paste their output
into your card comment.

## When to stop and ask

If a fix needs a judgement you cannot make — content that is not there, an image
to license, a code to test, content that would have to be removed — call
`kanban_block` with **one** precise question naming the page and the exact text.
A block is a good outcome, not a failure.

## Languages

A book written in another language is written **wholly** in that language:
Portuguese is **português de Portugal** (never Brazilian), Spanish follows the
Cambridge Investigate variant, German is German. Variants are never guessed: if
the school's own sources do not settle a variant, block and ask.