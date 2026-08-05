"""Build release.zip — complete curriculum in LOE-style folder structure.

Default behavior bundles everything into a single ZIP. Pass CLI flags to
include or exclude specific sections, restrict to one stage, or change the
output path. Dry-run with --list to see what would be included.

Produces a top-level ZIP with:

  README.md                        — text overview of what's in the release
  00-Start-Here.pdf                — orientation for new users
  01-Index-and-Table-of-Contents.pdf — master TOC with hyperlinks
  02-Scope-and-Sequence.pdf        — full curriculum map
  04-Quick-Reference/              — phonograms, rules, spelling analysis
  05-Teacher-Handbooks/            — 5 bound-book-style stage handbooks
  06-Lesson-Packs/                 — 248 per-lesson bundles (5 stage folders)
  07-Worksheets/                   — 178 standalone practice sheets
  08-Decodable-Readers/            — 25 readers + index
  09-Quick-Checks/                 — placement + 5 stage quick-checks
  10-Assessments/                  — 8 stage mastery assessments
  11-Game/                         — phonogram trainer (web game)
  12-Audio/                        — 74 phonogram MP3s
  13-Certificates/                 — 5 printable completion certificates

All paths inside the ZIP use forward slashes (POSIX) for cross-platform use.

Usage:
  python scripts/build-release.py                          # full release (default)
  python scripts/build-release.py --output custom.zip      # custom output path
  python scripts/build-release.py --stage 3                # only Stage 3 assets
  python scripts/build-release.py --no-game --no-audio     # skip game + audio
  python scripts/build-release.py --no-lessons             # skip 06-Lesson-Packs/
  python scripts/build-release.py --list                   # dry-run, list contents
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"


# ── Helpers ────────────────────────────────────────────────────────────

def add_file(zf: zipfile.ZipFile, src: Path, arcname: str) -> bool:
    """Add a file to the ZIP. Returns True if added, False if missing."""
    if src.exists():
        zf.write(src, arcname.replace("\\", "/"))
        return True
    return False


def add_directory(zf: zipfile.ZipFile, src_dir: Path, arc_prefix: str,
                  stage_filter: int | None = None) -> int:
    """Add all files from a directory recursively.

    stage_filter: if set, only include files whose path contains
    'stage-N/' matching the given stage. Used for per-stage filtering.
    """
    if not src_dir.exists():
        return 0
    count = 0
    for f in sorted(src_dir.rglob("*")):
        if not f.is_file():
            continue
        if stage_filter is not None:
            rel = f.relative_to(src_dir).as_posix()
            if f"stage-{stage_filter}/" not in rel + "/":
                continue
        rel = f.relative_to(src_dir).as_posix()
        zf.write(f, f"{arc_prefix}/{rel}".replace("\\", "/"))
        count += 1
    return count


# ── Section builders ───────────────────────────────────────────────────

def _stages(args) -> list[int]:
    """Resolve which stages to include (1-5)."""
    return [args.stage] if args.stage else [1, 2, 3, 4, 5]


def build_readme(zf, args, stats):
    """Section 0: README.md."""
    if args.no_readme:
        stats["skipped"].append("README.md")
        return
    if args.list:
        stats["included"].append("README.md")
        return
    readme_text = """Uncovering the Logic of English — Release ZIP

This ZIP contains the complete open-source curriculum (248 lessons, 5 stages,
75 phonograms, 31 spelling rules, 25 decodable readers) plus all printable
aids, the phonogram trainer web game, and 74 phonogram audio MP3s.

QUICK START
-----------
1. Open 00-Start-Here.pdf — orientation for new users.
2. Open 01-Index-and-Table-of-Contents.pdf — master TOC with clickable links.
3. Print 09-Quick-Checks/placement-test.pdf and run it to find your starting stage.
4. Open 06-Lesson-Packs/stage-N/ and start with lesson pack #1.

WHAT'S IN THIS RELEASE
----------------------
00-Start-Here.pdf                      — orientation
01-Index-and-Table-of-Contents.pdf     — master clickable TOC
02-Scope-and-Sequence.pdf              — full curriculum map
04-Quick-Reference/                    — phonograms, rules, spelling analysis,
                                          diacritical legend, glossary (HTMLs + PDFs)
05-Teacher-Handbooks/                  — 5 bound-book-style stage handbooks (PDFs)
06-Lesson-Packs/                       — 248 per-lesson bundles
06-Stage-Overview/stage-N.pdf          — merged per-stage review (PDF)
07-Worksheets/                         — 178 standalone practice sheets
                                          (organized by stage + category)
07-Worksheets/stage-N-worksheets.pdf   — merged per-stage worksheets
08-Decodable-Readers/                  — 25 decodable story PDFs + index
08-Decodable-Readers/stage-N-readers.pdf — merged per-stage readers
09-Quick-Checks/                       — placement test + 5 stage quick-checks
10-Assessments/                        — 8 stage mastery assessments

METHODOLOGY
-----------
Speech-to-print. Spelling drives reading. 75 phonograms + 31 spelling rules
cover 98% of English words. No sight words. The 5-step Spelling Analysis
routine is used in every lesson.

Source methodology: Uncovering the Logic of English by Denise Eide
(https://logicofenglish.com/).

LICENSE
-------
This is an open-source adaptation released for educational use. The
methodology and phonogram list are not copyrighted (drawn from public-domain
phonics tradition). The lesson content, generators, and design are released
under MIT license. The commercial LoE product line (Doodling Dragons /
Whistling Whales / Knitting Knights artwork, etc.) is not included.

For questions, issues, or contributions, see the project repository.
"""
    zf.writestr("README.md", readme_text)
    stats["included"].append("README.md")


def build_handbook_nav(zf, args, stats):
    """Section 1: Top-level handbook PDFs (00-, 01-, 02-, binding)."""
    if args.no_nav:
        stats["skipped"].append("00-/01-/02- handbook PDFs")
        return
    handbook = BUILD / "handbook"
    if not handbook.exists():
        return
    count = 0
    for f in sorted(handbook.glob("*.pdf")):
        name = f.name
        # 00-Start-Here, 01-Index, 02-Scope at top level
        if name.startswith(("00-", "01-", "02-")):
            arc = name
        elif name.startswith("04-"):
            if args.no_reference:
                continue
            arc = f"04-Quick-Reference/{name}"
        elif "handbook" in name and name.startswith("stage-"):
            # Stage handbooks handled by build_handbooks() unless --no-handbooks
            if args.no_handbooks:
                continue
            arc = f"05-Teacher-Handbooks/{name}"
        elif name.startswith("certificate-"):
            if args.no_certs:
                continue
            arc = f"13-Certificates/{name}"
        elif "readers-index" in name:
            if args.no_readers:
                continue
            arc = f"08-Decodable-Readers/{name}"
        else:
            continue  # Other handbook PDFs (assessments, quick-checks) handled separately
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(f, arc)
        count += 1
    # Landing page
    landing_pdf = handbook / "00-Landing-Page.pdf"
    if landing_pdf.exists() and not args.no_nav:
        if args.list:
            stats["included"].append("00-Landing-Page.pdf")
        else:
            zf.write(landing_pdf, "00-Landing-Page.pdf")
    # Binding instructions
    binding_pdf = handbook / "binding-instructions.pdf"
    if binding_pdf.exists():
        if args.list:
            stats["included"].append("binding-instructions.pdf")
        else:
            zf.write(binding_pdf, "binding-instructions.pdf")


def build_landing_html(zf, args, stats):
    """Section 1b: Landing page HTML."""
    if args.no_nav:
        stats["skipped"].append("00-Landing-Page.html")
        return
    landing_html = ROOT / "docs" / "index.html"
    if not landing_html.exists():
        return
    if args.list:
        stats["included"].append("00-Landing-Page.html")
    else:
        zf.write(landing_html, "00-Landing-Page.html")


def build_handbooks(zf, args, stats):
    """Section 5: Stage-N handbooks from build/handbook/stage-N-handbook.pdf."""
    if args.no_handbooks:
        stats["skipped"].append("05-Teacher-Handbooks/")
        return
    handbook = BUILD / "handbook"
    if not handbook.exists():
        return
    for stage in _stages(args):
        f = handbook / f"stage-{stage}-handbook.pdf"
        if not f.exists():
            continue
        arc = f"05-Teacher-Handbooks/stage-{stage}-handbook.pdf"
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(f, arc)


def build_certs(zf, args, stats):
    """Section 13: Completion certificates."""
    if args.no_certs:
        stats["skipped"].append("13-Certificates/")
        return
    handbook = BUILD / "handbook"
    if not handbook.exists():
        return
    for stage in _stages(args):
        f = handbook / f"certificate-stage-{stage}.pdf"
        if not f.exists():
            continue
        arc = f"13-Certificates/certificate-stage-{stage}.pdf"
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(f, arc)


def build_lesson_packs(zf, args, stats):
    """Section 6: Per-lesson PDFs from packs/stage-N/*.pdf."""
    if args.no_lessons:
        stats["skipped"].append("06-Lesson-Packs/")
        return
    packs = ROOT / "packs"
    if not packs.exists():
        return
    for stage in _stages(args):
        stage_dir = packs / f"stage-{stage}"
        if not stage_dir.exists():
            continue
        count = 0
        for pdf in sorted(stage_dir.glob("*.pdf")):
            arc = f"06-Lesson-Packs/stage-{stage}/{pdf.name}"
            if args.list:
                stats["included"].append(arc)
            else:
                zf.write(pdf, arc)
            count += 1
        if count and not args.list:
            print(f"  OK  06-Lesson-Packs/stage-{stage}/  ({count} lesson packs)")


def build_worksheets(zf, args, stats):
    """Section 7: Worksheets from build/worksheets/<sub>/."""
    if args.no_worksheets:
        stats["skipped"].append("07-Worksheets/")
        return
    for sub in ["phonograms", "rules", "cards", "blank"]:
        sub_dir = BUILD / "worksheets" / sub
        if not sub_dir.exists():
            continue
        if args.list:
            stats["included"].append(f"07-Worksheets/{sub}/")
        else:
            count = add_directory(zf, sub_dir, f"07-Worksheets/{sub}",
                                 stage_filter=args.stage)
            if count:
                print(f"  OK  07-Worksheets/{sub}/  ({count} files)")
    # Per-stage merged worksheets PDF
    for stage in _stages(args):
        f = BUILD / f"stage-{stage}-worksheets.pdf"
        if not f.exists():
            continue
        arc = f"07-Worksheets/stage-{stage}-worksheets.pdf"
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(f, arc)


def build_readers(zf, args, stats):
    """Section 8: Decodable readers from build/readers/."""
    if args.no_readers:
        stats["skipped"].append("08-Decodable-Readers/")
        return
    readers_dir = BUILD / "readers"
    if readers_dir.exists():
        if args.list:
            stats["included"].append("08-Decodable-Readers/")
        else:
            count = add_directory(zf, readers_dir, "08-Decodable-Readers",
                                 stage_filter=args.stage)
            if count:
                print(f"  OK  08-Decodable-Readers/  ({count} reader PDFs)")
    # Per-stage merged readers PDF
    for stage in _stages(args):
        f = BUILD / f"stage-{stage}-readers.pdf"
        if not f.exists():
            continue
        arc = f"08-Decodable-Readers/stage-{stage}-readers.pdf"
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(f, arc)


def build_stage_overview(zf, args, stats):
    """Section 6b: Per-stage combined PDF (stage-N.pdf)."""
    for stage in _stages(args):
        f = BUILD / f"stage-{stage}.pdf"
        if not f.exists():
            continue
        arc = f"06-Stage-Overview/stage-{stage}.pdf"
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(f, arc)


def build_quick_checks(zf, args, stats):
    """Section 9: Quick checks from build/quick-checks/."""
    if args.no_quick_checks:
        stats["skipped"].append("09-Quick-Checks/")
        return
    qc_dir = BUILD / "quick-checks"
    if qc_dir.exists():
        if args.list:
            stats["included"].append("09-Quick-Checks/")
        else:
            count = add_directory(zf, qc_dir, "09-Quick-Checks")
            if count:
                print(f"  OK  09-Quick-Checks/  ({count} files)")


def build_assessments(zf, args, stats):
    """Section 10: Assessment PDFs from build/assessments/."""
    if args.no_assessments:
        stats["skipped"].append("10-Assessments/")
        return
    assessments_dir = BUILD / "assessments"
    if assessments_dir.exists():
        if args.list:
            stats["included"].append("10-Assessments/")
        else:
            count = add_directory(zf, assessments_dir, "10-Assessments")
            if count:
                print(f"  OK  10-Assessments/  ({count} files)")


def build_reference(zf, args, stats):
    """Section 4: Reference HTMLs (browser-printable classroom aids)."""
    if args.no_reference:
        stats["skipped"].append("04-Quick-Reference/ HTMLs")
        return
    ref_dir = ROOT / "reference"
    if not ref_dir.exists():
        return
    for html in sorted(ref_dir.glob("*.html")):
        if html.name.startswith("quick-check-stage-"):
            continue
        arc = f"04-Quick-Reference/{html.name}"
        if args.list:
            stats["included"].append(arc)
        else:
            zf.write(html, arc)


def build_game(zf, args, stats):
    """Section 11: Web game HTML + audio MP3s."""
    if args.no_game:
        stats["skipped"].append("11-Game/")
        return
    game_html = ROOT / "games" / "phonogram-trainer.html"
    if game_html.exists():
        if args.list:
            stats["included"].append("11-Game/phonogram-trainer.html")
        else:
            zf.write(game_html, "11-Game/phonogram-trainer.html")
            print("  OK  11-Game/phonogram-trainer.html")
    if args.no_audio:
        return
    audio_dir = ROOT / "games" / "audio"
    if audio_dir.exists():
        if args.list:
            stats["included"].append("12-Audio/")
        else:
            count = add_directory(zf, audio_dir, "12-Audio")
            if count:
                print(f"  OK  12-Audio/  ({count} MP3s)")


# ── CLI ────────────────────────────────────────────────────────────────

def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build release.zip — partial or full curriculum bundle.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  build-release.py                          # full release (default)
  build-release.py --output my.zip          # custom output path
  build-release.py --stage 3                # only Stage 3 assets
  build-release.py --no-game --no-audio     # skip game + audio
  build-release.py --no-lessons             # skip 06-Lesson-Packs/
  build-release.py --list                   # dry-run, list contents""")
    p.add_argument("--output", "-o", type=Path,
                   help="Output ZIP path (default: release.zip in project root)")
    p.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], metavar="N",
                   help="Restrict per-stage assets to one stage (1-5). "
                        "Affects lesson packs, worksheets, readers, handbooks, certificates.")
    p.add_argument("--list", action="store_true",
                   help="Dry-run: print what would be included, do not write the ZIP")

    # Section exclusion flags
    p.add_argument("--no-readme", action="store_true", help="Skip README.md")
    p.add_argument("--no-nav", action="store_true",
                   help="Skip 00/01/02 handbook PDFs + landing page")
    p.add_argument("--no-handbooks", action="store_true",
                   help="Skip 05-Teacher-Handbooks/ stage handbooks")
    p.add_argument("--no-lessons", action="store_true", help="Skip 06-Lesson-Packs/")
    p.add_argument("--no-worksheets", action="store_true", help="Skip 07-Worksheets/")
    p.add_argument("--no-readers", action="store_true", help="Skip 08-Decodable-Readers/")
    p.add_argument("--no-quick-checks", action="store_true", help="Skip 09-Quick-Checks/")
    p.add_argument("--no-assessments", action="store_true", help="Skip 10-Assessments/")
    p.add_argument("--no-game", action="store_true", help="Skip 11-Game/ phonogram trainer")
    p.add_argument("--no-audio", action="store_true", help="Skip 12-Audio/ MP3s (keeps game HTML)")
    p.add_argument("--no-certs", action="store_true", help="Skip 13-Certificates/")
    p.add_argument("--no-reference", action="store_true", help="Skip 04-Quick-Reference/ HTMLs")
    return p


def main():
    args = build_argparser().parse_args()

    out = args.output if args.output else (ROOT / "release.zip")
    stats = {"included": [], "skipped": []}

    if args.list:
        # Dry-run: just enumerate what would be included
        # Use a dummy in-memory ZIP so the section builders can be called
        # uniformly without touching disk.
        with zipfile.ZipFile(out, "w") if False else _NullZip() as zf:
            _run_sections(zf, args, stats)
        print(f"==> {out.name} (DRY RUN — not written)")
        print()
        print(f"Would include {len(stats['included'])} entries:")
        for entry in stats["included"]:
            print(f"  + {entry}")
        print()
        if stats["skipped"]:
            print(f"Skipped {len(stats['skipped'])} sections:")
            for entry in stats["skipped"]:
                print(f"  - {entry}")
        return

    print(f"==> Building {out.name}")
    print()

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        _run_sections(zf, args, stats)

    size_mb = os.path.getsize(out) / (1024 * 1024)
    with zipfile.ZipFile(out, "r") as zf:
        n_files = len(zf.namelist())
    print()
    print(f"Done: {out.name} — {size_mb:.1f} MB, {n_files} files")
    if stats["skipped"]:
        print(f"Skipped {len(stats['skipped'])} sections: {', '.join(stats['skipped'])}")


def _run_sections(zf, args, stats):
    """Call every section builder in order."""
    build_readme(zf, args, stats)
    build_handbook_nav(zf, args, stats)
    build_landing_html(zf, args, stats)
    build_handbooks(zf, args, stats)
    build_lesson_packs(zf, args, stats)
    build_stage_overview(zf, args, stats)
    build_worksheets(zf, args, stats)
    build_readers(zf, args, stats)
    build_quick_checks(zf, args, stats)
    build_assessments(zf, args, stats)
    build_reference(zf, args, stats)
    build_game(zf, args, stats)
    build_certs(zf, args, stats)


class _NullZip:
    """No-op ZipFile substitute for --list dry-runs."""

    def __enter__(self): return self
    def __exit__(self, *a): pass
    def write(self, src, arcname): pass
    def writestr(self, name, data): pass


if __name__ == "__main__":
    main()