# Brief — replace every self-recorded audio and every .vercel link (Português · 5.º Ano)

Root: /root/prime-books/experiments/y05-portuguese-anthropic
Python (all deps, Chromium via each build.py): /root/.venvs/y05exp/bin/python
Read first: BRIEF-units-2-3.md (house design/brief) and your unit's report in jobs/logs/<unit>.report.md.

## The owner's decision (non-negotiable)
1. NO audio recorded by us. Every «Ouvir / faixa / QR áudio» block that plays one of our own
   edge-tts tracks (URLs …/library/y05-portuguese-anthropic/audio/…) must go.
2. NO QR code or printed URL may point to prime-books-pi.vercel.app (or any *.vercel.app). That
   site is temporary and will disappear. This includes the «Soluções (professor)» QR at the end of
   each unit: remove it (the solutions move into the book's back matter — another job does that;
   in its place put a short line «Soluções: no fim do livro.» or use the space for content).
3. REDO each affected activity with something else, preferring REAL PUBLIC resources:
   audio/video/pages on stable public sites — RTP Ensina (ensina.rtp.pt), RTP Arquivos, Plano
   Nacional de Leitura (pnl2027.gov.pt), Casa da Leitura, DGE, Biblioteca Nacional, museums,
   municipalities, Ciência Viva, Infopédia, Priberam, Wikipédia (pt), official YouTube channels
   of public institutions. Verify each URL (HTTP 200, content matches) with web_extract/curl and
   READ what it actually contains: questions you write about a resource must be answerable from
   that resource. Never invent the content of a video/audio you could not verify — if you can
   only verify the title/description, write open questions accordingly.
   Where no fitting public audio exists, redesign the activity (e.g. reading aloud in pairs,
   the teacher reads the text printed in the book, a dramatised reading, a different oral task)
   so it still teaches the same skill. Listening tests (compreensão do oral) may become «o
   professor lê em voz alta o texto» ONLY if the text is then printed for the teacher — do not
   print it on the pupil's test page; instead write it into <unit>/site/textos-professor.md (the
   back-matter job collects these files).
4. Keep every page full and composed exactly in the house design; keep the unit's page count
   and folios exactly as they are; keep activity numbering coherent; no text in images.
5. pt-PT (AO90). The book says «5.º Ano» (labels) / «5.º ano» (prose), never «Year 5».
6. Keep existing QR codes that already point to public sites (Priberam, Museu da
   Biodiversidade, Município de Barcelos, DGE, TNDM, IP Património …) — re-verify they load.
   New QRs: segno with viewBox + 4-module quiet zone, as in the unit's build.py.
7. Update the unit's solutions file (<unit>/site/solucoes-<unit>.html, or site/solucoes.html for
   Unit 1) to match the new activities: accepted answers for every changed item.

## Workspace rules
Edit ONLY your unit folder. Never touch other unit folders, fm/, public/, fonts/, git, skills or
memory. Delete nothing outside your folder. You may delete your unit's own audio/*.mp3 files and
the audio section of its audio_scripts.py (they are no longer used).

## QA before you report (mandatory)
Rebuild; metrics clean (no overflow/collision); render every CHANGED page ≥130 dpi and review it
with vision + measurement; decode every QR in the unit PDF (tiled cv2 at 200 dpi) and prove that
NONE contains "vercel" and every decoded URL returns HTTP 200; grep the unit sources for
"vercel", "audio/", "Year " — must be zero hits in anything printed; fonts only Fraunces/Figtree/
DM Mono/Caveat (Type0), no Type3, no fallback fonts; page count unchanged. Save before/after PNGs
of changed pages in <unit>/qa-evidence/ .
Report to jobs/logs/<job>.report.md: every replaced audio/QR (page, old → new, URL, how verified),
every redesigned activity, solutions updates, final checks, honest leftovers.
