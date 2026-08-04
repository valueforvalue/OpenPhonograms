"""Detect drift between source Markdown and rendered PDFs.

Compares each generated MD file in lessons/, worksheets/, readers/ against the
corresponding PDF in build/. Reports any source that is newer than its PDF,
indicating a stale build.

Exit code:
  0 = no drift
  1 = drift detected (some MDs newer than their PDFs)
  2 = missing PDF (source exists but was never rendered)

Usage:
  python scripts/check-drift.py                # check everything
  python scripts/check-drift.py --stage 1      # check one stage
  python scripts/check-drift.py --quiet        # only print problems
"""

import argparse
import csv
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "framework" / "lesson-catalog.csv"
LESSONS_DIR = ROOT / "lessons"
WORKSHEETS_DIR = ROOT / "worksheets"
READERS_DIR = ROOT / "readers"
BUILD_DIR = ROOT / "build"


def check_lesson_pdf(stage: int, lesson_id: str) -> tuple[Path, Path | None, str]:
    """Return (md_path, pdf_path_or_None, status).

    status: 'ok' | 'drift' | 'missing' | 'no-pdf-yet'
    """
    md = LESSONS_DIR / f"stage-{stage}" / f"{lesson_id}.md"
    if not md.exists():
        return md, None, "missing-md"
    pdf = BUILD_DIR / f"stage-{stage}" / f"{lesson_id}.pdf"
    if not pdf.exists():
        return md, None, "missing"
    if md.stat().st_mtime > pdf.stat().st_mtime:
        return md, pdf, "drift"
    return md, pdf, "ok"


def check_worksheet_or_reader(rel_path: str) -> tuple[Path, Path | None, str]:
    """Check a worksheet or reader file. rel_path relative to its source dir."""
    # Try worksheets first, then readers
    for src_dir, build_subdir in [
        (WORKSHEETS_DIR, "worksheets"),
        (READERS_DIR, "readers"),
    ]:
        md = src_dir / rel_path
        if md.exists():
            # PDFs preserve relative path under build/worksheets/ or build/readers/
            pdf = BUILD_DIR / build_subdir / rel_path.replace(".md", ".pdf")
            if not pdf.exists():
                return md, None, "missing"
            if md.stat().st_mtime > pdf.stat().st_mtime:
                return md, pdf, "drift"
            return md, pdf, "ok"
    return Path(rel_path), None, "missing-md"


def main():
    parser = argparse.ArgumentParser(description="Detect source/build drift")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], help="Check one stage only")
    parser.add_argument("--include-worksheets", action="store_true", help="Also check worksheets (PDFs live in build/worksheets/, must be rendered separately)")
    parser.add_argument("--include-readers", action="store_true", help="Also check readers (PDFs live in build/readers/, must be rendered separately)")
    parser.add_argument("--quiet", action="store_true", help="Only print problems")
    args = parser.parse_args()

    if not CATALOG.exists():
        print(f"Error: catalog not found at {CATALOG}")
        sys.exit(2)

    counts = {"ok": 0, "drift": 0, "missing": 0, "missing-md": 0}
    problems = []

    # 1. Lessons from catalog (always checked)
    with open(CATALOG, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        stage = int(row["stage"])
        if args.stage and stage != args.stage:
            continue
        md, pdf, status = check_lesson_pdf(stage, row["lesson_id"])
        counts[status] = counts.get(status, 0) + 1
        if status != "ok":
            problems.append((status, md, pdf))

    # 2. Worksheets (opt-in)
    if args.include_worksheets:
        for md in WORKSHEETS_DIR.rglob("*.md"):
            rel = md.relative_to(WORKSHEETS_DIR)
            _, pdf, status = check_worksheet_or_reader(str(rel))
            counts[status] = counts.get(status, 0) + 1
            if status != "ok":
                problems.append((status, md, pdf))

    # 3. Readers (opt-in)
    if args.include_readers:
        for md in READERS_DIR.rglob("*.md"):
            rel = md.relative_to(READERS_DIR)
            _, pdf, status = check_worksheet_or_reader(str(rel))
            counts[status] = counts.get(status, 0) + 1
            if status != "ok":
                problems.append((status, md, pdf))

    # Report
    scope = f"stage {args.stage}" if args.stage else "all stages"
    extra = []
    if args.include_worksheets:
        extra.append("worksheets")
    if args.include_readers:
        extra.append("readers")
    scope_full = scope + (f" + {'+'.join(extra)}" if extra else "")

    if not args.quiet:
        print(f"==> Drift check ({scope_full})")
        print(f"  OK:      {counts['ok']}")
        print(f"  Drift:   {counts['drift']}  (MD newer than PDF)")
        print(f"  Missing: {counts['missing']}  (MD exists, PDF never built)")
        if counts["missing-md"]:
            print(f"  No MD:   {counts['missing-md']}  (catalog references missing MD)")

    if problems:
        if not args.quiet:
            print()
            print("Problems:")
        for status, md, pdf in problems:
            if status == "drift":
                print(f"  DRIFT   {md.relative_to(ROOT)}")
            elif status == "missing":
                print(f"  MISSING {md.relative_to(ROOT)}")
            elif status == "missing-md":
                print(f"  NO-MD   catalog: {md}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
