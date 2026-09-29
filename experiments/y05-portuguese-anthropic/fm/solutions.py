"""Back matter «Soluções» and «Textos para o professor ler em voz alta», built from the units' own files.

    site/solucoes.html (Unit 1), uN/site/solucoes-uN.html (Units 2–7)  -> «Soluções»
    uN/site/textos-professor.md (whichever units wrote one)             -> «Textos para o professor ler em voz alta»

The unit files are web pages for the teacher; here they become small, splittable blocks (one answer per block) that a
paginator (PAGINATE_JS, run by Chrome before printing) pours into two-column pages in the house back-matter style
(«Fim do livro · Soluções», like the Year 9 edition). Everything tied to our own recordings is dropped (<audio>, the
«Áudios» sections, «Texto do áudio» / «Transcrição do áudio» boxes, lines about synthetic voices); anything that
still names a vercel address is dropped and reported.
"""
import html as H
import os
import re
from html.parser import HTMLParser

VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr"}
INLINE_KEEP = {"b", "strong", "i", "em", "u", "sub", "sup", "small", "br"}
AUDIO_WORDS = re.compile(r"(?i)\baudio/|\.mp3\b|vozes sint[ée]ticas|edge[- ]tts|neural tts")
AUDIO_BOX = re.compile(r"(?i)(texto|transcri[çc][ãa]o) do [áa]udio|^[áa]udios?$")


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs or {}), parent, []

    def cls(self):
        return self.attrs.get("class", "") or ""

    def elems(self):
        return [k for k in self.kids if isinstance(k, Node)]

    def text(self):
        out = []
        for k in self.kids:
            out.append(k if isinstance(k, str) else ("\n" if k.tag == "br" else k.text()))
        return "".join(out)


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def parse(src):
    src = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", "", src)
    t = TreeBuilder()
    t.feed(src)
    return t.root


def find(node, tag):
    if isinstance(node, Node):
        if node.tag == tag:
            return node
        for k in node.kids:
            r = find(k, tag)
            if r:
                return r
    return None


def inline(node):
    """inner HTML with only safe inline tags kept (links -> their text)"""
    out = []
    for k in node.kids:
        if isinstance(k, str):
            out.append(H.escape(k, quote=False))
        elif k.tag == "br":
            out.append("<br>")
        elif k.tag in ("audio", "script", "img", "svg"):
            continue
        elif k.tag in INLINE_KEEP:
            t = {"strong": "b", "em": "i"}.get(k.tag, k.tag)
            out.append(f"<{t}>{inline(k)}</{t}>")
        else:
            out.append(inline(k))
    s = "".join(out)
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s*<br>\s*", "<br>", s)


def pagerefs(s):
    """«(p. 12)» / «(pp. 4–7)» / «p. 110» -> DM Mono page tags"""
    return re.sub(r"\b(pp?\.\s?\d+(?:\s?[–-]\s?\d+)?(?:\s?e\s?\d+)?)", r'<span class="pg">\1</span>', s)


def plain(s):
    return re.sub(r"<[^>]+>", "", s)


class Blocks:
    def __init__(self):
        self.out, self.dropped = [], []

    def add(self, cls, html, tag="p", keep_next=False):
        if not plain(html).strip():
            return
        if "vercel" in html.lower():
            self.dropped.append(("vercel", plain(html)[:120]))
            return
        html = re.sub(r"(?i)\btextos-professor\.md\b", "«Textos para o professor», no fim do livro", html)
        html = re.sub(r"≈\s*", "cerca de ", html)  # Figtree has no «≈»
        if AUDIO_WORDS.search(html):
            self.dropped.append(("audio", plain(html)[:120]))
            return
        c = cls + (" kn" if keep_next else "")
        self.out.append(f'<{tag} class="{c}">{html}</{tag}>')


def table_blocks(t, B):
    rows = [r for r in _all(t, "tr")]
    if not rows:
        return
    head = [inline(c).strip() for c in rows[0].elems() if c.tag == "th"]
    body = rows[1:] if head else rows
    if not head:  # a puzzle grid (crossword / word search): one unsplittable block, kept as a table
        B.out.append('<div class="grid">' + grid_html(t) + "</div>")
        return
    pts = len(head) >= 3 and re.match(r"(?i)pontos|pts|cota", head[-1] or "")
    for r in body:
        cells = [c for c in r.elems() if c.tag in ("td", "th")]
        if not cells:
            continue
        vals = [inline(c) for c in cells]
        if pts:
            n, mid, p = vals[0], " — ".join(v for v in vals[1:-1] if v), vals[-1]
            B.add("a", f'<b class="n">{n}</b> {pagerefs(mid)} <span class="pts">{p}&nbsp;p.</span>' if p else f'<b class="n">{n}</b> {pagerefs(mid)}')
        elif len(vals) == 1:
            B.add("t", pagerefs(vals[0]))
        else:
            B.add("a", f'<b class="n">{vals[0]}</b> ' + " · ".join(pagerefs(v) for v in vals[1:] if v))


def _all(node, tag):
    out = []
    for k in node.elems():
        if k.tag == tag:
            out.append(k)
        out += _all(k, tag)
    return out


def grid_html(t):
    rows = []
    for r in _all(t, "tr"):
        cells = []
        for c in r.elems():
            if c.tag not in ("td", "th"):
                continue
            cl = c.cls()
            num = ""
            txt = ""
            for k in c.kids:
                if isinstance(k, Node) and k.tag == "i":
                    num = f"<i>{H.escape(k.text().strip())}</i>"
                elif isinstance(k, str):
                    txt += k
                else:
                    txt += k.text()
            cells.append(f'<td class="{H.escape(cl)}">{num}{H.escape(txt.strip())}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    kind = "ws" if "ws" in t.cls() else "cw"
    return f'<table class="{kind}" style="--cols:{max((r.count("<td") for r in rows), default=1)}">' + "".join(rows) + "</table>"


def walk(node, B, state):
    for k in node.kids:
        if isinstance(k, str):
            if k.strip():
                B.add("t", pagerefs(H.escape(k.strip())))
            continue
        tag, cl = k.tag, k.cls()
        if tag in ("audio", "script", "style", "h1", "img", "svg"):
            continue
        if tag == "div" and re.search(r"\bk\b", cl):
            continue
        if tag == "h2":
            t = inline(k)
            state["skip"] = bool(AUDIO_BOX.search(plain(t).strip()))
            if state["skip"]:
                B.dropped.append(("audio section", plain(t)))
                continue
            B.add("sh", pagerefs(t), "div", keep_next=True)
            continue
        if state.get("skip"):
            continue
        if tag in ("h3", "h4"):
            B.add("s3", pagerefs(inline(k)), "div", keep_next=True)
        elif tag == "dl":
            dts = k.elems()
            i = 0
            while i < len(dts):
                if dts[i].tag == "dt":
                    dd = dts[i + 1] if i + 1 < len(dts) and dts[i + 1].tag == "dd" else None
                    n = inline(dts[i])
                    if dd is not None:
                        inner = dd_html(dd, B)
                        B.add("a", f'<b class="n">{n}</b> {inner}')
                        i += 2
                        continue
                    B.add("a", f'<b class="n">{n}</b>')
                elif dts[i].tag == "dd":
                    B.add("a", dd_html(dts[i], B))
                i += 1
        elif tag == "p":
            nxt = next_elem(k)
            if nxt is not None and nxt.tag == "audio":
                B.dropped.append(("audio label", plain(inline(k))))
                continue
            B.add("nt" if "note" in cl else "t", pagerefs(inline(k)))
        elif tag in ("ul", "ol"):
            items = [li for li in k.elems() if li.tag == "li"]
            for j, li in enumerate(items):
                mark = f"{j + 1}." if tag == "ol" and "c" not in cl.split() else "•"
                B.add("li", f'<span class="bu">{mark}</span> {pagerefs(inline(li))}')
        elif tag == "table":
            table_blocks(k, B)
        elif tag == "div" and "grids" in cl:
            parts = []
            for g in k.elems():
                if g.tag == "table":
                    parts.append('<div class="gcell">' + grid_html(g) + "</div>")
                else:
                    parts.append('<div class="gcell glist">' + list_html(g) + "</div>")
            B.out.append('<div class="grids">' + "".join(parts) + "</div>")
        elif tag == "details":
            summ = next((x for x in k.elems() if x.tag == "summary"), None)
            st = inline(summ) if summ else ""
            if AUDIO_BOX.search(plain(st)):
                B.dropped.append(("audio transcript", plain(st)))
                continue
            if st:
                B.add("s3", st, "div", keep_next=True)
            rest = Node("div")
            rest.kids = [x for x in k.kids if x is not summ]
            walk(rest, B, state)
        elif tag == "blockquote":
            B.add("q", inline(k), "blockquote")
        elif tag == "div" and "note" in cl:
            B.add("nt", pagerefs(inline(k)))
        elif tag in ("div", "section", "article", "main", "body", "html", "span", "a"):
            walk(k, B, state)
        else:
            B.add("t", pagerefs(inline(k)))


def dd_html(dd, B):
    """a <dd> may hold a blockquote or a list: flatten them inline, keeping the quote's line breaks"""
    out = []
    for k in dd.kids:
        if isinstance(k, str):
            out.append(H.escape(k, quote=False))
        elif k.tag == "blockquote":
            out.append(f'<span class="qi">{inline(k)}</span>')
        elif k.tag in ("ul", "ol"):
            out.append(" " + " · ".join(inline(li) for li in k.elems() if li.tag == "li"))
        elif k.tag == "audio":
            continue
        else:
            w = Node("x")
            w.kids = [k]
            out.append(inline(w))
    s = re.sub(r"\s+", " ", "".join(out)).strip()
    return pagerefs(s)


def list_html(node):
    """the «Horizontais / Verticais» answer lists beside a crossword"""
    out = []
    for k in node.kids:
        if isinstance(k, str):
            if k.strip():
                out.append(H.escape(k.strip()))
        elif k.tag in ("b", "strong"):
            out.append(f"<b class='lh'>{inline(k)}</b>")
        elif k.tag in ("ol", "ul"):
            out.append("<ul>" + "".join(f"<li>{inline(li)}</li>" for li in k.elems() if li.tag == "li") + "</ul>")
        else:
            w = Node("x")
            w.kids = [k]
            out.append(inline(w))
    return "".join(out)


def next_elem(k):
    sib = k.parent.kids
    i = sib.index(k)
    for x in sib[i + 1:]:
        if isinstance(x, str):
            if x.strip():
                return None
            continue
        return x
    return None


def chip(u, extra=""):
    return (f'<div class="uchip" style="--c:{u["c"]}"><span class="ul">Unidade {u["n"]}</span>'
            f'<b>{H.escape(u["title"])}</b><span class="ug">{H.escape(u.get("genre", ""))} · pp. {u["first"]}–{u["last"]}{extra}</span></div>')


def sol_path(root, u):
    return os.path.join(root, "site", "solucoes.html") if u["n"] == 1 else os.path.join(root, u["folder"], "site", f"solucoes-u{u['n']}.html")


def tpl_path(root, u):
    return os.path.join(root, "site" if u["n"] == 1 else os.path.join(u["folder"], "site"), "textos-professor.md")


def solutions_blocks(root, units):
    blocks, report = [], []
    for u in units:
        p = sol_path(root, u)
        if not os.path.exists(p):
            report.append(dict(unit=u["n"], file=p, missing=True))
            continue
        tree = parse(open(p, encoding="utf-8").read())
        body = find(tree, "body") or tree
        B = Blocks()
        walk(body, B, {})
        blocks.append(chip(u))
        blocks += B.out
        report.append(dict(unit=u["n"], file=os.path.relpath(p, root), blocks=len(B.out), dropped=B.dropped,
                           mtime=os.path.getmtime(p)))
    return blocks, report


# ---------------------------------------------------------------- markdown (textos-professor.md)
def md_inline(s):
    s = H.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<i>\1</i>", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s


def md_blocks(md):
    B = Blocks()
    lines = md.replace("\r\n", "\n").split("\n")
    para, quote = [], []

    def flush_para():
        if para:
            B.add("t", pagerefs(md_inline(" ".join(x.strip() for x in para))))
            para.clear()

    def flush_quote():
        if quote:
            # consecutive «>» lines are verse/prose lines; an empty «>» separates paragraphs (one block each)
            chunks, cur = [], []
            for x in quote:
                if x.strip():
                    cur.append(md_inline(x.strip()))
                elif cur:
                    chunks.append(cur)
                    cur = []
            if cur:
                chunks.append(cur)
            for c in chunks:
                B.add("q", "<br>".join(c), "blockquote")
            quote.clear()

    for ln in lines:
        s = ln.rstrip()
        if s.startswith(">"):
            flush_para()
            quote.append(s[1:].lstrip() if s[1:2] == " " or len(s) == 1 else s[1:])
            continue
        flush_quote()
        if not s.strip():
            flush_para()
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            flush_para()
            if len(m.group(1)) == 1:
                continue  # the file's own title: the unit chip replaces it
            B.add("sh" if len(m.group(1)) == 2 else "s3", pagerefs(md_inline(m.group(2))), "div", keep_next=True)
            continue
        m = re.match(r"^\s*(\d+)[.)]\s+(.*)", s)
        if m:
            flush_para()
            B.add("li", f'<span class="bu">{m.group(1)}.</span> {pagerefs(md_inline(m.group(2)))}')
            continue
        m = re.match(r"^\s*[-*•]\s+(.*)", s)
        if m:
            flush_para()
            B.add("li", f'<span class="bu">•</span> {pagerefs(md_inline(m.group(1)))}')
            continue
        para.append(s)
    flush_para()
    flush_quote()
    return B


def teacher_blocks(root, units):
    blocks, report = [], []
    for u in units:
        p = tpl_path(root, u)
        if not os.path.exists(p):
            continue
        B = md_blocks(open(p, encoding="utf-8").read())
        if not B.out:
            continue
        blocks.append(chip(u))
        blocks += B.out
        report.append(dict(unit=u["n"], file=os.path.relpath(p, root), blocks=len(B.out), dropped=B.dropped,
                           mtime=os.path.getmtime(p)))
    return blocks, report


# ---------------------------------------------------------------- paginator (runs in Chrome before printing)
PAGINATE_JS = r"""<script>
(async function(){
  await document.fonts.ready;
  const tpl = document.getElementById('pg-templates');
  let folio = parseInt(document.body.dataset.start, 10);
  const report = [];
  // word boundaries (just after each run of spaces) inside an element, in document order
  const bounds = el => { const out = []; const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
    while ((n = w.nextNode())) { const re = /\s+/g; let m; while ((m = re.exec(n.data))) if (m.index + m[0].length < n.data.length || n.nextSibling || true) out.push([n, m.index + m[0].length]); }
    return out; };
  const headOf = (el, k) => { const c = el.cloneNode(true); const b = bounds(c)[k]; const r = document.createRange();
    r.setStart(b[0], b[1]); r.setEnd(c, c.childNodes.length); r.deleteContents(); return c; };
  const tailOf = (el, k) => { const c = el.cloneNode(true); const b = bounds(c)[k]; const r = document.createRange();
    r.setStart(c, 0); r.setEnd(b[0], b[1]); r.deleteContents(); c.classList.add('cont'); c.classList.remove('kn'); return c; };
  for (const src of Array.from(document.querySelectorAll('.flowsrc'))) {
    const sec = src.dataset.sec;
    const queue = Array.from(src.children);
    let first = true, page = null, cols = null;
    const pages = [];
    const newPage = () => {
      const t = tpl.querySelector(`template[data-sec="${sec}"][data-first="${first ? 1 : 0}"]`);
      const node = t.content.firstElementChild.cloneNode(true);
      src.parentNode.insertBefore(node, src);
      first = false; page = node; cols = node.querySelector('.cols'); pages.push(node);
    };
    const over = () => cols.scrollWidth > cols.clientWidth + 1 || cols.scrollHeight > cols.clientHeight + 1;
    const fits = el => { cols.appendChild(el); const ok = !over(); cols.removeChild(el); return ok; };
    newPage();
    while (queue.length) {
      const b = queue.shift();
      cols.appendChild(b);
      if (!over()) continue;
      cols.removeChild(b);
      // split a long paragraph / quote across the page break (keep ≥ 4 words on each side)
      const splittable = (b.tagName === 'P' || b.tagName === 'BLOCKQUOTE') && !b.classList.contains('nt');
      if (splittable) {
        const n = bounds(b).length;
        let lo = 3, hi = n - 4, best = -1;
        while (lo <= hi) { const mid = (lo + hi) >> 1; if (fits(headOf(b, mid))) { best = mid; lo = mid + 1; } else hi = mid - 1; }
        if (best >= 3) {
          cols.appendChild(headOf(b, best));
          queue.unshift(tailOf(b, best));
          newPage();
          continue;
        }
      }
      const carry = [];
      while (cols.lastElementChild && cols.lastElementChild.classList.contains('kn')) carry.unshift(cols.removeChild(cols.lastElementChild));
      if (!cols.children.length) { carry.forEach(c => cols.appendChild(c)); cols.appendChild(b); continue; }
      newPage();
      carry.forEach(c => cols.appendChild(c));
      queue.unshift(b);
    }
    pages[pages.length - 1].classList.add('lastp');
    src.remove();
    for (const p of pages) {
      p.classList.add(folio % 2 ? 'odd' : 'even');
      p.querySelector('.folio').textContent = folio;
      const c = p.querySelector('.cols');
      const r = c.getBoundingClientRect();
      let bot = 0, colBots = [0, 0];
      c.querySelectorAll('*').forEach(e => { for (const rr of e.getClientRects()) { if (!rr.height) continue; bot = Math.max(bot, rr.bottom - r.top);
        const k = rr.left - r.left < r.width / 2 ? 0 : 1; colBots[k] = Math.max(colBots[k], rr.bottom - r.top); } });
      report.push([sec, folio, c.children.length, Math.round(bot / r.height * 100), c.scrollWidth > c.clientWidth + 1,
                   colBots.map(v => Math.round(v / r.height * 100))]);
      folio++;
    }
  }
  const all = document.querySelectorAll('section.page'); if (all.length) all[all.length - 1].classList.add('lastall');
  const pre = document.createElement('pre'); pre.id = 'report'; pre.style.display = 'none';
  pre.textContent = JSON.stringify(report); document.body.appendChild(pre);
  document.body.dataset.done = '1';
})();
</script>"""
