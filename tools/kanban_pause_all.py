#!/usr/bin/env python3
"""Freeze the board and hand the lane to the default profile.

The teacher's call (15 Sep, second direction): the standardiser lane is paused
while ONE new standardised book is built as a pilot. The dispatcher only claims
'ready' cards, so every open card is blocked - a config flag alone did not stop
it, and demoting to 'todo' would be undone by recompute_ready().

    /usr/local/lib/hermes-agent/venv/bin/python tools/kanban_pause_all.py [--dry-run]
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, "/usr/local/lib/hermes-agent")
os.environ.setdefault("HERMES_KANBAN_BOARD", "prime-books")

from hermes_cli import kanban_db as kb                      # noqa: E402
from hermes_cli import kanban_db_connect as kbc             # noqa: E402

BOARD = "prime-books"
TARGET_PROFILE = "default"
REASON = ("PAUSED by the teacher (15 Sep): the standardisation lane is frozen while one "
          "NEW standardised book is built as a pilot (Physical Education, Year 01). "
          "Nothing in this lane runs until the pilot is approved. Unblocking this card "
          "puts it back in the queue.")


def main() -> int:
    dry = "--dry-run" in sys.argv
    with kbc.connect_closing(board=BOARD) as conn:
        rows = conn.execute(
            "SELECT id, title, status, assignee FROM tasks "
            "WHERE status IN ('ready', 'todo', 'running') ORDER BY status, title").fetchall()
        print(f"{len(rows)} open card(s) to freeze")
        for tid, title, status, assignee in rows:
            if dry:
                print(f"  would block {tid} {status:8} {title[:56]}")
                continue
            ok = kb.block_task(conn, tid, reason=REASON, kind="transient")
            print(f"  {'blocked' if ok else 'FAILED '} {tid} {status:8} {title[:56]}")
        if not dry:
            try:
                conn.commit()
            except Exception:
                pass
        moved = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE assignee IS NULL OR assignee != ?",
            (TARGET_PROFILE,)).fetchone()[0]
        print(f"{moved} card(s) still assigned to another profile")
        if not dry and moved:
            with kb.write_txn(conn):
                conn.execute("UPDATE tasks SET assignee = ? WHERE assignee IS NULL OR assignee != ?",
                             (TARGET_PROFILE, TARGET_PROFILE))
            print(f"reassigned {moved} card(s) -> {TARGET_PROFILE}")
    if not dry:
        # Workers already in flight do not see the block; end them.
        out = subprocess.run(["bash", "-c",
                              "ps -eo pid,args | grep '[w]ork kanban task' | awk '{print $1}'"],
                             capture_output=True, text=True).stdout.split()
        for pid in out:
            subprocess.run(["kill", "-TERM", pid], capture_output=True)
        print(f"terminated {len(out)} in-flight worker(s): {' '.join(out) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())