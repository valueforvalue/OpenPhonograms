#!/usr/bin/env python3
"""
image-check.py — List images referenced in lessons that don't exist yet.

Usage:
    python image-check.py            # List all missing images
    python image-check.py --prompts  # Output generation prompts for missing images
"""

import argparse
import csv
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "lessons"
WORKSHEETS_DIR = PROJECT_ROOT / "worksheets"
READERS_DIR = PROJECT_ROOT / "readers"
IMAGES_DIR = PROJECT_ROOT / "images"
FRAMEWORK_DIR = PROJECT_ROOT / "framework"
MANIFEST_PATH = FRAMEWORK_DIR / "image-manifest.csv"


def find_image_refs() -> dict[str, list[Path]]:
    """Scan all markdown files and return {image_src: [referencing_files]}."""
    refs: dict[str, list[Path]] = {}
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    for md_dir in [LESSONS_DIR, WORKSHEETS_DIR, READERS_DIR, PROJECT_ROOT]:
        if not md_dir.exists():
            continue
        for md_file in md_dir.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            for match in img_pattern.finditer(text):
                src = match.group(2)
                if src not in refs:
                    refs[src] = []
                refs[src].append(md_file)

    return refs


def load_manifest() -> dict[str, dict]:
    """Load image-manifest.csv into {filename: row}."""
    manifest = {}
    if not MANIFEST_PATH.exists():
        return manifest
    with open(MANIFEST_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            manifest[row["filename"]] = row
    return manifest


def cmd_list_missing():
    refs = find_image_refs()
    manifest = load_manifest()
    missing = 0

    for src, files in sorted(refs.items()):
        img_path = PROJECT_ROOT / src
        if img_path.exists():
            continue
        missing += 1
        print(f"\n📷 {src}")
        print(f"   Referenced by: {len(files)} file(s)")
        for f in files[:3]:
            print(f"     - {f.relative_to(PROJECT_ROOT)}")
        if len(files) > 3:
            print(f"     ... and {len(files) - 3} more")
        # Check manifest
        if src in manifest:
            m = manifest[src]
            print(f"   Manifest: {m.get('description', '—')}")
            print(f"   Prompt exists: yes")

    print(f"\n{'—' * 40}")
    print(f"Total missing images: {missing}")
    print(f"Total referenced images: {len(refs)}")


def cmd_output_prompts():
    refs = find_image_refs()
    manifest = load_manifest()

    print("# Image Generation Prompts\n")
    print("Generate each image using these prompts. Consistent style across all images.\n")

    for src, files in sorted(refs.items()):
        img_path = PROJECT_ROOT / src
        if img_path.exists():
            continue

        if src in manifest:
            m = manifest[src]
            print(f"## {src}")
            print(f"**Size:** {m.get('size', '1200x900')} | **Format:** {m.get('format', 'png')}")
            print(f"**Description:** {m.get('description', '—')}")
            print(f"\n**Prompt:**\n```\n{m.get('prompt', '—')}\n```\n")
        else:
            print(f"## {src}")
            print(f"**No manifest entry — needs prompt.** Referenced by {len(files)} file(s).")
            print(f"\n**Suggested prompt:**\n```\n[WRITE PROMPT HERE]\n```\n")


def main():
    parser = argparse.ArgumentParser(description="Check missing images for Logic of English materials")
    parser.add_argument("--prompts", action="store_true", help="Output generation prompts for missing images")
    args = parser.parse_args()

    if args.prompts:
        cmd_output_prompts()
    else:
        cmd_list_missing()


if __name__ == "__main__":
    main()
