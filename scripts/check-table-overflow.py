"""Scan rendered PDFs for content that overflows the right margin.

For each page, finds the maximum x-coordinate of any text rectangle. If that
exceeds the page width minus the configured margin, the content overflows.

Margin defaults to render.py's spec:
  - lessons/readers/curriculum: 0.75 in = 54 pt
  - worksheets:                  0.5 in  = 36 pt

Exit codes:
  0 = no overflow
  1 = overflow detected in one or more PDFs

Usage:
  python scripts/check-table-overflow.py                 # check build/
  python scripts/check-table-overflow.py --packs         # check packs/ instead
  python scripts/check-table-overflow.py --quiet         # only print problems
"""

import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    import pypdfium2 as pdfium
except ImportError:
    print("Error: pypdfium2 not installed. Install with: pip install pypdfium2")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

# Margins in PDF points (72 pt/in)
MARGIN_LESSON = 54   # 0.75 in
MARGIN_WORKSHEET = 36  # 0.5 in


def margin_for(rel_path: str) -> float:
    """Return the margin (in pt) for a PDF based on its path."""
    s = str(rel_path).lower()
    if "worksheet" in s or "quick-check" in s or "blank" in s:
        return MARGIN_WORKSHEET
    return MARGIN_LESSON


def check_pdf(pdf_path: Path, tolerance: float = 1.0) -> list[tuple[int, float, float]]:
    """Return list of (page_num, max_right, overflow_pt) for pages that overflow.

    overflow_pt is how many points past the right margin the content extends.
    tolerance (default 1.0pt) absorbs sub-point rounding noise from weasyprint.
    """
    overflows = []
    pdf = pdfium.PdfDocument(str(pdf_path))
    margin = margin_for(pdf_path)
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        width, _ = page.get_size()
        right_limit = width - margin
        textpage = page.get_textpage()
        max_right = 0.0
        for i in range(textpage.count_rects()):
            rect = textpage.get_rect(i)
            if rect[2] > max_right:
                max_right = rect[2]
        if max_right > right_limit + tolerance:
            overflows.append((page_num + 1, max_right, max_right - right_limit))
    return overflows


def main():
    parser = argparse.ArgumentParser(description="Check PDF content for right-margin overflow")
    parser.add_argument("--packs", action="store_true", help="Check packs/ instead of build/")
    parser.add_argument("--quiet", action="store_true", help="Only print problems")
    parser.add_argument("--tolerance", type=float, default=1.0, help="Tolerance in pt (default 1.0)")
    args = parser.parse_args()

    pdf_dir = ROOT / ("packs" if args.packs else "build")
    if not pdf_dir.exists():
        print(f"Error: directory not found: {pdf_dir}")
        sys.exit(2)

    pdfs = sorted(pdf_dir.rglob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {pdf_dir}")
        sys.exit(0)

    total_pages = 0
    pdfs_with_overflow = 0
    problems = []

    for pdf_path in pdfs:
        overflows = check_pdf(pdf_path, tolerance=args.tolerance)
        total_pages += 1
        if overflows:
            pdfs_with_overflow += 1
            problems.append((pdf_path, overflows))

    if not args.quiet:
        print(f"==> Overflow check ({pdf_dir.relative_to(ROOT)})")
        print(f"  PDFs scanned:   {len(pdfs)}")
        print(f"  With overflow:  {pdfs_with_overflow}")

    if problems:
        if not args.quiet:
            print()
            print("Overflows:")
        for pdf_path, overflows in problems:
            rel = pdf_path.relative_to(ROOT)
            for page_num, max_right, overflow_pt in overflows:
                print(f"  OVERFLOW  {rel}  page {page_num}  ({overflow_pt:.1f}pt past margin)")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
