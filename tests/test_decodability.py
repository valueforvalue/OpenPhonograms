"""Tests for decodability of every reader in the curriculum.

A reader is decodable when every word in its content can be read
using only phonograms taught at or before the reader's declared
(after_lesson) point in its stage. This test prevents regressions
where new readers slip in with non-decodable vocabulary (e.g. advanced
multi-letter phonograms before they're taught, or contractions that
introduce sounds outside the schema).
"""
import csv
import re
from pathlib import Path

import pytest


SINGLE = set("abcdefghijklmnopqrstuvwxyz")


def _get_pgs_up_to(stage_target: int, lesson_target: int) -> set[str]:
    """All phonograms introduced at or before stage_target/lesson_target."""
    pgs = set()
    with open("framework/lesson-catalog.csv", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            st = int(row["stage"]); ln = int(row["lesson_num"])
            pg = row.get("new_phonogram", "").strip().strip('"')
            if not pg:
                continue
            if st < stage_target or (st == stage_target and ln <= lesson_target):
                pgs.add(pg)
    return pgs


def _find_undecodable(text: str, allowed_pgs: set[str]) -> list[tuple[str, str]]:
    """Return (word, leftover) for words that fail with allowed_pgs."""
    allowed = SINGLE | {p.lower() for p in allowed_pgs}
    bad = []
    clean = re.sub(r'[#*_`>|]', ' ', text)
    clean = re.sub(r'\([^\)]*\)', ' ', clean)
    for word in re.findall(r"[a-zA-Z']+", clean):
        w = word.lower().rstrip("'s").rstrip("'")
        if len(w) <= 1:
            continue
        pgs_sorted = sorted(allowed, key=lambda x: -len(x))
        rx = re.compile('(' + '|'.join(re.escape(p) for p in pgs_sorted) + ')', re.IGNORECASE)
        pos = 0; leftover = ""
        while pos < len(w):
            m = rx.match(w, pos)
            if m: pos = m.end()
            else: leftover += w[pos]; pos += 1
        if leftover:
            bad.append((word, leftover))
    return bad


def _all_readers() -> list[Path]:
    """All reader MD files in readers/ (flat or stage-N/)."""
    readers = Path("readers")
    return sorted(p for p in readers.rglob("*.md"))


def _parse_reader_header(path: Path) -> tuple[int, int] | None:
    """Return (stage, after_lesson) from the reader's MD header, or None if absent."""
    content = path.read_text(encoding="utf-8")
    # Accept both formats:
    #   "**Stage 2** · Decodable Reader · After Lesson 14"
    #   "**Stage 2** · Reader 1 · New phonogram: **sh**"
    m = re.search(r'\*\*Stage (\d+)\*\*[^\d]*After Lesson (\d+)', content)
    if m:
        return int(m.group(1)), int(m.group(2))
    # No 'After Lesson' header — skip audit (e.g. 001-fred-the-frog uses old format)
    return None


def test_every_reader_with_header_is_decodable():
    """Every reader with a parseable header must be decodable at its declared stage/lesson.

    Only checks generated decodable readers (have 'Decodable Reader' in the header).
    Lesson readers and legacy files use different formats and are skipped.
    """
    failures = []
    for path in _all_readers():
        header = _parse_reader_header(path)
        if header is None:
            continue
        content = path.read_text(encoding="utf-8")
        # Only audit readers using the standard "Decodable Reader" template
        if "Decodable Reader" not in content:
            continue
        stage, after = header
        allowed = _get_pgs_up_to(stage, after)
        bad = _find_undecodable(content, allowed)
        if bad:
            unique = sorted(set(w for w, _ in bad))
            failures.append((path, unique))
    assert not failures, (
        f"Decodability violations in {len(failures)} readers:\n"
        + "\n".join(f"  {p}: {w}" for p, w in failures)
    )


def test_all_readers_have_minimum_word_count():
    """Every reader should have at least 80 words in its story section (issue #16 quality bar)."""
    too_short = []
    for path in _all_readers():
        content = path.read_text(encoding="utf-8")
        m = re.search(r'## Story\s*(.+?)\s*##', content, re.DOTALL)
        if not m:
            continue
        story = re.sub(r'\*\*([^*]+)\*\*', r'\1', m.group(1))
        wc = len(re.findall(r"[a-zA-Z']+", story))
        if wc < 80:
            too_short.append((path, wc))
    assert not too_short, (
        f"Readers below 80 words:\n"
        + "\n".join(f"  {p}: {wc}w" for p, wc in too_short)
    )


def test_readers_have_required_sections():
    """Every reader with a parseable header must include Warm-Up, Story, and Think About It.

    Older readers (e.g. 001-fred-the-frog.md, lesson readers) use legacy formats
    with page-based or lesson-based structure. Only check new-style readers.
    """
    bad = []
    for path in _all_readers():
        content = path.read_text(encoding="utf-8")
        # Skip legacy readers that don't use the Decodable Reader template
        if "Decodable Reader" not in content:
            continue
        required = ["## Warm-Up", "## Story", "## Think About It"]
        missing = [s for s in required if s not in content]
        if missing:
            bad.append((path, missing))
    assert not bad, (
        f"Readers missing sections:\n"
        + "\n".join(f"  {p}: missing {m}" for p, m in bad)
    )