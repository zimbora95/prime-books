#!/usr/bin/env python3
"""Send a card back: comment the reason, then move it from Done to Ready.

The teacher's verdict outranks the gate. A book that passed the checker but looks
unchanged goes back in the queue with the reason recorded on the card, so the
worker's brief carries it into the next run.

    .venv/bin/python tools/kanban_redo.py <slug|all> --reason "not visibly different" [--dry-run]
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import time

sys.path.insert(0, "/usr/local/lib/hermes-agent")
os.environ.setdefault("HERMES_KANBAN_BOARD", "prime-books")

from hermes_cli import kanban_db as kb                      # noqa: E402
from hermes_cli import kanban_db_connect as kbc             # noqa: E402

BOARD = "prime-books"


def reopen(conn: sqlite3.Connection, tid: str, reason: str, dry: bool) -> tuple[bool, str]:
    row = conn.execute("SELECT status FROM tasks WHERE id = ?", (tid,)).fetchone()
    if row is None:
        return False, "no such card"
    if row[0] != "done":
        return False, f"card is {row[0]}, not done"
    if dry:
        return True, "would reopen"
    cols = {r[1] for r in conn.execute("PRAGMA table_info(tasks)")}
    sets = ["status = 'ready'", "claim_lock = NULL", "claim_expires = NULL", "worker_pid = NULL"]
    for c in ("current_run_id", "completed_at"):
        if c in cols:
            sets.append(f"{c} = NULL")
    if "consecutive_failures" in cols:
        sets.append("consecutive_failures = 0")
    cur = conn.execute(f"UPDATE tasks SET {', '.join(sets)} WHERE id = ? AND status = 'done'", (tid,))
    if cur.rowcount != 1:
        return False, "card changed underneath us"
    conn.execute(
        "INSERT INTO task_events (task_id, run_id, kind, payload, created_at) VALUES (?, NULL, 'status', ?, ?)",
        (tid, json.dumps({"status": "ready", "requested_status": "ready",
                          "reason": "teacher redo", "note": reason}), int(time.time())),
    )
    try:
        kb.invalidate_descendants_for_parent_reopen(conn, tid, author="redo")
    except Exception:
        pass                                    # no descendants: nothing to invalidate
    kb.recompute_ready(conn)
    conn.commit()
    return True, "reopened -> ready"


def main() -> int:
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    reason = ("not visibly different on inspection: say in your summary what a "
              "teacher would see changed")
    if "--reason" in argv:
        i = argv.index("--reason")
        reason = argv[i + 1] if i + 1 < len(argv) else reason
        del argv[i:i + 2]                       # never mistake words of the reason for slugs
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2

    with kbc.connect_closing(board=BOARD) as conn:
        if args == ["all"]:
            rows = conn.execute("SELECT id, title FROM tasks WHERE status = 'done'").fetchall()
        else:
            rows = []
            for slug in args:
                r = conn.execute(
                    "SELECT id, title FROM tasks WHERE title LIKE ? AND status = 'done'",
                    (f"%({slug})",),
                ).fetchall()
                if not r:
                    print(f"  {slug}: no done card on this board")
                rows += r
        print(f"{len(rows)} card(s) to send back")
        for tid, title in rows:
            comment = f"RE-DO: {reason}"
            if not dry:
                subprocess.run(["hermes", "kanban", "comment", "--author", "teacher", tid, comment],
                               capture_output=True, text=True)
            ok, msg = reopen(conn, tid, reason, dry)
            print(f"  {'ok  ' if ok else 'FAIL'} {tid} {title[:58]:58} {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())