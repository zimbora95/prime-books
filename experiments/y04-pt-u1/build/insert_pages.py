#!/usr/bin/env python3
"""Insert N new pages after page X and shift every later page by +N.

usage: insert_pages.py AFTER COUNT "colour|kind|running label" [--dry]
Shifts: fragment file names (NN.html), the PAGES registry in build.py, page-scoped CSS ids
(#pNN inside each fragment) and every printed cross-reference in all fragments:
  p. NN · pp. NN–NN · página(s) NN · páginas NN e NN · páginas NN a NN.
New fragments are created as placeholders. Backups: pages-before-insert-<AFTER>/.
Run only when no builder is editing pages.
"""
import pathlib, re, sys, shutil
HERE = pathlib.Path(__file__).resolve().parent
P = HERE / 'pages'
args = [a for a in sys.argv[1:] if a != '--dry']
DRY = '--dry' in sys.argv
AFTER, SHIFT = int(args[0]), int(args[1])
col, kind, label = args[2].split('|')

def sh(n):
    n = int(n)
    return n + SHIFT if n > AFTER else n

REF = re.compile(r'(?P<w>\b(?:pp?\.|[Pp]áginas?)\s?)(?P<a>\d{1,3})(?P<rest>(?:\s?[–-]\s?\d{1,3}|\s(?:e|a)\s\d{1,3})?)')
def fix_refs(t):
    def r(m):
        rest = re.sub(r'\d{1,3}', lambda k: str(sh(k.group())), m.group('rest'))
        return f"{m.group('w')}{sh(m.group('a'))}{rest}"
    return REF.sub(r, t)

files = sorted((f for f in P.glob('*.html') if re.fullmatch(r'\d+', f.stem)), key=lambda f: int(f.stem))
new, changed = {}, 0
for f in files:
    n = int(f.stem); t = f.read_text()
    t2 = fix_refs(t)
    if n > AFTER:
        t2 = re.sub(rf'#p{n}\b', f'#p{n + SHIFT}', t2)
    name = f'{sh(n):02d}.html'
    changed += (t2 != t or name != f.name)
    new[name] = t2
for k in range(1, SHIFT + 1):
    new[f'{AFTER + k:02d}.html'] = f'<div class="head"><h1>Página {AFTER + k} (em construção)</h1></div>\n'
bp = HERE / 'build.py'; s = bp.read_text()
s2 = re.sub(r'^(    \(")(\d+)(")', lambda m: f'{m.group(1)}{sh(m.group(2)):02d}{m.group(3)}', s, flags=re.M)
m = re.search(rf'^    \("{AFTER:02d}",.*\n', s2, re.M)
assert m, f'registry line for page {AFTER} not found'
ins = ''.join(f'    ("{AFTER + k:02d}", "{col}", "{kind}", "{label}"),\n' for k in range(1, SHIFT + 1))
s2 = s2[:m.end()] + ins + s2[m.end():]
print('fragments changed:', changed, '| registry entries:', len(re.findall(r'^    \("\d+"', s2, re.M)))
if DRY:
    print('dry run: nothing written'); sys.exit()
bak = HERE / f'pages-before-insert-{AFTER}'
if not bak.exists():
    shutil.copytree(P, bak); shutil.copy(bp, HERE / f'build.py.before-insert-{AFTER}')
for f in files: f.unlink()
for name, t in new.items(): (P / name).write_text(t)
bp.write_text(s2)
print('done')
