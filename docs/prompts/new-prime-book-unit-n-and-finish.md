# PROMPT — NEW PRIME BOOK · UNIT N  (use with /queue, one per unit)

Continue the Prime Book **[SLUG]**: build **UNIT [N] — [TITLE]** ([subunits from the inputs]).
Read first:
- `experiments/[SLUG]/continuity.json` (next folio, next activity number);
- Unit 1's `src/` and renders (the design system);
- the last unit's report;
- `prime-books-book-builder/references/new-book-unit-by-unit-lessons.md`.

All the Unit 1 "Fixed decisions" apply unchanged:
- US Letter and print-safe margins;
- static fonts and the Type3 / fallback gate;
- NO self-recorded audio and NO `.vercel` QR codes, only verified public resources;
- solutions and teacher texts in `uN/site/*.md`;
- every label in the book's language («[N].º Ano»);
- copyright extracts ≤ 4 lines;
- same art style and characters;
- continuous folios and activity numbers;
- even page count, no blanks.

Work only in `experiments/[SLUG]/u[N]/`, never in earlier units. If a shared CSS change is
unavoidable, list it in the report and rebuild every unit that imports it.
Page count: [16 / 24 / 40]. Run the same QA gate. Publish the book with all finished units
assembled in order. Update `continuity.json`. Report pages, QR → URL list, checks and cost.

# PROMPT — NEW PRIME BOOK · FINISH (after the last unit)

Finish **[SLUG]**:
1. **Covers.** The master's front and back re-set in the book's language on the same art.
   The logo top sits at the house height on the BookVault wrap: about 19 mm below the trim.
   Measure against `public/library/y04-portuguese/bookvault/*cover-file.png`.
2. **Front matter (roman numerals).** Imprint, how-to-use, map of the year, contents (one colour bar segment
   and one tinted card per unit), reading log (ONE «Por minha conta» row), pupil profile.
3. **Back matter.**
   - Soluções and Textos para o professor, both built from the `uN/site/*.md` files.
   - Glossary.
   - Recursos digitais: only the public QR codes, re-decoded.
   - References and credits, annual plan, end-of-year page, colophon (no audio credits).
4. **Assemble.** Even page count, no blank pages. Run the full-book QA:
   - every QR decoded, zero "vercel";
   - no «Year» in the text;
   - fonts gate passes;
   - contents spot-checked.
5. **Publish.** Under `/finished/book/[SLUG]`.
6. **BookVault pack.** `tools/make_bookvault_files.py [SLUG] --force`:
   - zero FAIL;
   - page count 4n−1 for US Letter;
   - ask me for the spine width from BookVault's sizing calculator.
   Verify the Download Bookvault files are served byte-identical (md5).
