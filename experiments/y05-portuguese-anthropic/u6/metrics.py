import build, subprocess, re, os, json, html as H
# per-page probe: [folio, contentBottom mm, tipTop mm, maxRight mm, overflowing boxes]
JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();let bot=0,right=0;let tipTop=null;const ov=[];
p.querySelectorAll('.pin-b').forEach(t=>{const b=t.getBoundingClientRect();tipTop=tipTop===null?b.top-r.top:Math.min(tipTop,b.top-r.top)});
p.querySelectorAll('*').forEach(el=>{if(el.closest('.folio,.tab,.run,.p-open,.pin-b'))return;const b=el.getBoundingClientRect();if(!b.height||el.children.length)return;bot=Math.max(bot,b.bottom-r.top);right=Math.max(right,b.right-r.left)});
p.querySelectorAll('*').forEach(el=>{if(el.scrollWidth>el.clientWidth+2&&getComputedStyle(el).overflow!=='visible'&&!el.classList.contains('page'))ov.push('X:'+(el.className||el.tagName));if(el.scrollHeight>el.clientHeight+2&&getComputedStyle(el).overflow!=='visible'&&!el.classList.contains('page'))ov.push('Y:'+(el.className||el.tagName))});
const det=[];if(DETAIL.includes(i+113))p.querySelectorAll('.sec,.it,.dq,.xh,.art-box,.story,.wr,.plan').forEach(e=>{const b=e.getBoundingClientRect();det.push((e.className+(e.querySelector('.n')?'#'+e.querySelector('.n').textContent:''))+':'+mm(b.top-r.top)+'-'+mm(b.bottom-r.top))});
out.push([i+113,mm(bot),tipTop===null?null:mm(tipTop),mm(right),[...new Set(ov)].slice(0,5),det])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},500)})</script>"""
import sys
DET = [int(a) for a in sys.argv[1:]]
html = open("build/unit.html").read()
open("build/chk.html", "w").write(html.replace("</body>", JS.replace("DETAIL", json.dumps(DET)) + "</body>"))
r = subprocess.run([build.CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + os.path.abspath("build/chk.html")],
                   capture_output=True, text=True, timeout=600)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
print("folio contentBottom tipTop maxRight overflow  (page 297x210; content bottom <= ~270, right <= 194)")
for row in json.loads(H.unescape(m.group(1))):
    det = row.pop()
    for d in det: print('     ', d)
    flag = "  <-- LOW" if row[1] > 272 else ("  <-- short" if row[1] < 240 else "")
    if row[2] is not None and row[1] > row[2] - 2: flag += "  <-- TIP COLLISION"
    print(row, flag)
