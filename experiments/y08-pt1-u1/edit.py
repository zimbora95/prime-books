"""Tiny edit helpers for the experiment (exact-string replace, fails loudly)."""
import pathlib
ROOT = pathlib.Path(__file__).parent
P = ROOT / "src" / "book.html"
C = ROOT / "src" / "pages.css"


def rep(path, pairs):
    t = path.read_text()
    for a, b in pairs:
        if a not in t:
            raise SystemExit(f"NOT FOUND in {path.name}: {a[:80]!r}")
        t = t.replace(a, b, 1)
    path.write_text(t)


def add_css(text):
    with C.open("a") as f:
        f.write(text)
