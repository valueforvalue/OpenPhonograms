# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Build release.zip — complete curriculum in Model C layout.

Default behavior bundles everything into a single ZIP. Pass CLI flags to
include or exclude specific sections, restrict to one stage, or change the
output path. Dry-run with --list to see what would be included.

Model C ZIP shape (this script's default):
  05-Teacher-Handbooks/  — 5 bound-book-style stage handbooks (TM)
  06-Lesson-Packs/       — 5 merged PDFs (one per stage) + singles/ subfolder
                            (cover + lesson + worksheet + flash cards per pack)
  [06-Stage-Overview/    — OPTIONAL: per-stage merged workbook PDFs]
  [07-Worksheets/        — OPTIONAL: standalone practice sheets]
  + readers, quick-checks, game, audio, certificates, reference, etc.

Worksheet content lives INSIDE lesson packs by default (Model C). Use
--with-worksheets / --with-stage-overview for the LOE-style bound
workbook + standalone extras.

Produces a top-level ZIP with:

  README.md                        — text overview of what's in the release
  00-Start-Here.pdf                — orientation for new users
  01-Index-and-Table-of-Contents.pdf — master TOC with hyperlinks
  02-Scope-and-Sequence.pdf        — full curriculum map
  04-Quick-Reference/              — phonograms, rules, spelling analysis
  05-Teacher-Handbooks/            — 5 bound-book-style stage handbooks
  06-Lesson-Packs/                 — 5 merged PDFs + per-lesson singles in singles/
                                       — Model C: includes worksheets + flash cards
  07-Worksheets/                   — 178 standalone practice sheets (opt-in via --with-worksheets)
  08-Decodable-Readers/            — 25 readers + index
  09-Quick-Checks/                 — placement + 5 stage quick-checks
  11-Game/                         — phonogram trainer (web game) + bundled audio MP3s
  13-Certificates/                 — 5 printable completion certificates

All paths inside the ZIP use forward slashes (POSIX) for cross-platform use.

Usage:
  python scripts/build-release.py                          # Model C (default)
  python scripts/build-release.py --output custom.zip      # custom output path
  python scripts/build-release.py --stage 3                # only Stage 3 assets
  python scripts/build-release.py --no-game --no-audio     # skip game + audio
  python scripts/build-release.py --no-lessons             # skip 06-Lesson-Packs/
  python scripts/build-release.py --with-worksheets        # include standalone worksheets
  python scripts/build-release.py --with-stage-overview    # include per-stage workbook PDFs
  python scripts/build-release.py --list                   # dry-run, list contents
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
# Allow `from version import get_version` inside framework/stamp.py
sys.path.insert(0, str(ROOT / "framework"))
sys.path.insert(0, str(ROOT))  # for framework.pdf_merge imports

# Source-of-truth list of reference HTML basenames that get rendered to PDF
# and shipped under 04-Quick-Reference/ in the release ZIP.
# Derived from reference/*.html at import time; excludes quick-checks
# (which go to 09-Quick-Checks/) and the 04-Quick-Reference-{Phonograms,Spelling-Analysis,Spelling-Rules}
# entries which are generated separately by build-quick-references.py.
def _load_reference_basenames() -> set[str]:
    ref_dir = ROOT / "reference"
    if not ref_dir.exists():
        return set()
    out = set()
    for html in ref_dir.glob("*.html"):
        if html.name.startswith("quick-check-stage-"):
            continue
        # Feedback.html is shipped at ZIP root only (issue #25); no PDF variant
        if html.name == "Feedback.html":
            continue
        out.add(html.name.removesuffix(".html"))
    return out


REFERENCE_PDF_BASENAMES = _load_reference_basenames()


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


def build_feedback_html(zf, args, stats):
    """Section 0b: Feedback.html at ZIP root (issue #25).

    Hand-authored HTML form that POSTs to Formspark. Lives at the ZIP
    root so a teacher can double-click it from the extracted folder.
    """
    if args.no_readme:
        # Treat Feedback.html as part of the README/root bundle — skip
        # together so a `--no-readme` build is still self-contained.
        stats["skipped"].append("Feedback.html")
        return
    feedback = ROOT / "reference" / "Feedback.html"
    arc = "Feedback.html"
    if args.list:
        stats["included"].append(arc)
        return
    if not add_file(zf, feedback, arc):
        stats["skipped"].append("Feedback.html (missing source)")
        return
    print(f"  OK  {arc}")


def build_readme(zf, args, stats):
    """Section 0: README.md."""
    if args.no_readme:
        stats["skipped"].append("README.md")
        return
    if args.list:
        stats["included"].append("README.md")
        return
    readme_text = """OpenPhonograms — Release ZIP

This ZIP contains the complete OpenPhonograms curriculum (244 lessons, 5 stages,
75 phonograms, 31 spelling rules, 25 decodable readers) plus all printable
aids and the phonogram trainer web game (which bundles its own audio MP3s).

QUICK START
-----------
1. Open 00-Start-Here.pdf — orientation for new users.
2. Open 01-Index-and-Table-of-Contents.pdf — master TOC with clickable links.
3. Print 09-Quick-Checks/placement-test.pdf and run it to find your starting stage.
4. Open 06-Lesson-Packs/stage-1-all-lessons.pdf and start teaching.

WHAT'S IN THIS RELEASE
----------------------
00-Start-Here.pdf                      — orientation
01-Index-and-Table-of-Contents.pdf     — master clickable TOC
02-Scope-and-Sequence.pdf              — full curriculum map
04-Quick-Reference/                    — phonograms, rules, spelling analysis,
                                          diacritical legend, glossary (HTMLs + PDFs)
Feedback.html                         — submit feedback (opens in browser, needs internet)
   04-Quick-Reference-Print-PDFs/       — 3 generated summary PDFs for printing
   04-Quick-Reference-Browser-PDFs/     — printable PDF companions of the reference HTMLs
05-Teacher-Handbooks/                  — 5 bound-book-style stage handbooks (PDFs)
06-Lesson-Packs/                       — 5 merged per-stage PDFs + singles/ subfolder
                                          (each with cover, lesson, worksheets, cards)
                                          Open stage-N-all-lessons.pdf to start.
06-Stage-Overview/stage-N.pdf          — OPTIONAL: merged per-stage workbook (--with-stage-overview)
07-Worksheets/                         — OPTIONAL: standalone practice sheets
                                          (organized by stage + category; --with-worksheets)
08-Decodable-Readers/                  — 25 decodable story PDFs + index
09-Quick-Checks/                       — placement test + 5 stage quick-checks

(Stage mastery assessments are included in 06-Lesson-Packs/singles/<stage>/lesson-NN-assessment-N.pdf
 and inside 06-Stage-Overview/stage-N.pdf; no separate 10-Assessments/ section needed.)

METHODOLOGY
-----------
Speech-to-print. Spelling drives reading. 75 phonograms + 31 spelling rules
cover 98% of English words. No sight words. The 5-step Spelling Analysis
routine is used in every lesson.

Source methodology: Open-source. MIT licensed. Phonograms drawn from the
public-domain phonics tradition (1800s onward).

LICENSE
-------
This is an open-source adaptation released for educational use. The
methodology and phonogram list are not copyrighted (drawn from public-domain
phonics tradition). The lesson content, generators, and design are released
under MIT license.

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
            # Issue #27: generated summary PDFs go in the Print-PDFs subfolder
            arc = f"04-Quick-Reference/04-Quick-Reference-Print-PDFs/{name}"
        elif "handbook" in name and name.startswith("stage-"):
            # Stage handbooks are added by build_handbooks() — skip here
            # to avoid duplicate-name warnings in the ZIP.
            continue
        elif name.startswith("certificate-"):
            # Certificates are added by build_certs() — skip here to avoid
            # duplicate-name warnings in the ZIP.
            continue
        elif "readers-index" in name:
            if args.no_readers:
                continue
            arc = f"08-Decodable-Readers/{name}"
        # Issue #12: include all rendered reference HTMLs as PDFs in 04-Quick-Reference/.
        # Matches the source-of-truth list in reference/*.html (excluding quick-checks,
        # which go to 09-Quick-Checks/).
        elif name.removesuffix(".pdf") in REFERENCE_PDF_BASENAMES:
            if args.no_reference:
                continue
            # Issue #27: per-HTML PDF companions live in the Browser-PDFs
            # subfolder. (Source HTMLs are no longer shipped in the release —
            # the rendered PDFs are the deliverable.)
            arc = f"04-Quick-Reference/04-Quick-Reference-Browser-PDFs/{name}"
        # Issue #12 (option a): route quick-check PDFs through 09-Quick-Checks/.
        # Quick-check PDFs are also added separately by build_quick_checks()
        # from build/quick-checks/. Skip here to avoid duplicate entries in
        # the release ZIP (Python's zipfile warns on duplicate names).
        elif name.startswith("quick-check-stage-"):
            continue
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
    """Section 6: Merged per-stage PDF at top level, singles in singles/."""
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
        merged_name = f"stage-{stage}-all-lessons.pdf"
        singles_count = 0
        for pdf in sorted(stage_dir.glob("*.pdf")):
            if pdf.name == merged_name:
                arc = f"06-Lesson-Packs/{pdf.name}"
                if args.list:
                    stats["included"].append(arc)
                else:
                    zf.write(pdf, arc)
            else:
                arc = f"06-Lesson-Packs/singles/stage-{stage}/{pdf.name}"
                if args.list:
                    stats["included"].append(arc)
                else:
                    zf.write(pdf, arc)
                singles_count += 1
        if not args.list:
            print(f"  OK  06-Lesson-Packs/stage-{stage}-all-lessons.pdf + {singles_count} singles")


def build_worksheets(zf, args, stats):
    """Section 7: Worksheets from build/worksheets/<sub>/.

    Model C default: skip. Worksheet content lives inside lesson packs
    (06-Lesson-Packs/) so teachers have it where they need it. Opt in
    via --with-worksheets if you want standalone extra practice sheets.
    """
    if args.no_worksheets or not args.with_worksheets:
        if args.no_worksheets:
            stats["skipped"].append("07-Worksheets/ (--no-worksheets)")
        else:
            stats["skipped"].append("07-Worksheets/ (Model C: in packs)")
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
    """Section 8: Decodable readers from build/readers/.

    Layout: 08-Decodable-Readers/stage-N/{slug}.pdf
    Stage-1 readers are stored flat at build/readers/*.pdf and copied
    to 08-Decodable-Readers/stage-1/. Stage 2-5 readers are in
    build/readers/stage-N/ subfolders.
    """
    if args.no_readers:
        stats["skipped"].append("08-Decodable-Readers/")
        return
    readers_dir = BUILD / "readers"
    if not readers_dir.exists():
        return

    for stage in _stages(args):
        if stage == 1:
            # Stage-1 readers live in build/readers/stage-1/ subfolder
            # (rendered there by render-extras.py). Copy from there.
            stage_dir = readers_dir / "stage-1"
            count = 0
            if stage_dir.exists():
                for f in sorted(stage_dir.glob("*.pdf")):
                    arc = f"08-Decodable-Readers/stage-1/{f.name}"
                    if args.list:
                        stats["included"].append(arc)
                    else:
                        zf.write(f, arc)
                    count += 1
            if count and not args.list:
                print(f"  OK  08-Decodable-Readers/stage-1/  ({count} readers)")
            continue
        # Stages 2-5: subfolder layout
        stage_dir = readers_dir / f"stage-{stage}"
        if not stage_dir.exists():
            continue
        count = 0
        for f in sorted(stage_dir.glob("*.pdf")):
            arc = f"08-Decodable-Readers/stage-{stage}/{f.name}"
            if args.list:
                stats["included"].append(arc)
            else:
                zf.write(f, arc)
            count += 1
        if count and not args.list:
            print(f"  OK  08-Decodable-Readers/stage-{stage}/  ({count} readers)")

    # readers-index.pdf lives at build/readers/, not in any stage subdir.
    # Include it at the root of 08-Decodable-Readers/.
    index = readers_dir / "readers-index.pdf"
    if index.exists():
        if args.list:
            stats["included"].append("08-Decodable-Readers/readers-index.pdf")
        else:
            zf.write(index, "08-Decodable-Readers/readers-index.pdf")
            print("  OK  08-Decodable-Readers/readers-index.pdf")


def build_stage_overview(zf, args, stats):
    """Section 6b: Per-stage combined PDF (stage-N.pdf).

    Model C default: skip. Stage-overview content (phonogram + rule +
    flash card worksheets) lives inside lesson packs (06-Lesson-Packs/).
    Opt in via --with-stage-overview for the LOE-style bound workbook.
    """
    if not args.with_stage_overview:
        stats["skipped"].append("06-Stage-Overview/ (Model C: in packs)")
        return
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
    """Section 10: REMOVED per issue #7. Assessment PDFs are already in:
    - 06-Lesson-Packs/<stage>/lesson-NN-assessment-N.pdf
    - 06-Stage-Overview/stage-N.pdf
    This function is kept as a no-op for backward compatibility with --no-assessments arg.
    """
    if args.no_assessments:
        stats["skipped"].append("10-Assessments/ (no-op, see #7)")
        return
    return  # no-op


def build_reference(zf, args, stats):
    """Section 4: Reference PDFs (printable browser-rendered classroom aids).

    Source HTMLs under reference/ are NOT shipped in the release. The PDFs
    rendered from them by scripts/render-references.py are the deliverable,
    and live in 04-Quick-Reference-Browser-PDFs/. Feedback.html still ships
    at ZIP root via build_feedback_html() (issue #25).
    """
    # No-op: PDF companions are added by build_handbook_nav() from
    # build/handbook/. This function is kept for arg/back-compat symmetry.
    if args.no_reference:
        stats["skipped"].append("04-Quick-Reference/ PDFs")
    return


def build_game(zf, args, stats):
    """Section 11: Web game HTML + audio MP3s (audio is a game asset).

    Audio lives under games/audio/ in source and ships under
    11-Game/audio/ in the release so the web game is self-contained.
    --no-audio is kept as a deprecated alias for --no-game.
    """
    if args.no_game or args.no_audio:
        stats["skipped"].append("11-Game/ (game + audio)")
        return
    game_html = ROOT / "games" / "phonogram-trainer.html"
    if game_html.exists():
        if args.list:
            stats["included"].append("11-Game/phonogram-trainer.html")
        else:
            zf.write(game_html, "11-Game/phonogram-trainer.html")
            print("  OK  11-Game/phonogram-trainer.html")
    audio_dir = ROOT / "games" / "audio"
    if audio_dir.exists():
        if args.list:
            stats["included"].append("11-Game/audio/")
        else:
            count = add_directory(zf, audio_dir, "11-Game/audio")
            if count:
                print(f"  OK  11-Game/audio/  ({count} MP3s)")


# ── CLI ────────────────────────────────────────────────────────────────

def _relativize_build_pdfs() -> None:
    """Post-process release ZIP: rewrite file:// links to relative paths."""
    import zipfile, tempfile
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import TextStringObject, NameObject
    from pathlib import Path as _Path

    release_zip = ROOT / 'release.zip'
    if not release_zip.exists():
        return

    with tempfile.TemporaryDirectory() as tmp:
        # Extract
        with zipfile.ZipFile(str(release_zip)) as z:
            z.extractall(tmp)
            pdfs = [n for n in z.namelist() if n.endswith('.pdf')]

        # Build filename → release-path lookup (PDFs + HTML)
        name_to_path: dict[str, str] = {}
        for p in pdfs:
            name = p.split('/')[-1]
            if name not in name_to_path:
                name_to_path[name] = p
        # Also index HTML files
        with zipfile.ZipFile(str(release_zip)) as z:
            for p in z.namelist():
                if p.endswith('.html'):
                    name = p.split('/')[-1]
                    if name not in name_to_path:
                        name_to_path[name] = p

        total_links = 0
        pdf_count = 0
        for rel_path in pdfs:
            extracted = _Path(tmp) / rel_path
            if not extracted.exists():
                continue
            reader = PdfReader(str(extracted))
            release_dir = _Path(rel_path).parent if '/' in rel_path else _Path('.')
            rewritten = 0
            for page in reader.pages:
                if '/Annots' not in page:
                    continue
                for annot in page['/Annots']:
                    obj = annot.get_object()
                    uri_obj = obj.get('/A', {}).get('/URI')
                    if uri_obj is None:
                        continue
                    uri = str(uri_obj)
                    if not uri.startswith('file:///'):
                        continue
                    target_name = uri.split('/')[-1]
                    target_release = name_to_path.get(target_name)
                    if target_release is None or target_release == rel_path:
                        continue
                    # Compute relative from source dir to target
                    try:
                        rel = _Path(target_release).relative_to(release_dir, walk_up=True)
                    except ValueError:
                        rel = _Path(target_release)
                    obj['/A'][NameObject('/URI')] = TextStringObject(rel.as_posix())
                    rewritten += 1
            if rewritten > 0:
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                with open(extracted, 'wb') as f:
                    writer.write(f)
                total_links += rewritten
                pdf_count += 1

        if total_links:
            print(f"  Relativized {total_links} links in {pdf_count} PDFs")
            # Repack
            new_zip = release_zip.with_suffix('.tmp.zip')
            with zipfile.ZipFile(str(new_zip), 'w', zipfile.ZIP_DEFLATED) as zout:
                for f in sorted(_Path(tmp).rglob('*')):
                    if f.is_file():
                        arc = str(f.relative_to(tmp)).replace('\\', '/')
                        zout.write(str(f), arc)
            new_zip.replace(release_zip)


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
    p.add_argument("--no-worksheets", action="store_true", help="Skip 07-Worksheets/ (Model C default)")
    p.add_argument("--with-worksheets", action="store_true",
                   help="Include 07-Worksheets/ (standalone practice sheets; Model C opts out by default)")
    p.add_argument("--with-stage-overview", action="store_true",
                   help="Include 06-Stage-Overview/ (bound workbook PDFs; Model C opts out by default)")
    p.add_argument("--no-readers", action="store_true", help="Skip 08-Decodable-Readers/")
    p.add_argument("--no-quick-checks", action="store_true", help="Skip 09-Quick-Checks/")
    p.add_argument("--no-assessments", action="store_true", help="Skip 10-Assessments/")
    p.add_argument("--no-game", action="store_true", help="Skip 11-Game/ phonogram trainer")
    p.add_argument("--no-audio", action="store_true", help="Skip 11-Game/audio/ MP3s (deprecated alias for --no-game; audio is now a game asset)")
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

    # Now relativize file:// links using the release ZIP's layout.
    _relativize_build_pdfs()

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
    build_feedback_html(zf, args, stats)
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