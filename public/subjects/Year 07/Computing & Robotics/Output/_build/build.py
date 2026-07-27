"""
Prime Books build engine  —  Cambridge Computing Year 07
Markdown (+ custom ::: blocks) -> HTML -> PDF (Chromium, 210x270mm)

Usage:
    python build.py            # full book
    python build.py 7_1        # single chapter preview (fast iteration)
"""
import re, sys, json, pathlib, html as _html

ROOT = pathlib.Path(__file__).parent
BOOK = ROOT / 'book'
OUT = ROOT.parent
IMAGES = OUT / 'Images'

# ----------------------------------------------------------------- inline
def esc(t):
    return _html.escape(t, quote=False)

def inline(t):
    """Inline markdown: `code`, **bold**, *ital*, [txt](url), ^sup^, ~sub~."""
    out, i, n = [], 0, len(t)
    # protect code spans first
    parts = re.split(r'(`[^`]+`)', t)
    for p in parts:
        if p.startswith('`') and p.endswith('`') and len(p) > 1:
            out.append('<code>' + esc(p[1:-1]) + '</code>')
            continue
        s = esc(p)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<em>\1</em>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
        s = re.sub(r'\^([^\^]+)\^', r'<sup>\1</sup>', s)
        s = re.sub(r'~([^~]+)~', r'<sub>\1</sub>', s)
        out.append(s)
    return ''.join(out)

# ----------------------------------------------------------------- code hl
PY_KW = r'\b(?:False|None|True|and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b'
PY_BI = r'\b(?:print|input|int|str|float|len|range|round|abs|min|max|sum|list|type|bool|sorted|append|show|scroll|sleep|display|randint|set_pixel|clear|is_pressed|get_x|get_y|temperature|running_time|open|write|read)\b'

def hl(code, lang='python'):
    """Tiny tokenising highlighter -> spans. Escapes first, then wraps.
    Placeholders use LETTERS only: the numeric-literal pass below would
    otherwise match the digits inside a numeric placeholder and corrupt it."""
    s = esc(code)
    toks = []
    def key(i):
        # 0 -> \x00aa\x00, 1 -> \x00ab\x00 ...
        return '\x00' + chr(97 + i // 26) + chr(97 + i % 26) + '\x00'
    def stash(txt):
        toks.append(txt)
        return key(len(toks) - 1)
    # strings & comments out of harm's way
    s = re.sub(r'&#x27;[^\n&]*?&#x27;|&quot;[^\n&]*?&quot;|\'[^\'\n]*\'|"[^"\n]*"',
               lambda m: stash(f'<span class="s">{m.group(0)}</span>'), s)
    s = re.sub(r'#[^\n]*', lambda m: stash(f'<span class="c">{m.group(0)}</span>'), s)
    if lang == 'python':
        s = re.sub(PY_KW, lambda m: f'<span class="k">{m.group(0)}</span>', s)
        s = re.sub(PY_BI, lambda m: f'<span class="f">{m.group(0)}</span>', s)
    s = re.sub(r'(?<![\w.])(\d+\.?\d*)(?![\w])',
               lambda m: f'<span class="n">{m.group(0)}</span>', s)
    s = re.sub(r'\x00([a-z]{2})\x00',
               lambda m: toks[(ord(m.group(1)[0]) - 97) * 26
                              + (ord(m.group(1)[1]) - 97)], s)
    return s

# ----------------------------------------------------------------- blocks
FEATURES = {
    'scenario':  ('f-scenario',  'Scenario',          '◆'),
    'warmup':    ('f-warm',      'Warm up',           '✦'),
    'remember':  ('f-remember',  'Do you remember?',  '↺'),
    'know':      ('f-know',      'Did you know?',     '✧'),
    'further':   ('f-further',   'Go further',        '→'),
    'challenge': ('f-challenge', 'Challenge yourself','▲'),
    'practise':  ('f-practise',  'Practise',          '●'),
    'keywords':  ('f-keywords',  'Keywords',          '▮'),
}

def render(md):
    """Block-level renderer."""
    lines = md.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    out, i, n = [], 0, len(lines)
    while i < n:
        L = lines[i]
        s = L.strip()

        # ---- raw HTML passthrough
        if s.startswith('<!--html'):
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith('-->'):
                buf.append(lines[i]); i += 1
            i += 1
            out.append('\n'.join(buf)); continue

        # ---- ::: feature block
        m = re.match(r'^:::\s*([a-z]+)(?:\s+(.*))?$', s)
        if m:
            kind, arg = m.group(1), (m.group(2) or '').strip()
            buf, depth = [], 1
            i += 1
            while i < n:
                t = lines[i].strip()
                if re.match(r'^:::\s*[a-z]+', t): depth += 1
                elif t == ':::':
                    depth -= 1
                    if depth == 0: break
                buf.append(lines[i]); i += 1
            i += 1
            out.append(feature(kind, arg, '\n'.join(buf)))
            continue

        # ---- fenced code
        if s.startswith('```'):
            lang = s[3:].strip() or 'python'
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(lines[i]); i += 1
            i += 1
            body = '\n'.join(buf)
            if lang == 'out':
                out.append(f'<div class="out">{esc(body)}</div>')
            else:
                out.append(f'<pre class="code">{hl(body, lang)}</pre>')
            continue

        # ---- table
        if s.startswith('|') and i + 1 < n and re.match(r'^\|[\s:\-|]+\|$', lines[i+1].strip()):
            head = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            th = ''.join(f'<th>{inline(c)}</th>' for c in head)
            tb = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                         for r in rows)
            out.append(f'<table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table>')
            continue

        # ---- headings
        if s.startswith('#### '):
            out.append(f'<h4 class="mini">{inline(s[5:])}</h4>'); i += 1; continue
        if s.startswith('### '):
            out.append(f'<h3 class="sub">{inline(s[4:])}</h3>'); i += 1; continue
        if s.startswith('## '):
            txt = s[3:]
            mm = re.match(r'^\[([^\]]+)\]\s*(.*)$', txt)
            if mm:
                out.append(f'<h2 class="topic"><span class="num">{inline(mm.group(1))}'
                           f'</span>{inline(mm.group(2))}</h2>')
            else:
                out.append(f'<h2 class="topic">{inline(txt)}</h2>')
            i += 1; continue

        # ---- figure   !fig[caption](name.png){class}
        mf = re.match(r'^!fig\[(.*?)\]\((.+?)\)(?:\{(.+?)\})?$', s)
        if mf:
            cap, src, cls = mf.group(1), mf.group(2), (mf.group(3) or '')
            capm = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', cap)
            caphtml = (f'<b>{inline(capm.group(1))}</b> {inline(capm.group(2))}'
                       if capm else inline(cap))
            fc = f'<figcaption>{caphtml}</figcaption>' if cap else ''
            out.append(f'<figure class="{cls}"><img src="../Images/{src}">{fc}</figure>')
            i += 1; continue

        # ---- lists
        if re.match(r'^[-*]\s+', s) or re.match(r'^\+\s+', s):
            tick = s.startswith('+')
            items, i = collect_list(lines, i, r'^[-*+]\s+')
            cls = 'tick' if tick else 'dot'
            li = ''.join(f'<li>{render_li(x)}</li>' for x in items)
            out.append(f'<ul class="{cls}">{li}</ul>'); continue
        if re.match(r'^\d+[.)]\s+', s):
            items, i = collect_list(lines, i, r'^\d+[.)]\s+')
            li = ''.join(f'<li>{render_li(x)}</li>' for x in items)
            out.append(f'<ol class="ol-sig">{li}</ol>'); continue
        if re.match(r'^[a-z][.)]\s+', s):
            items, i = collect_list(lines, i, r'^[a-z][.)]\s+')
            li = ''.join(f'<li>{render_li(x)}</li>' for x in items)
            out.append(f'<ol class="alpha">{li}</ol>'); continue

        # ---- hr
        if s in ('---', '***'):
            out.append('<hr class="rule">'); i += 1; continue

        # ---- blank
        if not s:
            i += 1; continue

        # ---- paragraph
        buf = []
        while i < n and lines[i].strip() and not stops(lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        out.append(f'<p>{inline(" ".join(buf))}</p>')
    return '\n'.join(out)

def stops(s):
    return (s.startswith(('#', ':::', '```', '|', '!fig', '<!--html'))
            or s in ('---', '***')
            or re.match(r'^[-*+]\s+', s) or re.match(r'^\d+[.)]\s+', s)
            or re.match(r'^[a-z][.)]\s+', s))

def collect_list(lines, i, pat):
    """Gather list items incl. indented continuations / nested blocks."""
    items, n = [], len(lines)
    while i < n:
        s = lines[i].strip()
        if not re.match(pat, s): break
        body = [re.sub(pat, '', s, count=1)]
        i += 1
        sub = []
        while i < n and (lines[i].startswith('   ') or lines[i].startswith('\t')) \
                and lines[i].strip():
            sub.append(lines[i][3:] if lines[i].startswith('   ') else lines[i][1:])
            i += 1
        if sub: body.append('\x01' + '\n'.join(sub))
        items.append('\n'.join(body))
        while i < n and not lines[i].strip() and i + 1 < n and re.match(pat, lines[i+1].strip()):
            i += 1
    return items, i

def render_li(x):
    if '\x01' in x:
        head, sub = x.split('\x01', 1)
        return inline(head.strip()) + render(sub)
    return inline(x.strip())

def feature(kind, arg, body):
    if kind == 'raw':
        return body
    cls, label, glyph = FEATURES.get(kind, ('f-further', arg or kind.title(), '→'))
    if arg and kind in ('practise', 'challenge', 'further', 'know', 'warmup',
                        'remember', 'scenario', 'keywords'):
        label = arg
    inner = render(body)
    return (f'<section class="feat {cls}">'
            f'<div class="feat-lab"><span class="gl">{glyph}</span>{esc(label)}</div>'
            f'{inner}</section>')

# ----------------------------------------------------------------- assemble
def build(chapters, out_pdf, title):
    css = (ROOT / 'book.css').read_text(encoding='utf-8')
    parts = []
    for ch in chapters:
        p = BOOK / f'{ch}.md'
        if not p.exists():
            print(f'  !! missing {p.name}'); continue
        raw = p.read_text(encoding='utf-8')
        # front-matter:  <!-- unit: u1 -->
        um = re.search(r'<!--\s*unit:\s*(u\d)\s*-->', raw)
        ucls = um.group(1) if um else 'u1'
        raw = re.sub(r'<!--\s*unit:.*?-->', '', raw)
        parts.append(f'<div class="{ucls}">\n{render(raw)}\n</div>')
        print(f'  ok {p.name:22s} {len(raw):7,d} chars')

    doc = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<title>{esc(title)}</title><style>{css}</style></head>
<body>{''.join(parts)}</body></html>"""
    hp = ROOT / '_render.html'
    hp.write_text(doc, encoding='utf-8')

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(hp.resolve().as_uri(), wait_until='networkidle')
        pg.wait_for_timeout(1200)
        pg.pdf(path=str(out_pdf), width='210mm', height='270mm',
               print_background=True, prefer_css_page_size=True,
               margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        b.close()
    import fitz
    d = fitz.open(out_pdf)
    print(f'\n>> {out_pdf.name}: {len(d)} pages, {d[0].rect.width:.1f}x{d[0].rect.height:.1f}pt')
    return len(d)

FULL = ['00_cover', '01_imprint', '02_contents', '03_introduction',
        '05_gettingsetup', '10_unit71', '20_unit72', '30_unit73', '40_unit74',
        '50_unit75', '60_unit76', '90_glossary', '95_backcover']

if __name__ == '__main__':
    BOOK.mkdir(exist_ok=True)
    if len(sys.argv) > 1:
        chs = sys.argv[1:]
        build(chs, ROOT / '_preview.pdf', 'preview')
    else:
        build(FULL, OUT / 'Cambridge Computing Year 07.pdf',
              'Computing 7 · Prime School')
