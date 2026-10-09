#!/usr/bin/env python3
"""Rewrite the secondary cards' briefs to match their new blocked state.

The bodies still said "while the parent is open this card stays in todo" - true
when they were seeded, false since the re-lane. Only the body column changes; the
lifecycle is untouched (no API writes an open card's body, hence the direct
UPDATE, with a comment left on every card by tools/kanban_secondary_triage.py).

    .venv/bin/python tools/kanban_fix_secondary_bodies.py [--dry-run]
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/lib/hermes-agent")
os.environ.setdefault("HERMES_KANBAN_BOARD", "prime-books")

from hermes_cli import kanban_db as kb                      # noqa: E402
from hermes_cli import kanban_db_connect as kbc             # noqa: E402

REPO = Path(__file__).resolve().parent.parent
BOARD = "prime-books"
TEMPLATE = """BLOCKED: NO STANDARD YET - {subject}, Year {year:02d}

Slug:   {slug}
Master: public/library/{slug}/book.pdf ({pages} pages)
Why:    A-2.2 is locked for Years 1-4 and this is Year {year:02d}, so there is
        nothing to conform to yet. Do not restyle this master against a primary
        standard, and do not run tools/standards_check.py on it.
To fix: settle Standard B on the teacher-decisions card (t_709ae0fe); this card
        is then re-briefed and queued. No other condition is missing.
"""


def main() -> int:
    dry = "--dry-run" in sys.argv
    library = {r["slug"]: r for r in json.loads((REPO / "public/library.json").read_text())}
    n = 0
    with kbc.connect_closing(board=BOARD) as conn:
        rows = conn.execute(
            "SELECT id, title FROM tasks WHERE title LIKE 'Out of scope:%' "
            "AND status NOT IN ('done','archived')").fetchall()
        for tid, title in rows:
            slug = title.split("(")[-1].rstrip(")")
            row = library.get(slug)
            if not row:
                print(f"  {tid}: no library row for {slug}")
                continue
            body = TEMPLATE.format(subject=row["subject"], year=row["year"],
                                   slug=slug, pages=row["pages"])
            if dry:
                n += 1
                continue
            with kb.write_txn(conn):
                conn.execute("UPDATE tasks SET body = ? WHERE id = ?", (body, tid))
            n += 1
    print(f"{'would rewrite' if dry else 'rewrote'} {n} card briefs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
