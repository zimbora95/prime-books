#!/usr/bin/env python3
"""Build editable Prime Books Contents workbooks from the six supplied CSVs.

The workbook keeps the site's standard `Contents` sheet as its active sheet,
plus a title-cased copy of the complete Drive export on `Source export`. The
original CSV and any earlier workbook/PDF remain archived in inputs-raw/.
"""
from __future__ import annotations

import csv
import math
import re
import shutil
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "public" / "inputs-raw"
INPUTS = REPO / "public" / "inputs"
BOOKS = (
    (4, "y04-portuguese"),
    (5, "y05-portuguese"),
    (6, "y06-portuguese"),
    (8, "y08-portuguese-1st"),
    (10, "y10-portuguese-1st"),
    (11, "y11-portuguese-1st"),
)
HEADING_RE = re.compile(r"^Unidade\s+(\d+)(?:\.(\d+))?\s*[-–—:]\s*(.+)$", re.I)
SMALL_WORDS = {
    "a", "à", "às", "ao", "aos", "as", "da", "das", "de", "do", "dos",
    "e", "em", "na", "nas", "no", "nos", "o", "os", "ou", "para", "por",
    "pelo", "pela", "pelos", "pelas", "um", "uma", "uns", "umas", "com", "sem",
    "sob", "sobre", "entre", "até", "após", "contra", "como", "que", "and",
    "or", "the", "of", "in", "on", "to", "for", "by", "from", "with", "at",
}
NAVY = "173047"
TEAL = "187A78"
MINT = "E8F3F1"
PALE = "F1F5F7"
INK = "243746"
MUTED = "5B6E79"
WHITE = "FFFFFF"
RULE = "D4DEE3"


def title_case_text(text: str) -> str:
    """Title-case Portuguese labels; keep function words lowercase in phrases."""
    parts = re.split(r"( - |: |, )", " ".join(text.split()))
    out: list[str] = []
    start_of_phrase = True

    def cap_component(value: str) -> str:
        if not value or any(char.isdigit() for char in value) or value.isupper():
            return value
        return value[0].upper() + value[1:].lower()

    for part in parts:
        if not part:
            continue
        if part in {" - ", ": ", ", "}:
            out.append(part)
            start_of_phrase = True
            continue
        cased = []
        for word in part.split():
            if word.lower() in SMALL_WORDS and not start_of_phrase:
                value = word.lower()
            else:
                apostrophe_parts = word.split("'")
                if len(apostrophe_parts) == 2 and apostrophe_parts[0].lower() in {"d", "n"}:
                    prefix = apostrophe_parts[0].lower() if not start_of_phrase else cap_component(apostrophe_parts[0])
                    value = prefix + "'" + cap_component(apostrophe_parts[1])
                else:
                    value = "'".join(cap_component(piece) for piece in apostrophe_parts)
                value = "-".join(cap_component(piece) for piece in value.split("-"))
            cased.append(value)
            start_of_phrase = False
        out.append(" ".join(cased))
    return "".join(out)


def standardize_heading(label: str) -> tuple[str, str]:
    match = HEADING_RE.match(label)
    if not match:
        raise ValueError(f"Unrecognised heading: {label!r}")
    major, minor, title = match.groups()
    number = f"{major}.{minor}" if minor else major
    kind = "Subunit" if minor else "Unit"
    return kind, f"Unidade {number} - {title_case_text(title.strip())}"


def read_source(path: Path) -> tuple[list[str], list[list[str]], list[tuple[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        data = list(csv.reader(handle))
    if not data or data[0][:2] != ["section_ids/name", "section_ids/chapter_ids/name"]:
        raise ValueError(f"Unexpected CSV header in {path.name}")
    headings: list[tuple[str, str]] = []
    body: list[list[str]] = []
    for line, row in enumerate(data[1:], start=2):
        row += [""] * max(0, 2 - len(row))
        if len(row) != 2:
            raise ValueError(f"Expected two columns at {path.name}:{line}")
        row = [cell.strip() for cell in row]
        if row[0]:
            headings.append(standardize_heading(row[0]))
            row[0] = f"Unidade {HEADING_RE.match(row[0]).group(1)}" + (
                f".{HEADING_RE.match(row[0]).group(2)}" if HEADING_RE.match(row[0]).group(2) else ""
            ) + " - " + title_case_text(HEADING_RE.match(row[0]).group(3).strip())
        body.append(row)
    units = [title for kind, title in headings if kind == "Unit"]
    if len(units) != 8 or sum(kind == "Subunit" for kind, _ in headings) != 13:
        raise ValueError(f"Unexpected hierarchy in {path.name}: {len(units)} units / {len(headings) - len(units)} subunits")
    return data[0][:2], body, headings


def style_sheet(ws, widths: tuple[float, ...]) -> None:
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A2"
    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.row_dimensions[1].height = 28
    for cell in ws[1]:
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.font = Font(name="Aptos", size=10, bold=True, color=WHITE)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color=TEAL))


def build_workbook(year: int, slug: str, source: Path) -> tuple[Path, dict[str, int]]:
    source_headers, source_rows, headings = read_source(source)
    wb = Workbook()
    contents = wb.active
    contents.title = "Contents"
    contents.append(["Section type", "Title", "Page"])
    for kind, title in headings:
        contents.append([kind, title, ""])
    style_sheet(contents, (18, 104, 12))
    contents.auto_filter.ref = f"A1:C{contents.max_row}"
    contents.sheet_properties.tabColor = TEAL
    for row in contents.iter_rows(min_row=2):
        kind = row[0].value
        shade = MINT if kind == "Subunit" else PALE
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=shade)
            cell.font = Font(name="Aptos", size=10, bold=(kind == "Unit"), color=INK)
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            cell.border = Border(bottom=Side(style="hair", color=RULE))
        row[0].font = Font(name="Aptos", size=9, bold=True, color=TEAL if kind == "Subunit" else NAVY)
        row[2].alignment = Alignment(horizontal="center", vertical="center")
        row[1].alignment = Alignment(vertical="center", wrap_text=True, indent=1 if kind == "Subunit" else 0)
        contents.row_dimensions[row[0].row].height = 26

    export = wb.create_sheet("Source export")
    export.append(source_headers)
    for row in source_rows:
        export.append(row)
    style_sheet(export, (58, 112))
    export.auto_filter.ref = f"A1:B{export.max_row}"
    export.sheet_properties.tabColor = "D1A65A"
    for row in export.iter_rows(min_row=2):
        is_heading = bool(row[0].value)
        shade = MINT if is_heading else WHITE
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=shade)
            cell.font = Font(name="Aptos", size=9, bold=is_heading and cell.column == 1, color=INK)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(bottom=Side(style="hair", color=RULE))
        max_lines = max(
            1,
            math.ceil(len(str(row[0].value or "")) / 58),
            math.ceil(len(str(row[1].value or "")) / 112),
        )
        export.row_dimensions[row[0].row].height = max(22, min(72, max_lines * 15 + 6))

    wb.properties.title = f"Portuguese First Language — Year {year} Scheme of Work"
    wb.properties.subject = "Editable scheme of work; Contents is the site import sheet"
    wb.properties.creator = "Prime School"
    wb.properties.description = "Contents sheet plus the full two-column source export."
    out = INPUTS / f"{slug} - input.xlsx"
    out.parent.mkdir(parents=True, exist_ok=True)
    temp = out.with_name(out.stem + ".tmp.xlsx")
    wb.save(temp)
    wb.close()
    temp.replace(out)

    check = load_workbook(out, read_only=True, data_only=True)
    if check.sheetnames != ["Contents", "Source export"]:
        raise ValueError(f"Unexpected worksheets in {out.name}: {check.sheetnames}")
    rows = list(check["Contents"].iter_rows(values_only=True))
    if rows[0] != ("Section type", "Title", "Page") or len(rows) != 22:
        raise ValueError(f"Contents import sheet failed verification: {out.name}")
    if list(check["Source export"].iter_rows(values_only=True))[0] != tuple(source_headers):
        raise ValueError(f"Source export sheet lost its original headers: {out.name}")
    check.close()
    counts = {"units": len([1 for kind, _ in headings if kind == "Unit"]),
              "subunits": len([1 for kind, _ in headings if kind == "Subunit"]),
              "source_rows": len(source_rows)}
    return out, counts


def archive_generated_pdf(slug: str) -> None:
    pdf = INPUTS / f"{slug} - input.pdf"
    if not pdf.exists():
        return
    archive = RAW / "previous-generated-pdfs"
    archive.mkdir(parents=True, exist_ok=True)
    destination = archive / pdf.name
    if destination.exists():
        if destination.read_bytes() != pdf.read_bytes():
            raise FileExistsError(f"Refusing to replace archived PDF: {destination}")
        pdf.unlink()
    else:
        shutil.move(str(pdf), str(destination))


def main() -> int:
    for year, slug in BOOKS:
        source = RAW / f"{slug} - input.csv"
        if not source.is_file():
            raise FileNotFoundError(f"Missing supplied source CSV: {source}")
        workbook, counts = build_workbook(year, slug, source)
        archive_generated_pdf(slug)
        print(f"{slug}: {counts['units']} units; {counts['subunits']} subunits; "
              f"{counts['source_rows']} source rows; {workbook.name}")
    print(f"Built {len(BOOKS)} editable workbooks in {INPUTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())