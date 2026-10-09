
import build, subprocess, re, os, json, html as H, sys
JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const px=96/25.4;const mm=v=>Math.round(v/px*10)/10;const out={};
document.querySelectorAll('.page').forEach((p,pi)=>{const R=p.getBoundingClientRect();const items=[];
 const tw=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);let n;while(n=tw.nextNode()){if(!n.textContent.trim())continue;if(n.parentElement.closest('.folio,.run,.tab,.mk'))continue;const r=document.createRange();r.selectNodeContents(n);for(const b of r.getClientRects()){if(b.width>0)items.push({t:'txt',l:b.left,r:b.right,top:b.top,b:b.bottom,s:n.textContent.trim().slice(0,30)})}}
 const W=[];p.querySelectorAll('.ln,.fill,.vf td.cor span,.xh-f span i,.refl .r span').forEach(e=>{const b=e.getBoundingClientRect();if(!b.width)return;W.push({t:e.className||e.tagName,l:b.left,r:b.right,top:b.top,b:b.bottom,e:e})});
 const all=items.concat(W);const res=[];
 W.forEach(w=>{let best=null;all.forEach(o=>{if(o===w)return;const ov=Math.min(o.r,w.r)-Math.max(o.l,w.l);if(ov<2)return;if(o.b<=w.top+1.5 || (o.t!=='txt'&&o.b<w.b-3)){ if(o.b< w.b-3 && (best===null||o.b>best.b))best=o;}});
  const ctx=(w.e.closest('.it')&&w.e.closest('.it').querySelector('.n'))?w.e.closest('.it').querySelector('.n').textContent:'';
  res.push([ctx,w.t,mm(w.b-R.top),best?mm(w.b-best.b):null,best?(best.t==='txt'?best.s:best.t):'',mm(w.r-w.l)])});
 out[pi+113]=res});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},500)})</script>"""
html = open("build/unit.html").read()
open("build/chk2.html", "w").write(html.replace("</body>", JS + "</body>"))
r = subprocess.run([build.CHROME, "--headless", "--no-sandbox", "--disable-gpu","--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + os.path.abspath("build/chk2.html")],capture_output=True, text=True, timeout=600)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
d=json.loads(H.unescape(m.group(1)))
json.dump(d,open('qa/lines.json','w'))
lim=float(sys.argv[1]) if len(sys.argv)>1 else 7
for pg,rows in d.items():
    for row in rows:
        if row[3] is not None and row[3]<lim: print(pg,row)
