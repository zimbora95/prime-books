"""Sync a book's markdown from public/Prime Books/ to Firestore.
The assistant runs this after editing a book's markdown locally, so the
Firestore-backed live view picks up the change on the next refresh.

Usage:
    python tools/firestore_sync.py "Lower Primary/Year 01/Global Perspectives"
    python tools/firestore_sync.py --all   # sync all books
"""
import json, os, re, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(r"C:\Users\alexa\Documents\GitHub\prime-books")
BOOKS = ROOT / "public" / "Prime Books"
PROJECT = "primeschool-2216d"
COLLECTION = "books"

def slugify(year: str, subject: str) -> str:
    """y01-global-perspectives"""
    y = re.search(r"(\d+)", year)
    yy = int(y.group(1)) if y else 0
    subj = re.sub(r"[^a-z0-9]+", "-", subject.strip().lower()).strip("-")
    return f"y{yy:02d}-{subj}"

def get_token():
    d = json.load(open(r"C:/Users/alexa/.config/configstore/firebase-tools.json"))
    return d["tokens"]["access_token"]

def push_book(book_dir: Path, tok: str) -> bool:
    """Concatenate markdown and push to Firestore."""
    md_dir = book_dir / "MARKDOWN"
    if not md_dir.is_dir():
        return False

    # read all markdown
    parts = []
    for fname in sorted(md_dir.iterdir()):
        if fname.suffix == ".md":
            parts.append(f"<!-- file: {fname.name} -->\n{fname.read_text(encoding='utf-8')}\n")
    if not parts:
        return False
    markdown = "\n".join(parts)

    # extract title from front-matter h1
    title = None
    for line in markdown.split("\n"):
        m = re.search(r"<h1>(.*?)</h1>", line)
        if m:
            title = m.group(1)
            break
    title = title or book_dir.name

    # parse subject and year from path: .../Level/Year NN/Subject
    parts = book_dir.relative_to(BOOKS).parts
    subject = parts[-1] if len(parts) >= 1 else book_dir.name
    year_dir = parts[-2] if len(parts) >= 2 else "Year 1"
    level = parts[-3] if len(parts) >= 3 else ""
    m = re.match(r"Year\s*(\d+)", year_dir, re.IGNORECASE)
    year = int(m.group(1)) if m else 0
    slug = slugify(year_dir, subject)

    # Firestore PATCH
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/{COLLECTION}/{slug}"
    body = {
        "fields": {
            "title": {"stringValue": title},
            "slug": {"stringValue": slug},
            "subject": {"stringValue": subject},
            "year": {"integerValue": year},
            "level": {"stringValue": level},
            "coverUrl": {"stringValue": f"/library/{slug}/cover.webp"},
            "markdown": {"stringValue": markdown},
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        method="PATCH",
        headers={
            "Authorization": "Bearer " + tok,
            "Content-Type": "application/json",
        },
    )
    try:
        urllib.request.urlopen(req, timeout=30)
        print(f"  {slug} -> OK  ({len(markdown)} chars, title: {title})")
        return True
    except urllib.error.HTTPError as e:
        print(f"  {slug} -> ERROR {e.code}: {e.read().decode()[:200]}")
        return False

def find_book_by_partial(partial: str) -> Path | None:
    """Match a partial path like 'Year 01/Global Perspectives'."""
    partial = partial.replace("\\", "/").strip("/")
    for level in sorted(BOOKS.iterdir()):
        if not level.is_dir(): continue
        for yd in sorted(level.iterdir()):
            if not yd.is_dir(): continue
            for sd in sorted(yd.iterdir()):
                if not sd.is_dir(): continue
                if not (sd / "MARKDOWN").is_dir(): continue
                rel = str(sd.relative_to(BOOKS)).replace("\\", "/")
                if partial.lower() in rel.lower():
                    return sd
    return None

if __name__ == "__main__":
    tok = get_token()
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg == "--all":
        n = 0
        for level in sorted(BOOKS.iterdir()):
            if not level.is_dir(): continue
            for yd in sorted(level.iterdir()):
                if not yd.is_dir(): continue
                for sd in sorted(yd.iterdir()):
                    if not sd.is_dir(): continue
                    if push_book(sd, tok):
                        n += 1
        print(f"\nSynced {n} books to Firestore.")
    elif arg:
        d = find_book_by_partial(arg)
        if d:
            push_book(d, tok)
        else:
            print(f"Book not found: {arg}")
            sys.exit(1)
    else:
        print("Usage: firestore_sync.py '<Level/Year/Subject>'  or  --all")
        sys.exit(1)