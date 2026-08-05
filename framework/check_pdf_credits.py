#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Verify generated PDFs contain source attribution (issue #36).

Uses pypdf to extract text from all pages of a sample PDF per stage
and asserts the text contains "Denise Eide" or "Uncovering the Logic
of English". Wired into the build pipeline as
'just check-pdf-credits'.

We check all pages (not just page 1) because the footer often lands on
the last page when content fills the first.

Usage:
    python framework/check_pdf_credits.py
    python framework/check_pdf_credits.py --build-dir build

Exits 0 on success, 1 on failure.
"""
import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

# Phrases that confirm the source attribution is present in a PDF
# (We check for the methodology author name, not the literal footer
# string, because pdftotext extraction can rewrap words.)
CREDIT_PHRASES = (
    "Denise Eide",
    "Uncovering the Logic of English",
)


def _extract_all_pages_text(pdf: Path) -> str:
    """Return text from ALL pages of the PDF (or empty if unreadable)."""
    try:
        import pypdf
    except ImportError:
        print("  Error: pypdf not installed. Install with: pip install pypdf")
        sys.exit(2)
    try:
        reader = pypdf.PdfReader(str(pdf))
        out = []
        for page in reader.pages:
            try:
                out.append(page.extract_text() or "")
            except Exception:
                out.append("")
        return "\n".join(out)
    except Exception as e:
        return f"ERROR: {e}"


def _sample_pdfs_per_stage(build_dir: Path) -> dict[int, Path | None]:
    """Pick a sample PDF from each stage (1-5).

    Tries in order: lesson pack PDFs, then merged worksheets/overview
    PDFs. Returns the first one that exists.
    """
    out: dict[int, Path | None] = {}
    for stage in range(1, 6):
        candidates = [
            # Lesson pack (one PDF per lesson, includes the footer)
            build_dir / "packs" / f"stage-{stage}" / f"lesson-01-*.pdf",
            # Merged per-stage worksheets (footer lands on last page)
            build_dir / f"stage-{stage}-worksheets.pdf",
            # Merged per-stage overview (everything in stage)
            build_dir / f"stage-{stage}.pdf",
        ]
        for c in candidates:
            if c.is_file():
                out[stage] = c
                break
            if "*" in c.name:
                matches = list(c.parent.glob(c.name))
                if matches:
                    out[stage] = matches[0]
                    break
        if stage not in out:
            out[stage] = None
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--build-dir", type=Path, default=BUILD,
                   help="Build directory containing generated PDFs")
    p.add_argument("--quiet", action="store_true", help="Only print failures")
    args = p.parse_args()

    # Force UTF-8 stdout only when running as a script (not when imported
    # as a module — pytest capture doesn't survive TextIOWrapper replacement).
    if __name__ == "__main__" and hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    build_dir: Path = args.build_dir
    if not build_dir.exists():
        print(f"  Error: build directory not found: {build_dir}")
        print("  Run 'just render-all' first to generate PDFs.")
        sys.exit(2)

    samples = _sample_pdfs_per_stage(build_dir)
    if not any(samples.values()):
        print(f"  Error: no sample PDFs found in {build_dir}")
        sys.exit(2)

    failures = []
    for stage in range(1, 6):
        pdf = samples.get(stage)
        if pdf is None:
            if not args.quiet:
                print(f"  Stage {stage}: (no PDF sample found, skipping)")
            continue
        text = _extract_all_pages_text(pdf)
        if text.startswith("ERROR"):
            failures.append((stage, pdf.name, text))
            print(f"  Stage {stage}: FAIL {pdf.name}: {text}")
            continue
        if any(phrase in text for phrase in CREDIT_PHRASES):
            print(f"  Stage {stage}: PASS {pdf.name}")
        else:
            failures.append((stage, pdf.name, "no credit phrase found"))
            # Show first 200 chars of text for debugging
            preview = text[:200].replace("\n", " ").strip()
            print(f"  Stage {stage}: FAIL {pdf.name}: no 'Denise Eide' / 'Uncovering the Logic of English'")
            print(f"             Text preview: {preview!r}")

    if failures:
        print(f"\n  {len(failures)} of {sum(1 for v in samples.values() if v)} PDFs missing source attribution.")
        print("  Run 'just gen-footers' then 'just render-all' to add footers and re-render.")
        sys.exit(1)
    else:
        print(f"\n  All {sum(1 for v in samples.values() if v)} sampled PDFs contain source attribution.")
        sys.exit(0)


if __name__ == "__main__":
    main()