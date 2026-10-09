#!/usr/bin/env python3
"""Which pages of a book actually changed, and what do they look like?

    .venv/bin/python tools/page_diff.py <slug> [--out /tmp/diff]

Compares the committed-previous revision of public/library/<slug>/book.pdf with
the working copy: per-page render diff, then side-by-side PNGs of the pages that
changed so a human can look at them.
"""
import subprocess
import sys
from pathlib import Path

import pymupdf

REPO = Path("/root/prime-books")
slug = sys.argv[1]
out = Path(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/diff")
out.mkdir(parents=True, exist_ok=True)
rel = f"public/library/{slug}/book.pdf"

commit = subprocess.run(["git", "-C", str(REPO), "log", "--format=%H", "-1", "--", rel],
                        capture_output=True, text=True).stdout.strip()
old_bytes = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}^:{rel}"],
                           capture_output=True).stdout
old_path = out / f"{slug}-OLD.pdf"
old_path.write_bytes(old_bytes)

old, new = pymupdf.open(old_path), pymupdf.open(REPO / rel)
print(f"{slug}: old {len(old)} pp {old[0].rect.width:.0f}x{old[0].rect.height:.0f} | "
      f"new {len(new)} pp {new[0].rect.width:.0f}x{new[0].rect.height:.0f}")

changed, same = [], 0
for i in range(min(len(old), len(new))):
    a = old[i].get_pixmap(dpi=72).samples
    b = new[i].get_pixmap(dpi=72).samples
    if a == b:
        same += 1
    else:
        changed.append(i + 1)
print(f"identical pages: {same} | changed pages: {len(changed)} -> {changed[:20]}"
      f"{' ...' if len(changed) > 20 else ''}")

for n in [p for p in changed[:4]]:
    op, np_ = old[n - 1].get_pixmap(dpi=100), new[n - 1].get_pixmap(dpi=100)
    w, h = op.width + np_.width + 12, max(op.height, np_.height)
    sheet = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, w, h), False)
    sheet.clear_with(255)
    for pm, x in ((op, 0), (np_, op.width + 12)):
        pm.set_origin(x, 0)
        sheet.copy(pm, pm.irect)
    p = out / f"{slug}-p{n:03d}.png"
    sheet.save(p)
    print("  wrote", p)