# Report: *Rua das Palavras*, Português (Língua Materna) Year 4, Unidade 1

**Status:** v2 rebuilt with **Beatrix Potter-style animal illustrations** (all 14 images regenerated from a new animal cast sheet), and ready for your approval. The v1 human-cast version is archived in `archive-v1-human/`. Nothing has been committed or pushed.

- **Pages:** 24 (A4 portrait, an even count).
  - 1 cover, 1 cast page, 1 full-bleed opener, 1 unit map.
  - 16 pupil pages, 1 project page, 1 self-assessment page.
  - 2 teacher-notes pages.
- **Files**
  - Publish folder: `public/library/y04-portuguese-anthropic/`, containing `book.pdf` (18.3 MB), `cover.webp`, `preview/` and `audio/`. A new row has been added to `public/library.json`, with additions only.
  - Print file with 3 mm bleed: `experiments/y04-pt-u1/build/unit1-print.pdf` (215.9 × 303 mm).
  - Renders of every page: `renders/unit1/p01–p24.png`. Contact sheet: `renders/contact-sheet.png`.
  - Prototype before and after renders: `renders/proto-v1/`, `renders/proto-spread-v1…v3.png`.
- **Link (after deploy):** https://prime-books-pi.vercel.app/finished/book/y04-portuguese-anthropic

## Learning goals covered (AE 3.º ano, plus one 4.º ano extension)
| Domain | Goal | Pages |
|---|---|---|
| Oralidade | Select and record the relevant information from something heard (the radio news, with a QR audio) | 11 |
| Leitura | Tell apart the carta, convite, notícia and banda desenhada by their structure and purpose | 7–14 |
| Leitura | Read aloud with suitable intonation (the story, the comic, three voices for three sentence types) | 6, 13, 15 |
| Educação Literária | Predict a story from its title and illustration | 5–6 |
| Escrita | Write an invitation, a letter and an opinion (plan, write, revise) | 10, 19–20 |
| Gramática | Declarative, interrogative and exclamative sentences; affirmative and negative sentences | 15–17 |
| Escrita | Punctuation: . ? ! , : — | 18 |
| Extension ★★★ | Fact versus opinion (4.º ano) | 12 |

## Checks run
- **Overflow:** 0 overflow, overlap or spill errors across all 24 pages, checked by an automated DOM checker (`build/build.py`).
- **Fonts:** only embedded TrueType (Andika, Fraunces static instances, Patrick Hand). There are no Type3 or fallback fonts.
- **Visual review:** every page was checked by vision in 4-page strips, and the defects it found were fixed: the cover subtitle over foliage, the map path crossing labels, the story running into the "Depois de ler" section, the invitation card overlapping its tasks, the table heights and the punctuation glyph wrap.
- **Language:** PT-PT spelling following AO90. A scan for Brazilian forms found none.
- **QR codes:** both decode to the right URL from the printed page. The MP3s are in the publish folder, but they will **return 404 until the site is deployed**.

## Whole book — 168 pages (assembled 2026-09-28)
- Front matter: cover (p. 1), «Bem-vindo à Rua do Limoeiro» (p. 2), Índice (pp. 3–4).
- Units:
  - U1: pp. 5–26
  - U2: pp. 27–75
  - U3: pp. 76–99
  - U4: pp. 100–121
  - U5: pp. 122–144
  - U6: pp. 145–156
  - U7: pp. 157–164
- Back matter: glossary (pp. 165–166), credits (p. 167), back cover (p. 168).
- Teacher notes: compiled from `notes/*.md` by `build/compile_notes.py`. Page insertions: `build/insert_pages.py`, with backups in `build/pages-before-insert-*`.
- QA:
  - full build overflow-free (the remaining "past box" entries are deliberate margin bleeds of faded vignettes: pp. 30, 70, 136, 137);
  - contact-sheet vision pass: no gross defects;
  - all 6 QR codes decode to the site audio URLs, and all 5 MP3s are copied to the publish folder.
- Published locally:
  - `public/library/y04-portuguese-anthropic/book.pdf`: 168 pp., 21.15 MB, Ghostscript 200 dpi web version of `build/unit1.pdf`;
  - cover.webp and preview/;
  - `library.json`: pages 168, mb 21.15, display name «Português · Year 4 — Rua das Palavras».
- Not committed or pushed. The live site shows the old 24-page file until the user deploys.
- Builder job reports: `jobs/logs/*.report.md`.

## Revision 2026-09-28 (owner requests)
- **Covers:** the front and back covers are now the house covers of `y04-portuguese` (pages 1 and 114 of that master), inserted as-is (`build/finalize.py`).
- **Imprint:** a standard house imprint page is now p. 2. The former «Ficha técnica e créditos» page was folded into it (Texts and Credits rows), so the book stays at 168 pages.
- **US Letter:** the book was re-cut from A4 to US Letter (215.9 × 279.4 mm), the house trim and BookVault's 216 × 279 mm. The text block is 177 × 251.4 mm, with a 21 mm gutter. Pages that no longer fit carry a small page-scoped zoom (`/*letter-fit*/`, from 0.90 to 0.99, set by `build/fit_letter.py`). The A4 sources are in `build/a4-backup/`.
- **QR codes:** none point at the temporary .vercel site any more. All six now open public resources: RTP #EstudoEmCasa (aula 8 «A carta», aula 6 «A notícia», aula 48 «O texto dramático»), RTP Arquivos «Crianças e Livros» (poems of the sea), and CPLP «Contos Tradicionais da CPLP» (the original Cape Verde tale). The listening tasks are led by the teacher; the Rádio Limoeiro script is printed in the U1 teacher notes (p. 27). The synthetic MP3s are retired to `archive-audio-retired/`. See `qr-links.md`.
- **Build check:** multi-column text spilling into a hidden extra column is now detected (COLUMNS spill). It found and fixed pp. 55 and 67.
