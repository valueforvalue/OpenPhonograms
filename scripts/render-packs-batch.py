#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
render-packs-batch.py — Build lesson packs via render-then-split.

REPLACES build-lesson-pack.py's per-pack render path with a single
stage-level render that gets split by H1 bookmark into per-pack PDFs.

Why:
  Per-pack render on Windows costs ~10s (Pango/fontconfig scans 859
  system fonts per WeasyPrint call). 48 packs × 10s = 8 min per stage.
  Rendering all 48 packs as ONE document = ~30s. We pay one Pango scan
  instead of 48.

Output:
  packs/stage-N/lesson-NN-{slug}.pdf

Usage:
  python scripts/render-packs-batch.py --stage 1
  python scripts/render-packs-batch.py --all --jobs 4
"""

import argparse
import csv
import io
import re
import sys
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.build_log import get_logger, phase
from framework.pdf_merge import render_and_split

# Import the dashed-name module via importlib (Python doesn't allow
# `import build-lesson-pack`).
import importlib.util as _importlib_util
_BLP_PATH = ROOT / "scripts" / "build-lesson-pack.py"
_spec = _importlib_util.spec_from_file_location("build_lesson_pack", _BLP_PATH)
_blp = _importlib_util.module_from_spec(_spec)
_spec.loader.exec_module(_blp)
build_cover_page = _blp.build_cover_page
build_at_a_glance = _blp.build_at_a_glance
build_home_practice = _blp.build_home_practice
load_catalog = _blp.load_catalog
worksheet_for_lesson = _blp.worksheet_for_lesson
flashcards_for_lesson = _blp.flashcards_for_lesson
reader_for_lesson = _blp.reader_for_lesson
lesson_md_path = _blp.lesson_md_path
PAGE_BREAK = _blp.PAGE_BREAK

PACKS_DIR = ROOT / "packs"
TMP_DIR = ROOT / "build" / "tmp-render-packs"

log = get_logger("render-packs-batch")


def assemble_pack_markdown(row: dict, catalog: list[dict]) -> str | None:
    """Assemble all components of a pack into a single MD string.

    Returns the combined MD, or None if the lesson MD is missing.
    """

    lesson_path = lesson_md_path(row)
    if not lesson_path.exists():
        return None

    lesson_text = lesson_path.read_text(encoding="utf-8")
    # Strip the lesson's own "Next lesson:" footer
    lesson_text = re.sub(
        r"\*\*Next lesson:\*\*.*?(?=\n\n|\Z)",
        "",
        lesson_text,
        flags=re.DOTALL,
    )

    worksheet_path = worksheet_for_lesson(row)
    card_paths = flashcards_for_lesson(row, catalog)
    reader_path = reader_for_lesson(row)

    missing = []
    if row["type"] == "phonogram-intro" and not worksheet_path:
        missing.append("phonogram worksheet")
    new_rule = (row.get("new_rule") or "").strip()
    if new_rule and not worksheet_path and row["type"] in ("rule-intro", "rule-practice"):
        missing.append("rule worksheet")
    if row["type"] == "phonogram-intro" and not card_paths:
        missing.append("flash cards")

    parts = []
    parts.append(build_cover_page(row, missing))
    parts.append(PAGE_BREAK)
    parts.append(build_at_a_glance(row))
    parts.append(lesson_text)
    if worksheet_path:
        parts.append(PAGE_BREAK)
        # No extra H1 + HR wrapper here — the worksheet MD already
        # starts with its own title (e.g. "# Phonogram Practice: sh").
        # Adding `# Worksheet` + a thematic break above pushes the
        # worksheet body down ~1 line, which cascades into a
        # near-empty trailing page in long phonogram worksheets
        # (see issue #35). The PAGE_BREAK already gives the section
        # a clear visual start.
        parts.append(worksheet_path.read_text(encoding="utf-8"))
    if card_paths:
        parts.append(PAGE_BREAK)
        # See note above — the cards MD carries its own title.
        for cp in card_paths:
            parts.append(cp.read_text(encoding="utf-8"))
            parts.append("\n\n---\n\n")
    if reader_path and row["type"] != "reader":
        parts.append(PAGE_BREAK)
        # See note above — the reader MD carries its own title.
        parts.append(reader_path.read_text(encoding="utf-8"))
    parts.append(build_home_practice(lesson_text))
    return "\n".join(parts)


def stage_packs(stage: int, no_render: bool = False) -> tuple[int, int]:
    """Render all packs for one stage as one PDF, split by bookmark.

    Returns (ok_count, fail_count).
    """
    catalog = load_catalog()
    rows = [r for r in catalog if int(r["stage"]) == stage]
    rows.sort(key=lambda r: int(r["lesson_num"]))
    if not rows:
        log.info(f"Stage {stage}: no lessons in catalog")
        return 0, 0

    out_dir = PACKS_DIR / f"stage-{stage}"
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_pdf = TMP_DIR / f"stage-{stage}-packs.pdf"
    tmp_md_dir = TMP_DIR / f"stage-{stage}-mds"
    tmp_md_dir.mkdir(parents=True, exist_ok=True)

    # Write one MD file per pack (so weasyprint processes them as
    # separate sections with separate bookmarks).
    md_paths: list[Path] = []
    skip_rows: list[dict] = []
    for row in rows:
        pack_md = assemble_pack_markdown(row, catalog)
        if pack_md is None:
            skip_rows.append(row)
            continue
        slug = row["lesson_id"]
        lnum = int(row["lesson_num"])
        md_path = tmp_md_dir / f"lesson-{lnum:02d}-{slug}.md"
        md_path.write_text(pack_md, encoding="utf-8")
        md_paths.append(md_path)

    if not md_paths:
        log.warning(f"Stage {stage}: all packs skipped (missing lesson MDs)")
        return 0, len(rows)

    # title_to_path: maps H1 "Lesson Pack: Lesson N — Title" to output PDF
    def title_to_path(title: str) -> Path | None:
        if not title.startswith("Lesson Pack:"):
            return None  # ignore other H1s (at-a-glance + lesson H1)
        m = re.search(r"Lesson Pack: Lesson (\d+)", title)
        if not m:
            return None
        ln = int(m.group(1))
        for r in rows:
            if int(r["lesson_num"]) == ln:
                slug = r["lesson_id"]
                return out_dir / f"lesson-{ln:02d}-{slug}.pdf"
        return None

    if no_render:
        # Write stub PDFs with placeholder content (for debug + tests).
        for r in rows:
            slug = r["lesson_id"]
            ln = int(r["lesson_num"])
            stub = out_dir / f"lesson-{ln:02d}-{slug}.md"
            md = assemble_pack_markdown(r, catalog)
            if md is not None:
                stub.write_text(md, encoding="utf-8")
        log.info(f"Stage {stage}: wrote {len(rows)} stub MDs (no-render)")
        return len(rows), 0

    t0 = time.perf_counter()
    result = render_and_split(
        md_paths,
        title_to_path,
        combined_pdf=tmp_pdf,
        body_class=f"stage-{stage}",
    )
    total = time.perf_counter() - t0

    if not result.ok:
        log.error(f"Stage {stage}: {result.error}")
        return 0, len(rows)

    log.info(
        f"Stage {stage}: rendered {len(md_paths)} packs as 1 PDF "
        f"({result.render_seconds:.1f}s) + split ({result.split_seconds:.1f}s) "
        f"= {total:.1f}s total. Files written: {len(result.units)}."
    )
    if skip_rows:
        log.warning(
            f"Stage {stage}: skipped {len(skip_rows)} packs "
            f"(missing lesson MDs): {[r['lesson_id'] for r in skip_rows]}"
        )

    # Clean up temp (skip if KEEP_TMP env var set, for debugging)
    import os as _os
    if not _os.environ.get("KEEP_TMP"):
        for md_path in md_paths:
            md_path.unlink(missing_ok=True)
        tmp_md_dir.rmdir()
        tmp_pdf.unlink(missing_ok=True)

    return len(result.units), len(rows) - len(result.units)


def main():
    parser = argparse.ArgumentParser(
        description="Build lesson packs via render-then-split (fast batch path)"
    )
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5],
                        help="Build packs for one stage")
    parser.add_argument("--all", action="store_true",
                        help="Build packs for all stages")
    parser.add_argument("--no-render", action="store_true",
                        help="Write stub MDs only (debug pack assembly)")
    args = parser.parse_args()

    if not args.stage and not args.all:
        parser.error("specify --stage N or --all")

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    PACKS_DIR.mkdir(parents=True, exist_ok=True)

    stages = [args.stage] if args.stage else [1, 2, 3, 4, 5]
    phase("Render Lesson Packs (batch)")

    grand_ok = 0
    grand_fail = 0
    for stage in stages:
        ok, fail = stage_packs(stage, no_render=args.no_render)
        grand_ok += ok
        grand_fail += fail

    log.info(f"DONE: {grand_ok} packs built, {grand_fail} skipped/failed")
    sys.exit(1 if grand_fail else 0)


if __name__ == "__main__":
    main()