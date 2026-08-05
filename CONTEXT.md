# CONTEXT.md — Domain Glossary

Shared vocabulary for this project. Term + definition + avoid-list.

---

## Core Terms

### phonogram
A written symbol (letter or group of letters) that represents one or more speech sounds.

- **Single-letter:** a, b, c, ... z (26 total, q always taught as qu)
- **Multi-letter:** sh, th, ck, ee, ... gu (49 total)
- **Total:** 75 basic phonograms

> Avoid: "letter" (imprecise — sh is not a letter), "digraph" (LoE prefers "multi-letter phonogram"), "grapheme" (academic; use "phonogram").

### spelling rule
One of 31 governing rules that explain how phonograms interact. Numbered 1-31 with sub-rules (e.g., 12.1-12.9 for Silent E).

> Avoid: "phonics rule" (LoE uses "spelling rule"), "exception" (these are rules, not guidelines — 98% coverage).

### say-to-spell
Deliberately mispronouncing a word with clear vowel sounds to hear its spelling. /ə-bout/ → "ā-bout". NOT the normal pronunciation — a tool for spelling only.

> Avoid: "pronunciation" (say-to-spell is intentionally wrong), "sounding out" (different — sounding out uses real phonogram sounds).

### decodable
Text containing only phonograms the child has been taught. "The cat sat" is decodable after learning a, c, t, s, th, e.

> Avoid: "levelled reader" (commercial term, often includes sight words), "easy reader" (vague).

### spelling analysis
The 5-step core routine: Hear & Say → Segment → Write → Analyze → Read. Used in every lesson.

> Avoid: "spelling test" (analysis, not assessment), "dictation" (only one part of the routine).

### warm-up
Lesson opening. Always phonogram flash review. Child sees card, says ALL sounds within 2 seconds.

> Avoid: "review" (warm-up is fast drill; review is a separate lesson type).

---

## File Types

### lesson
A single teaching session. Markdown file in `lessons/stage-X/`. 248 total. Has header, warm-up, new learning, spelling analysis, quick check, next lesson, home practice.

### worksheet
Student practice page. In `worksheets/`. Types: phonogram practice, rule practice, blank templates, flash cards, game cards.

### reader
Decodable story. Standalone in `readers/` or embedded in a lesson. Controlled vocabulary — only taught phonograms.

### reference
Teacher-facing printable aid. HTML files in `reference/`. 8 total: quickstart, phonogram chart, spelling rules, spelling analysis, word lists, HF words, troubleshooting, morpheme wall.

### catalog
`framework/lesson-catalog.csv`. CSV index of all 248 lessons. Source of truth for lesson order, types, IDs, phonograms, rules.

### generator
Python script in `scripts/` that produces markdown files from data. Output must not be hand-edited — fix the generator.

---

## Stage Boundaries

| Stage | Lessons | Age | New Content |
|-------|---------|-----|-------------|
| 1 | 1-48 | Pre-K (4-5) | 26 single-letter PGs + phonemic awareness |
| 2 | 49-104 | K (5-6) | 25 multi-letter PGs + short vowels + 6 rules |
| 3 | 105-160 | Gr 1 (6-7) | Silent E + 17 PGs + 9 rules + syllables |
| 4 | 161-208 | Gr 2 (7-8) | Schwa + suffixing + Latin /sh/ + morphology |
| 5 | 209-248 | Gr 3+ (8+) | 25 roots + fluency + composition + grammar |

---

## Historical

### canonical-counts
Early editions listed 74/30/25. Current edition is 75/31/26. This curriculum uses the current canonical counts. qu bridges single-letter (taught in Stage 1) and multi-letter (listed as #1 in multi-letter list). Total unique: 74. Total counting qu in both: 75.

---

## Attribution & License

This is an open-source adaptation of the methodology described in
Denise Eide's *Uncovering the Logic of English* (2012).

- **License**: MIT — see [`LICENSE`](../LICENSE) (project code and content)
- **Attribution and trademarks**: See [`NOTICE`](../NOTICE)
- **Bundled font**: [Atkinson Hyperlegible](https://www.brailleinstitute.org/freefont)
  by the Braille Institute, redistributed under the
  [SIL Open Font License 1.1](../framework/fonts/OFL.txt)

This project is **not affiliated with, endorsed by, or sponsored by Logic of
English, Inc.** "Logic of English" and "Uncovering the Logic of English" are
trademarks of Logic of English, Inc.
