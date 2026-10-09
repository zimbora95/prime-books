#!/usr/bin/env python3
"""Re-cut the BookVault WRAP (the "Cover file") of every pack that is out of date.

Why this exists: the walk in tools/build_all_bookvault.py reuses a pack whenever
both files are newer than the master, and the builder's reuse path trusts
build.json. So a pack survives a change that does not touch the master's mtime
or page count - and the wrap's spine colour is exactly that kind of change: it
used to be taken from the YEAR LADDER, which is the primary series rule but
wrong for the secondary books, whose covers carry a subject/level stripe (Y7
teal, Y8 slate, Y9 ochre, Y10 burgundy, Y11 forest, Y12-13 navy). The Year 7
Humanities wrap shipped a gold spine against a teal book.

A wrap is rebuilt here when either
  * its cover file is older than the master it is cut from (the back page was
    edited - e.g. a back-cover standardisation), or
  * the spine colour recorded in build.json is not the book's own stripe colour
    (a pack built before the colour was taken from the book records none).

Cover-only: the interior pack is untouched, and the spine width comes from
public/bookvault.json exactly as the build server passes it.

    .venv/bin/python tools/sweep_bookvault_wraps.py --list      # what is stale
    .venv/bin/python tools/sweep_bookvault_wraps.py --shard 1/2 # rebuild half
    .venv/bin/python tools/sweep_bookvault_wraps.py y07-humanities

Status: $PB_WRAP_STATUS (default /root/pbwork-vault/wrap_sweep_status.json).
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
LIBRARY = REPO / "public/library"
PY = REPO / ".venv/bin/python"
SCRIPT = REPO / "tools" / "make_bookvault_files.py"

sys.path.insert(0, str(REPO / "tools"))
import make_wrap_cover as mwc          # noqa: E402


def packs() -> list[str]:
    out = []
    for d in sorted(LIBRARY.iterdir()):
        bv = d / "bookvault"
        if (d / "book.pdf").is_file() and (bv / f"{d.name}-cover-file.pdf").is_file():
            out.append(d.name)
    return out


def spine_mm(slug: str, settings: dict):
    saved = settings.get(slug) or {}
    if isinstance(saved, dict) and saved.get("spineMm"):
        return str(saved["spineMm"])
    return None


def stale_reason(slug: str) -> str | None:
    d = LIBRARY / slug
    master, cover = d / "book.pdf", d / "bookvault" / f"{slug}-cover-file.pdf"
    rec = d / "bookvault" / "build.json"
    try:
        row = next(r for r in json.loads((REPO / "public/library.json").read_text())
                   if r["slug"] == slug)
    except StopIteration:
        return "not in library.json"
    own = mwc.book_stripe_colour(master)
    recorded = None
    if rec.is_file():
        try:
            recorded = json.loads(rec.read_text()).get("cover", {}).get("spine_colour")
        except Exception:
            recorded = None
    if own and recorded != list(own):
        return f"spine {recorded or 'year-ladder'} != book stripe {own}"
    if cover.stat().st_mtime < master.stat().st_mtime:
        return "cover file older than the master"
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--list", action="store_true", help="report and build nothing")
    ap.add_argument("--shard", default=None, help="i/N")
    ap.add_argument("--force", action="store_true", help="rebuild every pack")
    a = ap.parse_args()

    status_path = pathlib.Path(os.environ.get(
        "PB_WRAP_STATUS", "/root/pbwork-vault/wrap_sweep_status.json"))
    status_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        settings = json.loads((REPO / "public/bookvault.json").read_text())
    except Exception:
        settings = {}

    todo = a.slugs or packs()
    todo = [(s, "forced" if a.force else stale_reason(s)) for s in todo]
    todo = [(s, why) for s, why in todo if why]
    if a.shard:
        i, n = (int(x) for x in a.shard.split("/"))
        todo = [t for k, t in enumerate(todo) if k % n == i - 1]

    state = json.loads(status_path.read_text()) if status_path.is_file() else {"books": {}}
    print(f"wraps to rebuild: {len(todo)} (shard {a.shard or 'all'})", flush=True)
    for slug, why in todo:
        print(f"  {slug:34s} {why}", flush=True)
    if a.list:
        return

    ok = fail = 0
    for k, (slug, why) in enumerate(todo, 1):
        t0 = time.time()
        cmd = [str(PY), str(SCRIPT), "--cover-only", slug]
        mm = spine_mm(slug, settings)
        if mm:
            cmd += ["--spine-mm", mm]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO), timeout=3600)
        line = (r.stdout or "").strip().splitlines()
        line = line[-1] if line else ""
        good = r.returncode == 0 and "FAIL:" not in line
        ok, fail = (ok + 1, fail) if good else (ok, fail + 1)
        print(f"[{k}/{len(todo)}] {slug}: {good and 'OK' or 'PROBLEM'} "
              f"{(time.time() - t0) / 60:.1f} min | {line[:160]}", flush=True)
        state["books"][slug] = {"state": "ok" if good else "problem",
                                "why": why, "minutes": round((time.time() - t0) / 60, 1),
                                "line": line[:300],
                                "when": time.strftime("%Y-%m-%d %H:%M:%S")}
        status_path.write_text(json.dumps(state, indent=1))
    state["finished_%s" % (a.shard or "all")] = time.strftime("%Y-%m-%d %H:%M:%S")
    status_path.write_text(json.dumps(state, indent=1))
    print(f"=== done: {ok} rebuilt, {fail} with a problem", flush=True)
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()