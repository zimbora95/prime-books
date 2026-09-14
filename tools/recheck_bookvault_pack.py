#!/usr/bin/env python3
"""Re-run the checks against a pack that is already built.

`validate()` is pure reading -- page geometry, fonts, transparency, ink -- so a
change to a CHECK never needs Ghostscript or a 300 DPI cover render again. This
re-validates the files on disk and rewrites build.json and the upload sheet with
the fresh rows, which is what the web page reads.

    .venv/bin/python tools/recheck_bookvault_pack.py y01-computing-and-robotics

It refuses to touch a pack whose binaries are missing: re-checking cannot create
a pack, and a record claiming checks for a file that is not there is worse than
no record.
"""
import json
import pathlib
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_bookvault_files as m  # noqa: E402


def main(slugs: list[str]) -> int:
    rc = 0
    for slug in slugs:
        od = m.out_dir(slug)
        bj = od / "build.json"
        if not bj.is_file():
            print(f"{slug}: no build.json -- build it first")
            rc = 1
            continue
        rec = json.loads(bj.read_text())
        text, cover = rec.get("text"), rec.get("cover")
        if not text or not cover:
            print(f"{slug}: record has no text/cover section")
            rc = 1
            continue
        missing = [p for p in (od / text["file"], od / cover["file"]) if not p.is_file()]
        if missing:
            print(f"{slug}: missing {', '.join(p.name for p in missing)} -- not re-checked")
            rc = 1
            continue

        checks = m.validate(slug, text, cover)
        sheet = m.write_spec_sheet(slug, text, cover, checks, m.settings_for(slug))
        rec["checks"] = checks
        rec["sheet"] = {"file": sheet.name, "url": f"/library/{slug}/bookvault/{sheet.name}"}
        rec["rechecked"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        rec["ok"] = all(c["pass"] for c in checks if c["level"] == "fail")
        bj.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        fails = [c["name"] for c in checks if not c["pass"] and c["level"] == "fail"]
        opens = [c["name"] for c in checks if not c["pass"] and c["level"] == "warn"]
        print(f"{slug}: {sum(1 for c in checks if c['pass'])} pass, {len(opens)} open"
              f"{', FAIL: ' + '; '.join(fails) if fails else ''}")
        if fails:
            rc = 1
    return rc


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    sys.exit(main(sys.argv[1:]))
