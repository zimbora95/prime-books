# Unit 2 build brief: for everyone who builds pages (read it all before writing)

**Book.** *Rua das Palavras*, Português Língua Materna, Year 4 (children aged 8–9, native speakers).
**Where.** Project root is `/root/prime-books/experiments/y04-pt-u1`. Page fragments go in `build/pages/NN.html`.
**Plan.** Read `06-unit2-plan.md` first: estantes, the scheme's content, checked facts and rights.
**Illustration style (book-wide rule).** Beatrix Potter watercolour animals. The cast is in `03-visual-guide.md`.

## Ground rules
- **Touch only your own files:** your pages, your `text/`, `notes/` and `audio/` files, and the audio and QR files named for your estante.
  - **Never** edit `build/build.py`, `build/style.css` or any other page.
  - Do not commit, push, or touch anything outside the project folder.
- **Language: European Portuguese with AO90 spelling.**
  - Use "estás a ler" (never the gerund), "ecrã", "autocarro", "casa de banho", "facto", "equipa".
  - Never use Brazilian forms: você, tela, ônibus, time, legal (for "cool"), gerund progressives.
  - Use polished, warm literary Portuguese for 8–9-year-olds. Keep most sentences at 18 words or fewer.
  - Use the travessão (—) for dialogue, and «aspas angulares».
  - Proofread every word.
- **Rights.** We print no text by António Torrado or Jorge Amado, and no quotations from them beyond their titles. Folk tales and fables are retold in our own words. Only the facts listed in the plan may be stated. Do not invent facts, publishers, dates or page numbers.
- **Characters.** The friends are animals: Inês (rabbit), Tomás (field mouse in a wheelchair), Amara (red squirrel), Farrusco (terrier puppy), Dona Rosa (badger, kiosk), Sr. Joaquim (tortoise, retired postman). Portuguese names for these species are often epicene, so do not attach species labels to names in the text. Let the pictures show the species.

## Design system (learn it from real pages before writing)
Study these pages as models: `07.html`, `08.html` (text plus annotation, tasks), `10.html`, `15.html`, `16.html` (grammar discovery, rule box, tasks), `19.html`, `20.html` (writing plan and draft), `11.html` (QR plus listening), and `06.html` (story with sidebar word box and QR). Also read `build/style.css` once.

- **Page head:**
  `<div class="head"><span class="stop"><i>1</i>Estante 1 · Conto de animais</span><h1>…</h1><p class="lede">…</p></div>`
  Inside `<i>` put the estante number, or an SVG icon (as on p. 16).
- **Tasks:**
  `<div class="task"><span class="n">1</span><div class="q"><svg class="ico"><use href="#i-escrever"/></svg><span>Instruction…</span>{{s1}}</div><div class="body">…</div></div>`
  Numbering restarts on every page. Every task carries a difficulty macro: `{{s1}}`, `{{s2}}` or `{{s3}}`.
- **Macros:** `{{lines:N:pitch_mm}}` gives N real writing lines (use a pitch of 8–10 mm for 8-year-olds). The stars macros are above.
- **Icons:** `<svg class="ico"><use href="#i-NAME"/></svg>`. NAME is one of: ouvir, falar, ler, escrever, desenhar, pares, grupo, qr, carta, convite, noticia, bd, jornal, jogo, gram, estrela, star, olho.
  Faces for self-rating: `<svg><use href="#f1"/></svg>` (f1 sad, f2 neutral, f3 happy).
- **Colour.** Your page colour arrives as `var(--c)`, with its tint as `var(--ct)`. Other colours available: `--red --yel --blue --sage --plum --teal --orng`, each with a `-t` tint. Also `--ink --ink2 --paper --paper2`.
- **Page CSS.** Put a `<style>` block at the end of your fragment. Scope **every** selector with `#pNN`, where NN is the page number without a leading zero (for example `#p27 .x`).
- **Images.** `build/img/<name>.jpg` (see the list of assignments below). Earlier images can also be reused: `12-writing.jpg`, `13-radio.jpg`, `04-mailbox-library.jpg`, `00-cast.jpg`, `05-inauguration.jpg`, `11-newsroom.jpg`.
  - Big figure: `<div class="fig" style="height:60mm"><img src="img/x.jpg" style="object-position:50% 40%" alt=""></div>`.
  - Vignettes can simply float on the page with no frame, because their paper matches the page colour.
- **Fonts.** Andika (body), `"FrS"`/`"FrH"`/`"FrX"` (Fraunces display families; see the `@font-face` rules in style.css), and Patrick Hand via the class `.hand`.
  - **Glyph safety:** never type ★ ☆ ✔ ✓ ☐ → ● or any emoji. Use the SVG icons and the macros instead. Ordinary Portuguese letters, « » — – … ‘ ’ “ ” and · are all safe.
- **Type sizes.** Body 14–15 pt; reading texts 14–15 pt with line-height ≥ 1.4; nothing below 11 pt on pupil pages.
- **Page geometry.** A4 with an inner box of about 177 × 263 mm. It does NOT scroll: anything that does not fit is a defect.

## Build and quality control (mandatory, and repeat until clean)
```
cd /root/prime-books/experiments/y04-pt-u1/build
/root/prime-books/.venv/bin/python build.py --pages 27,28,29,30,31,32 --out u2e1 --dpi 110
```
- Use your own `--out` name (u2e1 … u2e7) so you never collide with other builders.
- The JSON output lists `fonts` and `overflow`. Renders go to `renders/<out>/pNN.png`.
- **Must be true before you finish:**
  1. No `inner overflow` lines and no `OVERLAP` lines for your pages.
  2. No `SPILL` over 8 px, except on speech balloons, `.think` and `.sfx`.
  3. `fonts` contains only embedded TrueType fonts: Andika*, Fraunces*, PatrickHand*. No Type3 and no DejaVu.
  4. **Vision review of every page** (vision_analyze on `renders/<out>/pNN.png`). Act as a strict art director and editor. Check for:
     - collisions, clipped text, text over faces, empty dead zones or cramped areas;
     - writing space that is too small for an 8-year-old;
     - illustrations cropped badly;
     - hierarchy and alignment problems.
     Fix the problems and review again. Do at least two review rounds. Confirm any doubtful finding with a crop at 150 dpi before "fixing" it, because vision models sometimes hallucinate.
- **Pages should look premium** (DK / Usborne / Nordic textbook quality), not like a worksheet:
  - generous but full pages;
  - one clear focal element per page;
  - varied layouts across your 6 pages.

## Deliverables for each estante
1. `build/pages/NN.html` for your 6 pages, clean by the rules above.
2. `text/u2-eN.md`: the full reading text(s) plus every piece of learner-facing prose, so an editor can proofread it.
3. `notes/u2-eN.md`: teacher notes for your estante (in PT-PT). It must contain:
   - the objectives mapped to the scheme's lines (Oralidade / Leitura / EL / Escrita / Gramática) with page numbers;
   - suggested sessions (four to five 60-minute sessions);
   - **complete answers** for every closed task;
   - differentiation tips;
   - the resources used (QR/audio with URLs).
   Keep it under about 350 words: it will be typeset at 10 pt.
4. Your final answer:
   - a list of your pages with a one-line description each;
   - the build result (overflow/fonts);
   - the vision-review outcome;
   - any open issue, stated honestly.

## Audio and QR (only for estantes that have them)
- **TTS:**
  `/root/.hermes/cache/scratch/ttsvenv/bin/edge-tts --voice pt-PT-RaquelNeural --file audio/<name>.txt --write-media audio/<name>.mp3`
  The other voice is pt-PT-DuarteNeural.
- **QR:**
  `/root/prime-books/.venv/bin/python -c "import segno; segno.make('https://prime-books-pi.vercel.app/library/y04-portuguese-anthropic/audio/<name>.mp3', error='m').save('build/img/qr-<name>.svg', scale=4, border=0, dark='#1f2a44')"`
- **Test:** after building, render the page at 200 dpi and decode it with `cv2.QRCodeDetector().detectAndDecodeMulti`. It must return exactly that URL.

## Image assignments (the files appear in build/img/ once generated; if one is missing, lay out the page with the right proportions and use the name anyway)
| Estante | Pages | Images |
|---|---|---|
| 1 | 27–32 | u2-01-race.jpg (wide 1994×789 or 1536×1024), u2-02-nap.jpg (square) |
| 2 | 33–38 | u2-03-rabbit-door.jpg (wide), u2-04-ant.jpg (square) |
| 3 | 39–44 | u2-05-reading.jpg (wide) |
| 4 | 45–50 | u2-06-cat-swallow.jpg (wide), u2-07-seasons.jpg (square) |
| 5 | 51–56 | u2-08-capeverde.jpg (wide), u2-09-tia-ganga.jpg (square) |
| 6 | 57–62 | u2-10-diary.jpg (square), u2-11-week.jpg (wide) |
| 7 | 63–68 | u2-12-storm.jpg (wide), u2-13-key.jpg (square) |

Check the real pixel size with PIL before setting a figure height.
