# AGENTS.md — AI Agent Session Guide

Hand-curated. Read at session start. Keep under 30 lines.

## Project: OpenPhonograms Curriculum

Print-first reading curriculum. 244 markdown lessons, 75 phonograms, 31 spelling rules.

## Key Files

- `README.md` — GitHub landing, role picker (teacher vs developer)
- `TEACHER-GUIDE.md` — Entry point for humans and agents
- `curriculum.md` — Full methodology, phonogram list, rules, scope (55KB)
- `docs/BUILD.md` — Build from source (requirements, justfile, troubleshooting)
- `docs/USE.md` — Use the curriculum (teachers)
- `framework/lesson-catalog.csv` — 244-lesson index (source of truth)
- `framework/render.py` — Markdown → PDF pipeline (weasyprint)
- `scripts/generate-stage*.py` — Lesson/worksheet/reader generators
- `games/phonogram-trainer.html` — Web game (self-contained HTML)

## Generator Pattern

Every markdown file traces to a Python generator in `scripts/`. If you hand-edit a lesson, the generator will overwrite it. Fix the generator, not the output.

## PDF Pipeline

`framework/render.py` → `markdown` lib → `weasyprint` → PDF. Requires GTK3 runtime on Windows. Build via `just` (see justfile): `just doctor` to verify env, `just build` for full pipeline.

## Build Commands (justfile)

`just` lists 25 recipes. Common: `just build` (gen+render+packs), `just all` (+release), `just pack-stage 3`, `just doctor`. Just is a Makefile alternative — install via winget.

## Content Schema

Every lesson has: `# Lesson N: Title` / `**Stage X** · Lesson N · type` / `## Warm-Up` / `## New Learning` / `## Spelling Analysis` / `## Quick Check` / `**Next lesson:**` / `*Practice at home:*`

## Drift Watch

- Generator output vs catalog: filenames must match `lesson_id` column
- Worksheet data vs lesson data: same phonogram sounds, same words
- Game phonogram data vs curriculum: 75 phonograms, same sounds
- Worksheet phonograms: 75/75 (100% coverage; check via `just check-coverage`)
- PDF vs markdown: tables must fit letter-size page

## Domain Glossary

See `CONTEXT.md` for term definitions. Critical: "phonogram" ≠ "letter", "say-to-spell" ≠ "pronunciation", "decodable" ≠ "levelled".
