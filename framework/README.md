# Framework Toolchain: Markdown → Printable PDF

## Philosophy

Every lesson, worksheet, and reader is authored as a **single Markdown file**. Markdown is the source of truth — version-controllable, diffable, and human-readable. A Python toolchain converts markdown files to print-optimized PDFs with image placeholders that can be swapped for real images later.

```
lesson.md  ──[render.py]──►  lesson.pdf
                                │
                                ├── Print-optimized (page breaks, margins)
                                ├── Image placeholders with alt-text
                                ├── Phonogram sidebar on reader pages
                                └── Warm-up boxes with diacritical marks
```

## Directory Structure

```
UncoveringtheLogic/
├── curriculum.md              # Master curriculum document
├── framework/
│   ├── README.md              # This file
│   ├── lesson-catalog.csv     # Complete index: every lesson across all 5 stages
│   ├── image-manifest.csv     # Every image needed, by filename and description
│   ├── render.py              # MD → PDF conversion script
│   ├── generate.py            # Generate lesson stubs from catalog
│   ├── image-check.py         # List missing/needed images
│   ├── requirements.txt       # Python dependencies
│   └── templates/
│       ├── lesson-template.md
│       ├── worksheet-template.md
│       └── reader-template.md
├── lessons/
│   ├── stage-1/               # ~40 phonogram/phonemic-awareness lessons
│   ├── stage-2/               # ~60 CVC + multi-letter phonogram lessons
│   ├── stage-3/               # ~55 Silent E + vowel team lessons
│   ├── stage-4/               # ~50 schwa + suffixing + Latin lessons
│   └── stage-5/               # ~40 morphology + fluency lessons
├── worksheets/
│   ├── stage-1/               # One worksheet per phonogram
│   ├── stage-2/
│   ├── stage-3/
│   ├── stage-4/
│   └── stage-5/
├── readers/
│   ├── stage-2/               # Decodable readers with sidebar layout
│   ├── stage-3/
│   ├── stage-4/
│   └── stage-5/
└── images/
    ├── phonograms/            # Phonogram card images (75)
    ├── animals/               # Montessori-style animal photos
    └── illustrations/         # Reader illustrations
```

## Lesson Counts (vs. Official Logic of English)

| Our Stage | Grade | Lessons | Official Equivalent | Official Count |
|-----------|-------|---------|--------------------|----------------|
| Stage 1 | Pre-K/K | **48** | Foundations A | 40 + 8 review |
| Stage 2 | K/Gr 1 | **56** | Foundations B | 40 + 8 review |
| Stage 3 | Gr 1 | **56** | Foundations C | 40 + 8 review + 8 bonus |
| Stage 4 | Gr 2 | **48** | Foundations D | 40 + 8 review |
| Stage 5 | Gr 3+ | **40** | Essentials (partial) | 30 units × 5 parts |
| **Total** | | **248** | | ~350-360 units |

Our 248 lessons are comparable in scope: each of our lessons is one teaching session (20-60 min). Official Foundations splits content across more granular "parts." Our Stage 5 compresses Essentials' 30 units into 40 lessons focused on morphology and fluency.

### Lesson Type Breakdown

| Type | Count | Description |
|------|-------|-------------|
| phonogram-intro | 52 | Introduce one new phonogram with all sounds |
| phonemic-awareness | 13 | Oral blending, segmenting, sound manipulation |
| rule-intro | 18 | Introduce one spelling rule with practice words |
| spelling-analysis | 8 | Dedicated dictation/spelling practice sessions |
| review | 18 | Cumulative review of phonograms and rules |
| assessment | 8 | Stage mastery checks |
| word-building | 6 | Pattern-based word construction (CVC, CCVC, etc.) |
| vowel-concept | 7 | Short vowels, long vowels, vowel teams |
| reader | 7 | Decodable reader lessons with sidebar |
| morphology | 30 | Prefix, suffix, Latin/Greek root study |
| hf-word | 5 | High-frequency word sets (decoded, not memorized) |
| handwriting | 2 | Letter formation practice |
| syllable-division | 4 | Multi-syllable word strategies |
| schwa-practice | 3 | Say-to-spell and schwa identification |
| rule-practice | 5 | Focused rule application |
| say-to-spell | 1 | Say-to-spell technique introduction |
| fluency | 3 | Repeated reading, phrasing, rate |
| vocabulary | 3 | Tier 2 words, synonyms, relationships |
| composition | 3 | Sentence and paragraph writing |
| grammar | 3 | Parts of speech, sentence types, punctuation |
| **Total** | **248** | |

## Lesson Types

| Type | Template | Directory | Example |
|------|----------|-----------|---------|
| Phonogram introduction | `lesson-template.md` | `lessons/stage-X/` | Introduce `a`, practice writing, blend CVC |
| Spelling Analysis | `lesson-template.md` | `lessons/stage-X/` | 3-5 words via hear-segment-write-analyze-read |
| Rule introduction | `lesson-template.md` | `lessons/stage-X/` | Introduce Rule 26 (CK), practice with words |
| Worksheet | `worksheet-template.md` | `worksheets/stage-X/` | Independent practice for one phonogram/rule |
| Decodable reader | `reader-template.md` | `readers/stage-X/` | Story with sidebar, warm-up box, animal theme |

## Toolchain Usage

### Install dependencies
```bash
cd framework
pip install -r requirements.txt
```

### Generate lesson stubs from catalog
```bash
python generate.py --stage 1          # Generate all Stage 1 lessons
python generate.py --stage 2          # Generate all Stage 2 lessons
python generate.py --all              # Generate all lessons (all stages)
python generate.py --lesson stage-2/042-sh-phonogram  # Single lesson
```

### Render a single lesson to PDF
```bash
python render.py lessons/stage-1/002-phonogram-a.md
# Output: lessons/stage-1/002-phonogram-a.pdf
```

### Render all lessons in a stage
```bash
python render.py --stage 2
# Output: lessons/stage-2/*.pdf
```

### Check which images are needed
```bash
python image-check.py
# Output: list of images referenced in lessons but not yet in images/
```

### Render the full curriculum as PDF
```bash
python render.py --curriculum
# Output: curriculum.pdf
```

## Image Placeholder Convention

All images use a consistent markdown syntax with descriptive alt-text:

```markdown
![Phonogram card: a - /ă/ /ā/ /ä/](images/phonograms/a.png)
![Montessori-style: A brown dog sitting](images/animals/dog.png)
![Illustration: Jake the snake baking a cake](images/illustrations/jake-bakes-cake.png)
```

When the real image doesn't exist yet, `render.py` inserts a **placeholder box** showing the alt-text, dimensions, and filename — so the PDF is complete and usable even without images. Swap in real PNGs later and re-render.

## Print Specifications

| Property | Value |
|----------|-------|
| Page size | US Letter (8.5×11") |
| Margins | 0.75" all sides (0.5" for worksheets) |
| Body font | 14pt Georgia (lessons), 12pt (worksheets) |
| Phonogram display | 48pt Georgia bold |
| Code/word font | 16pt Courier New |
| Reader story font | 18-22pt Georgia |
| Page breaks | Before each new lesson section, after each reader page |
| Color | Lessons: full color OK. Worksheets: grayscale-safe. |
