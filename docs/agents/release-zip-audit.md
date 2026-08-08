# Release ZIP Audit — Deep Dive

Captured: this session, against current `release.zip` (81 MB, 921 files).

## LOE commercial product structure (per level A/B/C/D = our stages)

LOE ships per level:

| LOE Product | Format | Use |
|---|---|---|
| Teacher's Manual | 1 PDF per level, ~150 pp | Read on screen or print whole book |
| Student Workbook | 1 PDF per level, ~150 pp, manuscript OR cursive | Print whole book for student |
| Decodable Readers | Set of physical books | One per student |
| Phonogram Flash Cards | 75 cut-out cards | Print, cut, daily review |
| Spelling Rule Flash Cards | 31 cut-out cards | Print, cut, daily review |
| Phonogram Game Cards | 75 game tiles | Print, cut, use in games |
| Tactile Cards (cursive/manuscript) | 26 letter cards | Kinesthetic letter learning |
| Quick References | 3 laminated cards | At-teacher-desk reference |
| Scope & Sequence | PDF | Curriculum overview |
| Placement Test | PDF | Diagnostic |
| Assessments | 8 PDFs | Every 5th lesson |
| Online Supplement | Web app | Video lessons |

**No per-lesson bundles in LOE commercial.** Teacher prints the whole Teacher's Manual once, references daily, prints worksheets as needed.

## Our ZIP, mapped to LOE

| LOE Product | Our ZIP | Match? | Notes |
|---|---|---|---|
| Teacher's Manual | `05-Teacher-Handbooks/stage-N.pdf` | ✓ | 1 per stage, scripted |
| Student Workbook | `06-Stage-Overview/stage-N.pdf` | ✓ proxy | Combined phonogram+rule+flash worksheets |
| Decodable Readers | `08-Decodable-Readers/` | ✓ | Per-book PDFs |
| Phonogram Flash Cards | inside `06-Stage-Overview/` + inside `06-Lesson-Packs/` | ✓ partial | 26 standalone `07-Worksheets/cards/` also exist |
| Spelling Rule Flash Cards | inside `06-Stage-Overview/` | ✓ partial | 31 standalone `07-Worksheets/rules/` also exist |
| Phonogram Game Cards | **MISSING** | ❌ | Not generated |
| Tactile Cards | **MISSING** | ❌ | Not generated |
| Quick References | `04-Quick-Reference/` (5 PDFs) | ✓ | Includes glossary, diacritical legend, 3 master refs |
| Scope & Sequence | `02-Scope-and-Sequence.pdf` | ✓ | |
| Placement Test | `09-Quick-Checks/placement-test.pdf` | ✓ | |
| Assessments | in handbook + standalone quick-checks | ✓ | |
| Cursive / Manuscript | single style | partial | Cursive only? verify |
| Online Supplement | `11-Game/phonogram-trainer.html` | partial | Single HTML, no videos |
| **Lesson Packs** | `06-Lesson-Packs/stage-N/lesson-NN-*.pdf` | **OUR ADDITION** | Per-lesson bundle, not in LOE |
| **Stage Overview** | `06-Stage-Overview/stage-N.pdf` | **OUR ADDITION** | Workbook + flash card bundle |
| **Certificates** | `13-Certificates/` | **OUR ADDITION** | Not in LOE |

## What's UNIQUE to lesson packs (not in handbook)

Each `lesson-NN-*.pdf` pack has 7–16 pages:

1. **Cover** — prep checklist (paper, marker, etc.)
2. **At-a-glance card** — 1-page cut-out reference for THIS lesson's phonograms
3. **Teacher script** — same content as handbook
4. **Lesson-specific worksheet** — e.g. lesson 25 (phonogram n) has pg-n worksheet embedded
5. **Flash cards** — pages of cards for phonograms used in this lesson

**Unique value vs handbook:** at-a-glance card + lesson worksheet + relevant flash cards, all pre-bundled. Teacher prints ONE pack to teach ONE lesson.

## What's UNIQUE to handbook

- Table of contents (with bookmarks)
- Lesson scripts (same as pack)
- Stage assessment (full)
- Handwriting lessons
- Reviews

**No at-a-glance, no lesson worksheets, no flash cards.**

## What's UNIQUE to standalone worksheets

`07-Worksheets/` has 178 files:
- 75 phonogram worksheets (2-3 pp each)
- 31 spelling rule worksheets
- 18 flash card sheets
- 3 blank templates

Each phonogram worksheet appears 3 times in the ZIP:
1. Inside the matching lesson pack
2. Inside `06-Stage-Overview/stage-N.pdf`
3. As standalone `07-Worksheets/phonograms/pg-NN.pdf`

Each rule worksheet appears 2 times:
1. Inside `06-Stage-Overview/stage-N.pdf`
2. As standalone `07-Worksheets/rules/rule-NN.pdf`

## Three delivery models compared

### Model A (current): Loose units
- ZIP = 444 packs + 178 worksheets + 5 handbooks + 5 overviews + readers + reference + audio + certificates
- 81 MB, 921 files
- Pros: pick-and-choose what to print
- Cons: 2.5× duplication, hard to navigate ("which PDF has pg-n?"), build = 75 min on Windows

### Model B: Bound only (matches LOE exactly)
- ZIP = 5 handbooks (TM) + 5 overviews (workbook) + readers + reference + audio + 5 certs + quick-checks
- ~25 MB, ~150 files
- Pros: clean LOE structure, fast build (15 renders), one place per stage
- Cons: teacher must print whole handbook/workbook to use; no per-lesson bundles

### Model C: Hybrid (TM + lesson packs, no duplication)
- ZIP = 5 handbooks + 444 lesson packs + readers + reference + audio + certs
- ~50 MB, ~480 files
- Pros: matches LOE TM + adds our per-lesson convenience pack; no standalone worksheets
- Cons: 444 files is more than B; teacher might print both TM and packs (but they could just use packs)

## Render perf implications

Each WeasyPrint render on Windows = 10s (Pango/font scan). Each render on Linux = ~1s.

| Action | Current | Model A | Model B | Model C |
|---|---|---|---|---|
| Render handbooks | 5 | 5 | 5 | 5 |
| Render stage overviews | 5 | 5 | 5 | 0 |
| Render lesson PDFs (per source) | 244 | 244 | 0 | 0 |
| Render worksheets standalone | 178 | 178 | 0 | 0 |
| Render pack PDFs (composite) | 444 | 444 | 0 | 444 |
| **Total renders** | **876** | **876** | **10** | **449** |
| **Windows time** | **~145 min** | **~145 min** | **~2 min** | **~75 min** |
| **Linux time** | **~15 min** | **~15 min** | **~10 s** | **~8 min** |

**Critical insight:** Model B is 100× faster than A on Windows because every "render" is a content render (not just Pango scan). With `--skip-existing`, repeated Model B builds = ~5s on Windows.

## Recommendation

**Model C** is the right balance:
- LOE TM equivalent (handbook)
- Per-lesson convenience pack (cover + at-a-glance + lesson + worksheet + cards)
- No standalone worksheet duplication
- Skip per-lesson PDF render (assemble packs from MD sources directly via inline-render path)
- **Build: ~75 min cold Windows, ~30s with `--skip-existing`**

To execute Model C:
1. `07-Worksheets/` ships ONLY what's not in packs/overviews (which is nothing — remove or keep as extras)
2. `06-Stage-Overview/` removed (its content = workbook + cards, now lives in packs)
3. Build packs via inline-render (don't depend on `build/stage-N/*.pdf`)
4. Add `--skip-existing` to pack build

Open question for user: does removing `06-Stage-Overview/` (the workbook equivalent) break the LOE-parity? Or is it OK because packs contain the same worksheets?

## Decision points

1. **Worksheet duplication acceptable?** Today: 3 copies of each phonogram worksheet. Acceptable for "teacher flexibility" or waste?
2. **At-a-glance cards valuable enough to keep packs?** Teacher convenience vs simpler build.
3. **Print whole handbook or just packs?** If both shipped, teacher might print both. If only packs, no reference book.
4. **Standalone worksheets** (`07-Worksheets/phonograms/`, etc.) — keep as extras for teachers who want extra practice? Or remove?