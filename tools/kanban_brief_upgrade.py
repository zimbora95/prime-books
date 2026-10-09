#!/usr/bin/env python3
"""Append the visible-conformance requirement to every open card's brief.

Twelve books were reopened on 15 Sep because they cleared every machine check
without the teacher seeing a single difference. The requirement is now part of
the brief, not just of a RE-DO comment, so it applies to the whole queue.

    /usr/local/lib/hermes-agent/venv/bin/python tools/kanban_brief_upgrade.py [--dry-run]
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, "/usr/local/lib/hermes-agent")
os.environ.setdefault("HERMES_KANBAN_BOARD", "prime-books")

from hermes_cli import kanban_db as kb                      # noqa: E402
from hermes_cli import kanban_db_connect as kbc             # noqa: E402

BOARD = "prime-books"
MARKER = "VISIBLE CONFORMANCE"
SECTION = """

VISIBLE CONFORMANCE - required, added after the teacher's verdict of 15 Sep:

Passing the checker is NOT the finish line. Twelve books were sent back because
every machine check was cleared without the teacher being able to see a single
difference: fonts embedded, the folio pulled out of the text layer into a badge,
and the English word "CONTENTS" inserted beside the Portuguese "Indice" to trip
the contents detector. That is a defect, not a pass.

Your pass must change what a teacher sees on the page: the running-header band,
the unit colour palette, the folio badge, the unit opener - drawn as the
standard draws them.

Evidence is part of the job: render the pages you changed before and after and
attach the PNGs to this card

    hermes kanban attach <this task id> before-p008.png after-p008.png

A completion summary without attached renders is not accepted.

If the book already looks like the standard and only invisible work remained,
do not invent a restyle: block the card saying exactly that - "no visible work
remains" - listing the pages you inspected.
"""


def main() -> int:
    dry = "--dry-run" in sys.argv
    with kbc.connect_closing(board=BOARD) as conn:
        rows = conn.execute(
            "SELECT id, title, body FROM tasks "
            "WHERE status IN ('ready','running','blocked') "
            "AND title LIKE 'Standardise %' ORDER BY title").fetchall()
        done = 0
        for tid, title, body in rows:
            body = body or ""
            if MARKER in body:
                continue
            if dry:
                print(f"  would upgrade {tid} {title[:60]}")
                done += 1
                continue
            with kb.write_txn(conn):
                conn.execute("UPDATE tasks SET body = ? WHERE id = ?", (body.rstrip() + SECTION, tid))
            done += 1
        print(f"{'would upgrade' if dry else 'upgraded'} {done} card(s) of {len(rows)} open Standardise cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())