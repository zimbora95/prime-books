import build,subprocess,re,os,json,html as H
JS=r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();let bot=0,right=0;let tipTop=null;
p.querySelectorAll('.tip,[style*="bottom:21mm"]').forEach(t=>{const b=t.getBoundingClientRect();tipTop=tipTop===null?b.top-r.top:Math.min(tipTop,b.top-r.top)});
p.querySelectorAll('*').forEach(el=>{if(el.closest('.folio,.tab,.run,.p-open,.tip,[style*="bottom:21mm"]'))return;const b=el.getBoundingClientRect();if(!b.height||el.children.length)return;bot=Math.max(bot,b.bottom-r.top);right=Math.max(right,b.right-r.left)});
out.push([i+1,mm(bot),tipTop===null?null:mm(tipTop),mm(right)])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},500)})</script>"""
html=open("build/unit.html").read()
open("build/chk.html","w").write(html.replace("</body>",JS+"</body>"))
r=subprocess.run([build.CHROME,"--headless=new","--no-sandbox","--disable-gpu","--virtual-time-budget=8000","--window-size=794,1123","--dump-dom","file://"+os.path.abspath("build/chk.html")],capture_output=True,text=True,timeout=180)
m=re.search(r'<pre id="report">(.*?)</pre>',r.stdout,re.S)
print("page contentBottom tipTop maxRight  (page 297x210; usable bottom ~280, right<=194)")
for row in json.loads(H.unescape(m.group(1))): print(row)
