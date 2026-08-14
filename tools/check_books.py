"""Verify every manifest path resolves to a real file on disk.

A mismatch here is exactly what produced MissingPDFException / 404 on Vercel,
so this runs as a gate before committing or deploying.
"""
import json
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
PUBLIC = REPO / "public"
MANIFEST = PUBLIC / "library.json"

rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
bad = []
for r in rows:
    url = r["pdf"]
    rel = unquote(url.lstrip("/"))
    p = PUBLIC / rel
    if not p.is_file():
        bad.append((r["year"], r["subject"], url, "MISSING"))
    elif p.stat().st_size < 10_000:
        bad.append((r["year"], r["subject"], url, "TOO SMALL"))

# Also flag any on-disk book the manifest forgot.
on_disk = {
    str(p.relative_to(PUBLIC)).replace("\\", "/")
    for p in (PUBLIC / "books").rglob("*.pdf")
}
listed = {unquote(r["pdf"].lstrip("/")) for r in rows}
orphans = sorted(on_disk - listed)

print("manifest entries: %d" % len(rows))
print("resolved OK:      %d" % (len(rows) - len(bad)))
if bad:
    print("\nBROKEN:")
    for y, s, u, why in bad:
        print("  Year %-2d %-34s %s  <- %s" % (y, s, why, u))
if orphans:
    print("\nOn disk but NOT in manifest (%d):" % len(orphans))
    for o in orphans:
        print("  " + o)

# GitHub refuses blobs over 100 MB; warn well before that.
big = [
    (p.stat().st_size / 1048576, str(p.relative_to(PUBLIC)))
    for p in (PUBLIC / "books").rglob("*.pdf")
    if p.stat().st_size > 90 * 1048576
]
if big:
    print("\nOVER 90 MB (GitHub hard-refuses at 100 MB):")
    for mb, name in big:
        print("  %.1f MB  %s" % (mb, name))

total = sum(p.stat().st_size for p in (PUBLIC / "books").rglob("*.pdf"))
print("\ntotal: %.0f MB across %d files" % (total / 1048576, len(on_disk)))

sys.exit(1 if (bad or orphans or big) else 0)
