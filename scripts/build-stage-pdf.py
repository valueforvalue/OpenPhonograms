#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Merge per-stage worksheets + readers + cards into single stage PDFs.

For each stage (1-5), produces:
  build/stage-N-worksheets.pdf   (phonograms + rules + cards)
  build/stage-N-readers.pdf      (decodable readers)
  build/stage-N.pdf              (everything combined)

Usage:
  python scripts/build-stage-pdf.py [--stage N] [--rebuild]

Uses pypdf to merge existing PDFs in build/ (faster than re-rendering).
"""
import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

try:
    import pypdf
except ImportError:
    print("Error: pypdf not installed. Install with: pip install pypdf")
    sys.exit(2)


def collect_pdfs(*subdirs: str) -> list[Path]:
    """Gather all PDFs from given subdirs under build/, sorted."""
    pdfs: list[Path] = []
    for sub in subdirs:
        d = BUILD / sub
        if d.exists():
            pdfs.extend(sorted(d.glob("*.pdf")))
    return pdfs


def merge_pdfs(pdfs: list[Path], out: Path) -> int:
    """Merge PDFs into a single file. Returns page count, or 0 if no inputs."""
    if not pdfs:
        return 0
    writer = pypdf.PdfWriter()
    total_pages = 0
    for p in pdfs:
        try:
            reader = pypdf.PdfReader(str(p))
            for page in reader.pages:
                writer.add_page(page)
                total_pages += 1
        except Exception as e:
            print(f"  WARN: skip {p.relative_to(ROOT)}: {e}")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)
    return total_pages


def main():
    parser = argparse.ArgumentParser(description="Build merged per-stage PDFs")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5],
                        help="Build only one stage (default: all)")
    parser.add_argument("--rebuild", action="store_true",
                        help="Force rebuild even if output exists")
    args = parser.parse_args()

    stages = [args.stage] if args.stage else [1, 2, 3, 4, 5]

    # Worksheet subdirs per stage
    ws_subdirs = {
        1: ["worksheets/phonograms/stage-1", "worksheets/rules/stage-1",
            "worksheets/cards/stage-1"],
        2: ["worksheets/phonograms/stage-2", "worksheets/rules/stage-2",
            "worksheets/cards/stage-2"],
        3: ["worksheets/phonograms/stage-3", "worksheets/rules/stage-3",
            "worksheets/cards/stage-3"],
        4: ["worksheets/phonograms/stage-4", "worksheets/rules/stage-4",
            "worksheets/cards/stage-4"],
        5: ["worksheets/phonograms/stage-5", "worksheets/rules/stage-5",
            "worksheets/cards/stage-5"],
    }
    reader_subdir = {s: f"readers/stage-{s}" for s in stages}

    for s in stages:
        all_out = BUILD / f"stage-{s}.pdf"
        cards_out = BUILD / f"stage-{s}-cards.pdf"

        ws_pdfs = collect_pdfs(*ws_subdirs[s])
        rd_pdfs = collect_pdfs(reader_subdir[s])
        card_pdfs = collect_pdfs(f"worksheets/cards/stage-{s}")

        ws_count = len(ws_pdfs)
        rd_count = len(rd_pdfs)
        card_count = len(card_pdfs)
        all_pages = merge_pdfs(ws_pdfs + rd_pdfs, all_out) if (ws_pdfs or rd_pdfs) else 0
        card_pages = merge_pdfs(card_pdfs, cards_out)

        if all_out.exists() and all_out.stat().st_size < 1000:
            all_out.unlink()
        if cards_out.exists() and cards_out.stat().st_size < 1000:
            cards_out.unlink()

        print(f"Stage {s}: {ws_count}ws + {rd_count}rd → {all_out.name if all_pages else '(empty)'} | {card_count}cards → {cards_out.name if card_pages else '(empty)'}")


if __name__ == "__main__":
    main()