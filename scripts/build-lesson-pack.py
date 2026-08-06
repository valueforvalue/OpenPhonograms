# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

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
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# Force utf-8 stdout on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
# Allow `from framework.render import ...`
sys.path.insert(0, str(ROOT))

# Point WeasyPrint at MSYS2's GTK3 runtime DLLs on Windows (one-time install
# via MSYS2: pacman -S mingw-w64-x86_64-pango). Idempotent — no-op if set.
if sys.platform == "win32" and "WEASYPRINT_DLL_DIRECTORIES" not in os.environ:
    candidate = Path(r"C:/msys64/mingw64/bin")
    if candidate.exists():
        os.environ["WEASYPRINT_DLL_DIRECTORIES"] = str(candidate)

# Build logging (file + console). Must be imported after sys.path is set.
from framework.build_log import (
    get_logger,
    phase,
    Progress,
    WorkerLogQueue,
    set_worker_queue,
    attach_worker_handler,
    drain_worker_queue,
)

log = get_logger("pack")
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
        # Try stage-grouped mirror first, then flat
        for sub in (WORKSHEETS_PG / f"stage-{row['stage']}" / f"pg-{new_pg}.md",
                    WORKSHEETS_PG / f"pg-{new_pg}.md"):
            if sub.exists():
                return sub

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
        for sub in (WORKSHEETS_RULES / f"stage-{row['stage']}" / f"rule-{first_num}.md",
                    WORKSHEETS_RULES / f"rule-{first_num}.md"):
            if sub.exists():
                return sub

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
        "- [ ] At-a-glance reference card (page 2)",
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
| 2 | At-a-glance reference card |
| 3 | Teacher script |
| 4+ | Worksheet (if any) |
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


# At-a-glance data per phonogram: sounds + 5 example words + common mistake.
# Sourced from worksheets/phonograms/ data; this is a teaching summary,
# not the full worksheet.
AT_A_GLANCE_PG = {
    # Stage 1 single-letter
    "a": ("/ă/ /ā/ /ä/", "at, make, father", "Always teach all 3 sounds. 'A' is not just 'a says /ă/'."),
    "b": ("/b/", "bat, boy, bell", "B never says /b/ silently like the P-rule. Different sound."),
    "c": ("/k/ /s/", "cat, city", "Hard /k/ by default. Soft /s/ before e/i/y (Rule 1)."),
    "d": ("/d/", "dog, dig, desk", "D never goes silent in English."),
    "e": ("/ĕ/ /ē/", "bed, me", "Short at start of word, long when final or 'open syllable'."),
    "f": ("/f/", "fun, fish, four", "F is one of few sounds that can be spelled two ways (ph, gh)."),
    "g": ("/g/ /j/", "go, gem", "Hard /g/ by default. Soft /j/ before e/i/y (Rule 2)."),
    "h": ("/h/", "hat, his, house", "H is silent in a few words (honest, hour)."),
    "i": ("/ĭ/ /ī/ /ē/", "it, find, baby", "Three sounds. The /ē/ sound comes from open syllables (Rule 6)."),
    "j": ("/j/", "jam, jump, jug", "J never starts a true English base word."),
    "k": ("/k/", "kit, king, knee", "Silent K before N is common (knee, know, knife)."),
    "l": ("/l/", "leg, log, lake", "L is always pronounced in English."),
    "m": ("/m/", "man, make, more", "M is always pronounced."),
    "n": ("/n/", "net, nine, night", "Silent N in 'gn' before vowels (gnome, sign)."),
    "o": ("/ŏ/ /ō/", "hot, go", "Open-syllable O says /ō/ (no, open, total)."),
    "p": ("/p/", "pat, play, pen", "Silent P in a few words (pneumonia, psalm)."),
    "qu": ("/kw/", "quit, queen, quick", "Q always comes with U. U is silent in 'qu'."),
    "r": ("/r/", "red, run, rose", "R never goes silent in English."),
    "s": ("/s/ /z/", "sun, his, has", "S says /z/ between vowels (his, has, easy)."),
    "t": ("/t/", "top, tree, time", "Silent T in a few words (castle, listen, whistle)."),
    "u": ("/ŭ/ /ū/ /ü/", "up, use, put", "Three sounds. Long /ū/ in open syllables (music, unit)."),
    "v": ("/v/", "van, very, voice", "V never goes silent. Common: 5 vs V."),
    "w": ("/w/", "wet, win, water", "Silent W in a few words (wrong, write, two)."),
    "x": ("/ks/ /gz/", "box, exact", "X says /ks/ at end, /gz/ inside word (exact)."),
    "y": ("/y/ /ē/ /ī/", "yes, baby, by", "Three roles: consonant at start, vowel in middle/end (Rule 6, 7)."),
    "z": ("/z/", "zip, zoo, zero", "Z never goes silent."),
    # Stage 2 multi-letter
    "sh": ("/sh/", "ship, fish, shut", "Don't confuse sh with ch. sh = quiet, ch = louder."),
    "th": ("/th/ (voiced) /th/ (unvoiced)", "this, thin", "Two sounds. Voiced: this, that. Unvoiced: thin, bath."),
    "ck": ("/k/", "back, sick, duck", "Only after a short vowel (Rule 26). Long vowel uses 'k' (make, take)."),
    "ee": ("/ē/", "see, tree, feet", "EE always says /ē/. No exceptions."),
    "ng": ("/ng/", "ring, sing, long", "NG never says /n/ alone in English. No 'n' before 'g' without /ng/."),
    "ar": ("/är/", "car, far, star", "AR is controlled R + /ä/."),
    "or": ("/ôr/", "for, born, corn", "OR is controlled R + /ô/."),
    "er": ("/er/", "her, fern, bird", "ER is controlled R + /er/. Also unstressed: water, better (Rule 31)."),
    "oi": ("/oi/", "boil, coin, soil", "OI never at end of base word. Use OY (Rule 3)."),
    "oy": ("/oi/", "boy, toy, soy", "OY comes only at end of base word (Rule 3)."),
    "ai": ("/ā/", "rain, sail, train", "AI never at end. Use AY (Rule 3)."),
    "ay": ("/ā/", "day, play, stay", "AY only at end of base word (Rule 3)."),
    "ch": ("/ch/", "chip, beach, church", "CH says /ch/ after most consonants. CH after S = /sh/ (Rule 17)."),
    "wh": ("/hw/ /h/", "when, who", "WH often says /hw/ (which, what). WH before O = /h/ (who, whole)."),
    "ea": ("/ē/ /ĕ/", "eat, bread", "Two main sounds. EE-rule words say /ē/. Others vary."),
    "ow": ("/ō/ /ou/", "snow, cow", "Two sounds. /ō/ in 'snow, know', /ou/ in 'cow, now'."),
    "ou": ("/ou/ /ü/", "house, soup", "Multiple sounds. Most common /ou/ (house). /ü/ in soup, route, group."),
    "oo": ("/ü/ /ö/", "book, moon", "Two sounds. Short /ü/ (book, look). Long /ö/ (moon, food)."),
    "ed": ("/ĕd/ /d/ /t/", "jumped, played, walked", "Three sounds of -ED (Rule 20). Always spelling -ED."),
    "igh": ("/ī/", "high, light, night", "IGH says /ī/. GH is silent (Rule 28)."),
    "aw": ("/ô/", "saw, claw, yawn", "AW says /ô/. Common in 'aw' words."),
    "au": ("/ô/", "haul, sauce, author", "AU says /ô/. Common in 'au' words."),
    "ir": ("/er/", "bird, girl, first", "IR is controlled R + /er/."),
    "ur": ("/er/", "turn, burn, curl", "UR is controlled R + /er/."),
    "oa": ("/ō/", "boat, coat, road", "OA says /ō/. Comes before consonants."),
    "ear": ("/ēr/ /er/", "hear, earth", "Multiple sounds. /ēr/ (hear). /er/ (earth, learn)."),
    # Stage 3 advanced
    "dge": ("/j/", "bridge, badge, edge", "DGE only after short vowel (Rule 25). Long vowel uses 'j' (age, stage)."),
    "tch": ("/ch/", "catch, patch, witch", "TCH only after short vowel (Rule 27). Long vowel uses 'ch' (beach, teach)."),
    "kn": ("/n/", "knee, knife, knock", "K is silent in KN. N keeps the /n/ sound."),
    "gn": ("/n/", "gnome, sign, design", "G is silent in GN at start. Sometimes at end too (sign, design)."),
    "wr": ("/r/", "write, wrong, wrap", "W is silent in WR. R keeps the /r/ sound."),
    "eigh": ("/ā/", "eight, weigh, sleigh", "EIGH says /ā/. GH silent (Rule 28)."),
    "ei": ("/ē/ /ā/ /ī/", "ceiling, vein, height", "Three sounds. Most common /ē/ (ceiling). /ā/ in 'vein'. /ī/ in 'height'."),
    "ey": ("/ā/ /ē/", "they, key, money", "Two sounds. /ā/ at end of base word (they, survey). /ē/ inside (key, money)."),
    "ph": ("/f/", "phone, elephant, graph", "PH always says /f/."),
    "gh": ("/g/ (sometimes silent)", "ghost, ghost, ghost", "GH says /g/ at start (ghost). Often silent (high, light)."),
    "ough": ("/ō/ /ö/ /ow/ /ŭf/ /äf/ /ü/", "though, dough, bough, tough, laugh, through", "Six sounds! Toughest PG in English. Memorize per-word."),
    "augh": ("/ä/ /äf/", "laugh, draught", "Two sounds. /ä/ (daughter). /äf/ (laugh)."),
    "ew": ("/ü/ /ö/", "few, dew, new, threw", "Two sounds. /ü/ (few). /ö/ (new, threw)."),
    "ui": ("/ü/ /ö/", "suit, fruit, ruin", "Two sounds. /ü/ (suit). /ö/ (fruit, ruin)."),
    "eu": ("/ü/ /ö/", "feud, maneuver", "Two sounds. Less common PG."),
    "wor": ("/wer/", "work, word, world", "WOR says /wer/. Schwa + R (Rule 31.3)."),
    "ie": ("/ē/ /ī/", "piece, field, chief, lie", "Two sounds. /ē/ most common (piece, field). /ī/ in 'lie, tie'."),
    # Stage 4 Latin /sh/
    "ti": ("/sh/", "motion, nation, station", "TI says /sh/ inside words (Rule 17). Exception after S: question."),
    "ci": ("/sh/", "special, social, ancient", "CI says /sh/ inside words (Rule 17)."),
    "si": ("/sh/ /s/ /z/", "vision, mission, session", "SI says /sh/ at end of word after a vowel: vision, mission. Says /s/ or /z/ after consonant: session, prism."),
}


def build_at_a_glance(row: dict) -> str:
    """Build a 1-page at-a-glance reference card for the lesson.

    Shows the phonogram/rule at a glance with sounds, key words, and the
    most common mistake. Falls back to lesson title if no specific data.
    """
    stage = row["stage"]
    lnum = int(row["lesson_num"])
    title = row["title"]
    new_pg = (row.get("new_phonogram") or "").strip()
    new_rule = (row.get("new_rule") or "").strip()
    ltype = row["type"]

    # Pick what to show at the top
    if new_pg and new_pg in AT_A_GLANCE_PG:
        sounds, words, mistake = AT_A_GLANCE_PG[new_pg]
        pg_label = new_pg
        header_label = f"Phonogram {new_pg}"
        top_block = f"# {new_pg}"
        sounds_line = f"**Sounds:** {sounds}"
        words_line = words
        mistake_line = mistake
    elif new_pg:
        # PG not in our at-a-glance table — fall back to title
        pg_label = title.split()[-1]
        header_label = title
        top_block = f"# {title}"
        sounds_line = "**Sounds:** see lesson"
        words_line = "(see lesson for examples)"
        mistake_line = ""
    elif new_rule:
        # Rule lesson — refer to handbook for full details
        header_label = f"Rule {new_rule}"
        top_block = f"# Rule {new_rule}"
        sounds_line = f"**Rule:** see handbook for full text"
        words_line = "examples in lesson"
        mistake_line = "See handbook Rule " + str(new_rule)
    elif ltype == "reader":
        header_label = "Decodable Reader"
        top_block = f"# {title}"
        sounds_line = "**Focus:** see lesson for phonograms practiced"
        words_line = ""
        mistake_line = ""
    else:
        # Other lesson types (review, PA, handwriting, etc.)
        header_label = title
        top_block = f"# {title}"
        sounds_line = ""
        words_line = ""
        mistake_line = ""

    mistake_block = (
        f"\n\n**Common mistake:** {mistake_line}\n" if mistake_line else ""
    )

    return (
        f"<style>.at-a-glance {{ border: 3px solid #2a5c8a; padding: 18px; "
        f"border-radius: 8px; page-break-inside: avoid; }}\n"
        f".at-a-glance h1 {{ font-size: 48pt; text-align: center; margin: 0.1em 0; "
        f"color: #2a5c8a; }}\n"
        f".at-a-glance .label {{ font-size: 10pt; text-align: center; "
        f"text-transform: uppercase; letter-spacing: 0.1em; color: #666; "
        f"margin-bottom: 1em; }}\n"
        f".at-a-glance .stage {{ font-size: 9pt; text-align: center; "
        f"color: #888; margin-top: 0.5em; }}\n"
        f".at-a-glance .tear {{ border-top: 2px dashed #999; margin-top: 18px; "
        f"padding-top: 8px; text-align: center; font-size: 9pt; color: #888; }}</style>\n\n"
        f"<div class=\"at-a-glance\">\n\n"
        f"<div class=\"label\">At a Glance — {header_label}</div>\n\n"
        f"{top_block}\n\n"
        f"<div style=\"text-align:center; font-size: 13pt;\">{sounds_line}</div>\n\n"
        + (
            f"**Key words:** {words_line}\n" if words_line else ""
        )
        + mistake_block
        + f"\n<div class=\"stage\">Stage {stage} · Lesson {lnum}</div>\n"
        f"<div class=\"tear\">\u2702 Cut along dashed line for take-home reference card</div>\n"
        f"</div>\n"
    )


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _pack_worker(lesson_id: str, no_render: bool) -> dict:
    """Worker entry point for ProcessPoolExecutor.

    Loads the catalog in the worker process (cheap — single CSV read),
    builds one pack, returns a status dict (JSON-safe).
    """
    worker_log = get_logger("pack.worker")
    attach_worker_handler(worker_log)
    catalog = load_catalog()
    row = next((r for r in catalog if r["lesson_id"] == lesson_id), None)
    if row is None:
        return {"lesson_id": lesson_id, "status": "MISSING", "missing": ["catalog row"]}
    try:
        out, missing, md_path = build_one_pack(row, catalog, no_render=no_render)
    except Exception as exc:
        worker_log.error(f"FAIL {lesson_id}: {exc}", exc_info=True)
        return {"lesson_id": lesson_id, "status": "FAIL", "error": str(exc)}
    target = out if out else md_path
    target_str = str(target.relative_to(ROOT)) if target else None
    return {
        "lesson_id": lesson_id,
        "status": "OK" if not missing else "WARN",
        "target": target_str,
        "missing": missing,
    }


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
    parts.append(PAGE_BREAK)
    parts.append(build_at_a_glance(row))
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

    slug = lesson_id  # use lesson_id so file matches catalog row key
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
        # render's logger is wired to the build logger; in worker processes
        # the log line is captured by WorkerLogHandler and drained by main.
        render_md_to_pdf(temp_md, out_pdf, doc_type="lesson")
    except ModuleNotFoundError as e:
        missing.append(f"render unavailable: {e}")
        return None, missing, debug_md
    finally:
        if temp_md.exists():
            temp_md.unlink()

    return out_pdf, missing, debug_md


def _run_stage_parallel(rows: list[dict], no_render: bool, jobs: int, label: str) -> tuple[int, int]:
    """Build N packs in parallel. Returns (ok_count, warn_count)."""
    if not rows:
        return 0, 0
    n_workers = max(1, jobs)
    queue = WorkerLogQueue()
    set_worker_queue(queue)
    log.info(f"{label}: {len(rows)} packs, {n_workers} workers")
    ok = warn = 0
    with Progress(label, total=len(rows)) as progress:
        executor = ProcessPoolExecutor(max_workers=n_workers)
        try:
            futures = {
                executor.submit(_pack_worker, row["lesson_id"], no_render): row
                for row in rows
            }
            for fut in as_completed(futures):
                drain_worker_queue(queue, log)
                result = fut.result()
                status = result.get("status", "FAIL")
                if status == "OK":
                    ok += 1
                    log.info(f"  OK {result.get('target')}")
                elif status == "WARN":
                    warn += 1
                    log.warning(f"  WARN {result.get('target')}: missing {', '.join(result.get('missing', []))}")
                elif status == "MISSING":
                    log.warning(f"  SKIP {result['lesson_id']}: missing {result.get('missing', ['?'])[0]}")
                else:
                    log.error(f"  FAIL {result['lesson_id']}: {result.get('error')}")
                progress.tick()
                drain_worker_queue(queue, log)
        finally:
            executor.shutdown(wait=True)
            set_worker_queue(None)
    log.info(f"{label}: {ok} ok, {warn} with warnings")
    return ok, warn


def cmd_lesson(lesson_id: str, catalog: list[dict], no_render: bool = False):
    row = next((r for r in catalog if r["lesson_id"] == lesson_id), None)
    if not row:
        log.error(f"lesson_id not found in catalog: {lesson_id}")
        sys.exit(1)
    out, missing, md_path = build_one_pack(row, catalog, no_render=no_render)
    if out is None and md_path is None:
        log.warning(f"SKIP {lesson_id}: missing lesson MD")
        return
    target = out if out else md_path
    if missing:
        log.warning(f"WARN {target.relative_to(ROOT)}: missing {', '.join(missing)}")
    else:
        log.info(f"OK {target.relative_to(ROOT)}")


def cmd_stage(stage: int, bundle: bool, catalog: list[dict], no_render: bool = False, jobs: int = 1):
    phase(f"Pack Stage {stage}")
    rows = [r for r in catalog if int(r["stage"]) == stage]
    log.info(f"Building Stage {stage} packs: {len(rows)} lessons")
    ok, warn = _run_stage_parallel(rows, no_render, jobs, f"pack-stage-{stage}")
    if bundle:
        log.warning("(bundle mode not yet implemented — render per-lesson packs only)")


def cmd_all(catalog: list[dict], no_render: bool = False, jobs: int = 1):
    phase("Pack All Lessons")
    rows = list(catalog)
    log.info(f"Building all {len(rows)} packs")
    _run_stage_parallel(rows, no_render, jobs, "pack-all")


def main():
    parser = argparse.ArgumentParser(description="Build cohesive lesson packs")
    parser.add_argument("--lesson", help="Build pack for one lesson_id (e.g. pg-d)")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], help="Build all packs for a stage")
    parser.add_argument("--all", action="store_true", help="Build all 248 packs")
    parser.add_argument("--bundle", action="store_true", help="(Future) merge all stage packs into one PDF")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering (test pack assembly only)")
    parser.add_argument(
        "--jobs", "-j", type=int, default=1,
        help="Parallel worker processes (default: 1 = serial). Stage/all only.",
    )
    args = parser.parse_args()

    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = load_catalog()

    if args.lesson:
        cmd_lesson(args.lesson, catalog, no_render=args.no_render)
    elif args.stage:
        cmd_stage(args.stage, args.bundle, catalog, no_render=args.no_render, jobs=args.jobs)
    elif args.all:
        cmd_all(catalog, no_render=args.no_render, jobs=args.jobs)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
