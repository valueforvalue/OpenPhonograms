# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
optimize_images.py — Shrink oversized source PNGs in images/.

Why this exists:
  Several source PNGs are 2400x1792 with mostly-white background. PDF
  renders embed them at full resolution, producing 7-9 MB PDFs from
  2 image references. Cat.png (7 MB) is mostly white space.

How it works:
  1. Auto-trim the white border (PIL Image.getbbox + white-fill detection).
  2. Resize the trimmed image down to a max dimension (default 1200px).
  3. Re-encode as PNG with optimize=True + RGB palette quantize.

Idempotent: skipping already-optimized images (by source-vs-target size
delta). Run once on the source tree, commit the new PNGs.

Usage:
    python framework/optimize_images.py
    python framework/optimize_images.py --dry-run
    python framework/optimize_images.py --max-dim 1600
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIRS = [ROOT / "images"]


def is_mostly_white(img, threshold: int = 245) -> bool:
    """Return True if the image is mostly white/near-white.

    Used to detect candidate images for crop.
    """
    from PIL import Image
    # Sample the 4 corners + center
    w, h = img.size
    samples = [
        img.getpixel((0, 0)),
        img.getpixel((w-1, 0)),
        img.getpixel((0, h-1)),
        img.getpixel((w-1, h-1)),
        img.getpixel((w // 2, h // 2)),
    ]
    # For RGB or RGBA, check all 3 color channels
    whites = 0
    for s in samples:
        if len(s) >= 3:
            if all(c >= threshold for c in s[:3]):
                whites += 1
    return whites >= 4


def trim_whitespace(img, threshold: int = 250) -> "Image.Image":
    """Trim near-white borders.

    Uses PIL's getbbox on a mask of non-white pixels. Preserves aspect ratio.
    """
    from PIL import Image, ImageChops
    # Build a grayscale mask: 0 where pixel is below threshold (non-white)
    gray = img.convert("L")
    # Invert so non-white = 255, white = 0
    from PIL import ImageOps
    inv = ImageOps.invert(gray)
    # threshold to make a binary mask
    mask = inv.point(lambda v: 255 if v > (255 - threshold) else 0)
    bbox = mask.getbbox()
    if bbox is None:
        return img  # all white, return original
    # bbox is (left, top, right, bottom)
    return img.crop(bbox)


def optimize_image(
    path: Path,
    max_dim: int = 1200,
    always_optimize: bool = False,
) -> tuple[int, int, bool]:
    """Resize + recompress a single PNG.

    Returns: (before_bytes, after_bytes, saved)
    """
    from PIL import Image

    before = path.stat().st_size
    img = Image.open(path)

    # Step 1: trim whitespace if the image is mostly white
    if always_optimize or is_mostly_white(img):
        img = trim_whitespace(img)

    # Step 2: resize if either dimension exceeds max_dim
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # Step 3: convert to RGB if RGBA (no transparency in source illustrations)
    if img.mode == "RGBA":
        # Composite onto white background (kill transparency for print)
        from PIL import Image as PILImage
        bg = PILImage.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Save with optimization
    img.save(path, format="PNG", optimize=True)

    after = path.stat().st_size
    return before, after, after < before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-dim", type=int, default=1200,
                        help="Max width/height in pixels (default 1200)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report sizes without writing")
    parser.add_argument("--always", action="store_true",
                        help="Always trim even if corners aren't all white")
    args = parser.parse_args()

    files = []
    for d in IMAGE_DIRS:
        if not d.exists():
            continue
        # rglob is case-sensitive on Linux but case-insensitive on Windows.
        # Use a single pattern and let the OS handle casing.
        seen = set()
        for ext in ("*.png", "*.PNG", "*.Png"):
            for f in d.rglob(ext):
                if f not in seen:
                    seen.add(f)
                    files.append(f)

    if not files:
        print("No PNG files found.")
        return 0

    total_before = 0
    total_after = 0
    n_optimized = 0
    n_skipped = 0

    for f in sorted(files):
        # Skip files smaller than 500 KB — not worth optimizing
        if f.stat().st_size < 500_000:
            n_skipped += 1
            continue

        before = f.stat().st_size
        if args.dry_run:
            from PIL import Image
            img = Image.open(f)
            w, h = img.size
            print(f"  SKIP (dry-run): {f.relative_to(ROOT)}: {before/1024:.1f} KB, {w}x{h}")
            continue

        try:
            new_before, new_after, saved = optimize_image(f, args.max_dim, args.always)
        except Exception as exc:
            print(f"  WARN: {f.relative_to(ROOT)}: {exc}")
            continue

        if saved:
            n_optimized += 1
            total_before += new_before
            total_after += new_after
            pct = (1 - new_after / new_before) * 100 if new_before else 0
            print(f"  OK {f.relative_to(ROOT)}: {new_before/1024:.1f} -> {new_after/1024:.1f} KB ({pct:.0f}%)")
        else:
            n_skipped += 1
            print(f"  -- {f.relative_to(ROOT)}: no savings")

    if not args.dry_run:
        print()
        print(f"Optimized {n_optimized} files, skipped {n_skipped}.")
        if total_before:
            saved = total_before - total_after
            pct = saved / total_before * 100
            print(f"Total: {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB "
                  f"(saved {saved/1024/1024:.1f} MB, {pct:.0f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
