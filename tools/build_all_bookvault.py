#!/usr/bin/env python3
"""Build every book's BookVault pack ahead of time, so the page never waits.

Why: entering /book/<slug>/bookvault with no pack (or a stale one) makes the page
call the build endpoint and sit on "Building..." for a minute or two -- and for a
long book much longer. The record, the two files and the checks are all read from
library/<slug>/bookvault/ afterwards, so if the pack is already on disk the page
is instant.

This walks the library and calls the builder once per book. It is resumable: the
builder reuses a pack that is newer than its master, so a re-run costs a few
seconds per book and only rebuilds what is missing or out of date.

    .venv/bin/python tools/build_all_bookvault.py               # every book
    .venv/bin/python tools/build_all_bookvault.py --shard 1/2   # half of them
    .venv/bin/python tools/build_all_bookvault.py --only y01-mathematics

Two shards run in parallel in about half the time on a 2-core host; the packs are
derived files, so they are git-ignored and .vercelignore'd -- the live server
serves them, Vercel does not need them.

Status lands in $PB_VAULT_STATUS (default /root/pbwork-vault/build_all_status.json)
and $PB_VAULT_LOG (default /root/pbwork-vault/build_all.log).
"""
import argparse
import json
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
LIBRARY = REPO / "public/library"
PY = REPO / ".venv/bin/python"
SCRIPT = REPO / "tools/make_bookvault_files.py"

# A master with fewer pages than this cannot yield a printable interior (the front
# and back covers come out of it), so it is reported and skipped rather than built.
MIN_MASTER_PAGES = 14
TIMEOUT_S = 2700          # a 750-page master plus its 300 DPI cover render


def pack_files(slug: str) -> tuple[pathlib.Path, pathlib.Path]:
    d = LIBRARY / slug / "bookvault"
    return (d / f"{slug}-text-file.pdf", d / f"{slug}-cover-file.pdf")


def pack_complete(slug: str) -> bool:
    """Both deliverables present, start with a PDF header, and current.

    A book is only 'already built' when the interior AND the cover file are both
    on disk: a half-built pack (the record from a run whose cover render died, or
    a stray directory) would otherwise be left alone and the page would serve a
    missing download.

    Both files must also be NEWER than the builder script. A pack built by an
    earlier version of the builder carries that version's page geometry, and the
    live server only rebuilds when the MASTER changes -- so a stale pack would
    otherwise survive untouched and be served as if it were current.
    """
    text, cover = pack_files(slug)
    for f in (text, cover, LIBRARY / slug / "bookvault" / "build.json"):
        if not f.is_file():
            return False
    built_after = SCRIPT.stat().st_mtime
    for f in (text, cover):
        if f.stat().st_size < 20_000:
            return False
        if f.stat().st_mtime < built_after:
            return False
        with f.open("rb") as fh:
            if fh.read(5) != b"%PDF-":
                return False
    return True


def slugs() -> list[str]:
    out = []
    for d in sorted(LIBRARY.iterdir()):
        if (d / "book.pdf").is_file():
            out.append(d.name)
    return out


def master_pages(path: pathlib.Path) -> int:
    try:
        import pymupdf
        return pymupdf.open(path).page_count
    except Exception:
        return -1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--shard", default=None, help="i/N, e.g. 1/2")
    ap.add_argument("--force", action="store_true",
                    help="rebuild even a pack that is already up to date")
    a = ap.parse_args()

    status_path = pathlib.Path(
        __import__("os").environ.get("PB_VAULT_STATUS",
                                     "/root/pbwork-vault/build_all_status.json"))
    log_path = pathlib.Path(
        __import__("os").environ.get("PB_VAULT_LOG", "/root/pbwork-vault/build_all.log"))
    status_path.parent.mkdir(parents=True, exist_ok=True)

    todo = a.only if a.only else slugs()
    if a.shard:
        i, n = (int(x) for x in a.shard.split("/"))
        todo = [s for k, s in enumerate(todo) if k % n == i - 1]

    state = json.loads(status_path.read_text()) if status_path.is_file() else {}
    state.setdefault("started", time.strftime("%Y-%m-%d %H:%M:%S"))
    state.setdefault("books", {})
    try:
        settings = json.loads((REPO / "public/bookvault.json").read_text())
    except Exception:
        settings = {}
    log = log_path.open("a")

    def say(line: str) -> None:
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    say(f"=== {time.strftime('%H:%M:%S')} run: {len(todo)} books "
        f"(shard {a.shard or 'all'})")

    built = skipped = failed = 0
    for k, slug in enumerate(todo, 1):
        t0 = time.time()
        pages = master_pages(LIBRARY / slug / "book.pdf")
        if pages < MIN_MASTER_PAGES:
            skipped += 1
            say(f"[{k}/{len(todo)}] {slug}: SKIP, master is {pages} pages "
                f"(needs {MIN_MASTER_PAGES} to yield a printable interior)")
            state["books"][slug] = {"state": "skip", "master_pages": pages}
            status_path.write_text(json.dumps(state, indent=1))
            continue
        cmd = [str(PY), str(SCRIPT), slug]
        # The spine width is BookVault's sizing-calculator figure saved with this
        # book's specifications; the cover geometry depends on it, so pass it
        # through exactly as the build server does rather than letting the
        # per-page estimate decide.
        saved = settings.get(slug) or {}
        if isinstance(saved, dict) and saved.get("spineMm"):
            cmd += ["--spine-mm", str(saved["spineMm"])]
        # Force unless both deliverables are already on disk: the builder's reuse
        # path trusts build.json, and a pack with a record but no cover file (or
        # the other way round) would be served as a broken download.
        if a.force or not pack_complete(slug):
            cmd.append("--force")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=TIMEOUT_S, cwd=str(REPO))
        except subprocess.TimeoutExpired:
            failed += 1
            say(f"[{k}/{len(todo)}] {slug}: FAIL, timed out after {TIMEOUT_S}s")
            state["books"][slug] = {"state": "fail", "error": "timeout"}
            status_path.write_text(json.dumps(state, indent=1))
            continue
        took = time.time() - t0
        line = (r.stdout or "").strip().splitlines()
        line = line[-1] if line else ""
        ok = r.returncode == 0
        fails = "FAIL:" in line
        both = pack_complete(slug)
        if ok and not fails and not both:
            fails = True
            line += " (a file is missing: text/cover pack incomplete)"
        if ok and not fails:
            built += 1
        else:
            failed += 1
        say(f"[{k}/{len(todo)}] {slug}: {took/60:.1f} min {'OK' if ok and not fails else 'PROBLEM'} "
            f"| {line[:200]}")
        if not ok:
            say(f"      stderr: {(r.stderr or '')[-300:]}")
        state["books"][slug] = {"state": "ok" if ok and not fails else "problem",
                                "minutes": round(took / 60, 1),
                                "line": line[:300],
                                "when": time.strftime("%Y-%m-%d %H:%M:%S")}
        status_path.write_text(json.dumps(state, indent=1))

    state["finished_%s" % (a.shard or "all")] = time.strftime("%Y-%m-%d %H:%M:%S")
    status_path.write_text(json.dumps(state, indent=1))
    say(f"=== {time.strftime('%H:%M:%S')} done: {built} built/up to date, "
        f"{skipped} skipped, {failed} with a problem")
    # a non-zero exit only when something actually went wrong, so a notify says so
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
