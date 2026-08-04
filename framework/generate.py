#!/usr/bin/env python3
"""
generate.py — Generate lesson markdown stubs from lesson-catalog.csv.

Usage:
    python generate.py --stage 1          # Generate all Stage 1 lessons
    python generate.py --stage 2          # Generate all Stage 2 lessons
    python generate.py --all              # Generate all lessons (all stages)
    python generate.py --lesson stage-2/042-sh-phonogram  # Single lesson
"""

import argparse
import csv
import sys
from pathlib import Path

# Force UTF-8 on Windows consoles that default to cp1252
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "lessons"
WORKSHEETS_DIR = PROJECT_ROOT / "worksheets"
READERS_DIR = PROJECT_ROOT / "readers"
FRAMEWORK_DIR = PROJECT_ROOT / "framework"
TEMPLATES_DIR = FRAMEWORK_DIR / "templates"
CATALOG_PATH = FRAMEWORK_DIR / "lesson-catalog.csv"

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

LESSON_HEADER = """# Lesson {lesson_num}: {title}

**Stage {stage}** · Lesson {lesson_num} · Type: {lesson_type}

---

## Warm-Up: Phonogram Flash Review

> Flash previously taught phonogram cards. Child says ALL sounds within 2 seconds.

| Phonograms to review |
|----------------------|
| {review_phonograms} |

---

## New Learning: {title}

"""

PHONOGRAM_INTRO = """### The Phonogram **{phonogram}**

<div class="phonogram">{phonogram}</div>

**{phonogram}** says: {sounds}

| Sound | Example Word |
|-------|-------------|
{sound_table}

> Write **{phonogram}** three times on your whiteboard while saying its sounds.

"""

RULE_INTRO = """### Spelling Rule {rule_num}

<span class="rule-badge">Rule {rule_num}</span> **{rule_text}**

| Example Words |
|---------------|
{example_table}

"""

SPELLING_ANALYSIS = """## Spelling Analysis

Follow the 5-step routine for each word: Hear & Say → Segment → Write → Analyze → Read.

| Word | Phonograms | Rules | Say-to-Spell |
|------|-----------|-------|--------------|
{word_rows}

"""

READER_PAGE = """## Reader: {title}

<div class="warmup-box">
<div class="title">Warm-Up Words — read these first</div>

{warmup_words}

</div>

<div class="reader-page">

<div class="reader-text">

{story_text}

</div>

<div class="reader-sidebar">

### Spelling Aid

**New phonogram:** {new_phonogram}

**Sounds:** {sounds}

**Rule:** {rule_reference}

![{image_alt}]({image_path})

</div>

</div>

<div class="page-break"></div>

## After Reading

- What happened in the story? Retell it in your own words.
- Find all the words with **{new_phonogram}**. Read them again.
- Write one sentence using the new phonogram.

"""

PRACTICE_SECTION = """## Practice

### Write It
Write each word twice:

{word_list}

### Read It
Read these words sound by sound, then blend:

{read_list}

### Quiz
1. What sounds does **{phonogram}** say?
2. Which rule applies to these words?
3. Spell this word from dictation: _______________

"""

REVIEW_SECTION = """## Review

### Quick Check

{review_items}

### Words to Spell (Dictation)

{spell_list}

---

**Next lesson:** {next_lesson}

"""

FOOTER = """

---

<div class="page-break"></div>

## Lesson Complete!

✅ Phonogram review  
✅ New learning  
✅ Spelling Analysis  
✅ Reading practice  

**Practice at home:** Flash the phonogram cards for today's new phonogram and any that were slow during warm-up.

"""

# ---------------------------------------------------------------------------
# Lesson type generators
# ---------------------------------------------------------------------------

def generate_phonogram_intro(lesson: dict) -> str:
    phonogram = lesson["new_phonogram"]
    # Sound data from curriculum reference
    sounds_map = {
        "a": "/ă/ /ā/ /ä/", "d": "/d/", "g": "/g/ /j/", "c": "/k/ /s/",
        "o": "/ŏ/ /ō/ /ö/", "qu": "/kw/", "s": "/s/ /z/", "t": "/t/",
        "i": "/ĭ/ /ī/ /ē/", "p": "/p/", "u": "/ŭ/ /ū/ /ö/", "j": "/j/",
        "r": "/r/", "n": "/n/", "m": "/m/", "e": "/ĕ/ /ē/", "l": "/l/",
        "b": "/b/", "h": "/h/", "k": "/k/", "f": "/f/", "v": "/v/",
        "w": "/w/", "x": "/ks/ /z/", "y": "/y/ /ĭ/ /ī/ /ē/", "z": "/z/",
        "sh": "/sh/", "th": "/th/ /th/", "ck": "/k/", "ee": "/ē/",
        "ng": "/ng/", "ar": "/är/", "or": "/or/", "er": "/er/",
        "oi": "/oi/", "oy": "/oi/", "ai": "/ā/", "ay": "/ā/",
        "ch": "/ch/ /k/ /sh/", "wh": "/hw/", "ea": "/ē/ /ĕ/ /ā/",
        "ow": "/ow/ /ō/", "ou": "/ow/ /ō/ /ö/ /ŭ/", "oo": "/ö/ /ü/ /ō/",
        "ed": "/ed/ /d/ /t/", "igh": "/ī/", "aw": "/ä/", "au": "/ä/",
        "ir": "/er/", "ur": "/er/", "oa": "/ō/", "ear": "/er/",
        "dge": "/j/", "tch": "/ch/", "kn": "/n/", "gn": "/n/", "wr": "/r/",
        "eigh": "/ā/", "ei": "/ē/ /ā/ /ī/", "ey": "/ā/ /ē/",
        "ph": "/f/", "gh": "/g/", "ough": "/ō/ /ö/ /ow/ /ŭ/ /ä/ /ü/",
        "augh": "/ä/ /ă/", "ew": "/ü/ /ö/", "ui": "/ü/ /ö/", "eu": "/ü/ /ö/",
        "wor": "/wer/", "ie": "/ē/ /ī/", "ti": "/sh/", "ci": "/sh/",
        "si": "/sh/ /zh/", "bu": "/b/", "gu": "/g/",
    }
    sounds = sounds_map.get(phonogram, "/?/")
    words = lesson.get("word_list", "").split() if lesson.get("word_list") else ["—"]
    sound_table = "\n".join(f"| {s} | — |" for s in sounds.split())
    return PHONOGRAM_INTRO.format(
        phonogram=phonogram,
        sounds=sounds,
        sound_table=sound_table,
    )


def generate_rule_intro(lesson: dict) -> str:
    rule_num = lesson.get("new_rule", "")
    # Simple rule text lookup
    return RULE_INTRO.format(
        rule_num=rule_num,
        rule_text=f"Rule {rule_num}",
        example_table="| — |",
    )


def generate_spelling_analysis(lesson: dict) -> str:
    words = lesson.get("word_list", "").split() if lesson.get("word_list") else ["—"]
    word_rows = "\n".join(f"| {w} | | | |" for w in words)
    return SPELLING_ANALYSIS.format(word_rows=word_rows)


def generate_reader(lesson: dict) -> str:
    reader_path = lesson.get("reader", "")
    return READER_PAGE.format(
        title=lesson["title"],
        warmup_words="—",
        story_text="— [Story text to be written]",
        new_phonogram=lesson.get("new_phonogram", "—"),
        sounds="—",
        rule_reference=lesson.get("new_rule", "—"),
        image_alt="Illustration",
        image_path=lesson.get("image_needed", "images/illustrations/placeholder.png"),
    )


def generate_lesson(lesson: dict, dry_run: bool = False) -> str:
    """Generate markdown text for a single lesson entry."""
    stage = lesson["stage"]
    lesson_type = lesson["type"]
    review_phonograms = "Review all previously taught phonograms"

    text = LESSON_HEADER.format(
        lesson_num=lesson["lesson_num"],
        title=lesson["title"],
        stage=stage,
        lesson_type=lesson_type,
        review_phonograms=review_phonograms,
    )

    if lesson_type == "phonogram-intro":
        text += generate_phonogram_intro(lesson)
    elif lesson_type == "rule-intro":
        text += generate_rule_intro(lesson)
    elif lesson_type == "spelling-analysis":
        text += generate_spelling_analysis(lesson)
    elif lesson_type == "reader":
        text += generate_reader(lesson)
    elif lesson_type == "phonemic-awareness":
        text += f"### Activity: {lesson['title']}\n\n— [Phonemic awareness activity to be written]\n"
    elif lesson_type in ("review", "assessment"):
        text += f"### {lesson['title']}\n\n— [Review/assessment content to be written]\n"
    elif lesson_type == "morphology":
        text += f"### Morpheme: {lesson.get('new_phonogram', lesson['title'])}\n\n— [Morpheme content to be written]\n"
    else:
        text += f"— [{lesson_type} content to be written]\n"

    # Add image reference if lesson has one in the catalog
    image_needed = lesson.get("image_needed", "").strip()
    if image_needed:
        img_path = f"images/{image_needed}" if not image_needed.startswith("images/") else image_needed
        text += f"\n\n![{lesson.get('title', 'Illustration')}]({img_path})\n"

    # Add practice section for phonogram and rule intros
    if lesson_type in ("phonogram-intro", "rule-intro"):
        words = lesson.get("word_list", "—")
        text += PRACTICE_SECTION.format(
            word_list=words,
            read_list=words,
            phonogram=lesson.get("new_phonogram", ""),
        )

    # Add review
    next_num = int(lesson["lesson_num"]) + 1
    text += REVIEW_SECTION.format(
        review_items="- Check phonogram recall\n- Review new rule if introduced",
        spell_list=lesson.get("word_list", "—"),
        next_lesson=f"Lesson {next_num}",
    )

    text += FOOTER

    return text


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def load_catalog() -> list[dict]:
    with open(CATALOG_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cmd_generate_stage(stage: int):
    lessons = [l for l in load_catalog() if int(l["stage"]) == stage]
    stage_dir = LESSONS_DIR / f"stage-{stage}"
    stage_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating Stage {stage}: {len(lessons)} lessons")
    for lesson in lessons:
        lesson_id = lesson["lesson_id"]
        md_path = stage_dir / f"{lesson_id}.md"
        if md_path.exists():
            print(f"  ⏭ Skipping (exists): {lesson_id}.md")
            continue
        text = generate_lesson(lesson)
        md_path.write_text(text, encoding="utf-8")
        print(f"  ✓ {lesson_id}.md")


def cmd_generate_all():
    for stage in range(1, 6):
        cmd_generate_stage(stage)


def cmd_generate_single(lesson_ref: str):
    """Generate a single lesson by reference like 'stage-2/042-sh-phonogram'"""
    parts = lesson_ref.split("/")
    if len(parts) != 2:
        print(f"Error: use format 'stage-X/lesson_id', e.g. 'stage-2/042-sh-phonogram'")
        sys.exit(1)
    stage_str, lesson_id = parts
    stage = int(stage_str.replace("stage-", ""))
    stage_dir = LESSONS_DIR / f"stage-{stage}"
    stage_dir.mkdir(parents=True, exist_ok=True)

    for lesson in load_catalog():
        if int(lesson["stage"]) == stage and lesson["lesson_id"] == lesson_id:
            md_path = stage_dir / f"{lesson_id}.md"
            text = generate_lesson(lesson)
            md_path.write_text(text, encoding="utf-8")
            print(f"  ✓ {lesson_id}.md")
            return
    print(f"Error: lesson '{lesson_id}' not found in stage {stage}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate Logic of English lesson stubs")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], help="Generate all lessons in a stage")
    parser.add_argument("--all", action="store_true", help="Generate all lessons (all stages)")
    parser.add_argument("--lesson", type=str, help="Generate a single lesson (e.g. stage-2/042-sh-phonogram)")
    args = parser.parse_args()

    if args.stage:
        cmd_generate_stage(args.stage)
    elif args.all:
        cmd_generate_all()
    elif args.lesson:
        cmd_generate_single(args.lesson)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
