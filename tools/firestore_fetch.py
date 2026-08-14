"""Fetch a book's markdown from Firestore so the assistant can read the
latest version (the one already synced, not the stale PDF text layer).

Usage:
    python tools/firestore_fetch.py y01-global-perspectives
    python tools/firestore_fetch.py "Year 01/Global Perspectives"  # partial path
"""
import json, re, sys, urllib.request, urllib.error
from pathlib import Path

PROJECT = "primeschool-2216d"
COLLECTION = "books"

def get_token():
    d = json.load(open(r"C:/Users/alexa/.config/configstore/firebase-tools.json"))
    return d["tokens"]["access_token"]

def slug_from_partial(partial: str) -> str:
    """y01-global-perspectives from 'Year 01/Global Perspectives' or direct slug."""
    partial = partial.strip()
    # If already a slug like y01-something, return it
    if re.match(r"^y\d\d-", partial):
        return partial
    m = re.search(r"Year\s*(\d+)", partial, re.IGNORECASE)
    yy = int(m.group(1)) if m else 0
    subject = re.split(r"[/\\]", partial)[-1].strip()
    subj = re.sub(r"[^a-z0-9]+", "-", subject.lower()).strip("-")
    return f"y{yy:02d}-{subj}"

def fetch(slug: str):
    tok = get_token()
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/{COLLECTION}/{slug}"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
    try:
        r = urllib.request.urlopen(req, timeout=15)
        data = json.loads(r.read())
        fields = data.get("fields", {})
        md = fields.get("markdown", {}).get("stringValue", "")
        title = fields.get("title", {}).get("stringValue", "")
        print(md)
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()[:300]}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: firestore_fetch.py <slug or partial path>", file=sys.stderr)
        sys.exit(1)
    slug = slug_from_partial(sys.argv[1])
    fetch(slug)