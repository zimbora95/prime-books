#!/usr/bin/env python3
"""Re-lane the Years 5-13 cards onto the teacher's policy.

Every catalogue title has a card, nothing hides in `todo`, and a title that
cannot legitimately proceed goes to `blocked` with a reason the teacher can act
on. Years 5-13 cannot proceed because the locked standard (A-2.2) is Years 1-4
only: their cards are unlinked from the decision card, queued (promote), then
blocked `needs_input` with the reason. Idempotent.

    .venv/bin/python tools/kanban_secondary_triage.py [--dry-run]
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, "/usr/local/lib/hermes-agent")
os.environ.setdefault("HERMES_KANBAN_BOARD", "prime-books")

from hermes_cli import kanban_db as kb                      # noqa: E402
from hermes_cli import kanban_db_connect as kbc             # noqa: E402

BOARD = "prime-books"
DECISION = "t_709ae0fe"
AUTHOR = "hermes:prime-books-seed"
REASON = (
    "NO STANDARD YET: A-2.2 is locked for Years 1-4 only, so this secondary title "
    "has nothing to conform to. Do not restyle the master against a primary "
    "standard. To fix: settle Standard B on the teacher-decisions card, then this "
    "card is re-briefed and queued."
)
SEE = ("NO STANDARD YET - A-2.2 covers Years 1-4 and this title is outside that "
       "scope. The card body carries its slug, its measured page count and whether "
       "a source file exists on disk. Settle Standard B (teacher-decisions card) "
       "and this whole lane is re-briefed and queued in one pass.")


def main() -> int:
    dry = "--dry-run" in sys.argv
    done = 0
    with kbc.connect_closing(board=BOARD) as conn:
        rows = conn.execute(
            "SELECT id, title FROM tasks WHERE title LIKE 'Out of scope:%' "
            "AND status NOT IN ('done','archived') ORDER BY id").fetchall()
        print(f"{len(rows)} secondary cards")
        for tid, title in rows:
            slug = title.split("(")[-1].rstrip(")")
            if dry:
                print(f"  {tid} {slug}: unlink, promote, block")
                done += 1
                continue
            for parent in kb.parent_ids(conn, tid):
                kb.unlink_tasks(conn, parent, tid)
            ok, why = kb.promote_task(conn, tid, actor=AUTHOR, reason="queued on the teacher's policy")
            if not ok and "ready" not in (why or ""):
                print(f"  {tid} promote: {why}")
            kb.block_task(conn, tid, reason=REASON, kind="needs_input")
            kb.add_comment(conn, tid, AUTHOR, SEE)
            done += 1
        counts = dict(conn.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status"))
    print(f"{'would re-lane' if dry else 're-laned'} {done}")
    print("board:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) if not dry else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
