#!/usr/bin/env python3
"""Remove duplicate "-input-corrected.xlsx" files from the Drive backup tree.

Rule (the workshop's): a Subject folder should hold ONE input file. Where
`<slug>-input.xlsx` and `<slug>-input-corrected.xlsx` both exist and are the SAME
bytes, the corrected copy is redundant and goes.

Safety:
  * duplicates are proven by Drive's own md5Checksum — no download, no guessing;
  * the corrected file is TRASHED (files.update trashed=true), never deleted
    permanently — Drive API v3 files.delete would be irreversible;
  * a corrected file with no plain twin is KEPT: for five books it is the only
    spreadsheet that exists (y01-art-and-design, y07-physical-education,
    y07-science, y08-science, y10-physical-education).

    /root/pb-gdrive-venv/bin/python tools/drive_dedupe_inputs.py            # dry run
    /root/pb-gdrive-venv/bin/python tools/drive_dedupe_inputs.py --apply
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

FOLDER_ID = "1wUPlk_dAFqo0qIK_NZVVjJIVJjplz0H2"
TOKEN = Path("/root/.hermes/google_token.json")
FOLDER_MIME = "application/vnd.google-apps.folder"


def auth():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not TOKEN.is_file():
        sys.exit("NOT_AUTHENTICATED: run tools/gdrive_auth.py first")
    return build(
        "drive",
        "v3",
        credentials=Credentials.from_authorized_user_file(
            str(TOKEN), ["https://www.googleapis.com/auth/drive"]
        ),
        cache_discovery=False,
    )


def kids(svc, parent: str) -> list[dict]:
    out, tok = [], None
    while True:
        r = (
            svc.files()
            .list(
                q=f"'{parent}' in parents and trashed = false",
                fields="nextPageToken, files(id,name,mimeType,size,md5Checksum)",
                pageSize=1000,
                pageToken=tok,
            )
            .execute()
        )
        out += r.get("files", [])
        tok = r.get("nextPageToken")
        if not tok:
            return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually trash them")
    ap.add_argument("--folder", default=FOLDER_ID)
    args = ap.parse_args()

    svc = auth()
    meta = svc.files().get(fileId=args.folder, fields="name").execute()
    print(f"folder: {meta['name']}   {'APPLY' if args.apply else 'DRY RUN'}\n")

    dupes, kept, ok_folders = [], [], 0
    for year in sorted((f for f in kids(svc, args.folder) if f["mimeType"] == FOLDER_MIME),
                       key=lambda f: f["name"]):
        for sub in sorted((f for f in kids(svc, year["id"]) if f["mimeType"] == FOLDER_MIME),
                          key=lambda f: f["name"]):
            files = [f for f in kids(svc, sub["id"]) if f["mimeType"] != FOLDER_MIME]
            plain = [f for f in files if f["name"].endswith("-input.xlsx")]
            corr = [f for f in files if f["name"].endswith("-input-corrected.xlsx")]
            if not corr:
                ok_folders += 1
                continue
            for c in corr:
                twin = next(
                    (p for p in plain
                     if p["name"] == c["name"].replace("-input-corrected.xlsx", "-input.xlsx")),
                    None,
                )
                if twin and twin.get("md5Checksum") and twin["md5Checksum"] == c.get("md5Checksum"):
                    dupes.append((year["name"], sub["name"], c, twin))
                else:
                    kept.append((year["name"], sub["name"], c))
                    ok_folders += 1

    print(f"duplicate corrected files (identical bytes to the plain input): {len(dupes)}")
    for y, s, c, t in dupes:
        print(f"  {y} / {s}\n      TRASH {c['name']}  ({int(c['size']):,} B) — same md5 as {t['name']}")
    print(f"\ncorrected files KEPT (no plain twin — the only spreadsheet): {len(kept)}")
    for y, s, c in kept:
        print(f"  {y} / {s}  ->  {c['name']}")

    if not args.apply:
        print("\nDRY RUN — nothing trashed. Re-run with --apply.")
        return 0

    done = 0
    for y, s, c, _t in dupes:
        # files.delete in Drive v3 is PERMANENT; trashed=true is the reversible one.
        svc.files().update(fileId=c["id"], body={"trashed": True}).execute()
        done += 1
    print(f"\ntrashed {done} duplicate file(s) — recoverable from Drive trash for 30 days")
    return 0


if __name__ == "__main__":
    sys.exit(main())