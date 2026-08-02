#!/usr/bin/env python
"""Export every approved Prime Books cover for the web collection overview.

Reads the authoritative v2 cover plan and finished 300 dpi covers, then writes
web-sized WebP files plus public/collection-books.json for the storefront.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

FACTORY = Path(r"C:\Users\alexa\Documents\The Prime Books\_assets\v3")
PLAN = Path(r"C:\Users\alexa\Documents\The Prime Books\_assets\v2\plan.json")
SOURCE_COVERS = FACTORY / "cover"
PUBLIC = Path(__file__).resolve().parent / "public"
OUT = PUBLIC / "collection-covers"
MANIFEST = PUBLIC / "collection-books.json"
WEB_WIDTH = 720
WEB_HEIGHT = round(WEB_WIDTH * 3189 / 2480)


def main() -> None:
    books = json.loads(PLAN.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    expected = set()
    manifest = []

    for book in sorted(books, key=lambda item: (item["year"], item["subject"])):
        key = book["key"]
        src = SOURCE_COVERS / f"{key}.png"
        if not src.exists():
            raise FileNotFoundError(f"Missing approved cover: {src}")

        name = f"{key}.webp"
        expected.add(name)
        dst = OUT / name
        with Image.open(src) as image:
            image = image.convert("RGB")
            if image.size != (2480, 3189):
                raise ValueError(f"Unexpected dimensions for {src}: {image.size}")
            image = image.resize((WEB_WIDTH, WEB_HEIGHT), Image.Resampling.LANCZOS)
            image.save(dst, "WEBP", quality=84, method=6)

        manifest.append(
            {
                "key": key,
                "year": book["year"],
                "subject": book["subject"],
                "cover": f"/collection-covers/{name}",
            }
        )

    for stale in OUT.glob("*.webp"):
        if stale.name not in expected:
            stale.unlink()

    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    total_bytes = sum(path.stat().st_size for path in OUT.glob("*.webp"))
    print(
        f"Exported {len(manifest)} covers at {WEB_WIDTH}x{WEB_HEIGHT} "
        f"({total_bytes / 1024 / 1024:.1f} MiB) -> {OUT}"
    )
    print(f"Manifest -> {MANIFEST}")


if __name__ == "__main__":
    main()
