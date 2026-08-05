# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Check image coverage: every PNG on disk should be referenced in some markdown.

Catches:
- Orphan PNGs (on disk but not used anywhere)
- Missing PNGs (referenced but file doesn't exist)

Usage:
    python scripts/check-image-coverage.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Find all PNG/JPG files under images/
image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
all_images = {
    p.relative_to(ROOT).as_posix()
    for p in (ROOT / "images").rglob("*")
    if p.is_file() and p.suffix.lower() in image_extensions
}

# Find all image references in markdown
img_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
referenced = set()
for md_path in ROOT.rglob("*.md"):
    # Skip build artifacts and node_modules
    if any(part in md_path.parts for part in ("build", "node_modules", ".git", "packs")):
        continue
    try:
        text = md_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for match in img_pattern.finditer(text):
        ref = match.group(1).strip()
        # Strip any URL fragment / query
        ref = ref.split("#")[0].split("?")[0]
        # Skip external URLs and template placeholders
        if ref.startswith(("http://", "https://", "data:", "{")):
            continue
        referenced.add(ref)

orphans = sorted(all_images - referenced)
missing = sorted(referenced - all_images)

print(f"==> Image coverage check")
print(f"  Images on disk:   {len(all_images)}")
print(f"  Referenced:       {len(referenced)}")
print(f"  Orphans:          {len(orphans)}")
print(f"  Missing:          {len(missing)}")

if orphans:
    print("\nOrphan images (on disk but never used):")
    for p in orphans:
        print(f"  ORPHAN  {p}")

if missing:
    print("\nMissing images (referenced but file not found):")
    for p in missing:
        print(f"  MISSING  {p}")
    sys.exit(1)

if orphans:
    sys.exit(0)  # Orphans are warnings only

print("\nAll images referenced, none missing.")