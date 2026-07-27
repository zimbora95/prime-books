"""Render the 5 Prime Books cover proposals to individual PDFs + PNGs.
Each proposal is a genuinely different layout, not one template with new art.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright
import fitz

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / 'Cover'
OUT.mkdir(parents=True, exist_ok=True)

FONTS = f"""
@font-face{{font-family:'Fraunces';src:url('{(ROOT/'fonts'/'Fraunces.ttf').as_uri()}')format('truetype');font-weight:100 900}}
@font-face{{font-family:'Space Grotesk';src:url('{(ROOT/'fonts'/'SpaceGrotesk.ttf').as_uri()}')format('truetype');font-weight:300 700}}
@font-face{{font-family:'Source Sans 3';src:url('{(ROOT/'fonts'/'SourceSans3.ttf').as_uri()}')format('truetype');font-weight:200 900}}
@font-face{{font-family:'JetBrains Mono';src:url('{(ROOT/'fonts'/'JetBrainsMono.ttf').as_uri()}')format('truetype');font-weight:100 800}}
"""

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
@page{size:210mm 270mm;margin:0}
html,body{width:210mm;height:270mm}
.c{width:210mm;height:270mm;position:relative;overflow:hidden}
.fr{font-family:'Fraunces',serif}
.sg{font-family:'Space Grotesk',sans-serif}
.ss{font-family:'Source Sans 3',sans-serif}
.jb{font-family:'JetBrains Mono',monospace}
"""

def art(name):
    return (OUT / 'art' / f'{name}.png').as_uri()

# ---------------------------------------------------------------- A
A = f"""<div class="c" style="background:#0E1330;color:#fff">
  <img src="{art('cov_a_circuitbloom')}" style="position:absolute;left:50%;top:44%;
      transform:translate(-50%,-50%);width:178mm;opacity:.95">
  <div style="position:absolute;inset:0;background:radial-gradient(115% 75% at 50% 42%,
      rgba(14,19,48,.06) 0%,rgba(14,19,48,.70) 56%,rgba(14,19,48,.98) 100%)"></div>
  <div style="position:absolute;inset:0;padding:19mm 19mm 21mm;display:flex;
      flex-direction:column;justify-content:space-between">
    <div style="display:flex;justify-content:space-between;align-items:flex-start">
      <div style="display:flex;align-items:center;gap:2.6mm">
        <span style="color:#C9A35C;font-size:13pt;line-height:1">&#10022;</span>
        <span class="sg" style="font-weight:600;font-size:9.6pt;letter-spacing:.30em">PRIME BOOKS</span>
      </div>
      <div class="sg" style="font-size:8pt;letter-spacing:.20em;text-transform:uppercase;
          color:rgba(255,255,255,.70);text-align:right;padding-top:1mm">Cambridge<br>Lower Secondary</div>
    </div>
    <div style="text-align:center;padding-bottom:4mm">
      <div class="sg" style="font-weight:600;font-size:8.6pt;letter-spacing:.34em;
          text-transform:uppercase;color:#C9A35C;margin-bottom:6mm">Computing &amp; Robotics</div>
      <h1 class="fr" style="font-variation-settings:'opsz' 144,'SOFT' 22,'WONK' 1;font-weight:600;
          font-size:60pt;line-height:56pt;letter-spacing:-.035em">Computing</h1>
      <div class="fr" style="font-variation-settings:'opsz' 144,'SOFT' 40,'WONK' 1;font-weight:700;
          font-size:78pt;line-height:72pt;color:#FF5A47;margin-top:1mm">7</div>
      <div style="width:30mm;height:1.4mm;background:#C9A35C;border-radius:1mm;margin:7mm auto 6mm"></div>
      <p class="ss" style="font-weight:300;font-size:12.4pt;line-height:17pt;
          color:rgba(255,255,255,.90);max-width:118mm;margin:0 auto">Programming, data and digital
          systems for curious minds. Ages 11&#8211;14.</p>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;
        border-top:.5pt solid rgba(255,255,255,.26);padding-top:5mm">
      <div class="sg" style="font-size:8.6pt;letter-spacing:.10em;color:rgba(255,255,255,.74)">
        Student&rsquo;s Book &middot; First edition</div>
      <div style="display:flex;align-items:center;gap:2.6mm">
        <span class="sg" style="font-weight:600;font-size:9.4pt;letter-spacing:.22em">PRIME SCHOOL</span>
        <span style="color:#C9A35C;font-size:8pt">&bull;</span>
        <span class="sg" style="font-size:8.4pt;color:rgba(255,255,255,.68)">primeschool.pt</span>
      </div>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- B
B = f"""<div class="c" style="background:#FBF8F1;color:#0E1330">
  <div style="position:absolute;left:0;top:0;width:100%;height:96mm;padding:19mm 19mm 0">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14mm">
      <div style="display:flex;align-items:center;gap:2.6mm">
        <span style="color:#C9A35C;font-size:13pt;line-height:1">&#10022;</span>
        <span class="sg" style="font-weight:600;font-size:9.6pt;letter-spacing:.30em;color:#0E1330">PRIME BOOKS</span>
      </div>
      <div class="sg" style="font-size:8pt;letter-spacing:.20em;text-transform:uppercase;
          color:#6B7196;text-align:right;padding-top:1mm">Cambridge Lower Secondary</div>
    </div>
    <div class="sg" style="font-weight:600;font-size:9pt;letter-spacing:.28em;
        text-transform:uppercase;color:#2B5BE8;margin-bottom:5mm">Computing &amp; Robotics</div>
    <div style="display:flex;align-items:baseline;gap:6mm">
      <h1 class="fr" style="font-variation-settings:'opsz' 144,'SOFT' 20,'WONK' 1;font-weight:600;
          font-size:62pt;line-height:58pt;letter-spacing:-.04em">Computing</h1>
      <span class="fr" style="font-variation-settings:'opsz' 144,'SOFT' 44,'WONK' 1;font-weight:700;
          font-size:62pt;line-height:58pt;color:#FF5A47">7</span>
    </div>
    <p class="ss" style="font-weight:300;font-size:12.2pt;line-height:16.4pt;color:#3A4166;
        max-width:120mm;margin-top:6mm">Programming, data and digital systems for curious minds.
        Ages 11&#8211;14.</p>
  </div>
  <img src="{art('cov_b_pixelwave')}" style="position:absolute;left:0;bottom:26mm;
      width:210mm;height:150mm;object-fit:cover">
  <div style="position:absolute;left:0;bottom:0;width:100%;height:26mm;background:#0E1330;
      display:flex;align-items:center;justify-content:space-between;padding:0 19mm">
    <span class="sg" style="font-size:8.6pt;letter-spacing:.10em;color:rgba(255,255,255,.74)">
      Student&rsquo;s Book &middot; First edition</span>
    <div style="display:flex;align-items:center;gap:2.6mm">
      <span class="sg" style="font-weight:600;font-size:9.4pt;letter-spacing:.22em;color:#fff">PRIME SCHOOL</span>
      <span style="color:#C9A35C;font-size:8pt">&bull;</span>
      <span class="sg" style="font-size:8.4pt;color:rgba(255,255,255,.66)">primeschool.pt</span>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- C
C = f"""<div class="c" style="background:#0E1330;color:#fff">
  <div style="position:absolute;left:0;top:0;width:64mm;height:270mm;background:#00A38C"></div>
  <img src="{art('cov_c_isoterminal')}" style="position:absolute;right:0;top:0;
      width:150mm;height:270mm;object-fit:cover;opacity:.94">
  <div style="position:absolute;right:0;top:0;width:150mm;height:270mm;
      background:linear-gradient(255deg,rgba(14,19,48,.30) 0%,rgba(14,19,48,.80) 78%)"></div>
  <div style="position:absolute;left:0;top:0;width:64mm;height:270mm;padding:19mm 8mm 21mm 15mm;
      display:flex;flex-direction:column;justify-content:space-between;z-index:3">
    <div>
      <div style="color:#0E1330;font-size:14pt;line-height:1;margin-bottom:3mm">&#10022;</div>
      <div class="sg" style="font-weight:700;font-size:8.6pt;letter-spacing:.24em;
          color:#0E1330;writing-mode:vertical-rl;text-orientation:mixed;margin-top:4mm">PRIME BOOKS</div>
    </div>
    <div>
      <div class="sg" style="font-weight:600;font-size:7.6pt;letter-spacing:.16em;
          text-transform:uppercase;color:rgba(14,19,48,.78);line-height:12pt">Cambridge<br>Lower<br>Secondary</div>
      <div style="width:16mm;height:1.2mm;background:#0E1330;border-radius:1mm;margin:5mm 0"></div>
      <div class="sg" style="font-size:7.6pt;letter-spacing:.06em;color:rgba(14,19,48,.78);
          line-height:11pt">Student&rsquo;s Book<br>First edition</div>
    </div>
  </div>
  <div style="position:absolute;left:64mm;top:0;right:0;height:270mm;padding:24mm 19mm 21mm 16mm;
      display:flex;flex-direction:column;justify-content:center;z-index:3">
    <div class="sg" style="font-weight:600;font-size:8.6pt;letter-spacing:.28em;
        text-transform:uppercase;color:#7FF0DC;margin-bottom:5mm">Computing &amp; Robotics</div>
    <h1 class="fr" style="font-variation-settings:'opsz' 120,'SOFT' 24,'WONK' 1;font-weight:600;
        font-size:46pt;line-height:44pt;letter-spacing:-.03em">Computing<br>
        <span style="color:#FF5A47;font-weight:700">Seven</span></h1>
    <div style="width:26mm;height:1.4mm;background:#C9A35C;border-radius:1mm;margin:7mm 0 5mm"></div>
    <p class="ss" style="font-weight:300;font-size:11.4pt;line-height:15.6pt;
        color:rgba(255,255,255,.90);max-width:98mm">Programming, data and digital systems
        for curious minds. Ages 11&#8211;14.</p>
    <div style="margin-top:auto;display:flex;align-items:center;gap:2.6mm">
      <span class="sg" style="font-weight:600;font-size:9pt;letter-spacing:.22em">PRIME SCHOOL</span>
      <span style="color:#C9A35C;font-size:8pt">&bull;</span>
      <span class="sg" style="font-size:8.2pt;color:rgba(255,255,255,.66)">primeschool.pt</span>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- D
D = f"""<div class="c" style="background:#FBF8F1;color:#0E1330">
  <div style="position:absolute;inset:11mm;border:.9pt solid #D8D0BF"></div>
  <img src="{art('cov_d_flowlines')}" style="position:absolute;left:50%;top:53%;
      transform:translate(-50%,-50%);width:126mm">
  <div style="position:absolute;inset:0;padding:19mm;display:flex;flex-direction:column;
      justify-content:space-between;align-items:center;text-align:center">
    <div style="width:100%;display:flex;justify-content:space-between;align-items:flex-start;
        padding:0 6mm">
      <div style="display:flex;align-items:center;gap:2.4mm">
        <span style="color:#C9A35C;font-size:12pt;line-height:1">&#10022;</span>
        <span class="sg" style="font-weight:600;font-size:9pt;letter-spacing:.30em">PRIME BOOKS</span>
      </div>
      <div class="sg" style="font-size:7.8pt;letter-spacing:.20em;text-transform:uppercase;
          color:#6B7196;padding-top:1mm">Cambridge Lower Secondary</div>
    </div>
    <div style="position:absolute;left:0;right:0;top:44mm;text-align:center">
      <div class="jb" style="font-size:8.4pt;letter-spacing:.30em;color:#FF5A47;
          margin-bottom:5mm">COMPUTING &amp; ROBOTICS</div>
      <h1 class="fr" style="font-variation-settings:'opsz' 144,'SOFT' 18,'WONK' 0;font-weight:500;
          font-size:52pt;line-height:50pt;letter-spacing:-.03em">Computing
          <span style="color:#FF5A47;font-weight:700">7</span></h1>
    </div>
    <div style="position:absolute;left:0;right:0;bottom:40mm;text-align:center;padding:0 30mm">
      <div style="width:22mm;height:.9mm;background:#C9A35C;border-radius:1mm;margin:0 auto 5mm"></div>
      <p class="ss" style="font-weight:300;font-size:11.6pt;line-height:16pt;color:#3A4166">
        Programming, data and digital systems for curious minds. Ages 11&#8211;14.</p>
    </div>
    <div style="width:100%;display:flex;justify-content:space-between;align-items:flex-end;
        padding:0 6mm">
      <span class="sg" style="font-size:8.4pt;letter-spacing:.10em;color:#6B7196">
        Student&rsquo;s Book &middot; First edition</span>
      <div style="display:flex;align-items:center;gap:2.4mm">
        <span class="sg" style="font-weight:600;font-size:9pt;letter-spacing:.22em">PRIME SCHOOL</span>
        <span style="color:#C9A35C;font-size:8pt">&bull;</span>
        <span class="sg" style="font-size:8.2pt;color:#6B7196">primeschool.pt</span>
      </div>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- E
E = f"""<div class="c" style="background:#0E1330;color:#fff">
  <img src="{art('cov_e_lightsignal')}" style="position:absolute;inset:0;width:210mm;
      height:270mm;object-fit:cover;opacity:.96">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,
      rgba(14,19,48,.86) 0%,rgba(14,19,48,.20) 42%,rgba(14,19,48,.90) 100%)"></div>
  <div style="position:absolute;left:19mm;top:19mm;right:19mm;display:flex;
      justify-content:space-between;align-items:flex-start">
    <div style="display:flex;align-items:center;gap:2.6mm">
      <span style="color:#C9A35C;font-size:13pt;line-height:1">&#10022;</span>
      <span class="sg" style="font-weight:600;font-size:9.6pt;letter-spacing:.30em">PRIME BOOKS</span>
    </div>
    <div class="sg" style="font-size:8pt;letter-spacing:.20em;text-transform:uppercase;
        color:rgba(255,255,255,.72);text-align:right;padding-top:1mm">Cambridge Lower Secondary</div>
  </div>
  <div style="position:absolute;left:19mm;right:19mm;bottom:21mm">
    <div style="display:flex;gap:1.6mm;margin-bottom:7mm">
      <span style="display:block;width:9mm;height:1.5mm;background:#C9A35C;border-radius:1mm"></span>
      <span style="display:block;width:3mm;height:1.5mm;background:#C9A35C;border-radius:1mm"></span>
      <span style="display:block;width:9mm;height:1.5mm;background:#FF5A47;border-radius:1mm"></span>
      <span style="display:block;width:3mm;height:1.5mm;background:#FF5A47;border-radius:1mm"></span>
      <span style="display:block;width:3mm;height:1.5mm;background:rgba(255,255,255,.55);border-radius:1mm"></span>
    </div>
    <div class="sg" style="font-weight:600;font-size:8.6pt;letter-spacing:.30em;
        text-transform:uppercase;color:#FFD9A8;margin-bottom:5mm">Computing &amp; Robotics</div>
    <h1 class="fr" style="font-variation-settings:'opsz' 144,'SOFT' 26,'WONK' 1;font-weight:600;
        font-size:56pt;line-height:52pt;letter-spacing:-.035em">Computing
        <span style="color:#FF5A47;font-weight:700">7</span></h1>
    <p class="ss" style="font-weight:300;font-size:12pt;line-height:16.4pt;
        color:rgba(255,255,255,.90);max-width:126mm;margin-top:6mm">Programming, data and digital
        systems for curious minds. Ages 11&#8211;14.</p>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;
        border-top:.5pt solid rgba(255,255,255,.26);padding-top:5mm;margin-top:8mm">
      <span class="sg" style="font-size:8.6pt;letter-spacing:.10em;color:rgba(255,255,255,.74)">
        Student&rsquo;s Book &middot; First edition</span>
      <div style="display:flex;align-items:center;gap:2.6mm">
        <span class="sg" style="font-weight:600;font-size:9.4pt;letter-spacing:.22em">PRIME SCHOOL</span>
        <span style="color:#C9A35C;font-size:8pt">&bull;</span>
        <span class="sg" style="font-size:8.4pt;color:rgba(255,255,255,.68)">primeschool.pt</span>
      </div>
    </div>
  </div>
</div>"""

PROPOSALS = [
    ('01_circuit-bloom',   'Circuit Bloom',    A),
    ('02_pixel-wave',      'Pixel Wave',       B),
    ('03_split-terminal',  'Split Terminal',   C),
    ('04_flow-state',      'Flow State',       D),
    ('05_light-signal',    'Light Signal',     E),
]

def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 794, 'height': 1021})
        for slug, name, body in PROPOSALS:
            html = (f'<!doctype html><html><head><meta charset="utf-8">'
                    f'<style>{FONTS}{BASE}</style></head><body>{body}</body></html>')
            tmp = ROOT / f'_cov_{slug}.html'
            tmp.write_text(html, encoding='utf-8')
            pg.goto(tmp.resolve().as_uri(), wait_until='networkidle')
            pg.wait_for_timeout(900)
            pdf = OUT / f'{slug}.pdf'
            pg.pdf(path=str(pdf), width='210mm', height='270mm', print_background=True,
                   prefer_css_page_size=True,
                   margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
            d = fitz.open(pdf)
            d[0].get_pixmap(dpi=130).save(str(OUT / f'{slug}.png'))
            print(f'  {name:16s} -> {pdf.name}  {len(d)}pp '
                  f'{d[0].rect.width:.0f}x{d[0].rect.height:.0f}pt')
            d.close()
            tmp.unlink()
        b.close()

if __name__ == '__main__':
    main()
