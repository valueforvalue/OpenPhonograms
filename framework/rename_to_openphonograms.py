#!/usr/bin/env python3
"""Bulk rename project self-references from 'Uncovering the Logic of English'
to 'OpenPhonograms'.

Critical: this script ONLY replaces the project self-references, NEVER the
source book title (which is in italics: *Uncovering the Logic of English*).
The book title MUST be preserved in all attribution contexts.

Run:
    python framework/rename_to_openphonograms.py
    python framework/rename_to_openphonograms.py --dry-run

Exit code 0 = success, 1 = errors.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Patterns to replace (project self-references only).
# Each pattern is a 2-tuple: (regex_pattern, replacement).
# CRITICAL: patterns must NOT match the italicized source book title
# "*Uncovering the Logic of English*" (which is preserved in attribution).
# We achieve this by:
#   1. Matching only specific project-self-reference phrasings
#   2. Avoiding the literal phrase "Uncovering the Logic of English"
#      unless followed by a project-self suffix (e.g. "curriculum", "project")
REPLACEMENTS: list[tuple[str, str]] = [
    # Project name as a compound noun with "curriculum"
    (r"OpenPhonograms curriculum",
     "OpenPhonograms curriculum"),
    (r"OpenPhonograms Curriculum",
     "OpenPhonograms Curriculum"),
    # Project self-references in headlines
    (r"Build Guide — OpenPhonograms",
     "Build Guide — OpenPhonograms"),
    (r"Using OpenPhonograms — For Teachers",
     "Using OpenPhonograms — For Teachers"),
    (r"Welcome to OpenPhonograms",
     "Welcome to OpenPhonograms"),
    (r"# Architecture — OpenPhonograms",
     "# Architecture — OpenPhonograms"),
    # File headers in MD files
    (r"^# Uncovering the Logic of English$",
     "# OpenPhonograms"),
    (r"^# Copyright Review — Uncovering the Logic of English$",
     "# Copyright Review — OpenPhonograms"),
    (r"^## Project: OpenPhonograms Curriculum$",
     "## Project: OpenPhonograms Curriculum"),
    (r"^## Project: Uncovering the Logic of English$",
     "## Project: OpenPhonograms"),
    # In headings
    (r"^# Teach Your Child to Read: A Curriculum Based on \*Uncovering the Logic of English\*$",
     "# Teach Your Child to Read: An OpenPhonograms Curriculum"),
    # Project directory name in code/comments
    (r"OpenPhonograms curriculum/",
     "OpenPhonograms curriculum/"),
    # H1 in docs
    (r"^# Build Guide — OpenPhonograms$",
     "# Build Guide — OpenPhonograms"),
    (r"^# Use.md — Uncovering the Logic of English$",
     "# OpenPhonograms — Use"),
    # NOTICE header
    (r"^Uncovering the Logic of English — Open-Source Curriculum$",
     "OpenPhonograms — Open-Source Curriculum"),
    # AGENTS.md project header
    (r"^## Project: OpenPhonograms Curriculum$",
     "## Project: OpenPhonograms Curriculum"),
    # Hand-off in build handbook
    (r"<h1>Welcome to OpenPhonograms</h1>",
     "<h1>Welcome to OpenPhonograms</h1>"),
    # Game HTML title
    (r"<title>Phonogram Trainer — OpenPhonograms</title>",
     "<title>Phonogram Trainer — OpenPhonograms</title>"),
    (r"<title>Quick Check — OpenPhonograms</title>",
     "<title>Quick Check — OpenPhonograms</title>"),
    (r"<title>Phonogram Chart — OpenPhonograms</title>",
     "<title>Phonogram Chart — OpenPhonograms</title>"),
    (r"<title>Spelling Rules — OpenPhonograms</title>",
     "<title>Spelling Rules — OpenPhonograms</title>"),
    (r"<title>Spelling Analysis Protocol — OpenPhonograms</title>",
     "<title>Spelling Analysis Protocol — OpenPhonograms</title>"),
    (r"<title>Morpheme Wall — OpenPhonograms</title>",
     "<title>Morpheme Wall — OpenPhonograms</title>"),
    (r"<title>High-Frequency Words — OpenPhonograms</title>",
     "<title>High-Frequency Words — OpenPhonograms</title>"),
    (r"<title>Word Lists — OpenPhonograms</title>",
     "<title>Word Lists — OpenPhonograms</title>"),
    (r"<title>Troubleshooting — OpenPhonograms</title>",
     "<title>Troubleshooting — OpenPhonograms</title>"),
    (r"<title>Quickstart — OpenPhonograms</title>",
     "<title>Quickstart — OpenPhonograms</title>"),
    (r"<title>Placement Test — OpenPhonograms</title>",
     "<title>Placement Test — OpenPhonograms</title>"),
    (r"<title>Diacritical Marks Legend — OpenPhonograms</title>",
     "<title>Diacritical Marks Legend — OpenPhonograms</title>"),
    (r"<title>Glossary of Key Terms — OpenPhonograms</title>",
     "<title>Glossary of Key Terms — OpenPhonograms</title>"),
    # Build output banners
    (r"OpenPhonograms — Release ZIP",
     "OpenPhonograms — Release ZIP"),
    (r"This ZIP contains the complete open-source curriculum \(248 lessons, 5 stages,",
     r"This ZIP contains the complete OpenPhonograms curriculum (248 lessons, 5 stages,"),
    # Spell/Build messages
    (r"OpenPhonograms curriculum\.",
     "OpenPhonograms curriculum."),
    # NOTE: lowercase 'uncovering the logic of english' is intentionally
    # NOT replaced. It only appears in source-book attribution contexts
    # (e.g. 'a curriculum based on uncovering the logic of english')
    # and must be preserved. Project self-references always use title case.
    # Cross-reference file context lines
    # (Do NOT modify the source attribution footer — that text must remain
    # exactly as it appears, citing the source book by name.)
    # (r"Source: Adapted from the methodology of Uncovering the Logic of English",
    #  "Source: Adapted from the methodology of *Uncovering the Logic of English* (the source book). OpenPhonograms is an independent open-source curriculum."),
]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would change without modifying")
    args = p.parse_args()

    # Find all candidate files
    exts = {".md", ".py", ".html", ".json", ".yml", ".yaml", ".toml", ".css", ".js", ".txt"}
    files_to_check = []
    skip_dirs = {".git", "build", "release.zip", ".rpiv", "__pycache__", "node_modules"}
    for path in ROOT.rglob("*"):
        if any(p in path.parts for p in skip_dirs):
            continue
        if path.is_file() and path.suffix.lower() in exts:
            files_to_check.append(path)

    # Compile all patterns
    compiled = [(re.compile(p), r) for p, r in REPLACEMENTS]

    changes = []
    for f in files_to_check:
        try:
            content = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_content = content
        for pat, repl in compiled:
            new_content = pat.sub(repl, new_content)
        if new_content != content:
            changes.append((f, content, new_content))

    if not changes:
        print("No changes needed.")
        return 0

    # Print summary
    print(f"{'Would modify' if args.dry_run else 'Modifying'} {len(changes)} files:")
    for f, _, _ in changes[:30]:
        print(f"  {f.relative_to(ROOT)}")
    if len(changes) > 30:
        print(f"  ... and {len(changes) - 30} more")

    if not args.dry_run:
        for f, _, new_content in changes:
            f.write_text(new_content, encoding="utf-8")
        print(f"\nDone. {len(changes)} files updated.")
    return 0


if __name__ == "__main__":
    main()