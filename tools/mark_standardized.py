#!/usr/bin/env python3
"""Sign books off as standardised, or take the sign-off back.

    .venv/bin/python tools/mark_standardized.py y01-art-and-design
    .venv/bin/python tools/mark_standardized.py y07-science y08-science --undo
    .venv/bin/python tools/mark_standardized.py --list

Writes public/standardized.json (the flag store behind the /status page's
"Standardised" column) and regenerates public/status.json in the same breath, so
the page and the file can never disagree.

The flag is a HUMAN sign-off - it is never inferred from an input file existing.
Run tools/audit_standard.py first; commit and push the flag store to make the
sign-off visible on the deployed site as well as the workshop box.
"""
import argparse
import json
import os
import subprocess
import sys

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PUB = REPO / "public"
STORE = PUB / "standardized.json"
GEN = REPO / "tools" / "make_status_json.py"


def load() -> dict:
    try:
        raw = json.loads(STORE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return raw if isinstance(raw, dict) else {}


def save(data: dict) -> None:
    tmp = str(STORE) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, STORE)


def slugs() -> set:
    lib = json.loads((PUB / "library.json").read_text(encoding="utf-8"))
    return {b["slug"] for b in lib}


def regenerate() -> None:
    """Keep the generated page data in step with the flag store."""
    py = REPO / ".venv" / "bin" / "python"
    exe = str(py) if py.exists() else sys.executable
    subprocess.run([exe, str(GEN)], cwd=str(REPO), check=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("books", nargs="*", help="book slugs")
    ap.add_argument("--undo", action="store_true", help="remove the sign-off")
    ap.add_argument("--list", action="store_true", help="show who is signed off")
    args = ap.parse_args()

    data = load()

    if args.list or not args.books:
        if data:
            print(f"{len(data)} standardised:")
            for s in sorted(data):
                print("  ", s)
        else:
            print("no title is standardised yet")
        return 0

    known = slugs()
    unknown = [s for s in args.books if s not in known]
    if unknown:
        print("unknown slug(s), nothing written:", ", ".join(unknown))
        return 2

    for s in args.books:
        if args.undo:
            data.pop(s, None)
        else:
            data[s] = True
    save(data)
    regenerate()

    print(f"{'undone' if args.undo else 'standardised'}: {', '.join(args.books)}")
    print(f"flag store now holds {len(data)} sign-off(s)")
    if not args.undo:
        print("commit + push public/standardized.json to show this on the live site")
    return 0


if __name__ == "__main__":
    sys.exit(main())
