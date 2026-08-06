# justfile — Uncovering the Logic of English
# Run `just` with no args to list all recipes.
# Run `just <recipe>` to invoke. Most recipes print colored progress.

# Use bash for cross-platform shell semantics; git-bash on Windows.
set shell := ["bash", "-c"]
set dotenv-load := false

# Project paths — `_s` variants are forward-slash form for shell globs
project_root := justfile_directory()
scripts_dir := project_root / "scripts"
framework_dir := project_root / "framework"
lessons_dir := project_root / "lessons"
worksheets_dir := project_root / "worksheets"
readers_dir := project_root / "readers"
packs_dir := project_root / "packs"
build_dir := project_root / "build"
games_dir := project_root / "games"
scripts_dir_s := replace(scripts_dir, "\\", "/")
framework_dir_s := replace(framework_dir, "\\", "/")
lessons_dir_s := replace(lessons_dir, "\\", "/")
worksheets_dir_s := replace(worksheets_dir, "\\", "/")
readers_dir_s := replace(readers_dir, "\\", "/")
packs_dir_s := replace(packs_dir, "\\", "/")
build_dir_s := replace(build_dir, "\\", "/")
games_dir_s := replace(games_dir, "\\", "/")
project_root_s := replace(project_root, "\\", "/")

# Python interpreter
python := if os() == "windows" { "python" } else { "python3" }

# Parallel worker count for render + pack recipes. Override with `just jobs=8 build`.
# Default = number of logical CPUs. weasyprint is CPU-bound; >=physical cores is fine.
_default_jobs := if os() == "windows" { `wmic cpu get NumberOfLogicalProcessors /value 2^>nul ^| findstr NumberOfLogicalProcessors ^| awk -F= "{print $2}"` } else { `nproc` }
jobs := env_var_or_default("jobs", "4")

# Default: list all recipes
default:
    @just --list

# ─────────────────────────────────────────────────────────────────────────────
# Doctor — environment sanity check
# ─────────────────────────────────────────────────────────────────────────────

# Check prerequisites: Python deps, MSYS2/GTK3 (Windows), scripts present
doctor:
    @echo "==> Checking environment"
    @{{python}} --version
    @{{python}} -c "import markdown" 2>/dev/null && echo "  markdown: OK" || echo "  markdown: MISSING (pip install markdown)"
    @{{python}} -c "import weasyprint" 2>/dev/null && echo "  weasyprint: OK" || echo "  weasyprint: MISSING (pip install weasyprint)"
    @{{python}} -c "import edge_tts" 2>/dev/null && echo "  edge-tts: OK" || echo "  edge-tts: MISSING (pip install edge-tts) (optional)"
    @if [ "{{os()}}" = "windows" ]; then \
        if [ -d "C:/msys64/mingw64/bin" ]; then \
            echo "  MSYS2 GTK3 runtime: OK (C:/msys64/mingw64/bin)"; \
        else \
            echo "  MSYS2 GTK3 runtime: MISSING — install via: winget install MSYS2.MSYS2 && pacman -S mingw-w64-x86_64-pango"; \
        fi \
    fi
    @echo "==> Scripts present:"
    @ls {{scripts_dir_s}}/*.py 2>/dev/null | wc -l | xargs printf "  %s Python scripts\n"

# ─────────────────────────────────────────────────────────────────────────────
# Generate — markdown sources from data
# ─────────────────────────────────────────────────────────────────────────────

# Generate all 75 phonogram + 31 rule + 18 flash card + 3 blank worksheets
gen-worksheets:
    @echo "==> Generating worksheets"
    @{{python}} {{scripts_dir_s}}/generate-worksheets.py

# Generate all 248 lesson markdown files (all stages)
gen-lessons:
    @echo "==> Generating lessons (all stages)"
    @{{python}} {{scripts_dir_s}}/generate-stage1.py
    @{{python}} {{scripts_dir_s}}/generate-stage2.py
    @{{python}} {{scripts_dir_s}}/generate-stage3.py
    @{{python}} {{scripts_dir_s}}/generate-stage4.py
    @{{python}} {{scripts_dir_s}}/generate-stage5.py

# Generate a single stage of lessons (1-5)
gen-lessons-stage stage:
    @echo "==> Generating Stage {{stage}} lessons"
    @{{python}} {{scripts_dir_s}}/generate-stage{{stage}}.py

# Generate 25 standalone decodable readers (Stage 2-5)
gen-readers:
    @echo "==> Generating readers"
    @{{python}} {{scripts_dir_s}}/generate-readers.py

# Generate animal-themed readers using all 35 images
gen-animal-readers:
    @echo "==> Generating animal readers"
    @{{python}} {{scripts_dir_s}}/generate-animal-readers.py

# Generate game data (phonograms + spell words) and inject into the HTML
gen-game:
    @echo "==> Generating + injecting game data"
    @{{python}} {{scripts_dir_s}}/generate-game-data.py
    @{{python}} {{scripts_dir_s}}/inject-game-data.py

# Generate every markdown source from data
gen-all: gen-worksheets gen-lessons gen-readers gen-animal-readers gen-game
    @echo "==> All markdown sources generated"

# Generate 15 interim quick-check HTMLs (3 per stage) + combined stage PDFs
gen-quick-checks:
    @echo "==> Generating quick-check HTMLs + PDFs"
    @{{python}} {{scripts_dir_s}}/generate-quick-checks.py

# Generate placement test HTML (JS-scored cross-stage diagnostic)
gen-placement-test:
    @echo "==> Generating placement test HTML + PDF"
    @{{python}} {{scripts_dir_s}}/generate-placement-test.py

# ─────────────────────────────────────────────────────────────────────────────
# Render — markdown → PDF
# ─────────────────────────────────────────────────────────────────────────────

# Render one markdown file to PDF (relative path required)
render-file path:
    @echo "==> Rendering {{path}}"
    @{{python}} {{framework_dir_s}}/render.py {{path}}

# Render all lessons in one stage (1-5) — output: build/stage-N/*.pdf
render-stage stage:
    @echo "==> Rendering Stage {{stage}} lessons ({{jobs}} workers)"
    @{{python}} {{framework_dir_s}}/render.py --stage {{stage}} --jobs {{jobs}}

# Render all 248 lessons across all stages — output: build/stage-N/*.pdf
render-lessons:
    @echo "==> Rendering all lessons (all stages, {{jobs}} workers)"
    @{{python}} {{framework_dir_s}}/render.py --all --jobs {{jobs}}

# Render the full curriculum.md as one PDF — output: build/curriculum.pdf
render-curriculum:
    @echo "==> Rendering curriculum.pdf"
    @{{python}} {{framework_dir_s}}/render.py --curriculum

# Render all 248 lesson PDFs + curriculum
render-all: render-lessons render-curriculum
    @echo "==> All PDFs rendered"

# ─────────────────────────────────────────────────────────────────────────────
# Handbook — navigation PDFs, stage handbooks, certificates
# ─────────────────────────────────────────────────────────────────────────────

# Generate top-level navigation PDFs (Start Here, Index, Scope, Quick Refs)
gen-navigation:
    @echo "==> Generating navigation PDFs"
    @{{python}} {{scripts_dir_s}}/generate-navigation.py

# Generate 5 bound-book-style teacher handbooks (one per stage)
gen-handbooks:
    @echo "==> Generating stage handbooks"
    @{{python}} {{scripts_dir_s}}/generate-stage-handbook.py

# Generate 5 printable completion certificates (one per stage)
gen-certificates:
    @echo "==> Generating completion certificates"
    @{{python}} {{scripts_dir_s}}/generate-certificates.py

# Generate the clickable readers index
gen-readers-index:
    @echo "==> Generating readers index"
    @{{python}} {{scripts_dir_s}}/generate-readers-index.py

# Add source-attribution footer to all lesson/worksheet/reader MDs (issue #32)
gen-footers:
    @echo "==> Injecting source-attribution footers"
    @{{python}} {{framework_dir_s}}/inject_footer.py

# Verify PDFs contain the source attribution (issue #36)
check-pdf-credits:
    @echo "==> Checking PDFs for source attribution"
    @{{python}} {{framework_dir_s}}/check_pdf_credits.py

# Generate printable binding instructions (spine labels, tab labels, print guide)
gen-binding-instructions:
    @echo "==> Generating binding instructions"
    @{{python}} {{scripts_dir_s}}/generate-binding-instructions.py

# Render all worksheet and reader MDs to PDFs (worksheets/ + readers/ → build/)
render-extras:
    @echo "==> Rendering worksheet + reader PDFs ({{jobs}} workers)"
    @{{python}} {{scripts_dir_s}}/render-extras.py --jobs {{jobs}}

# Render reference/*.html files to PDF for printable distribution
render-references:
    @echo "==> Rendering reference HTMLs to PDF ({{jobs}} workers)"
    @{{python}} {{scripts_dir_s}}/render-references.py --jobs {{jobs}}

# Merge per-stage PDFs into stage-N-worksheets.pdf + stage-N-readers.pdf + stage-N.pdf
gen-stage-pdfs:
    @echo "==> Building merged stage PDFs"
    @{{python}} {{scripts_dir_s}}/build-stage-pdf.py

# Copy assessment lesson PDFs into build/assessments/ for the release ZIP
copy-assessments:
    @echo "==> Copying assessments"
    @{{python}} {{scripts_dir_s}}/copy-assessments.py

# ─────────────────────────────────────────────────────────────────────────────
# Packs — cohesive per-lesson bundles for teachers
# ─────────────────────────────────────────────────────────────────────────────

# Build one lesson pack by lesson_id (e.g. pg-d, reader-2)
pack-lesson lesson_id:
    @echo "==> Building pack for {{lesson_id}}"
    @{{python}} {{scripts_dir_s}}/build-lesson-pack.py --lesson {{lesson_id}}

# Build all 48 packs for one stage (1-5)
pack-stage stage:
    @echo "==> Building Stage {{stage}} packs"
    @{{python}} {{scripts_dir_s}}/build-lesson-pack.py --stage {{stage}} --jobs {{jobs}}

# Build all 248 lesson packs — output: packs/stage-N/lesson-NN-slug.pdf
pack-all:
    @echo "==> Building all 248 lesson packs ({{jobs}} workers)"
    @{{python}} {{scripts_dir_s}}/build-lesson-pack.py --all --jobs {{jobs}}

# Build packs without rendering PDFs (debug the assembly logic only)
pack-all-debug:
    @echo "==> Building all 248 packs (no-render mode)"
    @{{python}} {{scripts_dir_s}}/build-lesson-pack.py --all --no-render

# Rebuild packs from cached PDFs only (no render fallback). Use after
# changing pack assembly logic to skip re-rendering 248 PDFs.
rebuild-packs:
    @echo "==> Rebuilding packs from cached PDFs (no render)"
    @{{python}} {{scripts_dir_s}}/build-lesson-pack.py --all --jobs {{jobs}} --cache-only

# Rebuild one stage's packs from cache only
rebuild-packs-stage stage:
    @echo "==> Rebuilding Stage {{stage}} packs from cache (no render)"
    @{{python}} {{scripts_dir_s}}/build-lesson-pack.py --stage {{stage}} --jobs {{jobs}} --cache-only

# ─────────────────────────────────────────────────────────────────────────────
# Audio — neural TTS phonogram audio for the web game
# ─────────────────────────────────────────────────────────────────────────────

# Generate 74 MP3s using Microsoft Edge neural TTS (free, high quality)
audio:
    @echo "==> Generating phonogram audio (edge-tts)"
    @{{python}} {{games_dir_s}}/generate-audio-edge.py

# Generate audio via PowerShell + SAPI (Windows-only fallback)
audio-ps1:
    @echo "==> Generating phonogram audio (SAPI)"
    @powershell -ExecutionPolicy Bypass -File {{games_dir_s}}/generate-audio.ps1

# ─────────────────────────────────────────────────────────────────────────────
# Game — phonogram trainer web game
# ─────────────────────────────────────────────────────────────────────────────

# Open the web game in default browser (no server needed; self-contained HTML)
game-open:
    @start "" "{{games_dir_s}}/phonogram-trainer.html" 2>/dev/null || open "{{games_dir_s}}/phonogram-trainer.html" || xdg-open "{{games_dir_s}}/phonogram-trainer.html"

# ─────────────────────────────────────────────────────────────────────────────
# Release — package everything for distribution
# ─────────────────────────────────────────────────────────────────────────────

# Build release.zip with all PDFs + game + audio (assumes build/ exists)
release:
    @echo "==> Building release.zip"
    @{{python}} {{scripts_dir_s}}/build-release.py

# Dry-run: list what release.zip would contain without writing it
release-list:
    @echo "==> Listing release contents (dry run)"
    @{{python}} {{scripts_dir_s}}/build-release.py --list

# Build release with custom output path
release-to out:
    @echo "==> Building {{out}}"
    @{{python}} {{scripts_dir_s}}/build-release.py --output {{out}}

# Build release for a single stage (e.g. `just release-stage 3`)
release-stage stage:
    @echo "==> Building release for Stage {{stage}} only"
    @{{python}} {{scripts_dir_s}}/build-release.py --stage {{stage}}

# ─────────────────────────────────────────────────────────────────────────────
# Check — drift / overflow / coverage validators
# ─────────────────────────────────────────────────────────────────────────────

# Detect source MD newer than rendered PDF (auto-render drift)
check-drift:
    @echo "==> Drift check (lessons vs build/stage-N/*.pdf)"
    @{{python}} {{scripts_dir_s}}/check-drift.py

# Scan rendered PDFs for content past the right margin
check-overflow:
    @echo "==> Overflow check (build/)"
    @{{python}} {{scripts_dir_s}}/check-table-overflow.py
    @echo "==> Overflow check (packs/)"
    @{{python}} {{scripts_dir_s}}/check-table-overflow.py --packs

# Validate every catalog phonogram/rule has a matching worksheet (and vice versa)
check-coverage:
    @echo "==> Worksheet coverage check"
    @{{python}} {{scripts_dir_s}}/check-worksheet-coverage.py

# Validate every PNG on disk is referenced (and vice versa) in markdown
check-images:
    @echo "==> Image coverage check"
    @{{python}} {{scripts_dir_s}}/check-image-coverage.py

# Run all checks (drift + overflow + coverage + images)
check: check-drift check-overflow check-coverage check-images check-pdf-credits
    @echo ""
    @echo "==> All checks complete"

# Run pytest test suite (excludes slow integration tests by default)
test:
    @echo "==> Running pytest"
    @{{python}} -m pytest

# Run all tests including slow integration (build-stage-pdf + build-release)
test-slow:
    @echo "==> Running pytest including slow integration tests"
    @{{python}} -m pytest -m 'slow or not slow' -o 'addopts=-ra --strict-markers --tb=short' tests/

# ─────────────────────────────────────────────────────────────────────────────
# Aggregate — common workflows
# ─────────────────────────────────────────────────────────────────────────────

# Full build: generate → render → handbook → packs → release (long; ~5-10 min)
all: gen-all gen-footers render-all render-extras render-references gen-stage-pdfs gen-navigation gen-handbooks gen-certificates gen-readers-index gen-binding-instructions gen-quick-checks gen-placement-test pack-all copy-assessments release
    @echo ""
    @echo "==> Full build complete"
    @echo "    PDFs:      {{build_dir_s}}/"
    @echo "    Packs:     {{packs_dir_s}}/"
    @echo "    Release:   {{project_root_s}}/release.zip"

# Build without release ZIP (faster iteration loop)
build: gen-all gen-footers render-all render-extras render-references gen-stage-pdfs gen-navigation gen-handbooks gen-certificates gen-readers-index gen-quick-checks gen-placement-test pack-all copy-assessments
    @echo ""
    @echo "==> Build complete (no release ZIP)"
    @echo "    PDFs:  {{build_dir_s}}/"
    @echo "    Packs: {{packs_dir_s}}/"

# ─────────────────────────────────────────────────────────────────────────────
# Clean — remove build artifacts
# ─────────────────────────────────────────────────────────────────────────────

# Remove rendered PDFs in build/ (keeps markdown sources)
clean-build:
    @echo "==> Cleaning build/"
    @rm -rf {{build_dir_s}}

# Remove all generated lesson packs (keeps markdown + PDFs)
clean-packs:
    @echo "==> Cleaning packs/"
    @rm -rf {{packs_dir_s}}

# Remove release.zip
clean-release:
    @echo "==> Cleaning release.zip"
    @rm -f {{project_root_s}}/release.zip

# Remove generated audio files (keeps game HTML)
clean-audio:
    @echo "==> Cleaning games/audio/"
    @rm -rf {{games_dir_s}}/audio

# Remove EVERY build artifact (back to source-only state)
clean-all: clean-build clean-packs clean-release clean-audio
    @echo "==> All build artifacts removed. Source markdown preserved."

# Remove generated markdown sources too (full reset to bare repo)
clean-sources:
    @echo "==> WARNING: Removing generated lesson/worksheet/reader markdown"
    @echo "    (only catalog CSV + framework/ templates preserved)"
    @find {{lessons_dir_s}} -name "*.md" ! -name "README.md" -delete 2>/dev/null || true
    @find {{worksheets_dir_s}} -name "*.md" -delete 2>/dev/null || true
    @find {{readers_dir_s}} -name "*.md" -delete 2>/dev/null || true
    @echo "==> Sources removed. Restore with: just gen-all"
