#!/usr/bin/env python3
"""Seed the `prime-books` Kanban board with one card per catalogue title.

One card per title, three shapes:

  * STANDARDISE  - the master PDF exists and fails the A-2.2 checker. The card
                   carries the book's own failure list and the checker command
                   as its acceptance evidence. Assigned to `standardiser`.
  * BUILD        - the master is under the standard's 35-page minimum viable
                   extent, i.e. a placeholder: the title has to be authored onto
                   the standard first. Same worker, different brief.
  * OUT OF SCOPE - Years 5-13 have no standard yet (A-2.2 covers Years 1-4), so
                   their cards are created BLOCKED with a per-title reason: what
                   has to be fixed before they can proceed. They are on the board
                   and in the open, never hidden in `todo`.

Idempotent: every card carries `--idempotency-key pb-<slug>-<lane>`, so re-running
after an interruption returns the existing card instead of duplicating it.

Usage
    .venv/bin/python tools/kanban_seed.py --dry-run
    .venv/bin/python tools/kanban_seed.py
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOARD = "prime-books"
WORKER = "standardiser"
WORKSPACE = f"dir:{REPO}"
SPEC = "A-2.2-Y1-4"
# The standard's minimum viable extent. Below it a "master" is a placeholder
# sample, not a book: it gets a BUILD card, never a STANDARDISE card. This must
# stay equal to tools/standards_bot.py MIN_PAGES - an 18-page sample that fell
# between the two thresholds was seeded as a book needing a restyle.
STUB_PAGES = 35

HOUSE_RULES = """
HOUSE RULES - non-negotiable
1. Never delete, move or reword the teacher's content. Restyle it onto the
   standard. Additions (headings, captions, instruction lines) are allowed and
   must be listed in your completion summary.
2. Keep the book's own unit count, unit order and page order, and keep an EVEN
   page count (StPageFlip shows the back cover alone only on an even count).
3. Touch only this slug's files (public/library/<slug>/). Do not run
   git commit or git push - the publisher commits centrally after review.
4. Do not write public/standardized.json. "Standardised" is the teacher's click
   on /status; machine-clean means ready for sign-off, nothing more.
5. If a fix needs a judgement you cannot make (content that is not there, an
   image to license, a QR to test, content that would have to be removed), call
   kanban_block with ONE precise question naming the page and the exact text.
6. VISIBLE CONFORMANCE. Clearing the checker is not the finish line. A pass that
   embeds fonts, pulls the folio out of the text layer into a badge, or inserts
   an English label beside a heading to trip a detector is a defect, not a pass -
   twelve books were reopened on 15 Sep for exactly that. Your pass must change
   what a teacher sees: the running-header band, the unit colour palette, the
   folio badge, the unit opener, drawn as the standard draws them. Render the
   pages you changed before and after and ATTACH the PNGs to this card
   (hermes kanban attach <task id> before.png after.png): a summary without
   attached renders is not accepted, and the publisher will not ship the book.
   If the book already looks like the standard and only invisible work remains,
   block the card saying "no visible work remains" and list the pages inspected.
7. Read the skills prime-books-standard (the specification) and
   prime-books-book-builder (the PDF craft) before editing a page.
""".strip()


def sh(args: list[str], dry: bool) -> dict | None:
    if dry:
        print("    " + " ".join(a if "\n" not in a else a.split("\n")[0] + " …" for a in args))
        return None
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout[-2000:])
        print(p.stderr[-2000:])
        raise SystemExit(f"kanban create failed for: {args[2:5]}")
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        print(p.stdout[-2000:])
        raise SystemExit("could not parse --json output")


def create(title: str, body: str, key: str, dry: bool, **flags) -> str | None:
    args = ["hermes", "kanban", "--board", BOARD, "create", title,
            "--body", body, "--idempotency-key", key, "--json"]
    for k, v in flags.items():
        if v is None or v is False:
            continue
        flag = "--" + k.replace("_", "-")
        if v is True:
            args.append(flag)
        elif isinstance(v, list):
            for item in v:
                args += [flag, str(item)]
        else:
            args += [flag, str(v)]
    out = sh(args, dry)
    return None if out is None else str(out.get("id") or out.get("task_id"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run

    library = json.loads((REPO / "public/library.json").read_text())
    report = json.loads((REPO / "public/standards-report.json").read_text())
    verdicts = {b["slug"]: b for b in report["books"]}
    inputs = {os.path.basename(p)[:-5].replace(" - input", "")
              for p in glob.glob(str(REPO / "public/inputs/*.json"))}
    input_glob = {p.split(" - input")[0].split("/")[-1]: p for p in
                  glob.glob(str(REPO / "public/inputs/* - input.*"))}

    in_scope, out_scope, stubs, clean = [], [], [], []
    for row in library:
        slug = row["slug"]
        v = verdicts.get(slug, {})
        if v.get("spec") != SPEC:
            out_scope.append(row)
        elif v.get("ok"):
            clean.append(row)
        elif row["pages"] <= STUB_PAGES:
            stubs.append(row)
        else:
            in_scope.append(row)
    # easy first: fewest failures, then fewest pages -> the queue proves itself early
    in_scope.sort(key=lambda r: (len(verdicts[r["slug"]].get("failures") or []), r["pages"]))

    print(f"plan: {len(in_scope)} standardise · {len(stubs)} build · "
          f"{len(out_scope)} out of scope · {len(clean)} already clean "
          f"= {len(in_scope) + len(stubs) + len(out_scope)} cards")
    if not dry:
        pass

    # ---------------------------------------------------------------- 1. work lane
    made = 0
    for row in in_scope:
        slug, v = row["slug"], verdicts[row["slug"]]
        fails = "\n".join(f"  - {f}" for f in v.get("failures") or []) or "  (none)"
        warns = "\n".join(f"  - {w}" for w in (v.get("warnings") or [])[:8]) or "  (none)"
        src = (f"public/inputs/{Path(input_glob[slug]).name}" if slug in input_glob
               else "NONE - the master PDF is the only source on disk")
        pages = row["pages"]
        runtime, turns = ("90m", 25) if pages <= 40 else (("150m", 30) if pages <= 120 else ("210m", 40))
        body = f"""STANDARDISE - {row['subject']}, Year {row['year']:02d}

Slug:            {slug}
Master:          public/library/{slug}/book.pdf  ({pages} pages)
Standard:        {SPEC} - public/standards/years-1-4.json, /standard/years-1-4
Input file:      {src}
Checker:         tools/standards_check.py

MACHINE VERDICT ({report['generated']}) - these FAILURES must all be cleared:
{fails}

Warnings (fix only where clearly in scope; report the rest):
{warns}

ACCEPTANCE - the card is done when this exact command exits 0 and prints
"ok": true, and you paste its output into your kanban_complete summary:
    cd {REPO} && .venv/bin/python tools/standards_check.py {slug}
State the before/after failure counts in the summary, and re-run the checker
after your LAST edit - not before it.

{HOUSE_RULES}
"""
        create(f"Standardise {row['subject']} - Year {row['year']:02d} ({slug})", body,
               f"pb-{slug}-standardise", dry,
               assignee=WORKER, workspace=WORKSPACE, goal=True, goal_max_turns=turns,
               skill=["prime-books-standard", "prime-books-book-builder"],
               max_runtime=runtime, max_retries=1,
               created_by="hermes:prime-books-seed")
        made += 1

    # ---------------------------------------------------------------- 2. build lane
    for row in stubs:
        slug = row["slug"]
        src = (f"public/inputs/{Path(input_glob[slug]).name}" if slug in input_glob
               else "NONE - ask the teacher for the source before authoring")
        body = f"""BUILD - {row['subject']}, Year {row['year']:02d}

Slug:            {slug}
Current master:  public/library/{slug}/book.pdf  ({row['pages']} pages - a stub, not a book)
Standard:        {SPEC} - public/standards/years-1-4.json, /standard/years-1-4
Input file:      {src}

This title has no real book yet. Author it ONTO the standard from the input file
and any teacher material in the repo.

ACCEPTANCE - done when these both hold and their output is pasted into your
kanban_complete summary:
    cd {REPO} && .venv/bin/python tools/standards_check.py {slug}      # "ok": true
The rebuilt master stays the same slug, lands at public/library/{slug}/book.pdf
with an EVEN page count, and cover.webp is regenerated if the cover changed.

WHAT NOT TO DO: do not invent teacher content to fill pages. If the input file
cannot fill a book on the standard (extent, unit count, subject material), call
kanban_block with a specific content request naming what is missing. A blocked
card with a sharp question is the correct outcome for a thin input.

{HOUSE_RULES}
"""
        create(f"Build {row['subject']} - Year {row['year']:02d} ({slug})", body,
               f"pb-{slug}-build", dry,
               assignee=WORKER, workspace=WORKSPACE, goal=True, goal_max_turns=40,
               skill=["prime-books-standard", "prime-books-book-builder"],
               max_runtime="210m", max_retries=1,
               created_by="hermes:prime-books-seed")
        made += 1

    # ----------------------------------- 3. the decision card + the blocked lane
    no_input = sorted(r["slug"] for r in library
                      if r["slug"] not in inputs and r["pages"] > STUB_PAGES)
    decision_body = f"""The human items that gate the whole board. Unblock this card when
they are settled.

1. STANDARD B (Years 5-13) - {len(out_scope)} titles fall outside the A-2.2 lock,
   which covers Years 1-4 only. Measuring them against A-2.2 produces ~70
   meaningless failures, which is why they show no verdict on /status. Settle the
   standard for secondary, then those {len(out_scope)} cards are re-briefed and
   queued in one pass.

2. MISSING SOURCES - {len(no_input)} titles have a master PDF but no input file.
   Those that do: {', '.join(no_input[:12])}{' …' if len(no_input) > 12 else ''}
   A master with no source cannot be re-authored, only restyled.

3. SIGN-OFF - {', '.join(r['slug'] for r in clean) or 'none'} is machine clean and
   waiting for your click on /status. Certification is human by design: the
   machine cannot see whether content was preserved, whether an image is
   licensed, or whether a QR scans on paper.
"""
    decision_id = create("Teacher decisions: Standard B (Years 5-13), missing inputs, sign-off",
                         decision_body, "pb-decisions", dry,
                         assignee=WORKER, workspace=WORKSPACE,
                         initial_status="blocked", max_retries=1,
                         created_by="hermes:prime-books-seed")
    print(f"decision card: {decision_id or '(dry)'}")

    # Out-of-scope titles: queued, then blocked with a per-title reason (the
    # teacher's policy - every title is on the board, nothing hides in `todo`,
    # and a title that cannot legitimately proceed says why). The dispatcher must
    # never spawn a worker on one of these: there is no standard to conform to,
    # and an agent with no standard either invents one or restyles a secondary
    # book onto a primary one.
    for row in out_scope:
        slug = row["slug"]
        src = (f"source on disk: public/inputs/{slug} - input.*" if slug in input_glob
               else "NO source file on disk - the master PDF is all there is")
        body = f"""BLOCKED: NO STANDARD YET - {row['subject']}, Year {row['year']:02d}

Slug:   {slug}
Master: public/library/{slug}/book.pdf ({row['pages']} pages)
Why:    A-2.2 is locked for Years 1-4 only and this is Year {row['year']:02d}, so
        there is nothing to conform to yet. Do NOT restyle this master against a
        primary standard and do NOT run tools/standards_check.py on it.
To fix: settle Standard B on the decision card, then this card is re-briefed and
        queued. Measured today: {row['pages']} pages, {src}.
"""
        create(f"Standardise {row['subject']} - Year {row['year']:02d} ({slug})", body,
               f"pb-{slug}-outofscope", dry,
               assignee=WORKER, workspace=WORKSPACE,
               initial_status="blocked", max_retries=1,
               created_by="hermes:prime-books-seed")
        made += 1

    print(f"{'would create' if dry else 'created'} {made} work cards "
          f"+ 1 decision card on board '{BOARD}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
