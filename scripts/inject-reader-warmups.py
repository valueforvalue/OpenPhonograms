# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Inject warm-up sections into Stages 3-4 reader lessons.

Reader lessons (reader-2 through reader-6) lack warm-up sections.
This script inserts them in the right place, matching the schema used by
reader-1 (Stage 2) and the standalone readers in readers/.

Run once. Idempotent — skips files that already have warm-ups.

Usage:
  python scripts/inject-reader-warmups.py
"""

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# Warm-up content for each reader. Hand-curated from the story vocabulary.
WARMUPS = {
    "lessons/stage-3/reader-2.md": {
        "title": "Gwen Gives a Gift",
        "phonograms": "g (both sounds), silent E, ee, ai, ay, ow",
        "words": "Gwen &nbsp; Grace &nbsp; gift &nbsp; goat &nbsp; goose &nbsp; green &nbsp; gives &nbsp; golden &nbsp; gate &nbsp; grass",
    },
    "lessons/stage-3/reader-3.md": {
        "title": "Cole and His Bike",
        "phonograms": "silent E, ie, ai, ay, ck",
        "words": "Cole &nbsp; Kate &nbsp; bike &nbsp; rides &nbsp; hill &nbsp; fast &nbsp; red &nbsp; friend &nbsp; share &nbsp; calls",
    },
    "lessons/stage-3/reader-4.md": {
        "title": "The Sail Box",
        "phonograms": "silent E (all 9 reasons), ai, ay, dge, tch",
        "words": "Jake &nbsp; sail &nbsp; boat &nbsp; box &nbsp; shed &nbsp; blue &nbsp; paint &nbsp; folds &nbsp; tapes &nbsp; finds",
    },
    "lessons/stage-4/reader-5.md": {
        "title": "Firefly: Nightlight with Wings",
        "phonograms": "y (=/ē/), silent E, igh, ir",
        "words": "firefly &nbsp; light &nbsp; glow &nbsp; night &nbsp; wings &nbsp; summer &nbsp; garden &nbsp; dark &nbsp; blink &nbsp; shine",
    },
    "lessons/stage-4/reader-6.md": {
        "title": "Trains",
        "phonograms": "ai, ay, silent E, er, tch",
        "words": "train &nbsp; steam &nbsp; coal &nbsp; rail &nbsp; engine &nbsp; fast &nbsp; station &nbsp; track &nbsp; iron &nbsp; smoke",
    },
}


def make_warmup_block(title: str, phonograms: str, words: str) -> str:
    """Generate the warm-up markdown block."""
    return f"""## Warm-Up: Phonogram Flash Review

> Quick flash of phonograms used in today's story.

| Phonograms to review |
|----------------------|
| {phonograms} |

---

## Warm-Up Words — Read These First

Read each word sound by sound BEFORE reading the story:

> {words}

---

"""


def inject_warmup(md_path: Path, content: dict) -> bool:
    """Inject warm-up into a reader MD file. Returns True if changed."""
    text = md_path.read_text(encoding="utf-8")

    # Skip if already has warm-up
    if "## Warm-Up: Phonogram Flash Review" in text:
        print(f"  SKIP  {md_path.relative_to(ROOT)}  (already has warm-up)")
        return False

    # Insert after the first `---` separator (which is right after the title block)
    # Pattern: '# Title\n\n**Stage X** · ...\n\n---\n\n## ...'
    # We want to inject before the first '## ' section.
    match = re.search(r"\n---\n\n(## )", text)
    if not match:
        print(f"  FAIL  {md_path.relative_to(ROOT)}  (no '---' separator found)")
        return False

    insert_pos = match.end() - len("## ")
    warmup = make_warmup_block(content["title"], content["phonograms"], content["words"])
    new_text = text[:insert_pos] + warmup + text[insert_pos:]

    md_path.write_text(new_text, encoding="utf-8")
    print(f"  OK    {md_path.relative_to(ROOT)}")
    return True


def main():
    print("==> Injecting warm-up sections into Stages 3-4 readers")
    n_changed = 0
    for rel_path, content in WARMUPS.items():
        md_path = ROOT / rel_path
        if not md_path.exists():
            print(f"  MISS  {rel_path}  (file not found)")
            continue
        if inject_warmup(md_path, content):
            n_changed += 1
    print(f"\nDone: {n_changed} files updated")


if __name__ == "__main__":
    main()
