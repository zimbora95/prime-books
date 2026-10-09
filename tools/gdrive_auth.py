#!/usr/bin/env python3
"""Minimal-privilege Google Drive authorization (Drive scope ONLY).

The bundled google-workspace setup.py in this deployment requests Gmail +
Calendar + Contacts + Sheets + Docs + Drive in one go. For a backup uploader
that is far more access than needed, so this asks for Drive alone.

Two steps, PKCE, works headlessly:

    /root/pb-gdrive-venv/bin/python tools/gdrive_auth.py --url
        prints the consent URL and saves the pending PKCE state

    /root/pb-gdrive-venv/bin/python tools/gdrive_auth.py --code "<redirected url or code>"
        exchanges the code, writes ~/.hermes/google_token.json, then proves the
        token works by listing the target folder.

Token has a refresh_token (access_type=offline), so later runs need no consent.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SECRET = Path("/root/.hermes/google_client_secret.json")
TOKEN = Path("/root/.hermes/google_token.json")
PENDING = Path("/root/.hermes/drive_oauth_pending.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]
REDIRECT = "http://localhost:1"
FOLDER_ID = "1wUPlk_dAFqo0qIK_NZVVjJIVJjplz0H2"


def load_secret() -> dict:
    if not SECRET.is_file():
        sys.exit(f"missing {SECRET} — register the OAuth client first")
    d = json.loads(SECRET.read_text(encoding="utf-8"))
    return d.get("installed") or d.get("web") or d


def make_flow():
    from google_auth_oauthlib.flow import Flow

    inst = load_secret()
    return Flow.from_client_config(
        {
            "web": {
                "client_id": inst["client_id"],
                "client_secret": inst["client_secret"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT,
    )


def cmd_url() -> int:
    flow = make_flow()
    url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="false"
    )
    PENDING.write_text(
        json.dumps({"code_verifier": flow.code_verifier, "state": state}, indent=1), encoding="utf-8"
    )
    PENDING.chmod(0o600)
    print(url)
    return 0


def cmd_code(code: str) -> int:
    if not PENDING.is_file():
        sys.exit("no pending auth session — run --url first")
    pend = json.loads(PENDING.read_text(encoding="utf-8"))
    flow = make_flow()
    flow.code_verifier = pend["code_verifier"]
    flow.fetch_token(code=code)
    creds = flow.credentials
    if not creds.refresh_token:
        print("WARNING: no refresh_token — the token will expire in an hour", file=sys.stderr)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
    TOKEN.chmod(0o600)
    PENDING.unlink(missing_ok=True)

    from googleapiclient.discovery import build

    svc = build("drive", "v3", credentials=creds, cache_discovery=False)
    me = svc.about().get(fields="user(emailAddress,displayName),storageQuota(usage,limit)").execute()
    u = me.get("user", {})
    q = me.get("storageQuota", {})
    print(f"AUTHORISED as {u.get('emailAddress')} ({u.get('displayName')})")
    if q:
        used = int(q.get("usage", 0)) / 2**30
        lim = q.get("limit")
        print(f"drive usage: {used:.1f} GiB of {int(lim) / 2**30:.1f} GiB" if lim else f"drive usage: {used:.1f} GiB")

    m = svc.files().get(fileId=FOLDER_ID, fields="id,name,mimeType").execute()
    print(f"target folder reachable: {m['name']} ({m['id']})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", action="store_true")
    g.add_argument("--code")
    a = ap.parse_args()
    return cmd_url() if a.url else cmd_code(a.code.strip())


if __name__ == "__main__":
    sys.exit(main())
