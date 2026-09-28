# Audio for the QR codes of Unit 2 — «Texto Narrativo — Lugar, Tempo e Memória».
# The spoken text is read straight from the page sources (src/pages-*.html), so the
# recordings can never drift from the printed text.  Extracts of copyrighted works
# (2.5 Sophia, 2.6 Ondjaki) are NOT recorded.
# Run with the experiment venv:  python audio_scripts.py [name ...]  -> writes ./audio/u2-*.mp3
import asyncio, html, os, re, subprocess, sys, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"


def paras(fname, container_classes=("story", "dlg"), upto=None):
    """Paragraphs inside story/dialogue containers, in page order (optionally stop at a marker)."""
    src = open(os.path.join(HERE, "src", fname), encoding="utf-8").read()
    if upto:
        src = src[:src.index(upto)]
    out = []
    pat = r'<div class="(?:[^"]*\b(?:%s)\b[^"]*)"[^>]*>(.*?)\n\s*</div>' % "|".join(container_classes)
    for block in re.findall(pat, src, re.S):
        for cls, body in re.findall(r'<p(?: class="([^"]*)")?>(.*?)</p>', block, re.S):
            body = re.sub(r'<span class="hour">([^<]*)</span>', "", body)
            txt = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
            txt = re.sub(r"\s+", " ", txt)
            if txt:
                out.append((cls or "", txt))
    return out


def narrate(voice, pitch, rate, ps, pause=0.7):
    return [(voice, pitch, rate, t, pause) for _, t in ps]


def dialogue(ps):
    """Two voices: Raquel narrates and plays Carolina (lighter, quicker); Duarte plays the avô."""
    NARR = (R, "+0Hz", "-6%")
    who = {"A": (R, "+22Hz", "+2%"), "B": (D, "-4Hz", "-10%")}
    segs = []
    for cls, t in ps:
        if cls in who and t.startswith("—"):
            parts = [s.strip() for s in re.split(r"\s—\s|^—\s", t) if s.strip()]
            # parts alternate: speech, narrator tag, speech, ...
            for i, s in enumerate(parts):
                v = who[cls] if i % 2 == 0 else NARR
                segs.append((*v, s, 0.35))
            segs[-1] = (*segs[-1][:4], 0.8)
        else:
            segs.append((*NARR, t, 0.8))
    return segs


def tracks():
    lenda = paras("pages-02-lenda.html")
    viagem = paras("pages-03-viagem.html")
    bio = paras("pages-04-bio.html", upto="<!-- ======================= 37")
    pardais = paras("pages-08-problema.html", upto="<!-- ======================= 54")
    mist = paras("pages-09-misterio.html", upto="<!-- ======================= 58")
    reveal = re.search(r'<div class="upside"[^>]*>Revelação — (.*?)</div>',
                       open(os.path.join(HERE, "src", "pages-09-misterio.html"), encoding="utf-8").read(), re.S).group(1)
    ele = paras("pages-10-falas.html", ("dlg",), upto="<!-- ======================= 61")
    return {
        "u2-01-lenda-galo-barcelos":
            [(D, "+0Hz", "-8%", "A Lenda do Galo de Barcelos. Lenda tradicional portuguesa.", 1.2)] + narrate(D, "+0Hz", "-8%", lenda),
        "u2-02-relato-viagem-sintra":
            [(R, "+0Hz", "-6%", "Um dia em Sintra. Relato de viagem da Inês.", 1.2)] + narrate(R, "+10Hz", "-6%", viagem),
        "u2-03-biografia-aristides":
            [(D, "+0Hz", "-8%", "O cônsul que disse sim. Biografia de Aristides de Sousa Mendes.", 1.2)] + narrate(D, "+0Hz", "-8%", bio),
        "u2-04-os-pardais-da-horta":
            [(R, "+0Hz", "-6%", "Os Pardais da Horta.", 1.2)] + narrate(R, "+0Hz", "-6%", pardais),
        "u2-05-o-misterio-das-coisas-de-la":
            [(D, "+0Hz", "-8%", "O Mistério das Coisas de Lã.", 1.2)] + narrate(D, "+0Hz", "-8%", mist)
            + [(R, "+0Hz", "-6%", "Já resolveste o mistério? Então, ouve a revelação.", 1.5),
               (D, "+0Hz", "-8%", re.sub(r"\s+", " ", reveal).strip(), 1.0)],
        "u2-06-no-eletrico-28":
            [(R, "+0Hz", "-6%", "No Elétrico 28. Uma história contada a duas vozes.", 1.2)] + dialogue(ele),
    }


async def seg(voice, pitch, rate, text, path):
    await edge_tts.Communicate(text, voice, pitch=pitch, rate=rate).save(path)


async def main(only):
    os.makedirs(OUT, exist_ok=True)
    for name, parts in tracks().items():
        if only and name not in only:
            continue
        with tempfile.TemporaryDirectory(dir=os.path.join(HERE, "build")) as td:
            files = []
            for i, (v, p, r, t, pause) in enumerate(parts):
                f = os.path.join(td, f"{i:03d}.mp3")
                for attempt in range(4):
                    try:
                        await seg(v, p, r, t, f)
                        break
                    except Exception as e:  # transient network errors
                        if attempt == 3:
                            raise
                        await asyncio.sleep(3 * (attempt + 1))
                s = os.path.join(td, f"{i:03d}s.mp3")
                subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                                "anullsrc=r=24000:cl=mono", "-t", str(pause), "-q:a", "9", s], check=True)
                files += [f, s]
            lst = os.path.join(td, "list.txt")
            with open(lst, "w") as fh:
                fh.writelines(f"file '{f}'\n" for f in files)
            out = os.path.join(OUT, name + ".mp3")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                            "-ar", "24000", "-ac", "1", "-b:a", "64k", out], check=True)
            print(name, len(parts), "segments", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    if "--dry" in sys.argv:
        for n, ps in tracks().items():
            print("==", n, len(ps))
            for p in ps:
                print("  ", p[0][6:12], p[1], "|", p[3][:110])
    else:
        asyncio.run(main(set(a for a in sys.argv[1:])))
