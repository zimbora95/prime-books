# 05 - Collaboration

How more than one author works on the corpus without stepping on each other.
The rules are small on purpose: one branch per book, one lock file, one
definition of done.

## One git branch per book

Each book gets its own branch, named after its slug:

```
book/<slug>        e.g. book/y01-mathematics
```

- Never edit a book on `main`. Open the book's branch, or create it from `main`
  if it does not exist yet.
- One branch carries exactly one book's changes. Fixing Year 1 Mathematics and
  Year 7 Science in the same branch is a mistake.
- Merge a book's branch back to `main` when the book is done; the merge is the
  hand-over signal.

## The OWNER.md lock

Every book folder contains `OWNER.md`. It is the lock: only the person named in
it works on that book.

- To claim a book, edit `OWNER.md`, set the owner, and commit on the book's
  branch. Do not claim a book someone else has claimed.
- When you finish, clear the owner (set `(unassigned)`) and merge, so the lock
  is free for the next person.
- A book with an active owner in `OWNER.md` is out of bounds, even if its branch
  looks idle.

The lock is a convention, not a technical gate. It works because everyone
respects it; the branch naming makes collisions visible in `git log`.

## Definition of done

A book is done when all of these are true:

1. The Output PDF sits in `PDF/Output/Done/`. That folder move IS the "done"
   switch; there is no other flag.
2. The book holds exactly one Input PDF, one Output PDF and one cover, per
   `01-folder-standard.md`.
3. `MARKDOWN/` is the complete editable source (one .md per unit plus
   `00-front-matter.md`), and it matches the rendered PDF.
4. The anatomy gates pass: from `RESOURCES/System/_system`, run
   `check_anatomy.py --pdf "<slug>"`, `one_pdf.py`, `covers_front_back.py --go`,
   then `build_registry.py`.
5. The book passes review. Gates read no pixels: all green means the review
   starts, so open the PDF and look at it.
6. The design is one pack, end to end, per `02-design-system.md` (Pack A for
   Year 1-6, Pack B for Year 7+).
7. British English throughout, no em-dashes, fixed imprint boilerplate.

Only then merge the branch and clear the lock.

## Handing a book over

The person who merges runs `python tools/rebuild_canonical_tree.py --go` to
refresh the canonical tree, and `python tools/sync_library.py` in the site repo
to refresh `public/library/` and `library.json`. The book appears DONE on the
site because its PDF sits in `PDF/Output/Done/`.

## What never happens

- Never edit a book you have not claimed in `OWNER.md`.
- Never rename a published PDF.
- Never delete or silently overwrite reviewed material; supersede it.
- Never commit `public/Prime Books/` (it is a gitignored working mirror, per the
  `.gitignore` notes) or the third-party `PDF/Input/` references.
