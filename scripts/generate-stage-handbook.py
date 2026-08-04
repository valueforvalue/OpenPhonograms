"""Generate per-stage teacher handbook PDFs.

Combines all lesson PDFs in a stage into a single bound-book-style PDF with
PDF bookmarks for every lesson.

Output:
  build/handbook/stage-{N}-handbook.pdf   (one per stage, includes all lessons
                                            + assessment + stage cover page)

Usage:
  python scripts/generate-stage-handbook.py [--stage N] [--no-render]
"""

import argparse
import csv
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "framework" / "lesson-catalog.csv"
BUILD = ROOT / "build"
OUT_DIR = ROOT / "build" / "handbook"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_catalog() -> list[dict]:
    with open(CATALOG, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def make_stage_cover(stage: int, lessons: list[dict]) -> str:
    """Build a markdown cover-page for the stage handbook."""
    if stage == 1:
        age = "Pre-K (4-5)"
        title = "Stage 1: Phonemic Awareness & First Phonograms"
        desc = "Stage 1 develops the auditory foundation. Children learn to hear, blend, and segment sounds before letters are introduced. Then 26 single-letter phonograms are taught in 5 groups, with one phonemic-awareness lesson between each group."
        n_lessons = 48
        pg_count = 26
        rule_count = 0
    elif stage == 2:
        age = "Kindergarten (5-6)"
        title = "Stage 2: CVC Words & First Multi-Letter Phonograms"
        desc = "Stage 2 introduces 25 multi-letter phonograms plus the first spelling rules. Children practice Spelling Analysis on 3-5 words per lesson."
        n_lessons = 56
        pg_count = 25
        rule_count = 6
    elif stage == 3:
        age = "Grade 1 (6-7)"
        title = "Stage 3: Silent E & Vowel Teams"
        desc = "Stage 3 covers the 9 reasons for Silent E, then 17 advanced phonograms. Syllable division rules introduced. Say-to-Spell method used for multi-syllable words from Lesson 47 onward."
        n_lessons = 56
        pg_count = 17
        rule_count = 9
    elif stage == 4:
        age = "Grade 2 (7-8)"
        title = "Stage 4: Suffixing, Latin /sh/ & Morphology"
        desc = "Stage 4 begins with the schwa deep dive, then suffixing rules, Latin /sh/ phonograms (ti, ci, si), and morphology."
        n_lessons = 48
        pg_count = 3
        rule_count = 13
    else:  # stage 5
        age = "Grade 3+ (8+)"
        title = "Stage 5: Roots, Fluency & Composition"
        desc = "Stage 5 teaches 25 Latin/Greek roots. Fluency drills, sentence and paragraph composition, parts of speech, and punctuation."
        n_lessons = 40
        pg_count = 0
        rule_count = 0

    pg_list = ", ".join(sorted({(r.get("new_phonogram") or "").strip() for r in lessons if (r.get("new_phonogram") or "").strip()}))

    # Count lesson types
    types = {}
    for r in lessons:
        types[r["type"]] = types.get(r["type"], 0) + 1
    types_str = ", ".join(f"{v} {k}" for k, v in sorted(types.items(), key=lambda x: -x[1]))

    return f"""# {title}

**Stage {stage}** · {age} · {n_lessons} lessons

---

## About this handbook

{desc}

This handbook contains all {n_lessons} lessons of Stage {stage}, bound into a single PDF with clickable bookmarks. Each lesson starts on its own page. Use the PDF reader's bookmark sidebar to navigate.

### At a glance

- **Lessons:** {n_lessons}
- **New phonograms:** {pg_count}
- **New rules:** {rule_count}
- **Lesson types:** {types_str}
- **New phonograms taught:** {pg_list}

### How to use

1. **Print the lesson pack PDF** instead — each per-lesson pack bundles this lesson with its matched worksheet and flash cards. See `06-Lesson-Packs/stage-{stage}/` in the release ZIP.
2. **Use this handbook** for at-the-desk reference, lesson planning, or on a tablet.

### What this handbook replaces

This is the open-source equivalent of a commercial curriculum's "Teacher's Manual" — one bound book with all lessons and a complete index. The print commercial version runs 200-350 pages per level; this PDF runs {n_lessons} + cover pages.

---

*Curriculum: Uncovering the Logic of English (open-source adaptation)*

<div class="page-break"></div>

"""


def assemble_handbook(stage: int, no_render: bool = False):
    """Combine all lesson PDFs in a stage into one bound handbook PDF with bookmarks."""
    catalog = load_catalog()
    lessons = [r for r in catalog if int(r["stage"]) == stage]
    if not lessons:
        print(f"  SKIP  Stage {stage} (no lessons)")
        return None

    # 1. Render the cover page
    cover_md = OUT_DIR / f"stage-{stage}-handbook-cover.md"
    cover_md.write_text(make_stage_cover(stage, lessons), encoding="utf-8")

    if no_render:
        return cover_md

    from weasyprint import HTML as WHTML
    cover_pdf = cover_md.with_suffix(".pdf")
    WHTML(filename=str(cover_md)).write_pdf(str(cover_pdf))

    # 2. Merge cover + all lesson PDFs into one handbook
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter()
    writer.append_pages_from_reader(PdfReader(str(cover_pdf)))
    for r in sorted(lessons, key=lambda r: int(r["lesson_num"])):
        ln = int(r["lesson_num"])
        lid = r["lesson_id"]
        pdf = BUILD / f"stage-{stage}" / f"{lid}.pdf"
        if pdf.exists():
            writer.append_pages_from_reader(PdfReader(str(pdf)))
        else:
            print(f"  WARN  missing {pdf.relative_to(ROOT)}")

    out = OUT_DIR / f"stage-{stage}-handbook.pdf"
    with open(out, "wb") as f:
        writer.write(f)

    # Add per-lesson bookmarks
    cover_pages = len(PdfReader(str(cover_pdf)).pages)
    add_bookmarks(out, lessons, cover_pages)

    # Clean up temp
    cover_md.unlink(missing_ok=True)
    cover_pdf.unlink(missing_ok=True)

    print(f"  OK   {out.relative_to(ROOT)}  ({len(lessons)} lessons + cover)")
    return out


def add_bookmarks(pdf_path: Path, lessons: list[dict], cover_pages: int):
    """Add a top-level bookmark for each lesson in the merged handbook.

    cover_pages: number of pages in the cover section (usually 1).
    """
    from pypdf import PdfReader, PdfWriter

    # Re-read each lesson PDF to find its page count, then compute starting page
    page_offset = cover_pages
    bookmarks = []  # (page_index, title)
    for r in sorted(lessons, key=lambda r: int(r["lesson_num"])):
        ln = int(r["lesson_num"])
        lid = r["lesson_id"]
        title = r["title"]
        pdf = BUILD / f"stage-{r['stage']}" / f"{lid}.pdf"
        if pdf.exists():
            lesson_pages = len(PdfReader(str(pdf)).pages)
            bookmarks.append((page_offset, f"Lesson {ln}: {title}"))
            page_offset += lesson_pages

    # Re-open the merged PDF and add bookmarks
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    for page_idx, title in bookmarks:
        writer.add_outline_item(title, page_idx)

    with open(pdf_path, "wb") as f:
        writer.write(f)


def main():
    parser = argparse.ArgumentParser(description="Generate stage handbooks")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], help="One stage only")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering")
    args = parser.parse_args()

    stages = [args.stage] if args.stage else [1, 2, 3, 4, 5]
    print("==> Generating stage handbooks")
    for stage in stages:
        assemble_handbook(stage, no_render=args.no_render)
    print(f"\nDone: {len(stages)} handbook(s)")


if __name__ == "__main__":
    main()
