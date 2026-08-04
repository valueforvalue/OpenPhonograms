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
- [ ] Reader warm-ups: Stages 3-5 readers lack warm-up sections (7 files)

## Assessments

- [x] 8 stage-level assessments
- [ ] Interim quick-checks every 10-15 lessons (would catch problems earlier)
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
- [x] Stage filters + progress tracking
- [x] MP3 audio with TTS fallback
- [ ] Spelling practice mode (hear word, type spelling)
- [ ] Word builder mode (drag phonogram tiles)
- [ ] Multi-player support (two kids race)
- [ ] Printable score reports for teachers

## Teacher Support

- [x] TEACHER-GUIDE.md with cross-references
- [x] 8 reference HTMLs
- [x] Scripted teacher note templates
- [ ] Scripted lessons: embed teacher scripts into lesson templates
- [ ] Video lesson demonstrations
- [ ] Placement test for new students (which stage to start at)

## Distribution

- [x] GitHub repo with full source
- [x] PDF generation (build/ directory)
- [ ] Release ZIP with all PDFs + audio pack
- [ ] Website/landing page for the curriculum
- [ ] Printable workbook binding instructions
