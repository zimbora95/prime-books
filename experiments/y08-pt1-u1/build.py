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
    html = html.replace("{{SITE}}", SITE).replace("{{SLUG}}", SLUG)
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
        pg.emulate_media(media="print")
        report = pg.evaluate("""() => {
          const mm = 96/25.4, out = [];
          document.querySelectorAll('.page').forEach((p, i) => {
            const inn = p.querySelector('.inner'); if (!inn) return;
            const ib = inn.getBoundingClientRect();
            let low = ib.top;
            inn.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height) low = Math.max(low, r.bottom); });
            out.push([i+1, ((ib.bottom - low)/mm).toFixed(1)]);
          });
          return out;
        }""")
        for n, free in report:
            flag = "OVERFLOW" if float(free) < -0.5 else ("loose" if float(free) > 18 else "")
            print(f"  p{n:02d} free {free:>6} mm {flag}")
        pg.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
        b.close()


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
    n = renders(pdf, pages)
    print("pages:", n, "size MB:", round(pdf.stat().st_size / 1e6, 2))
