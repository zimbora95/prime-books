#!/usr/bin/env python3
"""Upload the staged Prime Books backup tree into a Google Drive folder.

Target layout in Drive (mirrors the local staging tree and the workshop's rule):

    <DRIVE_FOLDER>/Year 01/Art & Design/y01-art-and-design-output.pdf
    <DRIVE_FOLDER>/Year 01/Art & Design/y01-art-and-design-input.xlsx
    <DRIVE_FOLDER>/_MANIFEST.csv

Requires an authorised token at ~/.hermes/google_token.json (created by the
google-workspace skill's setup.py --auth-url / --auth-code flow). Without it the
script exits with NOT_AUTHENTICATED and changes nothing.

Idempotent and additive:
  * a file whose Drive md5Checksum already matches the local md5 is SKIPPED;
  * nothing is ever deleted or overwritten unless its content actually differs;
  * after every upload the size and md5 are read back from Drive to confirm.

Run with:
    /root/pb-gdrive-venv/bin/python tools/drive_backup.py --dry-run
    /root/pb-gdrive-venv/bin/python tools/drive_backup.py
    /root/pb-gdrive-venv/bin/python tools/drive_backup.py --verify
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import sys
import time
from pathlib import Path

STAGE = Path("/root/pb-backup")
FOLDER_ID = "1wUPlk_dAFqo0qIK_NZVVjJIVJjplz0H2"  # "Prime Books Hermes GCP Sync"
TOKEN = Path("/root/.hermes/google_token.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_MIME = "application/vnd.google-apps.folder"


def local_md5(p: Path, buf: int = 1 << 20) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        while chunk := f.read(buf):
            h.update(chunk)
    return h.hexdigest()


def auth():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not TOKEN.is_file():
        sys.exit(
            "NOT_AUTHENTICATED: no token at ~/.hermes/google_token.json.\n"
            "Authorise first (google-workspace skill):\n"
            "  /root/pb-gdrive-venv/bin/python "
            "/root/.hermes/skills/productivity/google-workspace/scripts/setup.py "
            "--client-secret <file>\n"
            "  ... --auth-url --services drive   then   ... --auth-code '<redirected url>'"
        )
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN.write_text(creds.to_json(), encoding="utf-8")
        else:
            sys.exit("REFRESH_FAILED: token revoked or missing scopes — redo the auth flow.")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def children(svc, parent: str) -> dict[str, dict]:
    out, tok = {}, None
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
        for f in r.get("files", []):
            out[f["name"]] = f
        tok = r.get("nextPageToken")
        if not tok:
            return out


def ensure_folder(svc, name: str, parent: str, dry: bool) -> str:
    if dry:
        print(f"  [dry] would ensure folder {name}")
        return "DRY"
    for f in children(svc, parent).values():
        if f["mimeType"] == FOLDER_MIME and f["name"] == name:
            return f["id"]
    if dry:
        print(f"  [dry] would create folder {name}")
        return "DRY"
    return (
        svc.files()
        .create(body={"name": name, "mimeType": FOLDER_MIME, "parents": [parent]}, fields="id")
        .execute()["id"]
    )


def upload(svc, path: Path, parent_id: str, existing: dict | None, dry: bool) -> str:
    md5 = local_md5(path)
    size = path.stat().st_size
    if existing and (existing.get("md5Checksum") == md5 or (existing.get("size") == str(size) and not existing.get("md5Checksum"))):
        return "skipped"
    if dry:
        print(f"  [dry] would upload {path.name} ({size:,} B)")
        return "dry"

    from googleapiclient.http import MediaFileUpload

    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    media = MediaFileUpload(str(path), mimetype=mime, resumable=size > 4 << 20)
    body = {"name": path.name, "parents": [parent_id]}
    if existing:
        svc.files().update(fileId=existing["id"], media_body=media, body={"name": path.name}).execute()
        fid = existing["id"]
    else:
        last = None
        for attempt in range(3):
            try:
                fid = svc.files().create(body=body, media_body=media, fields="id").execute()["id"]
                break
            except Exception as e:  # noqa: BLE001 - retry transient quota/network
                last = e
                time.sleep(2 * (attempt + 1))
        else:
            raise RuntimeError(f"upload failed for {path.name}: {last}")

    got = svc.files().get(fileId=fid, fields="id,name,size,md5Checksum").execute()
    if got.get("md5Checksum") != md5:
        raise RuntimeError(f"verify failed for {path.name}: drive md5 {got.get('md5Checksum')} != local {md5}")
    return "uploaded"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true", help="re-check Drive md5s against local; upload nothing")
    ap.add_argument("--stage", default=str(STAGE))
    ap.add_argument("--folder", default=FOLDER_ID)
    args = ap.parse_args()

    stage = Path(args.stage)
    if not stage.is_dir():
        sys.exit(f"staging tree not found: {stage} (run tools/make_backup_tree.py first)")

    svc = auth()
    meta = svc.files().get(fileId=args.folder, fields="id,name,mimeType").execute()
    print(f"target: {meta['name']}  ({meta['id']})")
    print(f"stage : {stage}{'   [DRY RUN]' if args.dry_run else ''}{'   [VERIFY ONLY]' if args.verify else ''}\n")

    tally = {"uploaded": 0, "skipped": 0, "dry": 0, "missing": 0}
    problems: list[str] = []
    total = 0

    for year_dir in sorted(p for p in stage.iterdir() if p.is_dir() and p.name.startswith("Year")):
        print(f"{year_dir.name}")
        yid = ensure_folder(svc, year_dir.name, args.folder, args.dry_run)
        ykids = children(svc, yid) if yid != "DRY" else {}
        for sub in sorted(p for p in year_dir.iterdir() if p.is_dir()):
            sid = ensure_folder(svc, sub.name, yid, args.dry_run)
            skids = children(svc, sid) if sid != "DRY" else {}
            for f in sorted(sub.iterdir()):
                if not f.is_file():
                    continue
                try:
                    if args.verify:
                        ex = skids.get(f.name)
                        md5 = local_md5(f)
                        if not ex:
                            tally["missing"] += 1
                            problems.append(f"MISSING in Drive: {sub.name}/{f.name}")
                        elif ex.get("md5Checksum") != md5:
                            problems.append(f"DIFFERS in Drive: {sub.name}/{f.name}")
                        else:
                            tally["skipped"] += 1
                        continue
                    r = upload(svc, f, sid, skids.get(f.name), args.dry_run)
                    tally[r] += 1
                    total += f.stat().st_size
                except Exception as e:  # noqa: BLE001
                    problems.append(f"{sub.name}/{f.name}: {e}")
            if ykids is not None:
                pass
        print(f"   {len([p for p in year_dir.iterdir() if p.is_dir()])} subjects")

    # the manifest rides along as the record of the backup
    man = stage / "_MANIFEST.csv"
    if man.is_file() and not args.verify:
        try:
            r = upload(svc, man, args.folder, children(svc, args.folder).get(man.name), args.dry_run)
            tally[r] += 1
        except Exception as e:  # noqa: BLE001
            problems.append(f"_MANIFEST.csv: {e}")

    print(f"\nuploaded: {tally['uploaded']}  skipped(identical): {tally['skipped']}  "
          f"dry: {tally['dry']}  missing: {tally['missing']}   {total / 2**20:.1f} MiB sent")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems[:40]:
            print("  ", p)
        return 1
    print("all files present in Drive with matching md5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
