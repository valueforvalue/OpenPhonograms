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
- [ ] learning-records/: Capture design decisions as they emerge

## Lesson Template Pattern
```
Step 1: Phonogram Review (flash known cards)
Step 2: New Phonogram/Concept Introduction
Step 3: Practice (writing, sand tray)
Step 4: Quiz (click-to-reveal)
Step 5: Blending/Segmenting Drill
Step 6: Spelling Analysis (when applicable)
Step 7: Reading Practice
Step 8: Celebration + Next Lesson Link
```
