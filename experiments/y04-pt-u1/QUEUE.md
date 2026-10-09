# Production status and queue

## Detached job runner (survives chat turns)
`jobs/run.sh` runs `jobs/order.txt` with 7 in parallel, each as a one-shot `hermes chat -Q --query-file jobs/<name>.md` (claude-opus-5.5).
- Logs: `jobs/logs/<name>.log`
- Reports: `jobs/logs/<name>.report.md`
- Finished marker: `jobs/logs/<name>.done`
- All finished: `jobs/logs/ALL.done`

In-chat subagents (delegate_task) were killed each time a new user message arrived, so they are no longer used.

## Jobs, in order
1. u5-imgs (DONE)
2. u67-imgs
3. u2-e1, u2-e2, u2-e3, u2-e4, u2-e5, u2-e67 (finish and QA drafted pages)
4. u3-v1, u3-v2, u3-v3
5. u4-c1, u4-c2
6. u5-a, u5-b, u5-c, u5-d
7. u6 (pp. 143–152, including the teacher notes on p. 152)

## Mine (done)
- **Framing pages:** 1 (cover, updated for the whole book), 25/26/69, 73/74/94, 97/98/115/116, 119/120/137/138, 141/142.
- **Unit 7:** 153–160.
- **Back matter:** glossary 161–162, credits 163, back cover 164.

## Mine (after ALL.done)
1. Teacher notes: U2 70–72, U3 95–96, U4 117–118, U5 139–140.
2. `build/insert_index.py --dry`, then run it. This inserts the Índice spread as pp. 3–4 and shifts all pages ≥ 3 by +2, giving 166 pages.
3. Write `pages/03.html` and `pages/04.html` (contents: one colour bar and one tinted card per unit).
4. Check the map-page SVG labels for bare page numbers, which the regex does not catch.
5. Full build at dpi 110 and the print version with `--bleed`.
6. Whole-book overflow, vision and proofreading pass.
7. Decode every QR code with cv2.
8. Contact sheets.
9. Publish:
   - book.pdf, cover.webp and preview/ to `public/library/y04-portuguese-anthropic/`;
   - `library.json`: title «Português · Year 4 — Rua das Palavras» (drop «(Unidade 1)»), plus the page count and mb.
10. Update REPORT.md, DESIGN-RATIONALE.md and 05-image-list.md. Credits page p. 163: reconcile it with the job reports (texts and rights).
