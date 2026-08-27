"""Mark a Prime Book done, or un-done.

Done = the Output pdf sits inside PDF/Output/Done/ (a FOLDER MOVE, not a flag).
The collection list reads done-state from the PDF being inside Done/.

Usage:
    python tools/mark_done.py "Year 01/Art & Design"      # move the single Output pdf into Done/
    python tools/mark_done.py "Year 01/Art & Design" --undo   # move it back to Output/
    python tools/mark_done.py --list                        # show every done book
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

REPO = Path(r"C:\Users\alexa\Documents\GitHub\prime-books")
BOOKS = REPO / "public" / "Prime Books"


def find_book(partial: str) -> Path | None:
    partial = partial.replace("\\", "/").strip("/").lower()
    for year_dir in sorted(p for p in BOOKS.iterdir() if p.is_dir()):
        for sd in sorted(p for p in year_dir.iterdir() if p.is_dir()):
            rel = f"{year_dir.name}/{sd.name}".lower()
            if partial in rel:
                return sd
    return None


def single_output_pdf(book: Path) -> Path | None:
    out_dir = book / "PDF" / "Output"
    if not out_dir.is_dir():
        return None
    pdfs = [p for p in out_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
    return pdfs[0] if len(pdfs) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", nargs="?", help="partial path, e.g. \"Year 01/Art & Design\"")
    ap.add_argument("--undo", action="store_true", help="move the Done pdf back to Output/")
    ap.add_argument("--list", action="store_true", help="list every done book")
    args = ap.parse_args()

    if args.list:
        n = 0
        for year_dir in sorted(p for p in BOOKS.iterdir() if p.is_dir()):
            for sd in sorted(p for p in year_dir.iterdir() if p.is_dir()):
                done_dir = sd / "PDF" / "Output" / "Done"
                if done_dir.is_dir():
                    pdfs = [p for p in done_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
                    if pdfs:
                        n += 1
                        print(f"  DONE  {year_dir.name}/{sd.name}  ->  {pdfs[0].name}")
        print(f"\n{n} books marked done.")
        return 0

    if not args.book:
        print("Give a book path, or use --list. See docstring.")
        return 1

    book = find_book(args.book)
    if book is None:
        print(f"Book not found: {args.book}")
        return 1

    out_dir = book / "PDF" / "Output"
    done_dir = out_dir / "Done"

    if args.undo:
        if not done_dir.is_dir():
            print(f"{book.name}: nothing in Done/ to undo.")
            return 0
        for p in sorted(done_dir.iterdir()):
            if p.is_file():
                shutil.move(str(p), str(out_dir / p.name))
                print(f"UNDONE  {book.name}: {p.name} moved back to Output/")
        done_dir.rmdir() if not any(done_dir.iterdir()) else None
        return 0

    pdf = single_output_pdf(book)
    if pdf is None:
        print(f"{book.name}: PDF/Output must hold EXACTLY ONE pdf to mark done.")
        return 1
    done_dir.mkdir(exist_ok=True)
    shutil.move(str(pdf), str(done_dir / pdf.name))
    print(f"DONE  {book.name}: {pdf.name} moved to PDF/Output/Done/")
    return 0


if __name__ == "__main__":
    sys.exit(main())