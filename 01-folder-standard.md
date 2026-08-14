# 01 - Folder Standard

The Prime Books corpus lives in one canonical shape. This file is the contract:
any book, any level, any machine, the folder layout is the same.

## The content root

```
public/Prime Books/<Level>/<Year NN>/<Subject>/
```

The five levels, with the exact year each holds:

| Level | Years |
|---|---|
| Lower Primary | Years 01-02 |
| Upper Primary | Years 03-06 |
| Lower Secondary | Years 07-09 |
| Upper Secondary | Years 10-11 (including combined "Year 10-11") |
| Advanced Levels | Years 12-13 (including combined "Year 12-13") |

These are the UK key stages in their Cambridge form. A book's level is decided
by its YEAR, never by subject. The MEGA archive uses a different, older grouping
(its "1. Lower Primary" spans Years 01-04); when copying from MEGA, remap by
year, not by the MEGA level name. `6. Extracurricular` and `7. Kindergarden`
sit outside the five levels and are not part of this tree.

## Inside one book

```
<Subject>/
  PDF/Input/         EXACTLY ONE source PDF (the "Input Book", third-party
                     reference, scope and sequence only, never republished)
  PDF/Output/        EXACTLY ONE built flipbook PDF (the student book)
  PDF/Output/Done/   the Output PDF moved in here marks the book DONE
  MARKDOWN/          one .md per unit plus 00-front-matter.md (the editable
                     source of truth)
  BOOK COVER/        EXACTLY ONE cover file (from public/collection-covers/)
  OWNER.md           lock and definition of done (see 05-collaboration.md)
```

No other folders belong here. In particular there is never a `FEEDBACK.docx`,
never a `*superseded*` folder, and no `_kit` or machinery subfolders. Real
teacher reviews live in the MEGA archive under `ARTIFACTS/reviews/`; build
engines live in `WORKSTATION/_build` and are local only.

## File naming

- Output PDF: `Prime Book - {Subject} - Year {N} - Student Book.pdf`
  Example: `Prime Book - Art & Design - Year 1 - Student Book.pdf`
- Cover: the collection cover pattern `Y<NN>-<SubjectNoSpaces>.webp`
  Example: `Y01-ArtDesign.webp`
- Never rename a PDF that is already published. The destination's existing
  filename wins; only mint a name for a brand new book.

## Done is a folder move, not a flag

A finished book's Output PDF sits inside `PDF/Output/Done/`. The collection
list reads done-state from the PDF being inside `Done/`. To un-do a book, move
it back to `PDF/Output/`. There is no status field to keep in step: the file's
location IS the state.

## Where the pieces come from

- Source input PDFs: the MEGA archive
  `C:\Users\alexa\Documents\MEGA\Projects\Prime Books\BOOKS\<level>\...`
  Copy each book's single source PDF into its `PDF/Input/`.
- Cover art: `public/collection-covers/` (one file per book). Copy the single
  cover into the book's `BOOK COVER/`.
- Logos (Prime Book and Prime School) and fonts: `public/Resources/`.
- The master index (Excel/CSV): `public/Subjects Excel-Csv/`.

## The invariants

Violating any of these is a fail:

1. Exactly ONE Input PDF and ONE Output PDF per book.
2. "Done" means the Output PDF is inside `PDF/Output/Done/`.
3. Exactly ONE cover file in `BOOK COVER/`.
4. No "superseded" folders anywhere.
5. MARKDOWN is the editable source of truth; the PDF is the rendered output.

## Verification

The rebuild and the audit live in `tools/`:

```
python tools/rebuild_canonical_tree.py          # dry run: counts + report
python tools/rebuild_canonical_tree.py --go     # build public/Prime Books/
```

Every run reports, in `docs/PATHS-TO-CORRECT.md`, the exact paths of any book
that does not hold exactly one Input, one Output and one cover. Those are the
paths to correct; the script never guesses and never deletes.

The MEGA archive is the archival master. `public/Prime Books/` is the canonical
working tree (gitignored, local to the workshop, never deployed). The site
serves web-optimised copies built from it by `tools/sync_library.py` into
`public/library/`.
