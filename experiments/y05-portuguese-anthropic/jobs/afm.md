# Job afm: book matter — Portuguese covers, solutions in the back matter, no .vercel, reassembly
You are a headless build agent. Root /root/prime-books/experiments/y05-portuguese-anthropic; Python /root/.venvs/y05exp/bin/python. Read
/root/prime-books/experiments/y05-portuguese-anthropic/BRIEF-no-own-audio.md (the owner's rules), the fm report jobs/logs/fm.report.md, and fm/*.py.
Your folder: fm/ (edit only fm/, plus you may read everything). Seven other agents (jobs a1–a7) are
right now replacing all self-recorded audio and .vercel QR codes inside the units; do not touch unit
folders.

TASKS
1. COVERS in Portuguese. The owner chose the front and back cover of the master
   /root/prime-books/public/library/y05-portuguese/book.pdf (page 1 and last page) — same art, same
   layout — but every word must be pt-PT: front «Português» / «5.º Ano» / «Manual do aluno» in place of
   «Portuguese 1st Language» / «Year 5» / «Student Manual» (page 1 carries live text spans over the art:
   inspect with get_text('dict') and match font, size, colour and position; fonts are in
   /root/prime-books/tools/cover_assets/). The back cover is raster (text baked in): rebuild it on the
   same art in Portuguese — find how it was made (tools/cover_std.py, tools/cover_assets/back_copy.json,
   back art files) and re-render ONLY this book's back with Portuguese copy: «PRIME BOOKS», title
   «Português», «5.º Ano · Manual do aluno», the existing Portuguese blurb, card «NESTE LIVRO» with the
   bullets, footer «Prime Books · Português» / «9–10 anos · 1.º e 2.º Ciclos» (or the house pt-PT
   equivalent of «Ages 9–10 · Upper Primary» — decide sensibly) / «primeschool.pt». Keep the magenta
   stripe, the sketch art and the geometry. Read the house references
   /root/.hermes/skills/productivity/prime-books-book-builder/references/back-cover-standard-prime-school-press.md
   and cover-wrap-raster-edits.md. These two pages become the book's first and last pages at assembly
   (make assemble.py take them instead of fm's own cover pages; the covers are A4-fitted by scaling to
   the width and cropping the height symmetrically, ~2.3 mm each).
2. SOLUTIONS move into the book: add back-matter pages «Soluções» built from every unit's solutions
   file (site/solucoes.html for Unit 1, uN/site/solucoes-uN.html) and «Textos para o professor ler em voz
   alta» from any uN/site/textos-professor.md the unit agents write. Style = house back matter (like the
   Year 9 edition /root/prime-books/public/library/y09-portuguese-anthropic/book.pdf, «Fim do livro ·
   Soluções»). Build them provisionally now, then again after the unit agents finish.
3. NO .vercel anywhere and NO self-recorded audio: update «Recursos digitais» (QR index: only the public
   QR codes actually in the units, re-harvested at the end), the imprint and the colophon (remove the
   synthetic-voices credits and any audio counts), «Como usar este livro» (the QR/áudio explanation must
   describe public links, not our audio), the contents, the glossary page refs. The book says «5.º Ano»,
   never «Year 5»; the reading log (p. vii) has exactly ONE «Por minha conta:» row (already set in
   build.py own_rows=1 — keep it).
4. PAGE COUNT: the volume must stay EVEN with no blank pages; back matter grows by the solutions pages.
   Update plan.py/assemble.py expectations, the contents and every cross-reference.
5. TIMING: do tasks 1–4 now with provisional data; then wait for the unit agents (jobs/logs/a1..a7.done,
   check every ≤10 min with foreground sleeps, max 4 h), re-harvest, rebuild, run assemble.py and qa.py.
6. QA of the assembled book: page count even; every contents entry spot-checked; decode EVERY QR in the
   whole book and prove none contains "vercel" and all return HTTP 200; search every page's text for
   "vercel", "Year", "YEAR", "Ouvir a faixa", "vozes sintéticas" (must be none); fonts only
   Fraunces/Figtree/DM Mono/Caveat + the cover's Poppins/Andika, Type0 embedded, no Type3; vision-check
   the covers, the new back-matter pages and p. vii. Save before/after PNGs to fm/qa-evidence/.
Do NOT publish (nothing under public/, no git). Report to jobs/logs/afm.report.md, then stop.
