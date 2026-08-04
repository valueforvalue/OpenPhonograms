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

# Force UTF-8 on Windows consoles that default to cp1252
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "lessons"
WORKSHEETS_DIR = PROJECT_ROOT / "worksheets"
READERS_DIR = PROJECT_ROOT / "readers"
IMAGES_DIR = PROJECT_ROOT / "images"
FRAMEWORK_DIR = PROJECT_ROOT / "framework"
MANIFEST_PATH = FRAMEWORK_DIR / "image-manifest.csv"


def _is_template_var(s: str) -> bool:
    """True if the string is a Jinja2-style template placeholder like {cover_image_path}."""
    return bool(re.match(r'^\{.*\}$', s))


def _normalize_src(src: str) -> str:
    """Strip 'images/' prefix so 'images/animals/dog.png' -> 'animals/dog.png'."""
    if src.startswith("images/"):
        return src[7:]
    return src


def find_image_refs() -> dict[str, list[Path]]:
    """Scan all markdown files and return {normalized_image_src: [referencing_files]}.
    Deduplicates so 'animals/frog.png' and 'images/animals/frog.png' are merged.
    """
    refs: dict[str, list[Path]] = {}
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    for md_dir in [LESSONS_DIR, WORKSHEETS_DIR, READERS_DIR, PROJECT_ROOT]:
        if not md_dir.exists():
            continue
        for md_file in md_dir.rglob("*.md"):
            # Skip template files (they contain {placeholder} variables)
            if "templates" in str(md_file):
                continue
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            for match in img_pattern.finditer(text):
                src = match.group(2)
                # Skip template variables and web URLs
                if _is_template_var(src):
                    continue
                if src.startswith("http://") or src.startswith("https://"):
                    continue
                # Normalize: strip leading 'images/' so 'images/animals/frog.png'
                # and 'animals/frog.png' are the same key
                norm = _normalize_src(src)
                if norm not in refs:
                    refs[norm] = []
                refs[norm].append(md_file)

    return refs


def load_manifest() -> dict[str, dict]:
    """Load image-manifest.csv. Index by both raw key and 'images/' prefixed key."""
    manifest = {}
    if not MANIFEST_PATH.exists():
        return manifest
    with open(MANIFEST_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = row["filename"]
            manifest[key] = row
            manifest[f"images/{key}"] = row
    return manifest


def cmd_list_missing():
    refs = find_image_refs()
    manifest = load_manifest()
    missing = 0

    for src, files in sorted(refs.items()):
        # Check both normalized path and with 'images/' prefix
        img_path = PROJECT_ROOT / "images" / src
        if img_path.exists():
            continue
        missing += 1
        print(f"\n[IMG] {src}")
        print(f"   Referenced by: {len(files)} file(s)")
        for f in files[:3]:
            print(f"     - {f.relative_to(PROJECT_ROOT)}")
        if len(files) > 3:
            print(f"     ... and {len(files) - 3} more")

        m = manifest.get(src) or manifest.get(_normalize_src(src))
        if m:
            print(f"   [OK] Prompt exists: {m.get('description', '—')[:80]}")
        else:
            print(f"   [MISSING] No manifest entry — needs prompt")

    print(f"\n{'—' * 40}")
    print(f"Images referenced: {len(refs)}")
    print(f"Images missing:   {missing}")
    with_prompts = sum(
        1 for src in refs
        if not (PROJECT_ROOT / "images" / src).exists()
        and (manifest.get(src) or manifest.get(_normalize_src(src)))
    )
    without_prompts = sum(
        1 for src in refs
        if not (PROJECT_ROOT / "images" / src).exists()
        and not (manifest.get(src) or manifest.get(_normalize_src(src)))
    )
    existing = sum(1 for src in refs if (PROJECT_ROOT / "images" / src).exists())
    print(f"  Existing:       {existing}")
    print(f"  Need generate:  {missing} ({with_prompts} have prompts, {without_prompts} need prompts)")


def cmd_output_prompts():
    refs = find_image_refs()
    manifest = load_manifest()

    print("# Image Generation Prompts\n")
    print("Generate each image using these prompts. Consistent style across all images.\n")
    print("> **IMPORTANT:** Apply the Montessori Style Guide to EVERY image.")
    print("> See: framework/STYLE-GUIDE.md for the complete pre-prompt.\n")
    print("---\n")
    count = 0

    for src, files in sorted(refs.items()):
        img_path = PROJECT_ROOT / "images" / src
        if img_path.exists():
            continue

        m = manifest.get(src) or manifest.get(_normalize_src(src))
        if m:
            count += 1
            print(f"## {count}. {src}")
            print(f"**Size:** {m.get('size', '1200x900')} | **Format:** {m.get('format', 'png')}")
            print(f"**Description:** {m.get('description', '—')}")
            print(f"\n**Prompt:**\n```\n{m.get('prompt', '—')}\n```\n")
        else:
            count += 1
            print(f"## {count}. {src}")
            print(f"**No manifest entry — needs prompt.** Referenced by {len(files)} file(s).")
            print(f"\n**Suggested prompt:**\n```\n[WRITE PROMPT HERE]\n```\n")

    print(f"\n{'—' * 40}")
    print(f"Total images to generate: {count}")


def cmd_all_manifest():
    """Output ALL prompts from the manifest, not just referenced ones."""
    manifest = load_manifest()
    seen = set()
    count = 0

    print("# Complete Image Generation Prompts\n")
    print(f"Total images planned: {len(manifest) // 2} (each indexed twice)\n")
    print("> **IMPORTANT:** Apply the Montessori Style Guide to EVERY image.")
    print("> See: framework/STYLE-GUIDE.md for the complete pre-prompt.\n")
    print("---\n")

    for key, m in sorted(manifest.items()):
        # Skip duplicate 'images/' prefixed keys
        base_key = key.replace("images/", "")
        if base_key in seen:
            continue
        if key.startswith("images/"):
            seen.add(key[7:])
        else:
            seen.add(key)
            continue  # process only the 'images/' prefixed version for output

    seen.clear()
    for key, m in sorted(manifest.items()):
        if not key.startswith("images/"):
            continue
        base_key = key[7:]
        if base_key in seen:
            continue
        seen.add(base_key)
        count += 1
        print(f"## {count}. {base_key}")
        print(f"**Category:** {m.get('category', '—')}")
        print(f"**Size:** {m.get('size', '1200x900')} | **Format:** {m.get('format', 'png')}")
        print(f"**Description:** {m.get('description', '—')}")
        print(f"\n**Prompt:**\n```\n{m.get('prompt', '—')}\n```\n")

    print(f"\n{'—' * 40}")
    print(f"Total images: {count}")


def main():
    parser = argparse.ArgumentParser(description="Check missing images for Logic of English materials")
    parser.add_argument("--prompts", action="store_true", help="Output generation prompts for missing images")
    parser.add_argument("--all-manifest", action="store_true", help="Output ALL manifest prompts (not just referenced)")
    args = parser.parse_args()

    if args.all_manifest:
        cmd_all_manifest()
    elif args.prompts:
        cmd_output_prompts()
    else:
        cmd_list_missing()


if __name__ == "__main__":
    main()
