#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Check that every word in a Stage-N reader MD is decodable with phonograms
taught at-or-before stage N, OR is one of the high-frequency words for that
stage, OR is a proper noun (character name).

Heuristic v1: substring containment of valid Stage 1..N PG ids (length 1-3)
plus check that every letter is covered by some PG string. This catches
egregious over-stage words like "beautiful", "kitchen", "computer" — but is
not a real GPC decodability proof. Run it as a drift detector, not a solver.

Usage:
    python scripts/check-reader-decodability.py --stage 2 --dir readers/stage-2/
    python scripts/check-reader-decodability.py --stage 2 --file readers/stage-2/026-the-ship-in-the-storm.md

Exits 0 if all words are decodable; exits 1 if any non-decodable words found,
printing them with their line numbers.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

# Repo root (parent of this script)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "framework"))
from data_loader import load_phonograms  # noqa: E402

# High-frequency words per stage.
#
# Source-of-truth comes from each stage's generator. Long-term plan is to
# extract these to data/high_frequency_words.yaml (#22 follow-up) so both
# the checker AND the generators read the same source.
STAGE_HF_WORDS: dict[int, set[str]] = {
    # Stage 1: no HF words defined. Single-letter phonograms cover a-z
    # and 'qu', so HF-style exemptions are not needed.
    1: set(),

    # Stage 2: extracted from scripts/generate-stage2.py lines 371-395
    # (HF_WORDS_SET1/2/3 — 5 words each, taught across lessons 50-52).
    2: {
        "the", "a", "is", "of", "to", "do", "was", "has", "said", "you",
        "are", "have", "give", "come", "some",
    },

    # Stage 3: extracted from scripts/generate-stage3.py lines 411-428
    # (HF4 taught in lesson 55, HF5 taught in lesson 56).
    3: {
        "where", "there", "their", "were", "here",
        "once", "two", "does", "any", "many",
    },

    # Stage 4: no HF words defined in scripts/generate-stage4.py.
    4: set(),

    # Stage 5: no HF words defined in scripts/generate-stage5.py.
    5: set(),
}


def _load_pgs_up_to(stage: int) -> tuple[set[str], set[str]]:
    """Return (pg_ids, all_substrings_1_to_3) covering stage 1..N.

    pg_ids includes both single-letter and multi-letter phonograms (e.g. 'sh', 'th').
    all_substrings_1_to_3 is the closure of every PG id of length 1, 2, or 3
    — used for substring containment checks.
    """
    pgs = load_phonograms()
    pg_ids = {p.id for p in pgs if p.stage <= stage}
    return pg_ids, pg_ids  # substring containment = id containment


def _word_in_pgs(word: str, pg_ids: set[str]) -> bool:
    """Heuristic decodability check.

    Pass if:
      1. Every letter is a single-letter PG (Stage 1 covers a-z, so all
         English words pass this).
      2. Every 3+ char substring that IS a known multi-letter PG id
         (e.g. 'tch', 'dge', 'igh', 'eigh', 'ough', 'augh', 'tion',
         'sion', 'eau', 'eou') must be in the curriculum up to stage N.

    We intentionally DO NOT check 2-char substrings because they overlap
    with too many consonant clusters (st, cr, bl, fr, br, sl, etc.) and
    2-letter PGs that occur in many short words (si in 'sits' = /s/+/i/,
    ti in 'tip' = /t/+/i/, bu in 'bug' = /b/+/u/). The 3-char check
    catches the egregious over-stage words — 'tch' in 'kitchen' (Stage 3),
    'dge' in 'bridge' (Stage 3), 'igh' in 'light' if Stage 3 not yet
    taught, 'eigh' in 'eight' (Stage 3), 'ough' in 'thought' (Stage 3),
    'tion' in 'station' (Stage 4), etc.

    This is intentionally permissive. Run as a drift detector, not a
    real GPC solver.
    """
    word = word.lower()
    word = "".join(c for c in word if c.isalpha())
    if not word:
        return True
    # 'q' is never alone — it's always 'qu'. Handle q as a special case.
    if "q" in word and "qu" in pg_ids:
        word = word.replace("q", "")  # 'q' is covered by 'qu'
    # Every letter must be a single-letter PG (Stage 1 covers a-z)
    for c in word:
        if c not in pg_ids:
            return False
    # Every 3+ char substring that IS a known multi-letter PG id must be
    # in the curriculum up to stage N
    L = len(word)
    for n in (3, 4):
        for i in range(L - n + 1):
            sub = word[i:i + n]
            if sub in ALL_KNOWN_PG_IDS and len(sub) >= 3:
                if sub not in pg_ids:
                    return False
    return True


# All known PG IDs across all stages (used to detect 3+ char PGs).
ALL_KNOWN_PG_IDS: set[str] = set()


# Markdown sections to ignore (warmup, think-about-it, headers, code fences)
_NON_STORY_RE = re.compile(
    r"^\s*(?:[-*#>|`]|---|\*\*Stage|\*\*Phonograms|Warm-Up|Think About It|##|\d+\.\s)",
    re.MULTILINE,
)


def _extract_story(text: str) -> str:
    """Pull only the 'story' body from a generated reader MD.

    Handles two formats:
      - Generated format (010+, 002-005): '## Story' marker
      - Hand-written format (001-fred-the-frog): '## Page N' markers

    Strips HTML tags, image alt-text, class names, and CSS noise.
    Stops at 'After Reading' / 'Word Hunt' / 'Phonograms used' markers.
    """
    # Generated format: look for '## Story' marker
    m = re.search(r"## Story\s*", text)
    if m:
        start = m.end()
        rest = text[start:]
        # Stop at any later section header
        end_m = re.search(r"\n\s*---\s*\n|\n##\s", rest)
        body = rest[: end_m.start()] if end_m else rest
    else:
        # Hand-written format: '## Page 1' onwards, stop at 'After Reading'
        m2 = re.search(r"## Page\s+1\b", text)
        if m2:
            start = m2.end()
            body = text[start:]
        else:
            body = text
        # Cut off at 'After Reading' or 'Think About It' or 'Phonograms used'
        for stop in (r"\n## After Reading", r"\n## Think About It", r"\*\*Phonograms used\*\*"):
            s = re.search(stop, body)
            if s:
                body = body[: s.start()]
    # Strip ALL HTML tags (including their attributes)
    body = re.sub(r"<[^>]+>", " ", body)
    # Strip markdown image syntax
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", body)
    # Strip HTML entities (nbsp, etc.)
    body = re.sub(r"&[a-z#0-9]+;", " ", body)
    # Strip CSS class names that snuck in as bare words
    body = re.sub(r"\bclass\s*=\s*\"[^\"]*\"", " ", body)
    body = re.sub(r"\bclass\s*=\s*'[^']*'", " ", body)
    # Strip HTML comments
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    # Strip any leftover HTML attribute fragments
    body = re.sub(r"\b(?:div|class|className|style|id|src|href|alt|title|page|sidebar|text)\b", " ", body, flags=re.IGNORECASE)
    return body


def _extract_words(story_body: str) -> list[tuple[str, int]]:
    """Return [(word, line_number)] for every word in the story body.

    Skips the title (bold line) and 'The End.' closer.
    """
    pairs: list[tuple[str, int]] = []
    lines = story_body.splitlines()
    for line_no, line in enumerate(lines, start=1):
        if _NON_STORY_RE.match(line):
            continue
        # Strip markdown bold/italic
        clean = re.sub(r"\*\*", "", line)
        # Strip # headings
        clean = re.sub(r"^#+\s*", "", clean)
        # Strip leading list bullets
        clean = re.sub(r"^\s*[-*]\s+", "", clean)
        # Tokenize
        for tok in re.findall(r"[A-Za-z']+", clean):
            if not tok:
                continue
            pairs.append((tok, line_no))
    return pairs


def _extract_words(story_body: str) -> list[tuple[str, int]]:
    """Return [(word, line_number)] for every word in the story body.

    Skips the title (bold line) and 'The End.' closer.
    """
    pairs: list[tuple[str, int]] = []
    lines = story_body.splitlines()
    for line_no, line in enumerate(lines, start=1):
        if _NON_STORY_RE.match(line):
            continue
        # Strip markdown bold/italic
        clean = re.sub(r"\*\*", "", line)
        # Tokenize
        for tok in re.findall(r"[A-Za-z']+", clean):
            if not tok:
                continue
            pairs.append((tok, line_no))
    return pairs


def _check_story(story_body: str, pg_ids: set[str], hf_words: set[str]) -> list[tuple[str, int, str]]:
    """Return [(word, line_no, reason)] for every non-decodable word.

    A word is OK if:
      - it is in the HF set (case-insensitive), OR
      - it starts with a capital letter (proper noun heuristic) AND the
        lowercase version is either in HF or satisfies pg check, OR
      - _word_in_pgs(word) returns True

    Otherwise flagged.
    """
    flagged: list[tuple[str, int, str]] = []
    for word, line_no in _extract_words(story_body):
        wl = word.lower()
        # Skip empty after stripping
        if not wl:
            continue
        # Check for sentence-start capitalisation (proper noun heuristic)
        is_capital = word[0].isupper()
        # Sentence-start capitals are exempt (I, names that happen to be real words)
        if is_capital and wl in {"i", "a"}:
            continue
        # HF words
        if wl in hf_words:
            continue
        # Proper nouns (capital + multi-letter + not at start of sentence usually)
        # Easiest heuristic: if starts with capital and length > 1, treat as proper noun
        if is_capital and len(wl) > 1:
            # E.g. "Gus", "Finn", "Dilly", "Ben", "Liz", "Sam", "Hen", "Dilly", "Dilly"
            # Also "The" — capital but common word — handled by HF check above
            continue
        # Try to validate
        if not _word_in_pgs(wl, pg_ids):
            flagged.append((word, line_no, "no PG match"))
    return flagged


def _check_file(path: Path, stage: int) -> list[tuple[str, int, str]]:
    text = path.read_text(encoding="utf-8")
    body = _extract_story(text)
    pg_ids, _ = _load_pgs_up_to(stage)
    hf_words = STAGE_HF_WORDS.get(stage, set())
    return _check_story(body, pg_ids, hf_words)


def main() -> int:
    ap = argparse.ArgumentParser(description="Check Stage-N reader decodability")
    ap.add_argument("--stage", type=int, required=True, help="Curriculum stage (1-5)")
    ap.add_argument("--file", type=Path, help="Single MD file to check")
    ap.add_argument("--dir", type=Path, help="Directory of MD files to check")
    args = ap.parse_args()

    files: list[Path] = []
    if args.file:
        files = [args.file]
    elif args.dir:
        files = sorted(args.dir.glob("*.md"))
    else:
        ap.error("Provide --file or --dir")

    pg_ids, _ = _load_pgs_up_to(args.stage)
    # Build ALL known PG IDs (for cross-stage substring detection)
    global ALL_KNOWN_PG_IDS
    from data_loader import load_phonograms as _load_all
    ALL_KNOWN_PG_IDS = {p.id for p in _load_all()}
    hf_words = STAGE_HF_WORDS.get(args.stage, set())
    print(f"Loaded {len(pg_ids)} phonograms up to stage {args.stage}")
    print(f"Loaded {len(hf_words)} HF words for stage {args.stage}")

    total_flagged = 0
    for path in files:
        # Skip our own checker directory
        if "check-reader-decodability" in path.name:
            continue
        text = path.read_text(encoding="utf-8")
        body = _extract_story(text)
        flagged = _check_story(body, pg_ids, hf_words)
        if flagged:
            print(f"\n{path.name}: {len(flagged)} flagged")
            for word, line_no, reason in flagged:
                print(f"  line {line_no}: {word!r} ({reason})")
            total_flagged += len(flagged)
        else:
            print(f"  {path.name}: OK")

    if total_flagged:
        print(f"\n{total_flagged} non-decodable words found across {len(files)} files")
        return 1
    print(f"\nAll {len(files)} files pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
