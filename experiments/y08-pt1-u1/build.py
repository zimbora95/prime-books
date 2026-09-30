"""Build Promessa & Veredicto (Unit 1, PT Y8): HTML -> PDF -> page renders."""
import re, sys, pathlib, segno, io, pymupdf
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
SRC, BUILD = ROOT / "src", ROOT / "build"
BUILD.mkdir(exist_ok=True)
SLUG = "y08-portuguese-1st-anthropic"
SITE = "https://prime-books-pi.vercel.app"


def qr_svg(url: str, dark="#141829") -> str:
    q = segno.make(url, error="m")
    buf = io.BytesIO()
    q.save(buf, kind="svg", scale=1, border=3, dark=dark, light="#ffffff", xmldecl=False, svgns=True)
    svg = buf.getvalue().decode()
    return re.sub(r'(<svg[^>]*?) width="(\d+)" height="(\d+)"',
                  lambda m: f'{m.group(1)} viewBox="0 0 {m.group(2)} {m.group(3)}" shape-rendering="crispEdges"', svg, count=1)


def render_html() -> pathlib.Path:
    html = (SRC / "book.html").read_text()
    html = re.sub(r"\{\{INCLUDE:([^}]+)\}\}", lambda m: (SRC / m.group(1)).read_text(), html)
    html = html.replace("{{SITE}}", SITE).replace("{{SLUG}}", SLUG)
    # Guard: the .vercel site is a temporary workshop -- no printed QR may depend on it.
    bad = [u for u in re.findall(r"\{\{QR:([^}]+)\}\}", html) if "vercel" in u or "/library/" in u]
    if bad:
        raise SystemExit("QR points at the temporary site: " + ", ".join(bad))
    html = re.sub(r"\{\{QR:([^}]+)\}\}", lambda m: qr_svg(m.group(1)), html)
    out = SRC / "_book.built.html"  # stays in src/ so relative art + font paths resolve
    out.write_text(html)
    return out


def to_pdf(html_path: pathlib.Path, pdf: pathlib.Path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(html_path.as_uri(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        import os
        if os.environ.get("ALLOW_ODD"): pg.evaluate("window.__ALLOW_ODD = true")
        pg.emulate_media(media="print")
        # long texts flow paragraph by paragraph onto as many continuation pages as they need
        pg.evaluate("""() => {
          const fits = s => {
            const i = s.querySelector('.inner'), b = s.querySelector('.flow-body');
            const lim = i.getBoundingClientRect().bottom - parseFloat(getComputedStyle(i).paddingBottom) - 8;
            return b.getBoundingClientRect().bottom <= lim && i.scrollHeight <= i.clientHeight + 1;
          };
          document.querySelectorAll('section.flow').forEach(first => {
            let sec = first, guard = 0;
            while (!fits(sec) && guard++ < 40) {
              const cont = first.cloneNode(true);
              cont.id = first.id + '-c' + guard; cont.classList.add('cont');
              cont.querySelectorAll('.flow-head').forEach(e => e.remove());
              const cb = cont.querySelector('.flow-body'); cb.innerHTML = '';
              sec.after(cont);
              const body = sec.querySelector('.flow-body');
              while (!fits(sec) && body.children.length > 1) cb.prepend(body.lastElementChild);
              // pull sentences of the first moved paragraph back, so pages end full
              const moved = cb.firstElementChild;
              if (moved && moved.tagName === 'P' && !moved.classList.contains('src')) {
                const parts = moved.innerHTML.split(/(?<=[.!?…»])\s+(?=[—A-ZÁÉÍÓÚÂÊÔÀÇ«])/);
                if (parts.length > 1) {
                  const head = document.createElement('p'); head.className = 'split-a';
                  body.appendChild(head);
                  let k = 0;
                  while (k < parts.length - 1) {
                    head.innerHTML = parts.slice(0, k + 1).join(' ');
                    if (!fits(sec)) break;
                    k++;
                  }
                  if (k === 0) { head.remove(); }
                  else {
                    head.innerHTML = parts.slice(0, k).join(' ');
                    moved.innerHTML = parts.slice(k).join(' ');
                    moved.classList.add('split-b');
                  }
                }
              }
              sec = cont;
            }
          });
        }""")
        # ruled writing lines: real vector rules (one bordered 7.2 mm row per line), because
        # Chromium prints the CSS gradient/SVG-tile backgrounds as soft, uneven or missing bands
        pg.evaluate("""() => {
          const mm = 96 / 25.4, pitch = 7.2 * mm;
          document.querySelectorAll('.lines').forEach(l => {
            const n = Math.round(l.getBoundingClientRect().height / pitch);
            if (!n || l.children.length) return;
            l.style.backgroundImage = 'none';
            for (let k = 0; k < n; k++) {
              const r = document.createElement('i');
              r.className = 'rule';
              l.appendChild(r);
            }
          });
        }""")
        # pagination is computed, never typed: parity, folios and cross-references
        pg.evaluate("""() => {
          const secs = [...document.querySelectorAll('section.page')];
          const idx = new Map(secs.map((s, i) => [s.id, i + 1]));
          secs.forEach((s, i) => {
            s.classList.remove('recto', 'verso');
            s.classList.add((i + 1) % 2 ? 'recto' : 'verso');
            const n = s.querySelector('.folio .n'); if (n) n.textContent = i + 1;
          });
          document.querySelectorAll('[data-ref]').forEach(r => {
            const v = idx.get(r.dataset.ref);
            if (!v) throw new Error('dangling ref ' + r.dataset.ref);
            r.textContent = v;
          });
          if (secs.length % 2 && !window.__ALLOW_ODD) throw new Error('odd page count ' + secs.length);
        }""")
        report = pg.evaluate("""() => {
          const mm = 96/25.4, out = [];
          document.querySelectorAll('.page').forEach((p, i) => {
            const inn = p.querySelector('.inner'); if (!inn) return;
            const ib = inn.getBoundingClientRect();
            let low = ib.top;
            inn.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height) low = Math.max(low, r.bottom); });
            out.push([i+1, ((ib.bottom - low)/mm).toFixed(1), p.id || '']);
          });
          return out;
        }""")
        for n, free, pid in report:
            flag = "OVERFLOW" if float(free) < -0.5 else ("loose" if float(free) > 18 else "")
            print(f"  p{n:02d} free {free:>6} mm {flag:8} {pid}")
        pg.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
        b.close()


def std_covers(pdf: pathlib.Path):
    """Swap page 1 and the last page for the house-standard covers (covers/std_covers.py).
    The HTML keeps #s1/#s28 as placeholders so the page count and parity stay put."""
    cov = ROOT / "covers" / "std-covers-a4.pdf"
    if not cov.exists():
        print("  (no covers/std-covers-a4.pdf - HTML covers kept)")
        return
    src, c = pymupdf.open(pdf), pymupdf.open(cov)
    imp = ROOT / "covers" / "std-imprint-a4.pdf"
    out = pymupdf.open()
    out.insert_pdf(c, from_page=0, to_page=0)
    if imp.exists():   # page 2 of the HTML is the empty #f-std-imprint placeholder
        assert not src[1].get_text().strip(), "page 2 is not the imprint placeholder"
        out.insert_pdf(pymupdf.open(imp))
        out.insert_pdf(src, from_page=2, to_page=src.page_count - 2)
    else:
        out.insert_pdf(src, from_page=1, to_page=src.page_count - 2)
    out.insert_pdf(c, from_page=1, to_page=1)
    assert out.page_count == src.page_count
    tmp = pdf.with_suffix(".tmp.pdf")
    out.save(tmp, garbage=4, deflate=True)
    src.close(); out.close()
    tmp.replace(pdf)
    print("  covers: house standard (front + back) from", cov.name)


def renders(pdf: pathlib.Path, pages=None, dpi=70):
    doc = pymupdf.open(pdf)
    idx = range(len(doc)) if pages is None else [p - 1 for p in pages]
    for i in idx:
        doc[i].get_pixmap(dpi=dpi).save(BUILD / f"p{i+1:02d}.png")
    return len(doc)


if __name__ == "__main__":
    pages = [int(x) for x in sys.argv[1:]] or None
    h = render_html()
    pdf = BUILD / "book.pdf"
    to_pdf(h, pdf)
    std_covers(pdf)
    n = renders(pdf, pages)
    print("pages:", n, "size MB:", round(pdf.stat().st_size / 1e6, 2))
