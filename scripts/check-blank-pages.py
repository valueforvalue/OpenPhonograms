# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Scan rendered PDFs for blank pages.

A page is considered "blank" when its visible body text (excluding the
@page header/footer: bottom-center page counter and bottom-left license
stamp) is fewer than 20 characters after whitespace is stripped.

By default this script reports on PDFs already in build/ (produced by
`just build` or `python framework/render.py --stage N`). Pass `--render`
to render a small sample first so CI can smoke-test without rendering all
244 lessons (the full render is what previously hung; see issue #26).

Exit codes:
  0 = no PDF exceeds thresholds
  1 = at least one PDF has > 2 blank pages OR > median + 2σ total pages
  2 = pypdfium2 not installed / input directory missing

Usage:
  python scripts/check-blank-pages.py                       # report on build/lessons/
  python scripts/check-blank-pages.py --dir build/stage-1   # specific subdir
  python scripts/check-blank-pages.py --sample 5 --render   # render 5 first then check
  python scripts/check-blank-pages.py --json                # machine-readable output
  python scripts/check-blank-pages.py --threshold 1         # fail if > 1 blank (stricter)
"""

import argparse
import io
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    import pypdfium2 as pdfium
except ImportError:
    print("Error: pypdfium2 not installed. Install with: pip install pypdfium2")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

# Strip the @page footer (bottom-left license stamp + bare page numbers)
# so they don't count as body content when detecting blank pages.
FOOTER_RE = re.compile(
    r"OpenPhonograms\s*\u00b7\s*MIT licensed|^\s*\d+\s*$",
    re.MULTILINE,
)

# Minimum body characters for a page to count as "non-blank".
# The @page footer alone is ~40 chars; real body text is much more.
MIN_BODY_CHARS = 20


def measure_pdf(pdf_path: Path) -> tuple[int, int]:
    """Return (total_pages, blank_pages) for a single PDF."""
    pdf = pdfium.PdfDocument(str(pdf_path))
    total = len(pdf)
    blanks = 0
    for i in range(total):
        tp = pdf[i].get_textpage()
        text = tp.get_text_range()
        stripped = FOOTER_RE.sub("", text).strip()
        body_chars = len(stripped.replace(" ", "").replace("\n", "").replace("\t", ""))
        if body_chars < MIN_BODY_CHARS:
            blanks += 1
    return total, blanks


def render_sample(lessons_root: Path, sample: int) -> list[Path]:
    """Render first N lessons (alphabetical) and return only the PDFs
    produced by this call. Existing sibling PDFs are NOT returned —
    callers use this list to filter their measurement scope."""
    rendered: list[Path] = []
    md_files: list[Path] = []
    for stage in sorted(lessons_root.glob("stage-*")):
        md_files.extend(sorted(stage.glob("*.md")))
    md_files = md_files[:sample]

    for md in md_files:
        out = md.with_suffix(".pdf")
        print(f"  render {md.relative_to(ROOT)} -> {out.relative_to(ROOT)}")
        result = subprocess.run(
            [sys.executable, str(ROOT / "framework" / "render.py"), str(md)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"    FAIL: {result.stderr.strip()[:200]}")
            continue
        if out.exists():
            rendered.append(out)
    return rendered


def collect_pdfs(target: Path) -> list[Path]:
    """Return sorted list of PDFs under target (file or directory)."""
    if target.is_file():
        return [target]
    return sorted(target.rglob("*.pdf"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PDFs for blank pages")
    parser.add_argument(
        "--dir", default=str(ROOT / "build" / "lessons"),
        help="Directory to scan (default: build/lessons/)",
    )
    parser.add_argument(
        "--render", action="store_true",
        help="Render a sample of lessons first (lessons/stage-*/*.md) before checking",
    )
    parser.add_argument(
        "--sample", type=int, default=5, metavar="N",
        help="Number of lessons to render when --render is set (default: 5)",
    )
    parser.add_argument(
        "--threshold", type=int, default=2, metavar="N",
        help="Max blank pages per PDF before flagging (default: 2)",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit machine-readable JSON instead of a text table",
    )
    args = parser.parse_args()

    rendered_pdfs: list[Path] | None = None
    if args.render:
        if not args.json:
            print(f"Rendering sample of {args.sample} lessons...")
        rendered_pdfs = render_sample(ROOT / "lessons", args.sample)
        # PDFs are written next to MDs (lessons/stage-N/*.pdf).
        target = (ROOT / "lessons").resolve()
        display_target = ROOT / "lessons"
    else:
        display_target = Path(args.dir)
        target = display_target.resolve()
        if not target.exists():
            if not args.json:
                print(f"Error: directory not found: {target}")
            print(json.dumps({"error": f"directory not found: {target}"}))
            return 2

    pdfs = collect_pdfs(target)
    if rendered_pdfs is not None:
        # Restrict measurement to PDFs produced by THIS render call so
        # existing sibling PDFs in the source tree don't pollute the sample.
        rendered_set = set(rendered_pdfs)
        pdfs = [p for p in pdfs if p.resolve() in {r.resolve() for r in rendered_set}]
    if not pdfs:
        if not args.json:
            print(f"No PDFs found under {target}")
        return 0

    rows = []
    for pdf in pdfs:
        total, blanks = measure_pdf(pdf)
        try:
            display = str(pdf.relative_to(ROOT))
        except ValueError:
            display = str(pdf)
        rows.append({
            "file": display,
            "total_pages": total,
            "blank_pages": blanks,
        })

    totals = [r["total_pages"] for r in rows]
    median_pages = statistics.median(totals) if totals else 0
    if len(totals) >= 2:
        stdev_pages = statistics.stdev(totals)
    else:
        stdev_pages = 0.0
    page_cap = median_pages + 2 * stdev_pages

    failures = []
    for r in rows:
        too_many_blanks = r["blank_pages"] > args.threshold
        too_many_pages = r["total_pages"] > page_cap
        r["over_threshold"] = too_many_blanks or too_many_pages
        if r["over_threshold"]:
            failures.append(r)

    if args.json:
        print(json.dumps({
            "scanned": len(rows),
            "failures": len(failures),
            "median_pages": median_pages,
            "stdev_pages": stdev_pages,
            "page_cap": page_cap,
            "blank_threshold": args.threshold,
            "results": rows,
        }, indent=2))
    else:
        print(f"==> Blank-page check ({display_target})")
        print(f"  PDFs scanned:    {len(rows)}")
        print(f"  Median pages:    {median_pages}")
        print(f"  Stdev pages:     {stdev_pages:.2f}")
        print(f"  Page cap (μ+2σ): {page_cap:.1f}")
        print(f"  Blank threshold: > {args.threshold}")
        print()
        print(f"  {'file':<40} {'total':>6} {'blank':>6}")
        print(f"  {'-'*40} {'-'*6} {'-'*6}")
        for r in rows:
            mark = " !" if r["over_threshold"] else "  "
            print(f"  {mark}{r['file']:<38} {r['total_pages']:>6} {r['blank_pages']:>6}")
        if failures:
            print()
            print(f"FAIL: {len(failures)} PDF(s) exceed threshold")
            for r in failures:
                reasons = []
                if r["blank_pages"] > args.threshold:
                    reasons.append(f"{r['blank_pages']} blanks")
                if r["total_pages"] > page_cap:
                    reasons.append(f"{r['total_pages']} pages > cap")
                print(f"  {r['file']}: {', '.join(reasons)}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())