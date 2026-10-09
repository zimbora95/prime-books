#!/usr/bin/env python3
"""Fit every page to the US Letter text block after the A4 -> Letter re-cut.

The Letter block is 177 x 251.4 mm against A4's 177 x 263 mm, so a page that was
full on A4 overflows by up to ~12 mm. For each overflowing page this sets
`#pN .inner { zoom: z }` (one tagged line in the page fragment), with z the
smallest reduction that fits, then rebuilds and repeats until the build reports no
inner overflow. Pages that already fit are never touched (zoom stays 1).

usage: fit_letter.py [--rounds N]
"""
import json, pathlib, re, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
PY = '/root/prime-books/.venv/bin/python'
INNER_PX = 251.4 / 25.4 * 96
TAG = '/*letter-fit*/'
rounds = int(sys.argv[sys.argv.index('--rounds') + 1]) if '--rounds' in sys.argv else 5

def build(pages=None):
    cmd = [PY, 'build.py', '--dpi', '40', '--out', 'fit']
    if pages: cmd += ['--pages', ','.join(map(str, pages))]
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    out = r.stdout + r.stderr
    return {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'"p(\d+): inner overflow (\d+)px', out)}

def current_zoom(t, n):
    m = re.search(rf'#p{n} \.inner {{ zoom: ([0-9.]+); }}', t)
    return float(m.group(1)) if m else 1.0

def set_zoom(n, z):
    f = HERE / 'pages' / f'{n:02d}.html'
    t = f.read_text()
    t = re.sub(r'\n?<style>' + re.escape(TAG) + r'.*?</style>\n?', '\n', t, flags=re.S)
    t = t.rstrip('\n') + f'\n<style>{TAG} #p{n} .inner {{ zoom: {z:.3f}; }}</style>\n'
    f.write_text(t)

todo = [int(x) for x in sys.argv[sys.argv.index("--pages") + 1].split(",")] if "--pages" in sys.argv else None
for rnd in range(rounds):
    ov = build(todo)
    print(f'round {rnd}: {len(ov)} pages overflow', dict(sorted(ov.items())) if len(ov) < 25 else '')
    if not ov: break
    for n, px in ov.items():
        f = HERE / 'pages' / f'{n:02d}.html'
        z0 = current_zoom(f.read_text(), n)
        # overflow px are measured in the zoomed box's own units; shrink proportionally, plus a hair
        z = z0 * INNER_PX / (INNER_PX + px / z0) - 0.003
        set_zoom(n, max(z, 0.85))
    todo = sorted(ov)
print('done')
