# Planned Improvements

Open issues for the project. Checked = done, unchecked = planned.

## Content

- [x] 248 lessons across 5 stages
- [x] 32 decodable readers (25 standalone + 7 embedded)
- [x] 30 spelling rule worksheets
- [x] 69 phonogram practice worksheets
- [x] 18 flash card sheets
- [x] 3 blank templates (spelling analysis, handwriting, reading log)
- [x] Game materials (Bingo, Go Fish)
- [x] Phonogram trainer web game
- [x] 74 MP3 audio files (neural TTS)
- [x] 35 images (24 animals + 8 illustrations + 2 wall charts + 1 misc)
- [x] Missing phonogram worksheets: ti, ci, si (3 Latin PGs) — bu/gu not taught as lessons
- [x] Missing rule-12 worksheet: Silent E (9 reasons)
- [x] Reader warm-ups: Stages 3-4 readers (5 files; reader-7 is informational, not decodable)

## Assessments

- [x] 8 stage-level assessments
- [x] Interim quick-checks: 15 across stages (3 per stage early/mid/late)
- [ ] Assessment auto-grading (fill-in scores in markdown → render)

## Tooling

- [x] MD→PDF pipeline (render.py + weasyprint)
- [x] Lesson generators (5 stage scripts)
- [x] Worksheet/flash card generator
- [x] Reader generators (2 scripts)
- [x] Audio generator (neural TTS)
- [x] Image check tool
- [x] Auto-render drift detector (check-drift.py)
- [x] PDF table overflow checker (check-table-overflow.py)
- [x] Worksheet-to-lesson cross-reference validator (check-worksheet-coverage.py)

## Game

- [x] 4 modes: Flash, Match, Speed, Browse
- [x] 5th mode: Spell (hear word, type spelling)
- [x] Stage filters + progress tracking
- [x] MP3 audio with TTS fallback
- [ ] Word builder mode (drag phonogram tiles)
- [ ] Multi-player support (two kids race)
- [ ] Printable score reports for teachers

## Teacher Support

- [x] TEACHER-GUIDE.md with cross-references
- [x] 8 reference HTMLs + 15 quick-check HTMLs + 1 placement test = 24 reference files
- [x] Scripted teacher note templates
- [x] Placement test: reference/placement-test.html (JS-scored, 4 sections)
- [ ] Scripted lessons: embed teacher scripts into lesson templates
- [ ] Video lesson demonstrations

## Distribution

- [x] GitHub repo with full source
- [x] PDF generation (build/ directory)
- [x] Release ZIP with LOE-style folder structure (450 files, 18.8 MB)
  - 00-Start-Here.pdf, 00-Landing-Page.{pdf,html}, 01-Index-TOC.pdf, 02-Scope-and-Sequence.pdf (top-level navigation)
  - binding-instructions.pdf (top-level, printable)
  - 04-Quick-Reference/ (phonograms, rules, spelling analysis)
  - 05-Teacher-Handbooks/ (5 stage handbooks, 153-260 pages each, clickable bookmarks)
  - 06-Lesson-Packs/ (248 per-lesson bundles, 5 stage folders)
  - 07-Worksheets/ (178 standalone sheets, 4 categories)
  - 08-Decodable-Readers/ (25 readers + index)
  - 09-Quick-Checks/ (placement test + 5 stage quick-checks)
  - 10-Assessments/ (8 stage mastery assessments)
  - 11-Game/ (phonogram-trainer.html + bundled audio MP3s)
  - 13-Certificates/ (5 printable completion certificates)
  - README.md (text overview at root)
- [x] Website/landing page: docs/index.html + 00-Landing-Page.pdf
- [x] Printable workbook binding instructions: binding-instructions.pdf
