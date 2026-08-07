# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

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
sys.path.insert(0, str(ROOT))
CATALOG = ROOT / "framework" / "lesson-catalog.csv"
BUILD = ROOT / "build"
OUT_DIR = ROOT / "build" / "handbook"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_catalog() -> list[dict]:
    with open(CATALOG, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Human-readable section names per lesson type
TYPE_LABELS = {
    "phonemic-awareness": "Phonemic Awareness",
    "phonogram-intro": "Phonogram Lessons",
    "review": "Review Lessons",
    "vowel-concept": "Vowel Concepts",
    "handwriting": "Handwriting",
    "assessment": "Stage Assessment",
    "cvc-all": "CVC Words",
    "cvc-continuant": "CVC Continuant Blends",
    "cvc-stop": "CVC Stop Blends",
    "vc-words": "VC Words",
    "long-vowels": "Long Vowels",
    "silent-e-1": "Silent E",
    "silent-e-review-1": "Silent E Review",
    "silent-e-mastery": "Silent E Mastery",
    "silent-letter-review": "Silent Letter Review",
    "rule-intro": "Spelling Rules",
    "rule-practice": "Rule Practice",
    "rule-review": "Rule Review",
    "spelling-analysis": "Spelling Analysis",
    "say-to-spell": "Say-to-Spell",
    "syllable-division": "Syllable Division",
    "schwa-practice": "Schwa Practice",
    "hf-word": "High-Frequency Words",
    "reader": "Decodable Readers",
    "morphology": "Morphology",
    "vocabulary": "Vocabulary",
    "fluency": "Fluency",
    "composition": "Composition",
    "grammar": "Grammar",
    "practice": "Practice",
    "open-syllables": "Open Syllables",
    "ccvc-blends": "CCVC Blends",
    "ccvcc-blends": "CCVCC Blends",
    "cvcc-blends": "CVCC Blends",
}

# Section ordering per stage: defines which groups appear and in what order
# in the TOC. Stages not listed fall back to type-occurrence order.
SECTION_ORDER = {
    1: ["phonemic-awareness", "phonogram-intro", "review", "vowel-concept", "handwriting", "assessment"],
    2: ["phonogram-intro", "hf-word", "rule-intro", "rule-practice", "spelling-analysis", "reader", "review", "assessment"],
    3: ["silent-e-1", "silent-e-review-1", "phonogram-intro", "rule-intro", "syllable-division", "spelling-analysis", "hf-word", "reader", "assessment"],
    4: ["schwa-practice", "phonogram-intro", "rule-intro", "morphology", "hf-word", "reader", "review", "assessment"],
    5: ["phonogram-intro", "morphology", "vocabulary", "fluency", "composition", "grammar", "reader", "assessment"],
}


def make_toc(stage: int, lessons: list[dict]) -> str:
    """Generate a markdown table of contents listing every lesson grouped by type.

    Uses SECTION_ORDER when defined for the stage; otherwise falls back to
    first-occurrence order of lesson types.
    """
    ordered = sorted(lessons, key=lambda r: int(r["lesson_num"]))

    # Build groups: type -> list of (lesson_num, title)
    groups: dict[str, list[tuple[int, str]]] = {}
    for r in ordered:
        t = r["type"]
        groups.setdefault(t, []).append((int(r["lesson_num"]), r["title"]))

    # Choose section order
    if stage in SECTION_ORDER:
        order = list(SECTION_ORDER[stage])
        # Append any types that appeared but weren't in SECTION_ORDER
        for t in groups:
            if t not in order:
                order.append(t)
    else:
        order = list(groups.keys())

    lines = ["## Table of Contents", ""]
    lines.append("All lessons in this stage, grouped by section. PDF reader sidebar shows page numbers via bookmarks; for print, scan the lesson number to locate (matches the small number in each lesson's header).")
    lines.append("")

    for t in order:
        if t not in groups:
            continue
        label = TYPE_LABELS.get(t, t.replace("-", " ").title())
        lines.append(f"### {label}")
        lines.append("")
        for ln, title in groups[t]:
            # Internal link to the lesson anchor injected by framework/render.py
            lines.append(f"- **Lesson {ln}:** {title}")
        lines.append("")

    # Linear-order quick reference (all lessons in numerical order)
    lines.append("---")
    lines.append("")
    lines.append("## Quick Reference: Lessons in Teaching Order")
    lines.append("")
    lines.append("All lessons in this stage in strict numerical order. PDF reader sidebar shows page numbers via bookmarks.")
    lines.append("")
    for r in ordered:
        ln = int(r["lesson_num"])
        title = r["title"]
        lines.append(f"- **Lesson {ln}:** {title}")
    lines.append("")

    return "\n".join(lines)


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

<div class="brand-cover">

<img src="../../assets/logo/openphonograms-logo.svg" alt="OpenPhonograms" />

<p class="tagline">Teacher Manual &mdash; {n_lessons} lessons bound in one volume</p>

</div>

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
3. **See the Table of Contents on the next page** for a printable index of all {n_lessons} lessons grouped by section.

### What this handbook replaces

This is the open-source equivalent of a commercial curriculum's "Teacher's Manual" — one bound book with all lessons and a complete index. The print commercial version runs 200-350 pages per level; this PDF runs {n_lessons} + cover + TOC pages.

---

## Materials Needed for Stage {stage}

Before starting this stage, gather or print the following:

- **Whiteboard + markers** (or paper + pencil for each student)
- **Phonogram flashcards** (Stage {stage}: {pg_count} new phonograms — printed from `04-Quick-Reference/Phonogram-Chart.pdf` or `worksheets/cards/stage-{stage}/`)
- **Lesson packs** (printed from `06-Lesson-Packs/stage-{stage}/` — one pack per lesson, includes worksheet + flash cards)
- **Decodable readers** as needed (Stage {stage} uses readers listed in `08-Decodable-Readers/stage-{stage}/`)
- **Timer** (for spelling analysis and assessments)
- **Pencils, erasers, lined paper**

See the `binding-instructions.pdf` in the release root for help organizing these into a 3-ring binder per stage.

---

*Curriculum: OpenPhonograms (open-source, MIT licensed)*

<div class="page-break"></div>

{make_toc(stage, lessons)}

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

    cover_pdf = cover_md.with_suffix(".pdf")
    from framework.render import render_md_to_pdf
    render_md_to_pdf(cover_md, cover_pdf, doc_type="lesson")

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
