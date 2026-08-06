"""Inject source-attribution footer into generated MD files (issue #32).

DEPRECATED (post-CSS-density refactor): the footer is now rendered by
the framework's @page CSS rules, not injected into MD content. This
script is kept as a no-op so existing build pipelines still work.

The script still recognizes both the new ('Open-source. MIT licensed')
and legacy ('Source: Adapted from the methodology') footers and
STrips them from MD files. After running, the framework's CSS renders
the footer at the bottom of every PDF page automatically.

Usage:
    python framework/inject_footer.py                # walk defaults + strip
    python framework/inject_footer.py lessons/ worksheets/ readers/
    python framework/inject_footer.py --dry-run      # preview only
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# FOOTER is the fallback template used by HTML files (HTMLs don't get
# the CSS @page footer). The PDF footer is rendered by render.py's
# @page CSS, not from this string.
FOOTER = (
    "\n---\n\n"
    "*OpenPhonograms · MIT licensed. Phonograms are drawn from the "
    "public-domain phonics tradition (1800s onward).*\n"
)
FOOTER_MARKER = "OpenPhonograms · MIT licensed"  # marker for current FOOTER
# Old (pre-rebrand) footer marker. Matched so we can strip it during the
# one-time migration of remaining MD files.
LEGACY_FOOTER_MARKER = "Source: Adapted from the methodology"
# Pre-CSS-density in-text footer (used between rebrand and CSS-density
# refactor). Strip on migration to the new CSS-rendered footer.
LEGACY2_FOOTER_MARKER = "Open-source. MIT licensed"


def needs_footer(content: str) -> bool:
    """True if the file has a footer that should be stripped."""
    if LEGACY_FOOTER_MARKER in content:
        return True
    if LEGACY2_FOOTER_MARKER in content:
        return True
    if FOOTER_MARKER in content:
        return True
    return False


def strip_existing_footer(content: str) -> str:
    """Remove any existing footer (current or legacy) so we can write a fresh one."""
    for marker in (FOOTER_MARKER, LEGACY_FOOTER_MARKER, LEGACY2_FOOTER_MARKER):
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


def strip_footer(path: Path, dry_run: bool = False) -> str:
    """Strip footer from a single MD file. Returns 'updated' or 'unchanged'."""
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "skipped"
    if not needs_footer(content):
        return "unchanged"
    new_content = strip_existing_footer(content)
    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return "updated"


# Backwards compat alias — old callers used add_footer.
def add_footer(path: Path, dry_run: bool = False) -> str:
    """DEPRECATED: now strips the footer instead of injecting it.

    Kept for callers that haven't migrated. Returns 'updated' if the
    footer was removed, 'unchanged' if none was present.
    """
    return strip_footer(path, dry_run)


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