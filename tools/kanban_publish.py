#!/usr/bin/env python3
"""Publish the books whose kanban card is `done` (i.e. the gate proved them).

Workers never commit - that is deliberate, so no half-restyled master ever
reaches the live site. This is the other half: take every card in `done`, stage
only the two files the site serves (book.pdf, cover.webp), commit one book per
commit, and optionally push both branches the deploy expects.

`done` on the board means the machine gate passed. It does not mean the teacher
signed it off; the /status Standardised column stays theirs.

    .venv/bin/python tools/kanban_publish.py [--dry-run] [--push]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/lib/hermes-agent")
os.environ.setdefault("HERMES_KANBAN_BOARD", "prime-books")

from hermes_cli import kanban_db_connect as kbc                 # noqa: E402

REPO = Path("/root/prime-books")
BOARD = "prime-books"
BRANCHES = ("deploy-squash", "main")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)


def open_cards() -> dict[str, dict]:
    """slug -> what the board knows about that book's done card.

    Two conditions stop a book shipping even though its card says done:
      * its brief demands visual evidence (a RE-DO card, or any card briefed
        after the teacher's verdict) and no render has been attached;
      * a RE-DO comment is newer than the completion - i.e. the teacher sent it
        back after the pass that completed it.
    """
    out: dict[str, dict] = {}
    with kbc.connect_closing(board=BOARD) as conn:
        rows = conn.execute(
            "SELECT id, title, body, completed_at FROM tasks WHERE status = 'done'").fetchall()
        for tid, title, body, completed in rows:
            if not ("(" in title and title.rstrip().endswith(")")):
                continue
            slug = title.rstrip().rsplit("(", 1)[1].rstrip(")")
            if not (slug.startswith("y") and "-" in slug and "/" not in slug):
                continue
            attach = conn.execute(
                "SELECT COUNT(*) FROM task_attachments WHERE task_id = ?", (tid,)).fetchone()[0]
            redo = conn.execute(
                "SELECT MAX(created_at) FROM task_comments WHERE task_id = ? "
                "AND body LIKE 'RE-DO%'", (tid,)).fetchone()[0]
            out[slug] = {
                "tid": tid,
                "needs_evidence": "VISIBLE CONFORMANCE" in (body or ""),
                "attachments": attach,
                "completed_at": completed,
                "last_redo": redo,
            }
    return out


def _stamp(v) -> float:
    """created_at/completed_at are epoch ints in this schema; be forgiving."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    dry = "--dry-run" in sys.argv
    push = "--push" in sys.argv
    cards = open_cards()
    print(f"{len(cards)} book(s) with a done card: {', '.join(sorted(cards)) or 'none'}")
    if not cards:
        return 0
    if not dry:
        # Satisfy the pre-commit hook up front: it rejects a commit whose book's
        # markdown companion has drifted (md_sync --check), so sync first.
        sync = subprocess.run([str(REPO / ".venv/bin/python"), str(REPO / "tools/md_sync.py")],
                              cwd=REPO, capture_output=True, text=True)
        print("md_sync:", (sync.stdout or sync.stderr).strip().splitlines()[-1:] or "ok")

    committed = []
    for slug in sorted(cards):
        meta = cards[slug]
        # The teacher's two vetoes, checked before the gate so the reason printed
        # is the real one.
        if meta["needs_evidence"] and not meta["attachments"]:
            print(f"  {slug}: done, but no before/after render attached -> NOT published")
            continue
        if meta["last_redo"] and _stamp(meta["last_redo"]) >= _stamp(meta["completed_at"]):
            print(f"  {slug}: reopened after that pass (RE-DO newer than completion) -> NOT published")
            continue
        # The two files the site serves, plus the book's markdown companion - the
        # read-text view is generated from the PDF, so shipping the PDF without it
        # leaves stale text on the site.
        paths = [f"public/library/{slug}/book.pdf", f"public/library/{slug}/cover.webp",
                 f"public/markdown/{slug}.md"]
        if not dry:
            # Trust nothing: the board says done, but re-run the gate on the bytes
            # about to be published. A book that no longer passes is not shipped.
            verdict = Path("/tmp/pb_publish_verdict.json")
            subprocess.run([str(REPO / ".venv/bin/python"),
                            str(REPO / "tools/standards_check.py"), slug, "--json", str(verdict)],
                           cwd=REPO, capture_output=True, text=True)
            try:
                data = json.loads(verdict.read_text())
                rec = (data.get("books") if isinstance(data, dict) else data)[0]
            except Exception:
                print(f"  {slug}: gate unreadable -> skipped")
                continue
            if not rec.get("ok"):
                print(f"  {slug}: gate says NOT clean ({len(rec.get('failures') or [])} failures) -> skipped")
                continue
            git("add", "--", *paths)
            if not git("diff", "--cached", "--quiet", "--", *paths).returncode:
                print(f"  {slug}: no change on disk")
                continue
            spec = rec.get("spec") or "A-2.2-Y1-4"
            msg = f"Standardise {slug}: passes the {spec} gate (kanban {BOARD})"
            r = git("commit", "-m", msg, "--", *paths)
            if r.returncode != 0:
                print(f"  {slug}: commit failed -> {(r.stderr or r.stdout).strip()[:200]}")
                continue
        else:
            print(f"  {slug}: would commit book.pdf + cover.webp")
        committed.append(slug)

    print(f"{'would commit' if dry else 'committed'} {len(committed)}")
    if push and committed and not dry:
        for br in BRANCHES:
            r = git("push", "origin", f"HEAD:{br}")
            print(f"  push {br}: {'ok' if r.returncode == 0 else (r.stderr or r.stdout).strip()[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
