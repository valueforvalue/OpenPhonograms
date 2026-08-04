"""Build cohesive lesson packs for teacher use.

A pack combines, for one lesson:
  - Cover page (stage, lesson #, title, type, new PG/rule, prep checklist)
  - Lesson markdown (the teaching script)
  - Worksheet (matched from worksheets/phonograms or worksheets/rules)
  - Flash cards for all PGs taught so far in this stage
  - Reader (if lesson type is 'reader' or catalog's reader column is set)
  - Home practice footer (derived from lesson MD)

Output:
  packs/stage-{N}/lesson-{NN}-{slug}.pdf

Usage:
  python scripts/build-lesson-pack.py --lesson pg-d
  python scripts/build-lesson-pack.py --stage 1
  python scripts/build-lesson-pack.py --all
  python scripts/build-lesson-pack.py --stage 1 --bundle   # one giant stage PDF
"""

import argparse
import csv
import io
import re
import sys
from pathlib import Path

# Force utf-8 stdout on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
# Allow `from framework.render import ...`
sys.path.insert(0, str(ROOT))
LESSONS_DIR = ROOT / "lessons"
WORKSHEETS_PG = ROOT / "worksheets" / "phonograms"
WORKSHEETS_RULES = ROOT / "worksheets" / "rules"
WORKSHEETS_CARDS = ROOT / "worksheets" / "cards"
WORKSHEETS_BLANK = ROOT / "worksheets" / "blank"
READERS_DIR = ROOT / "readers"
CATALOG_PATH = ROOT / "framework" / "lesson-catalog.csv"
PACKS_DIR = ROOT / "packs"

PAGE_BREAK = "\n\n<div class=\"page-break\"></div>\n\n"


def load_catalog() -> list[dict]:
    """Load lesson catalog as list of dicts."""
    with open(CATALOG_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def lesson_md_path(row: dict) -> Path:
    """Path to the lesson MD file for a catalog row."""
    return LESSONS_DIR / f"stage-{row['stage']}" / f"{row['lesson_id']}.md"


def worksheet_for_lesson(row: dict) -> Path | None:
    """Match a worksheet to the lesson based on lesson type + catalog columns."""
    lesson_type = row["type"]
    new_pg = (row.get("new_phonogram") or "").strip()
    new_rule = (row.get("new_rule") or "").strip()

    # phonogram-intro → phonogram practice worksheet for the new PG
    if lesson_type == "phonogram-intro" and new_pg:
        candidate = WORKSHEETS_PG / f"pg-{new_pg}.md"
        if candidate.exists():
            return candidate

    # silent-e sub-reasons (12.1, 12.2, ..., 12.9) or '12.all' → rule-12 worksheet
    if new_rule.startswith("12.") or new_rule == "12" or new_rule == "12.all":
        candidate = WORKSHEETS_RULES / "rule-12.md"
        if candidate.exists():
            return candidate

    # rule-intro or any lesson introducing a new rule → rule worksheet
    # Handle multi-rule values: '19-20' (both), '12.1-12.4' (range — covered above),
    # '13-14' (range of regular rules)
    if new_rule:
        # Try first numeric token before any '.', '-', '+', ',' separator
        first_num = re.split(r"[.\-+,]", new_rule, maxsplit=1)[0]
        candidate = WORKSHEETS_RULES / f"rule-{first_num}.md"
        if candidate.exists():
            return candidate

    return None


def flashcards_for_lesson(row: dict, catalog: list[dict]) -> list[Path]:
    """Flash cards covering all PGs taught up to and including this lesson in the same stage."""
    stage = int(row["stage"])
    lesson_num = int(row["lesson_num"])

    # Collect all PGs introduced in this stage at-or-before this lesson
    pgs_introduced = []
    for r in catalog:
        if int(r["stage"]) != stage:
            continue
        if int(r["lesson_num"]) > lesson_num:
            continue
        pg = (r.get("new_phonogram") or "").strip()
        if pg:
            pgs_introduced.append((int(r["lesson_num"]), pg))

    if not pgs_introduced:
        return []

    # Group PGs by stage-group batch (singles 1-7, multi 1-12) based on
    # how the existing flash-singles/flash-multi sheets were generated.
    # singles: Stage 1 lesson_num 9-40 in groups of ~4
    # multi: Stage 2+ lesson_nums in groups of ~4
    # Heuristic: pick the flash sheet whose index covers this PG's lesson_num.
    if stage == 1:
        # Single-letter PGs in Stage 1: lessons 9,10,11,12,13,14 then 16-21, etc.
        # flash-singles-1 covers lessons 9-12 (a,d,g,c)
        # flash-singles-2 covers 13-16 (o,qu,s,t) — but qu/s/t may split differently
        # Simplest correct mapping: pick the highest flash-singles-N where
        # 4*(N-1) <= (stage1_lnum_of_last_pg - 9) < 4*N
        last_lnum = pgs_introduced[-1][0]
        # stage 1 PGs start at lesson 9, so index = (last - 9) // 4 + 1, clamped to 1-7
        sheet_idx = max(1, min(7, (last_lnum - 9) // 4 + 1))
        card = WORKSHEETS_CARDS / f"flash-singles-{sheet_idx}.md"
        return [card] if card.exists() else []
    else:
        # Stage 2+ multi-letter PGs.
        # Each flash-multi-N covers 4 PGs from the cumulative multi-letter pool
        # (MULTI dict first, then MULTI3 dict, in catalog order across stages).
        # qu is a special case: single-letter taught in Stage 1, multi-letter
        # listed first in MULTI; exclude from this count.
        all_multis = []
        for r in catalog:
            pg = (r.get("new_phonogram") or "").strip()
            if pg and len(pg) > 1 and pg != "qu":
                all_multis.append((int(r["stage"]), int(r["lesson_num"]), pg))
        if not all_multis:
            return []
        # Position of this lesson in the cumulative multi-letter sequence:
        # count how many multi-letter PGs are at-or-before this lesson
        this_pos = sum(
            1 for s, ln, _ in all_multis
            if (s, ln) <= (stage, lesson_num)
        )
        sheet_idx = max(1, min(12, (this_pos - 1) // 4 + 1))
        card = WORKSHEETS_CARDS / f"flash-multi-{sheet_idx}.md"
        return [card] if card.exists() else []


def reader_for_lesson(row: dict) -> Path | None:
    """Path to reader MD if catalog's reader column references one."""
    reader_ref = (row.get("reader") or "").strip()
    if not reader_ref:
        return None
    # reader column values look like: "readers/stage-2/001-fred-the-frog.md"
    candidate = ROOT / reader_ref
    if candidate.exists():
        return candidate
    # Fallback: try without stage subdir
    fallback = READERS_DIR / Path(reader_ref).name
    if fallback.exists():
        return fallback
    return None


def build_cover_page(row: dict, missing_assets: list[str]) -> str:
    """Cover page MD for a lesson pack."""
    stage = row["stage"]
    lnum = int(row["lesson_num"])
    title = row["title"]
    ltype = row["type"]
    new_pg = (row.get("new_phonogram") or "").strip()
    new_rule = (row.get("new_rule") or "").strip()

    # Materials checklist
    checklist = [
        "- [ ] Phonogram cards for review",
        "- [ ] Whiteboard + marker",
        "- [ ] Pencil and paper",
    ]
    if ltype == "phonogram-intro" and new_pg:
        checklist.append(f"- [ ] New phonogram card: **{new_pg}**")
    if ltype == "rule-intro" and new_rule:
        checklist.append(f"- [ ] Spelling rule reference for Rule {new_rule}")
    if ltype == "reader":
        checklist.append("- [ ] Decodable reader printed or on tablet")
    if ltype == "assessment":
        checklist.append("- [ ] Pencils, timer, scoring sheet")

    new_pg_line = f"\n**New phonogram:** `{new_pg}`" if new_pg else ""
    new_rule_line = f"\n**New rule:** Rule {new_rule}" if new_rule else ""

    missing_block = ""
    if missing_assets:
        missing_block = "\n\n> **Missing assets:** " + ", ".join(missing_assets) + "\n"

    cover = f"""# Lesson Pack: Lesson {lnum} — {title}

**Stage {stage}** · Lesson {lnum} · `{ltype}`{new_pg_line}{new_rule_line}

---

## Prep Checklist

Print this pack before the lesson. Check off as you gather materials.

{chr(10).join(checklist)}

---

## Pack Contents

| Page | Section |
|------|---------|
| 1 | This cover page |
| 2 | Teacher script |
| 3+ | Worksheet (if any) |
| last | Flash cards for review |
{"| last | Reader (if any) |" if ltype == "reader" or (row.get("reader") or "").strip() else ""}

---

*Pack generated for the *Uncovering the Logic of English* curriculum.*
{missing_block}

<div class=\"page-break\"></div>

"""
    return cover


def build_home_practice(lesson_md: str) -> str:
    """Extract 'Practice at home' footer as its own section if present."""
    m = re.search(r"\*Practice at home:\*(.+?)(?:\n\n|$)", lesson_md, re.DOTALL)
    if not m:
        return ""
    practice = m.group(1).strip()
    return (
        f"\n\n<div class=\"page-break\"></div>\n\n"
        f"# Home Practice\n\n"
        f"> {practice}\n\n"
        f"---\n\n"
        f"*Sign and date when complete:* _______________________\n"
    )


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_one_pack(row: dict, catalog: list[dict], bundle: bool = False, no_render: bool = False) -> tuple[Path | None, list[str], Path | None]:
    """Build a single lesson pack. Returns (output_pdf_path, missing_assets, combined_md_path)."""
    stage = row["stage"]
    lnum = int(row["lesson_num"])
    lesson_id = row["lesson_id"]
    title = row["title"]

    missing = []
    lesson_path = lesson_md_path(row)
    if not lesson_path.exists():
        missing.append(f"lesson MD: {lesson_path.relative_to(ROOT)}")
        return None, missing, None  # cannot build without lesson MD

    lesson_text = lesson_path.read_text(encoding="utf-8")
    worksheet_path = worksheet_for_lesson(row)
    card_paths = flashcards_for_lesson(row, catalog)
    reader_path = reader_for_lesson(row)

    # Track missing assets
    if row["type"] == "phonogram-intro" and not worksheet_path:
        missing.append("phonogram worksheet")
    new_rule = (row.get("new_rule") or "").strip()
    if new_rule and not worksheet_path and row["type"] in ("rule-intro", "rule-practice"):
        missing.append("rule worksheet")
    # Flash cards: warn only if phonogram-intro and no cards found
    # (review/PA/assessment lessons don't need new stage cards — teacher uses binder)
    if row["type"] == "phonogram-intro" and not card_paths:
        missing.append("flash cards")

    # Strip the lesson's own "**Next lesson:**" footer (we don't want
    # the pack pointing to next lesson — pack is self-contained)
    lesson_text = re.sub(
        r"\*\*Next lesson:\*\*.*?(?=\n\n|\Z)",
        "",
        lesson_text,
        flags=re.DOTALL,
    )

    # Compose pack
    parts = []
    parts.append(build_cover_page(row, missing))
    parts.append(lesson_text)
    if worksheet_path:
        parts.append(PAGE_BREAK)
        parts.append(f"# Worksheet\n\n---\n\n")
        parts.append(worksheet_path.read_text(encoding="utf-8"))
    if card_paths:
        parts.append(PAGE_BREAK)
        parts.append(f"# Flash Cards for Review\n\n---\n\n")
        for cp in card_paths:
            parts.append(cp.read_text(encoding="utf-8"))
            parts.append("\n\n---\n\n")
    # Only append standalone reader MD if lesson is NOT itself a reader lesson.
    # Reader-type lessons already contain the full story inline.
    if reader_path and row["type"] != "reader":
        parts.append(PAGE_BREAK)
        parts.append(f"# Decodable Reader\n\n---\n\n")
        parts.append(reader_path.read_text(encoding="utf-8"))
    parts.append(build_home_practice(lesson_text))

    combined = "\n".join(parts)

    slug = slugify(title)
    out_dir = PACKS_DIR / f"stage-{stage}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / f"lesson-{lnum:02d}-{slug}.pdf"
    debug_md = out_dir / f"lesson-{lnum:02d}-{slug}.md"
    debug_md.write_text(combined, encoding="utf-8")

    if no_render:
        return None, missing, debug_md

    # Write combined MD to a temp path so render can read it
    # Use lesson dir as base so image paths in lesson MD still resolve
    temp_md = lesson_path.parent / f"_pack-{lesson_id}.md"
    temp_md.write_text(combined, encoding="utf-8")

    try:
        from framework.render import render_md_to_pdf
        render_md_to_pdf(temp_md, out_pdf, doc_type="lesson")
    except ModuleNotFoundError as e:
        missing.append(f"render unavailable: {e}")
        return None, missing, debug_md
    finally:
        if temp_md.exists():
            temp_md.unlink()

    return out_pdf, missing, debug_md


def cmd_lesson(lesson_id: str, catalog: list[dict], no_render: bool = False):
    row = next((r for r in catalog if r["lesson_id"] == lesson_id), None)
    if not row:
        print(f"Error: lesson_id not found in catalog: {lesson_id}")
        sys.exit(1)
    out, missing, md_path = build_one_pack(row, catalog, no_render=no_render)
    if out is None and md_path is None:
        print(f"  SKIP {lesson_id}: missing lesson MD")
        return
    target = out if out else md_path
    status = "OK" if not missing else f"WARN (missing: {', '.join(missing)})"
    print(f"  {status} {target.relative_to(ROOT)}")


def cmd_stage(stage: int, bundle: bool, catalog: list[dict], no_render: bool = False):
    rows = [r for r in catalog if int(r["stage"]) == stage]
    print(f"Building Stage {stage} packs: {len(rows)} lessons")
    n_ok = n_warn = 0
    for row in rows:
        out, missing, md_path = build_one_pack(row, catalog, no_render=no_render)
        if out is None and md_path is None:
            print(f"  SKIP {row['lesson_id']}: missing lesson MD")
            continue
        if missing:
            n_warn += 1
            target = out if out else md_path
            print(f"  WARN {target.relative_to(ROOT)}: missing {', '.join(missing)}")
        else:
            n_ok += 1
    print(f"Done: {n_ok} clean, {n_warn} with warnings")
    if bundle:
        print("(bundle mode not yet implemented — render per-lesson packs only)")


def cmd_all(catalog: list[dict], no_render: bool = False):
    for stage in range(1, 6):
        cmd_stage(stage, False, catalog, no_render=no_render)


def main():
    parser = argparse.ArgumentParser(description="Build cohesive lesson packs")
    parser.add_argument("--lesson", help="Build pack for one lesson_id (e.g. pg-d)")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], help="Build all packs for a stage")
    parser.add_argument("--all", action="store_true", help="Build all 248 packs")
    parser.add_argument("--bundle", action="store_true", help="(Future) merge all stage packs into one PDF")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering (test pack assembly only)")
    args = parser.parse_args()

    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = load_catalog()

    if args.lesson:
        cmd_lesson(args.lesson, catalog, no_render=args.no_render)
    elif args.stage:
        cmd_stage(args.stage, args.bundle, catalog, no_render=args.no_render)
    elif args.all:
        cmd_all(catalog, no_render=args.no_render)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
