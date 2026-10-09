# Changelog

## [1.1.0] — 2026-10-09

### Added
- Example words for each sound printed on flash card backs
- Explanatory "why" notes on lesson-pack common-mistake cards
- Centered watermark logo on completion certificates
- GitHub Actions CI workflow archiving smoke-test results
- Materials-version field on the feedback form (injected from VERSION at release build)

### Changed
- Stage 3–5 decodable readers pack 5 sentences per page; reader sidebar narrowed
- Stage handbooks use the dense body class + smaller phonogram graphics
- At-a-glance key words now cover every sound of multi-sound phonograms

### Fixed
- Phonogram sound lists: qu (/kw/ /k/), x (removed /gz/), y (+/ĭ/), ea (3 sounds), ou (5 sounds), oo (realigned), u (4 sounds), i (4 sounds)
- Stage 3 syllable division: correct counts, splits, and vowel sounds
- Phonogram chart + morpheme wall card boxes (grid → flexbox)
- Diacritical legend ü/ö example symbols
- Reader 001 page count (font + cover image height); reader 003 "red lamb" → "sad lamb"

## [1.0.0] — 2026-08-08

### Added
- Neural TTS audio generator via edge-tts (Aria voice, 74 MP3s)
- Windows SAPI audio generator (PowerShell)
- Phonogram trainer web game (4 modes, audio, stage filters)
- 148 printable worksheets (phonograms, rules, flash cards, blanks)
- 8 additional decodable readers (16 total)
- 30 spelling rule practice worksheets
- Scripted teacher note templates (phonogram, spelling, rule)
- Game materials (Phonogram Bingo, Go Fish)
- AGENTS.md, CONTEXT.md, docs/agents/INDEX.md
- ADR directory (0001-print-first, 0002-css-phonogram-cards, 0003-generator-as-source)
- CHANGELOG.md

### Changed
- Phonogram game: fixed reveal timing, replaced TTS with MP3 audio
- Audio: switched from SAPI to neural TTS (much higher quality)
- Teacher's guide: added cross-reference map, worksheets, readers
- Curriculum: removed external links, shortened wide tables

### Fixed
- render.py: unicode checkmark → ASCII (cp1252 console)
- Stage 2 assessments: raw Python dicts → clean phonogram text
- Prefix filename: un-dis → un-re (matches content)
- Stage 1 "Next lesson" labels: show proper titles
- Filenames aligned with lesson catalog (pa-08-initial-sounds, vocab-1/2/3)

## [0.1.0] — 2025-08-03

### Added
- Complete 248-lesson curriculum across 5 stages
- Print-first framework: markdown templates, render.py, weasyprint pipeline
- 7 decodable readers embedded in lessons
- 8 teacher reference HTMLs
- 35+ Montessori-style images (animals, illustrations)
- Lesson catalog CSV (248 rows)
- Image manifest CSV (43 entries)
- Style guide for image consistency
- Teacher's guide with stage overviews, pacing, materials checklist
- CSS-rendered phonogram cards (no images needed)
- Generator scripts for all 5 stages
- Image check tool with prompt generation
