# Build Guide — Uncovering the Logic of English

For developers, contributors, and anyone building the curriculum from source.

**If you just want to use the curriculum** (print PDFs, teach lessons), see [docs/USE.md](USE.md) instead.

---

## Table of Contents

1. [What This Project Is](#what-this-project-is)
2. [Architecture in 60 Seconds](#architecture-in-60-seconds)
3. [Requirements](#requirements)
4. [First-Time Setup](#first-time-setup)
5. [Build with Just (Recommended)](#build-with-just-recommended)
6. [Build Without Just (Manual)](#build-without-just-manual)
7. [Output Layout](#output-layout)
8. [Release Packaging](#release-packaging)
9. [Troubleshooting](#troubleshooting)
10. [Development Workflow](#development-workflow)
11. [Project Layout](#project-layout)

---

## What This Project Is

A print-first reading curriculum (248 lessons, Pre-K → Gr 3+) generated from data:

- **75 phonograms** (26 single-letter + 49 multi-letter)
- **31 spelling rules** (numbered, with sub-rules)
- **32 decodable readers** (controlled vocabulary)
- **248 lesson PDFs + 178 worksheet PDFs + 25 reader PDFs + 9 reference HTMLs**
- **8 stage assessments**, **1 phonogram trainer web game**, **74 audio MP3s**

Every printed artifact is generated from a Markdown source by Python scripts. The Markdown is human-readable and version-controlled. The generators are deterministic — re-runs produce identical output.

Source: [Uncovering the Logic of English](https://logicofenglish.com/) by Denise Eide.

## Architecture in 60 Seconds

```
framework/lesson-catalog.csv       ← Source of truth (248 rows)
        ↓
scripts/generate-*.py             ← Python generators (data → MD)
        ↓
lessons/stage-X/*.md               ← Generated Markdown
worksheets/**/*.md
readers/*.md
        ↓
framework/render.py               ← MD → HTML → PDF (weasyprint)
        ↓
build/stage-X/*.pdf                ← Rendered PDFs
packs/stage-X/*.pdf                ← Per-lesson bundles (cover + lesson + worksheet + cards)
        ↓
scripts/build-release.py          ← ZIP everything
        ↓
release.zip                        ← Distributable
```

Three pillars:
1. **Catalog CSV** = what to teach (lesson_id, type, new phonogram, new rule, etc.)
2. **Generator scripts** = how to teach it (turn catalog row into Markdown)
3. **Render pipeline** = print it (Markdown → styled HTML → PDF)

**Do not hand-edit generated Markdown.** Edit the catalog or generator. Next run will overwrite.

## Requirements

### Required (build + render)

| Tool | Min Version | Why |
|------|-------------|-----|
| **Python** | 3.10+ | Runs all generators + render |
| **markdown** (pip) | 3.5+ | MD → HTML conversion |
| **weasyprint** (pip) | 60+ | HTML → PDF conversion |
| **pypdf** (pip) | 5+ | PDF utilities (already installed for some scripts) |

### Optional (full pipeline)

| Tool | Min Version | Why |
|------|-------------|-----|
| **Just** (winget) | 1.50+ | Command runner — wraps every script |
| **MSYS2** (Windows) | latest | GTK3 runtime for weasyprint |
| **edge-tts** (pip) | latest | Neural TTS for phonogram audio |
| **PowerShell** (Windows) | 5+ | SAPI audio fallback |

### System Dependencies (Windows)

WeasyPrint on Windows requires GTK3 runtime DLLs (Pango, Cairo, GObject, etc.).

**Install MSYS2 once:**
```bash
winget install MSYS2.MSYS2 --silent
"C:/msys64/usr/bin/pacman.exe" -S --noconfirm mingw-w64-x86_64-pango
```

This installs ~150 MB of DLLs at `C:/msys64/mingw64/bin/`. The build scripts auto-detect this path.

**Linux:** GTK3 is usually present. If not: `apt install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`.

**macOS:** `brew install weasyprint` handles everything.

## First-Time Setup

### Option A: With Just (recommended)

```bash
# 1. Install Just (one-time)
winget install Casey.Just                      # Windows
brew install just                              # macOS
# Linux: see https://github.com/casey/just/releases

# 2. Clone
git clone https://github.com/YOUR-USER/UncoveringtheLogic.git
cd UncoveringtheLogic

# 3. Install Python deps
pip install markdown weasyprint pypdf edge-tts

# 4. (Windows only) Install GTK3 runtime
winget install MSYS2.MSYS2 --silent
"C:/msys64/usr/bin/pacman.exe" -S --noconfirm mingw-w64-x86_64-pango

# 5. Verify environment
just doctor

# 6. Full build
just all
```

### Option B: Without Just (manual)

```bash
git clone https://github.com/YOUR-USER/UncoveringtheLogic.git
cd UncoveringtheLogic
pip install markdown weasyprint pypdf edge-tts
# (Windows only) Install GTK3 runtime via MSYS2 (see above)

# Generate every Markdown source
python scripts/generate-worksheets.py
python scripts/generate-stage1.py
python scripts/generate-stage2.py
python scripts/generate-stage3.py
python scripts/generate-stage4.py
python scripts/generate-stage5.py
python scripts/generate-readers.py
python scripts/generate-animal-readers.py

# Render to PDF
python framework/render.py --all
python framework/render.py --curriculum

# Build cohesive per-lesson packs (cover + lesson + worksheet + cards)
python scripts/build-lesson-pack.py --all

# Build release ZIP
python scripts/build-release.py
```

## Build with Just (Recommended)

The `justfile` at repo root wraps every script. Run `just` with no args to list 25 recipes.

### Most Common Recipes

```bash
just doctor              # Verify environment (Python deps, GTK3, scripts)
just build               # Full pipeline without release ZIP (~80s)
just all                 # Full pipeline + release ZIP (~85s)
just render-lessons      # Render all 248 lesson PDFs
just render-stage 3      # Render just Stage 3 lessons
just pack-all            # Build all 248 lesson packs
just pack-stage 3        # Build Stage 3 packs only
just pack-lesson pg-d    # Build one pack (great for testing)
just gen-all             # Regenerate all Markdown from data
just check-drift         # Detect MD newer than its PDF
just check-overflow      # Scan PDFs for content past the right margin
just check-coverage      # Validate every PG/rule has a matching worksheet
just check               # Run all three checks
just clean-build         # Remove build/ directory
just clean-all           # Remove all build artifacts (keeps sources)
```

### Full Recipe List

```
doctor                          # Environment sanity check
gen-worksheets                  # Generate phonogram/rule/flash worksheets
gen-lessons                     # Generate all 248 lesson MD files
gen-lessons-stage <1-5>         # Generate one stage
gen-readers                     # Generate standalone readers
gen-animal-readers              # Generate animal-themed readers
gen-all                         # Generate every Markdown source

render-file <path>              # Render one MD file to PDF
render-stage <1-5>              # Render all lessons in a stage
render-lessons                  # Render all 248 lessons
render-curriculum               # Render curriculum.md as one PDF
render-all                      # Render all lessons + curriculum

pack-lesson <lesson_id>         # Build one lesson pack
pack-stage <1-5>                # Build all packs for a stage
pack-all                        # Build all 248 packs
pack-all-debug                  # Build packs in --no-render mode (debug assembly)

audio                           # Generate 74 MP3s (edge-tts)
audio-ps1                       # Generate audio via PowerShell SAPI

release                         # Build release.zip

all                             # Full pipeline + release ZIP
build                           # Full pipeline without release ZIP

clean-build                     # Remove build/
clean-packs                     # Remove packs/
clean-release                   # Remove release.zip
clean-audio                     # Remove games/audio/
clean-all                       # Remove every build artifact
clean-sources                   # Remove generated MD files (full reset)
```

## Build Without Just (Manual)

If you can't install Just, all the underlying commands work directly. See the [justfile](../justfile) for the exact command lines.

The build order matters:
1. **Generate first** (writes MD files)
2. **Render second** (MD → PDF)
3. **Pack third** (combines rendered PDFs)
4. **Release last** (zips everything)

## Output Layout

After `just all`:

```
build/                          # Rendered PDFs (gitignored)
  stage-1/                      #   48 lesson PDFs (raw, single-lesson)
  stage-2/ ... stage-5/         #   (used for handbooks + assessment copies)
  worksheets/                   #   178 worksheet PDFs (phonograms, rules, cards, blank)
  readers/                      #   25 reader PDFs
  quick-checks/                 #   15 quick-checks + placement test (combined)
  handbook/                     #   Top-level navigation + 5 stage handbooks + certificates
  assessments/                  #   8 stage mastery assessments
  curriculum.pdf                #   Master reference (1 PDF)

packs/                          # Per-lesson bundles (gitignored) — 248 PDFs
  stage-N/lesson-NN-{lesson_id}.pdf   # cover + lesson + worksheet + cards

release.zip                     # Everything in LOE-style folder structure (18.6 MB, 446 files)
```

**Release ZIP structure** (after extraction):

```
README.md                                 # Text overview
00-Start-Here.pdf                         # Orientation for new users
01-Index-and-Table-of-Contents.pdf        # Master clickable TOC
02-Scope-and-Sequence.pdf                 # Full curriculum map
04-Quick-Reference/                       # Phonograms, rules, spelling analysis
05-Teacher-Handbooks/                     # 5 bound-book-style handbooks (PDF)
06-Lesson-Packs/                          # 248 per-lesson bundles
07-Worksheets/                            # 178 standalone practice sheets
08-Decodable-Readers/                     # 25 decodable story PDFs + index
09-Quick-Checks/                          # Placement test + 5 stage quick-checks
10-Assessments/                           # 8 stage mastery assessments
11-Game/                                  # Phonogram trainer (web game)
12-Audio/                                 # 74 phonogram MP3s
13-Certificates/                          # 5 printable completion certificates
```

**Total**: 446 files, 18.6 MB unpacked. Clickable TOC links throughout.

## Release Packaging

`scripts/build-release.py` organizes everything into a teacher-friendly ZIP:

```
release.zip
├── pdfs/
│   ├── stage-1/ ... stage-5/         # Lesson PDFs grouped
│   ├── readers/                      # Decodable readers
│   ├── worksheets/                   # Practice sheets
│   └── phonograms/                   # Flash cards
├── game/
│   └── phonogram-trainer.html        # Self-contained web game
└── audio/                            # 74 MP3 files
```

The ZIP is platform-independent — open on any device with a PDF reader.

## Troubleshooting

### WeasyPrint: `cannot load library 'libgobject-2.0-0'`

GTK3 runtime not installed (or path not found).

**Fix (Windows):**
```bash
"C:/msys64/usr/bin/pacman.exe" -S --noconfirm mingw-w64-x86_64-pango
```

Verify: `ls C:/msys64/mingw64/bin/libgobject-2.0-0.dll`. The pack script auto-sets `WEASYPRINT_DLL_DIRECTORIES` to this path.

**Fix (Linux):** `apt install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`

**Fix (macOS):** `brew install weasyprint`

### `ModuleNotFoundError: No module named 'markdown'` (or `weasyprint`, `pypdf`, `edge_tts`)

Python deps not installed.

```bash
pip install markdown weasyprint pypdf edge-tts
```

### `just: command not found`

Install Just: `winget install Casey.Just` (Windows) / `brew install just` (macOS).

### Pack builder warns about missing assets

Should not happen — all 248 packs build clean. If you see warnings, the catalog or worksheets are out of sync. Run `just gen-worksheets` to refresh.

### Render output looks different from expected

WeasyPrint version matters. Pinned to 60+ for CSS feature parity. Update with caution.

```bash
pip install --upgrade weasyprint
```

### Fonts render as boxes / squares

The Georgia font fallback in render.py needs system fonts. Install via:
- Windows: usually present (`C:/Windows/Fonts/georgia.ttf`)
- Linux: `apt install fonts-liberation`
- macOS: built-in

### Build is slow

Expected: ~85 seconds for full `just all`. If slower:
- WeasyPrint's first import loads many DLLs (one-time cost)
- Each PDF render is 0.1-1.0s depending on content
- Image-heavy readers take longer

Speed up with `just pack-stage N` (one stage at a time) or `pack-lesson pg-d` (single pack).

## Development Workflow

### Modify a Lesson

**Don't edit `lessons/stage-X/lesson-NN.md` directly.** It's regenerated on every build.

1. Find the generator: `scripts/generate-stage{N}.py`
2. Edit the generator (it's the source of truth)
3. Run `just gen-lessons-stage N`
4. Run `just render-stage N` to verify

### Add a Phonogram Worksheet

1. Edit `scripts/generate-worksheets.py`
2. Add PG to `MULTI3` dict (or new dict for new category)
3. Run `just gen-worksheets`
4. New file at `worksheets/phonograms/pg-NAME.md`

### Add a Spelling Rule

1. Edit `scripts/generate-worksheets.py`
2. Add rule to `RULES_WORDS` dict (numeric key)
3. Add `apply_sec` for rule-specific practice section
4. Run `just gen-worksheets`

### Modify Curriculum Content (scope, sequence, methodology)

1. Edit `curriculum.md` directly (it's hand-authored, not generated)
2. Re-render: `just render-curriculum`

### Add a New Image

1. Generate or source PNG matching the Montessori style (see `framework/STYLE-GUIDE.md`)
2. Drop into `images/phonograms/`, `images/animals/`, or `images/illustrations/`
3. Reference in lesson MD: `![alt text](images/animals/dog.png)`
4. Run `just render-lessons`

### Test Pack Assembly Without Rendering

```bash
just pack-all-debug
```

Writes the combined Markdown for each pack to `packs/stage-N/lesson-NN-slug.md` without calling weasyprint. Useful for debugging the assembly logic.

## Quality Checks

Three validators that catch drift, layout problems, and coverage gaps:

### `just check-drift` (or `scripts/check-drift.py`)

Compares each generated lesson MD against its PDF in `build/`. Reports any MD newer than its PDF — meaning a source edit hasn't been re-rendered yet.

```bash
just check-drift                          # all 248 lessons
just check-drift --stage 3                # one stage
python scripts/check-drift.py --include-worksheets --include-readers
```

Exit 0 = clean. Exit 1 = drift detected. Wire into pre-commit to prevent stale PDFs.

### `just check-overflow` (or `scripts/check-table-overflow.py`)

Scans every rendered PDF for text that extends past the right margin. Catches tables that are too wide for letter-size, text that doesn't wrap, code blocks with long lines.

Uses `pypdfium2` (already in dev deps) to extract text rectangles.

```bash
just check-overflow                       # scans build/ and packs/
python scripts/check-table-overflow.py --packs --quiet
```

Exit 0 = clean. Exit 1 = overflow. Lists file:page with overflow amount.

### `just check-coverage` (or `scripts/check-worksheet-coverage.py`)

Reads the catalog and verifies every phonogram/rule taught in lessons has a matching worksheet. Catches:
- **Missing worksheet**: catalog has `new_phonogram='foo'` but no `worksheets/phonograms/pg-foo.md`
- **Orphan worksheet**: `worksheets/phonograms/pg-bar.md` exists but no lesson teaches 'bar'

Exit 0 = 100% coverage. Exit 1 = gap or orphan.

### `just check`

Runs all three. Use before committing changes to lesson MDs or worksheets.

## Project Layout

```
UncoveringtheLogic/
├── README.md                   ← GitHub landing page (you are not here)
├── justfile                    ← Build recipes (25 commands)
├── AGENTS.md                   ← AI agent session guide
├── CHANGELOG.md                ← Version history
├── CONTEXT.md                  ← Domain glossary
├── MISSION.md                  ← Project mission
├── NOTES.md                    ← Working notes + design decisions
├── RESOURCES.md                ← External reading list
├── ROADMAP.md                  ← Open issues
├── TEACHER-GUIDE.md            ← Comprehensive teacher reference
├── curriculum.md               ← Scope & sequence (55KB master doc)
│
├── docs/                       ← Documentation
│   ├── BUILD.md                ← (this file) Build from source
│   ├── USE.md                  ← Teacher: open PDFs, run lessons
│   └── agents/
│       ├── INDEX.md            ← Progressive disclosure index
│       ├── adr/                ← Architecture Decision Records
│       └── learning/           ← Mental models for new contributors
│
├── framework/                  ← Build tools
│   ├── README.md               ← Toolchain reference
│   ├── lesson-catalog.csv      ← 248-lesson index (source of truth)
│   ├── image-manifest.csv      ← Image inventory
│   ├── render.py               ← MD → PDF
│   ├── image-check.py          ← Missing-image scanner
│   ├── generate.py             ← Catalog → MD stubs
│   ├── STYLE-GUIDE.md          ← Image/asset conventions
│   ├── requirements.txt        ← Python dependencies
│   └── templates/              ← MD templates
│
├── scripts/                    ← Generators + builders
│   ├── generate-worksheets.py   # Phonogram/rule/card worksheets
│   ├── generate-stage1.py      # Stage 1 lessons (Pre-K)
│   ├── generate-stage2.py      # Stage 2 lessons (K)
│   ├── generate-stage3.py      # Stage 3 lessons (Gr 1)
│   ├── generate-stage4.py      # Stage 4 lessons (Gr 2)
│   ├── generate-stage5.py      # Stage 5 lessons (Gr 3+)
│   ├── generate-readers.py     # 25 standalone decodable readers
│   ├── generate-animal-readers.py  # Animal-themed readers (35 images)
│   ├── build-lesson-pack.py    # Per-lesson cohesive bundles
│   └── build-release.py        # Final ZIP packaging
│
├── lessons/                    ← 248 lesson MD files (generated)
│   ├── stage-1/ ... stage-5/
│
├── worksheets/                 ← 178 worksheet MD files (generated)
│   ├── phonograms/             #   75 PG worksheets
│   ├── rules/                  #   31 rule worksheets
│   ├── cards/                  #   18 flash card sheets
│   └── blank/                  #   3 reusable templates
│
├── readers/                    ← 25 reader MD files (generated)
│
├── packs/                      ← Per-lesson PDFs (build artifact, gitignored)
│
├── build/                      ← Rendered PDFs (build artifact, gitignored)
│
├── games/
│   ├── phonogram-trainer.html  # Self-contained web game (4 modes)
│   ├── generate-audio-edge.py  # Neural TTS audio generator
│   ├── generate-audio.ps1      # SAPI fallback
│   └── audio/                  # 74 generated MP3s
│
├── reference/                  ← 8 HTML reference aids (printable)
│
├── images/                     ← 35 generated images
│   ├── phonograms/
│   ├── animals/
│   └── illustrations/
│
└── release.zip                 ← Distributable (build artifact, gitignored)
```

---

**Last updated:** Generated alongside the justfile (commit `52a7d7f`).
