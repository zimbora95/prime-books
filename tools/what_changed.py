#!/usr/bin/env python3
"""What did the standardise commits actually change? old blob vs new blob."""
import subprocess, sys
from pathlib import Path
import fitz

REPO = Path("/root/prime-books")
SLUGS = sys.argv[1:]


def git(*a):
    return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True, text=True)


def gitb(*a):
    return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True).stdout


def info(path):
    d = fitz.open(path)
    p0 = d[0]
    return len(d), round(p0.rect.width), round(p0.rect.height), Path(path).stat().st_size


print(f"{'slug':32} {'old pp':>6} {'new pp':>6} {'old pgsize':>12} {'new pgsize':>12} {'bytes was':>10} {'now':>10}")
for slug in SLUGS:
    rel = f"public/library/{slug}/book.pdf"
    c = git("log", "--format=%H", "-1", "--", rel).stdout.strip()
    if not c:
        print(f"{slug:32} no commit touched it")
        continue
    old = Path(f"/tmp/old_{slug}.pdf")
    old.write_bytes(gitb("show", f"{c}^:{rel}"))
    try:
        o = info(old)
        n = info(REPO / rel)
    except Exception as e:
        print(f"{slug:32} unreadable: {e}")
        continue
    print(f"{slug:32} {o[0]:>6} {n[0]:>6} {o[1]}x{o[2]:>7} {n[1]}x{n[2]:>7} {o[3]:>10} {n[3]:>10}")
