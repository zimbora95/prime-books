"""Report characters used in the built HTML that each house font cannot draw.
Chromium silently falls back to DejaVu/Liberation for these."""
import re, html, glob, pathlib
from fontTools.ttLib import TTFont
HERE = pathlib.Path(__file__).parent
import os
src = (HERE / f"farol-u{os.environ.get('UNIT','1')}.html").read_text(encoding="utf-8")
txt = html.unescape(re.sub(r"<style.*?</style>|<[^>]+>", " ", src, flags=re.S))
chars = {c for c in txt if ord(c) > 127}
for f in sorted(glob.glob(str(HERE.parent / "fonts/static/*.ttf"))):
    cmap = TTFont(f).getBestCmap()
    miss = sorted(c for c in chars if ord(c) not in cmap)
    if miss:
        print(pathlib.Path(f).name, "missing:", " ".join(f"{c}(U+{ord(c):04X})" for c in miss))
