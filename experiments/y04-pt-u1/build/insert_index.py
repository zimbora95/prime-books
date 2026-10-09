#!/usr/bin/env python3
"""Insert a two-page contents spread (Índice) after page 2 and shift every later page by +2.

Run ONCE, only after every builder job has finished (jobs edit pages by number).
  --dry  : report what would change, write nothing.
Shifts: fragment file names (NN.html), the PAGES registry in build.py, page-scoped CSS ids
(#pNN inside each fragment), and every printed cross-reference in all fragments:
  p. NN · pp. NN–NN · página(s) NN · páginas NN e NN · páginas NN a NN.
Pages 1–2 are unchanged. The two new fragments are 03.html and 04.html (written separately).
"""
import pathlib, re, sys, shutil
HERE = pathlib.Path(__file__).resolve().parent
P = HERE / 'pages'
DRY = '--dry' in sys.argv
SHIFT = 2

def sh(n):
    n = int(n)
    return n + SHIFT if n >= 3 else n

REF = re.compile(r'(?P<w>\b(?:pp?\.|[Pp]áginas?)\s?)(?P<a>\d{1,3})(?P<rest>(?:\s?[–-]\s?\d{1,3}|\s(?:e|a)\s\d{1,3})?)')
def fix_refs(t):
    def r(m):
        rest = re.sub(r'\d{1,3}', lambda k: str(sh(k.group())), m.group('rest'))
        return f"{m.group('w')}{sh(m.group('a'))}{rest}"
    return REF.sub(r, t)

files = sorted((f for f in P.glob('*.html') if re.fullmatch(r'\d+', f.stem)), key=lambda f: int(f.stem))
changes = 0
new = {}
for f in files:
    n = int(f.stem); t = f.read_text()
    t2 = fix_refs(t)
    if n >= 3:
        t2 = re.sub(rf'#p{n}\b', f'#p{n + SHIFT}', t2)
    name = f'{n + SHIFT:02d}.html' if n >= 3 else f.name
    if t2 != t or name != f.name:
        changes += 1
    new[name] = t2
print('fragments affected:', changes)
bp = HERE / 'build.py'; s = bp.read_text()
def reg(m):
    n = int(m.group(1)); return f'("{n + SHIFT:02d}"' if n >= 3 else m.group(0)
s2 = re.sub(r'\("(\d+)"', reg, s)
m = re.search(r'^    \("02",.*\n', s2, re.M)
assert m, 'registry line for page 02 not found'
s2 = s2[:m.end()] + '    ("03", "red", "std", "Índice"),\n    ("04", "red", "std", "Índice"),\n' + s2[m.end():]
if DRY:
    print('dry run: nothing written'); sys.exit()
bak = HERE / 'pages-before-index'
if not bak.exists():
    shutil.copytree(P, bak); shutil.copy(bp, HERE / 'build.py.before-index')
for f in files: f.unlink()
for name, t in new.items(): (P / name).write_text(t)
bp.write_text(s2)
print('done; backup in pages-before-index/ and build.py.before-index')
