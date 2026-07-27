<!-- unit: u1 -->
<!--html
<section class="sheet bc">
  <div class="bc-top">
    <div class="bc-mark">
      <span class="bc-star">✦</span>
      <span class="bc-word">PRIME BOOKS</span>
    </div>
    <div class="bc-stage">Cambridge Lower Secondary</div>
  </div>

  <div class="bc-body">
    <h2 class="bc-h">Computing <span>7</span></h2>
    <p class="bc-lead">Somebody had to write the software in your pocket.
    This year, that somebody starts to be you.</p>

    <p class="bc-p">A complete first year of computing, built around six units that move from
    your first line of typed Python to designing an artificial intelligence of your own. Every
    idea is introduced through a real situation, tested with real data, and finished with a
    project worth keeping.</p>

    <div class="bc-grid">
      <div class="bc-u"><b>7.1</b>Block it out: moving from blocks to text</div>
      <div class="bc-u"><b>7.2</b>Decomposing problems: creating a smart solution</div>
      <div class="bc-u"><b>7.3</b>Connections are made: accessing the internet</div>
      <div class="bc-u"><b>7.4</b>The power of data: using data modelling</div>
      <div class="bc-u"><b>7.5</b>Living with AI: digital data</div>
      <div class="bc-u"><b>7.6</b>Sequencing and pattern recognition</div>
    </div>

    <div class="bc-feats">
      <div class="bc-f"><span>✦</span>Warm ups, scenarios and challenges in every unit</div>
      <div class="bc-f"><span>▲</span>Six full final projects with marking grids</div>
      <div class="bc-f"><span>●</span>Test plans that teach you to break your own work</div>
      <div class="bc-f"><span>▮</span>A glossary of 140 terms</div>
    </div>
  </div>

  <div class="bc-foot">
    <div class="bc-blurb">
      <p>Written by the Computing &amp; Robotics faculty at Prime School, an international
      Cambridge school in Cascais, Portugal.</p>
      <p class="bc-note">An independent publication. Not endorsed by Cambridge Assessment
      International Education.</p>
    </div>
    <div class="bc-meta">
      <div class="bc-isbn">
        <div class="bc-bars">
          <span></span><span></span><span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="bc-num">978-989-0000-07-1</div>
      </div>
      <div class="bc-school">
        <span class="bc-sname">PRIME SCHOOL</span>
        <span class="bc-web">primeschool.pt</span>
      </div>
    </div>
  </div>
</section>

<style>
.bc{background:#0E1330;color:#fff;padding:20mm 20mm 22mm;
  display:flex;flex-direction:column;position:relative;overflow:hidden}
.bc::before{content:'';position:absolute;right:-40mm;top:-40mm;width:150mm;height:150mm;
  border-radius:50%;background:rgba(43,91,232,.13)}
.bc::after{content:'';position:absolute;left:-30mm;bottom:-50mm;width:130mm;height:130mm;
  border-radius:50%;background:rgba(0,163,140,.10)}
.bc-top,.bc-body,.bc-foot{position:relative;z-index:2}
.bc-top{display:flex;justify-content:space-between;align-items:flex-start}
.bc-mark{display:flex;align-items:center;gap:2.6mm}
.bc-star{color:#C9A35C;font-size:12pt;line-height:1}
.bc-word{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:9.4pt;
  letter-spacing:.30em}
.bc-stage{font-family:'Space Grotesk',sans-serif;font-size:8pt;letter-spacing:.20em;
  text-transform:uppercase;color:rgba(255,255,255,.68);padding-top:1mm}
.bc-body{margin-top:auto;margin-bottom:auto;padding:8mm 0}
.bc-h{font-family:'Fraunces',serif;font-variation-settings:'opsz' 120,'SOFT' 24,'WONK' 1;
  font-weight:600;font-size:38pt;line-height:40pt;letter-spacing:-.025em;margin:0 0 5mm}
.bc-h span{color:#FF5A47}
.bc-lead{font-family:'Fraunces',serif;font-style:italic;
  font-variation-settings:'opsz' 44,'SOFT' 36;font-size:13.4pt;line-height:18pt;
  color:#fff;margin:0 0 5mm;max-width:140mm}
.bc-p{font-size:10.2pt;line-height:14.6pt;color:rgba(255,255,255,.86);margin:0 0 7mm;
  max-width:145mm}
.bc-grid{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm 7mm;margin-bottom:7mm}
.bc-u{font-size:9pt;line-height:12pt;color:rgba(255,255,255,.88);
  padding-left:11mm;position:relative}
.bc-u b{position:absolute;left:0;top:0;font-family:'Space Grotesk',sans-serif;
  font-weight:700;font-size:8.6pt;color:#7FB0FF}
.bc-feats{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm 7mm;
  border-top:.5pt solid rgba(255,255,255,.24);padding-top:5mm}
.bc-f{font-family:'Space Grotesk',sans-serif;font-size:8.6pt;line-height:11.4pt;
  color:rgba(255,255,255,.82);padding-left:6mm;position:relative}
.bc-f span{position:absolute;left:0;top:0;color:#C9A35C;font-size:8pt}
.bc-foot{display:flex;justify-content:space-between;align-items:flex-end;gap:10mm;
  border-top:.5pt solid rgba(255,255,255,.24);padding-top:5mm}
.bc-blurb{max-width:96mm}
.bc-blurb p{font-size:8.2pt;line-height:11pt;color:rgba(255,255,255,.72);margin:0 0 2mm}
.bc-note{color:rgba(255,255,255,.52) !important;font-size:7.4pt !important}
.bc-meta{display:flex;flex-direction:column;align-items:flex-end;gap:4mm}
.bc-isbn{background:#fff;border-radius:1mm;padding:2.6mm 3mm 2mm;text-align:center}
.bc-bars{display:flex;align-items:flex-end;gap:.5mm;height:11mm}
.bc-bars span{display:block;width:.6mm;background:#0E1330;height:100%}
.bc-bars span:nth-child(3n){width:1.1mm}
.bc-bars span:nth-child(4n){height:86%}
.bc-bars span:nth-child(5n){width:.4mm}
.bc-num{font-family:'JetBrains Mono',monospace;font-size:7.2pt;color:#0E1330;
  margin-top:1.4mm;letter-spacing:.04em}
.bc-school{display:flex;flex-direction:column;align-items:flex-end;gap:.8mm}
.bc-sname{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:9.6pt;
  letter-spacing:.22em}
.bc-web{font-family:'Space Grotesk',sans-serif;font-size:8pt;
  color:rgba(255,255,255,.62);letter-spacing:.06em}
</style>
-->
