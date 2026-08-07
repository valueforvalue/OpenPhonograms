"""Reusable mid-stage + final-stage assessment builder.

Used by all stage generators. Each assessment covers a defined set of phonograms
and rules, with reading + spelling + dictation subsections.

Usage in a stage generator:
    from framework.assessment import build_assessment, ASSESSMENT_TEMPLATE

    yield 9, build_assessment(
        n=9, title="Mid-Stage 2 Checkpoint",
        pgs=["a","b","c",...,"sh","th","ck"],
        rule_checklist="| Rule 26 | When do we use CK? | ☐ |\\n...",
        reading_words=["cat","ship","back","see","stop","hand"],
        spelling_words=["cat","ship","back","see","stop","that","sing","car"],
        next_steps="If >=85%: Continue. If weaker, review for 1-2 weeks and retest.",
    )
"""
from __future__ import annotations

from typing import Iterable

# Import phonograms to get sound notation per PG
try:
    from framework.phonograms import SINGLE, MULTI, MULTI3, MULTI4
except ImportError:
    # When imported from scripts/ that may not have framework/ on path
    from phonograms import SINGLE, MULTI, MULTI3, MULTI4  # type: ignore


def _get_sound(pg: str) -> str:
    """Return the canonical sound notation for a phonogram."""
    if pg in SINGLE:
        return SINGLE[pg]["sounds"]
    if pg in MULTI:
        return MULTI[pg]["sounds"]
    if pg in MULTI3:
        return MULTI3[pg]["sounds"]
    if pg in MULTI4:
        return MULTI4[pg]["sounds"]
    return "—"


def _pg_checklist(pgs: Iterable[str]) -> str:
    """Build the phonogram-recall checklist table rows."""
    rows = []
    for p in pgs:
        s = _get_sound(p)
        rows.append(f"| {p} | {s} | ☐ |")
    return "\n".join(rows)


def _word_checklist(words: Iterable[str]) -> str:
    """Build a simple word checklist."""
    return "\n".join(f"| {w} | ☐ |" for w in words)


# Generic assessment body. Each stage passes a config and the template fills it.
ASSESSMENT_TEMPLATE = """# Lesson {n}: {title}

**Stage {stage}** · Lesson {n} · assessment

---

## Overview

{overview}

---

## Phonogram Recall

> Adult: Show each phonogram card. Child says ALL sounds within 2 seconds. Check any that need extra review.

| Phonogram | Sound | Got It? |
|-----------|-------|---------|
{pg_checklist}

**Phonograms reviewed: {pg_total}**

---

## Reading Practice

> Child reads each word aloud. Mark sounds that are hesitant or wrong.

| Word | Got It? |
|------|---------|
{reading_checklist}

**Reading: {reading_total} words**

---

## Spelling

> Adult dictates each word. Child writes, then spells aloud.

| Word | Got It? |
|------|---------|
{spelling_checklist}

**Spelling: {spelling_total} words**

---

## Rules Check

> Adult asks each question. Child answers.

{rule_checklist}

**Rules: {rule_total} questions**

---

## Total Score

> ____ / {overall_total}

| Section | Score |
|---------|-------|
| Phonograms | ___ / {pg_total} |
| Reading | ___ / {reading_total} |
| Spelling | ___ / {spelling_total} |
| Rules | ___ / {rule_total} |

---

## Next Steps

{next_steps}

{teacher_script}
"""


def build_assessment(
    *,
    n: int,
    stage: int,
    title: str,
    pgs: list[str],
    reading_words: list[str],
    spelling_words: list[str],
    rule_checklist: str = "*(No new rules yet.)*",
    overview: str = "This checkpoint verifies the child is on track. Review any weak sections before moving on.",
    next_steps: str = "If \u226585%: Continue. If weaker, review trouble spots for 1 week and retest.",
    teacher_script: str = "",
) -> str:
    """Render a full assessment lesson body.

    Args:
        n: Lesson number within the stage.
        stage: Stage number (1-5).
        title: Display title, e.g. "Mid-Stage 2 Checkpoint".
        pgs: List of phonograms covered by this assessment.
        reading_words: Decodable words for the reading section.
        spelling_words: Decodable words for the dictation section.
        rule_checklist: Markdown table rows for the rules section. Pass an empty
            string or a single placeholder line if no rules yet.
        overview: One-sentence framing for what the assessment covers.
        next_steps: What to do based on the score.
        teacher_script: Optional teacher-script prose injected at the end.
    """
    pg_checklist = _pg_checklist(pgs)
    reading_checklist = _word_checklist(reading_words)
    spelling_checklist = _word_checklist(spelling_words)
    rule_total = rule_checklist.count("| \u2610 |") if "|\u2610" in rule_checklist else 1
    if not rule_checklist.strip() or rule_checklist.startswith("*("):
        rule_total = 0

    return ASSESSMENT_TEMPLATE.format(
        n=n, stage=stage, title=title,
        overview=overview,
        pg_checklist=pg_checklist, pg_total=len(pgs),
        reading_checklist=reading_checklist, reading_total=len(reading_words),
        spelling_checklist=spelling_checklist, spelling_total=len(spelling_words),
        rule_checklist=rule_checklist, rule_total=rule_total,
        overall_total=len(pgs) + len(reading_words) + len(spelling_words) + rule_total,
        next_steps=next_steps,
        teacher_script=teacher_script,
    )
