#!/usr/bin/env python3
"""Seed the Year 1 board: one card per Prime Book to be built to the standard.

The teacher's brief: every Year 1 book rebuilt fresh to Standard A-2.3-Y1-4 in the
shape of the reference edition (Physical Education Year 1), two books in flight at
a time, and nothing copied from the shelf that exists - new words, new plates, new
cast, per book.

Titles with no inputs are left out on the teacher's instruction: German B1/B2,
Portuguese 1st Language, Spanish A1/A2, Spanish B1/B2 (their masters are 4-12 page
stubs, so there is nothing to teach from).

Every card carries its own subject, its own slug, its own master to inventory, and
the shared brief in docs/year-1-book-brief.md. Idempotency keys are per book, so
re-running this script cannot make a second card for a title.

    .venv/bin/python tools/kanban_seed_year1.py --dry-run
    .venv/bin/python tools/kanban_seed_year1.py
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = "prime-books"
BRIEF = "docs/year-1-book-brief.md"

BOOKS = [
    {
        "slug": "y01-art-and-design",
        "subject": "Art & Design",
        "band": "Cambridge Early Years",
        "identity": "colour, line, shape and making; looking closely at real things "
                    "before drawing them",
        "cast": "the book's own named cast and its own studio place: an invented "
                "workshop world where the making happens",
    },
    {
        "slug": "y01-computing-and-robotics",
        "subject": "Computing & Robotics",
        "band": "Cambridge Early Years",
        "identity": "instructions, sequence, cause and effect; a robot is a set of "
                    "steps in a body",
        "cast": "the book's own named cast and its own place: an invented workshop "
                "where a small machine is built step by step",
    },
    {
        "slug": "y01-english",
        "subject": "English",
        "band": "Cambridge Early Years",
        "identity": "sounds, letters, first words, listening and speaking, and the "
                    "pleasure of a story told aloud",
        "cast": "the book's own named cast and its own place: an invented village "
                "and its everyday doings",
    },
    {
        "slug": "y01-german-a1a2",
        "subject": "German A1/A2",
        "band": "Cambridge Early Years",
        "identity": "first words in German: greetings, naming, simple questions and "
                    "answers",
        "cast": "the book's own named cast and its own place, with the German written "
                "for a beginner: short sentences, high-frequency words, every new word "
                "pictured",
        "language": "deutsch",
    },
    {
        "slug": "y01-global-perspectives",
        "subject": "Global Perspectives",
        "band": "Cambridge Early Years",
        "identity": "me and my world: family, school, community, looking after what "
                    "we share",
        "cast": "the book's own named cast and its own place: an invented school and "
                "its neighbourhood",
    },
    {
        "slug": "y01-mathematics",
        "subject": "Mathematics",
        "band": "Cambridge Early Years",
        "identity": "counting, comparing, shapes, patterns, position and simple "
                    "measuring - always with something in the hand",
        "cast": "the book's own named cast and its own place: an invented market "
                "town where counting has a reason",
    },
    {
        "slug": "y01-music-and-drama",
        "subject": "Music & Drama",
        "band": "Cambridge Early Years",
        "identity": "pulse, rhythm, singing, moving to music, and pretending to be "
                    "someone else",
        "cast": "the book's own named cast and its own place, in the same Beatrix "
                "Potter direction this book already sets the model for",
        "note": "This book is the standard's on-model art reference. Its plates must "
                "stay the measure: a new book matches them, this one is never "
                "re-illustrated to match another.",
    },
    {
        "slug": "y01-science",
        "subject": "Science",
        "band": "Cambridge Early Years",
        "identity": "observing, sorting, naming living things, weather and materials, "
                    "and asking why",
        "cast": "the book's own named cast and its own place: an invented garden and "
                "the changing seasons in it",
    },
]

# the teacher's exclusions: no inputs exist for these
EXCLUDED = ["y01-german-b1b2", "y01-portuguese", "y01-spanish-a1a2", "y01-spanish-b1b2"]


def body(b, master_pages):
    lang = (
        "\n## Language\n\nThis book is **wholly in %s**. Not a bilingual edition, not "
        "captions in English: the unit names, the instructions, the questions, the "
        "glossary and the imprint all read in %s. Every new word is pictured, and the "
        "sentences stay inside Year 1 reading load (80 words a page, instructions of "
        "seven words or fewer).\n" % (b["language"], b["language"])
        if b.get("language") else ""
    )
    note = "\n## Note\n\n%s\n" % b["note"] if b.get("note") else ""
    return f"""Build the fresh standardised **{b['subject']} · Year 1** Prime Book.

**Slug:** `{b['slug']}`
**Standard:** A-2.3-Y1-4 — read `public/standards/years-1-4.json` before anything else.
**Brief:** `{BRIEF}` — read it end to end; it is the shape of the finished book and the
list of rules that have already cost a rebuilt book.
**Reference edition:** Physical Education Year 1,
`public/library/y01-physical-education-standard/book.pdf` (71 pp, machine-clean). Copy
its method, never its content.

## This book's identity

- **Subject:** {b['subject']} · {b['band']}
- **What it teaches:** {b['identity']}
- **Cast and place:** {b['cast']}

## The master to inventory first

`public/library/{b['slug']}/book.pdf` ({master_pages} pages). Inventorise **every**
page of it before you write a word — the teacher placed that teaching there and none
of it may be lost. You may re-set it into the standard's page types, and you must
not copy its words, its art or its order wholesale: the teacher asked for a fresh
book, so the teaching stays and the book is new.
{lang}{note}
## Deliverable

A 71-page interior built by `work/{b['slug']}-book/build_book.py` (start from the
reference edition's engine), with its own `identity.json`, its own per-unit
`content/*.json`, its own per-plate `gen_art.py`, and its own plates placed through
the plate cache (JPEG at print resolution).

It is published as the **standardised edition**: `public/library/{b['slug']}-standard/`
— a folder of its own, never over the master at `public/library/{b['slug']}/`, which
is the teacher's own placed book and is read, never written. The reader URL is
`/finished/book/{b['slug']}-standard`.

Then, evidence first:

1. `.venv/bin/python tools/standards_check.py {b['slug']}-standard` → **0 failures**,
   with the output pasted into a card comment.
2. The builder's own fill report → `fill: every page reaches its foot and its right
   edge` (no half-blank pages, no page filled down one column only).
3. A contact sheet of all 71 pages **attached to this card** and looked at: every
   plate painted in the house direction (no photography), no page broken, no
   missing plate.
4. `hermes kanban attach <task id> contact-sheet.png` plus before/after renders of
   the pages you changed.
5. Leave `public/library.json` alone — the publisher adds the manifest row.

If something needs a judgement you cannot make, block this card with one precise
question naming the page and the exact text."""


def main():
    dry = "--dry-run" in sys.argv
    rows = json.load(open(os.path.join(REPO, "public", "library.json")))
    by_slug = {r["slug"]: r for r in rows}
    for slug in EXCLUDED:
        if slug in by_slug:
            print(f"excluded on the teacher's instruction: {slug}")
    made = []
    for b in BOOKS:
        row = by_slug.get(b["slug"])
        if not row:
            print(f"  ! no manifest row for {b['slug']} - skipped")
            continue
        if "--dry-run" in sys.argv:
            print(f"would create: {b['subject']} · Year 1  ({b['slug']}, "
                  f"master {row.get('pages')} pp)")
            continue
        cmd = [
            "hermes", "kanban", "--board", BOARD, "create",
            f"{b['subject']} · Year 1 — the fresh standard edition",
            "--body", body(b, row.get("pages")),
            "--assignee", "default",
            # the worker works in the real checkout: its book belongs under
            # work/<slug>-book/ and public/library/<slug>/, and a scratch workspace
            # is deleted when the task completes
            "--workspace", f"dir:{REPO}",
            "--skill", "prime-books-standard",
            "--skill", "prime-books-book-builder",
            "--idempotency-key", f"y1-fresh-{b['slug']}",
            "--created-by", "year-1-seed",
            "--json",
        ]
        out = subprocess.run(cmd, capture_output=True, text=True)
        if out.returncode != 0:
            print(f"  ! {b['slug']}: {out.stderr.strip()[:200]}")
            continue
        try:
            made.append(json.loads(out.stdout))
        except Exception:
            made.append({"raw": out.stdout.strip()})
        print(f"created: {b['subject']} · Year 1 ({b['slug']})")
    if made and not dry:
        print(json.dumps(made, indent=1)[:1200])
    print(f"{len(made)} card(s) on {BOARD}; dispatch with --max 2 for two books at a time")


if __name__ == "__main__":
    main()