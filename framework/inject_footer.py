"""Inject source-attribution footer into generated MD files (issue #32).

After generators emit their MD content, this script ensures every
lesson/worksheet/reader MD ends with the standardized source
attribution footer. The footer is the same one added to the templates
in framework/templates/*.md.

Usage:
    python framework/inject_footer.py                # walk defaults
    python framework/inject_footer.py lessons/ worksheets/ readers/
    python framework/inject_footer.py --dry-run      # preview only

The script is idempotent: files that already have the footer are
skipped. Files where the footer is not the LAST block are updated.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOOTER = (
    "\n---\n\n"
    "*Open-source. MIT licensed. Phonograms are drawn from the "
    "public-domain phonics tradition (1800s onward).*\n"
)
FOOTER_MARKER = "Open-source. MIT licensed"
# Old (pre-rebrand) footer marker. Matched so we can strip it during the
# one-time migration of remaining MD files.
LEGACY_FOOTER_MARKER = "Source: Adapted from the methodology"


def needs_footer(content: str) -> bool:
    """True if the file should have the footer appended/replaced."""
    # Has the legacy footer (pre-rebrand)? Always needs replacement.
    if LEGACY_FOOTER_MARKER in content:
        return True
    # Has the new footer? Check if it's the LAST block.
    if FOOTER_MARKER in content:
        return not content.rstrip().endswith(FOOTER.rstrip())
    # No footer at all.
    return True


def strip_existing_footer(content: str) -> str:
    """Remove any existing footer (new or legacy) so we can write a fresh one."""
    for marker in (FOOTER_MARKER, LEGACY_FOOTER_MARKER):
        if marker not in content:
            continue
        lines = content.splitlines()
        out = []
        for line in lines:
            if marker in line:
                break
            out.append(line)
        content = "\n".join(out).rstrip() + "\n"
    return content


def add_footer(path: Path, dry_run: bool = False) -> str:
    """Inject footer into a single MD file. Returns 'added', 'updated', or 'unchanged'."""
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "skipped"
    if not needs_footer(content):
        return "unchanged"
    content = strip_existing_footer(content)
    if not content.endswith("\n"):
        content += "\n"
    new_content = content + FOOTER
    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return "added" if FOOTER_MARKER not in content else "updated"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dirs", nargs="*", default=[
        "lessons", "worksheets", "readers", "reference",
    ], help="Directories to walk (default: lessons, worksheets, readers, reference)")
    p.add_argument("--dry-run", action="store_true", help="Preview only")
    args = p.parse_args()

    added = updated = unchanged = skipped = 0
    for d in args.dirs:
        dpath = ROOT / d
        if not dpath.exists():
            continue
        for md in sorted(dpath.rglob("*.md")):
            result = add_footer(md, dry_run=args.dry_run)
            if result == "added":   added += 1
            elif result == "updated": updated += 1
            elif result == "unchanged": unchanged += 1
            else: skipped += 1
    verb = "Would add" if args.dry_run else "Added"
    print(f"  {verb} {added} files, updated {updated}, unchanged {unchanged}, "
          f"skipped {skipped}")
    if not args.dry_run and (added or updated):
        print(f"  Footer: 'Open-source. MIT licensed. Phonograms drawn from the public-domain phonics tradition.'")


if __name__ == "__main__":
    main()