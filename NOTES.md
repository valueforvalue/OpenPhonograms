# Working Notes

## User Preferences
- Wants materials usable offline (HTML files, printable)
- Children's modules should be interactive (click-to-reveal, quizzes)
- Teacher aids must be scannable during a live lesson (<2 min)
- All materials organized beginner→advanced

## Design Decisions
- Single HTML files with embedded CSS (no build step, open in any browser)
- Interactive elements use vanilla JavaScript only (no frameworks, works offline)
- Print stylesheets included in every file (teacher aids double as wall references)
- Phonogram chart uses grid layout for dense-but-readable wall display
- Children's lessons use "step" pattern: introduce → practice → quiz → blend → celebrate

## Framework Design Decisions (2026-08-04 revision)
- **Canonical counts:** 75 phonograms, 31 rules, 26 single-letter. Earlier editions had 74/30/25 — curriculum now uses current edition numbers.
- **Multi-letter phonograms interleaved** during single-letter sequence, not saved for a separate phase. sh/th/ck appear when child knows ~15 single-letter phonograms.
- **Spelling aids = governing rules.** Only ~20 of 75 phonograms have dedicated rules. For the rest, the "aid" is knowing all sounds in frequency order. Worksheets: every phonogram gets practice; only those with rules get rule-work.
- **Decodable reader design:** sidebar with spelling aid on each page, diacritical marks in warm-up box ONLY (not in story text), Montessori-style realistic images, cohesive animal character per series, 1-4 sentences per page, large font.
- **Say-to-Spell is essential, not optional.** Introduced at first multi-syllable word (Stage 2, word: "little").
- **Phonogram-Rule Mapping table** added to curriculum.md — definitive reference for which phonograms carry which spelling aids.

## Next To Create
- [ ] Lessons 0004-0040: Complete Stage 1 phonogram sequence (remaining a-z + qu)
- [ ] Lessons for Stage 2: All multi-letter phonograms with spelling analysis
- [ ] Lessons for Stage 3: Silent E deep dive (9 lessons, one per reason)
- [ ] Lessons for Stage 4: Schwa and suffixing rules
- [ ] Lessons for Stage 5: Morpheme study units
- [ ] assets/quiz-widget.js: Reusable quiz component
- [ ] assets/phonogram-flash.js: Interactive flash card component
- [ ] reference/placement-test.html: Diagnostic tool to determine starting stage
- [ ] reference/scope-sequence-wall.html: Visual wall chart of entire progression
- [ ] lessons/readers/: Decodable reader HTML files with sidebar layout
- [ ] learning-records/: Capture design decisions as they emerge

## Lesson Template Pattern
```
Step 0: Warm-up words with diacritical marks (if a reader lesson)
Step 1: Phonogram Review (flash known cards)
Step 2: New Phonogram/Concept Introduction
Step 3: Practice (writing, sand tray)
Step 4: Quiz (click-to-reveal)
Step 5: Blending/Segmenting Drill
Step 6: Spelling Analysis (when applicable)
Step 7: Reading Practice (story text — clean, no diacritical marks)
Step 8: Celebration + Next Lesson Link
```

## Reader Page Template
```
┌─────────────────────────┬──────────────────┐
│ [WARM-UP BOX]           │  Sidebar         │
│ cāke tīme hōpe          │  Phonogram: a_e  │
│ (Silent E → long vowel) │  Sounds: /ā/     │
│                         │  Rule 12.1       │
├─────────────────────────┼──────────────────┤
│ [STORY TEXT — clean]    │                  │
│ Jake bakes a cake.      │  [Montessori-    │
│ He takes his time.      │   style animal   │
│                         │   illustration]  │
│ [Facing: illustration]  │                  │
└─────────────────────────┴──────────────────┘
```
