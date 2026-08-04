"""Render all worksheets and reader MDs to PDFs.

Renders:
  worksheets/phonograms/pg-*.md → build/worksheets/phonograms/pg-*.pdf
  worksheets/rules/rule-*.md      → build/worksheets/rules/rule-*.pdf
  worksheets/cards/*.md          → build/worksheets/cards/*.pdf
  worksheets/blank/*.md          → build/worksheets/blank/*.pdf
  readers/*.md                   → build/readers/*.pdf

Usage:
  python scripts/render-extras.py
"""

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
WORKSHEETS = ROOT / "worksheets"
READERS = ROOT / "readers"
OUT = ROOT / "build"

# Import render helper from framework
sys.path.insert(0, str(ROOT))
from framework.render import render_md_to_pdf


def main():
    count = 0

    # Worksheets
    for sub in ["phonograms", "rules", "cards", "blank"]:
        src_dir = WORKSHEETS / sub
        out_dir = OUT / "worksheets" / sub
        out_dir.mkdir(parents=True, exist_ok=True)
        if not src_dir.exists():
            continue
        for md in sorted(src_dir.glob("*.md")):
            pdf = out_dir / (md.stem + ".pdf")
            render_md_to_pdf(md, pdf, doc_type="worksheet")
            count += 1

    # Readers
    if READERS.exists():
        out_dir = OUT / "readers"
        out_dir.mkdir(parents=True, exist_ok=True)
        for md in sorted(READERS.glob("*.md")):
            pdf = out_dir / (md.stem + ".pdf")
            render_md_to_pdf(md, pdf, doc_type="reader")
            count += 1

    print(f"==> Rendered {count} worksheet/reader PDFs")


if __name__ == "__main__":
    main()
