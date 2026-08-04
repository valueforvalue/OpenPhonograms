"""Build release.zip — complete curriculum in LOE-style folder structure.

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
  python scripts/build-release.py
"""

import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
RELEASE = ROOT / "release"


def add_file(zf: zipfile.ZipFile, src: Path, arcname: str):
    """Add a file to the ZIP with the given arcname (forward slashes)."""
    if src.exists():
        zf.write(src, arcname.replace("\\", "/"))


def add_directory(zf: zipfile.ZipFile, src_dir: Path, arc_prefix: str):
    """Add all files from a directory recursively."""
    if not src_dir.exists():
        return 0
    count = 0
    for f in sorted(src_dir.rglob("*")):
        if f.is_file():
            rel = f.relative_to(src_dir).as_posix()
            zf.write(f, f"{arc_prefix}/{rel}".replace("\\", "/"))
            count += 1
    return count


def main():
    out = ROOT / "release.zip"
    print(f"==> Building {out.name}")
    print()

    # Stage ZIP creation: write to a tmp dir for ordering
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:

        # 0. README.md (text)
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
04-Quick-Reference/                    — phonograms, rules, spelling analysis
05-Teacher-Handbooks/                  — 5 bound-book-style stage handbooks (PDFs)
06-Lesson-Packs/                       — 248 per-lesson bundles
07-Worksheets/                         — 178 standalone practice sheets
08-Decodable-Readers/                  — 25 decodable story PDFs + index
09-Quick-Checks/                       — placement test + 5 stage quick-checks
10-Assessments/                        — 8 stage mastery assessments
11-Game/phonogram-trainer.html         — web game (5 modes)
12-Audio/                              — 74 phonogram MP3s
13-Certificates/                       — 5 printable completion certificates

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
        print("  OK  README.md")

        # 1. Top-level navigation PDFs (from build/handbook/)
        handbook = BUILD / "handbook"
        for f in sorted(handbook.glob("*.pdf")):
            name = f.name
            # 00-Start-Here, 01-Index, 02-Scope at top level
            if name.startswith(("00-", "01-", "02-")):
                zf.write(f, name)
                print(f"  OK  {name}")
            # 04-Quick-Reference-* → 04-Quick-Reference/
            elif name.startswith("04-"):
                zf.write(f, f"04-Quick-Reference/{name}")
                print(f"  OK  04-Quick-Reference/{name}")
            # stage-N-handbook → 05-Teacher-Handbooks/
            elif "handbook" in name and name.startswith("stage-"):
                zf.write(f, f"05-Teacher-Handbooks/{name}")
                print(f"  OK  05-Teacher-Handbooks/{name}")
            # certificate-stage-N → 13-Certificates/
            elif name.startswith("certificate-"):
                zf.write(f, f"13-Certificates/{name}")
                print(f"  OK  13-Certificates/{name}")
            # readers-index → 08-Decodable-Readers/
            elif "readers-index" in name:
                zf.write(f, f"08-Decodable-Readers/{name}")
                print(f"  OK  08-Decodable-Readers/{name}")

        # 2. Lesson packs grouped by stage (packs/stage-N/*.pdf)
        packs = ROOT / "packs"
        if packs.exists():
            for stage in range(1, 6):
                stage_dir = packs / f"stage-{stage}"
                if not stage_dir.exists():
                    continue
                count = 0
                for pdf in sorted(stage_dir.glob("*.pdf")):
                    zf.write(pdf, f"06-Lesson-Packs/stage-{stage}/{pdf.name}")
                    count += 1
                print(f"  OK  06-Lesson-Packs/stage-{stage}/  ({count} lesson packs)")

        # 3. Worksheets
        for sub in ["phonograms", "rules", "cards", "blank"]:
            sub_dir = BUILD / "worksheets" / sub
            if sub_dir.exists():
                count = add_directory(zf, sub_dir, f"07-Worksheets/{sub}")
                print(f"  OK  07-Worksheets/{sub}/  ({count} files)")

        # 4. Readers (PDFs from build/readers/)
        readers_dir = BUILD / "readers"
        if readers_dir.exists():
            count = add_directory(zf, readers_dir, "08-Decodable-Readers")
            print(f"  OK  08-Decodable-Readers/  ({count} reader PDFs)")

        # 5. Quick-checks (from build/quick-checks/)
        qc_dir = BUILD / "quick-checks"
        if qc_dir.exists():
            count = add_directory(zf, qc_dir, "09-Quick-Checks")
            print(f"  OK  09-Quick-Checks/  ({count} files)")

        # 6. Assessments (the lesson-type PDFs that are assessment)
        #    These live in build/stage-N/assessment-N.pdf — already copied above.
        #    Create a stage-organized index here too? For now, point to lesson packs.
        #    Future: copy assessment PDFs to 10-Assessments/ as standalone files.
        assessments_dir = BUILD / "assessments"
        if assessments_dir.exists():
            count = add_directory(zf, assessments_dir, "10-Assessments")
            print(f"  OK  10-Assessments/  ({count} files)")

        # 7. Game (HTML + audio)
        game_html = ROOT / "games" / "phonogram-trainer.html"
        if game_html.exists():
            zf.write(game_html, "11-Game/phonogram-trainer.html")
            print(f"  OK  11-Game/phonogram-trainer.html")
        audio_dir = ROOT / "games" / "audio"
        if audio_dir.exists():
            count = add_directory(zf, audio_dir, "12-Audio")
            print(f"  OK  12-Audio/  ({count} MP3s)")

    size_mb = os.path.getsize(out) / (1024 * 1024)
    with zipfile.ZipFile(out, "r") as zf:
        n_files = len(zf.namelist())
    print()
    print(f"Done: {out.name} — {size_mb:.1f} MB, {n_files} files")


if __name__ == "__main__":
    main()
