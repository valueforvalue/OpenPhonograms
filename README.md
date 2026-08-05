# Uncovering the Logic of English — Open-Source Curriculum

A print-first reading curriculum (Pre-K → Grade 3+) covering **248 lessons**, **75 phonograms**, **31 spelling rules**, and **25 decodable readers**.

Every printed artifact is generated from version-controlled Markdown by Python scripts. No DRM. No internet required.

Source methodology: [*Uncovering the Logic of English* by Denise Eide](https://logicofenglish.com/).

---

## Who Is This For?

| You want to... | Read |
|----------------|------|
| **Use the curriculum** — print PDFs, teach lessons | → [docs/USE.md](docs/USE.md) |
| **Build from source** — clone, render, customize | → [docs/BUILD.md](docs/BUILD.md) |
| **Understand the methodology** — read the scope & sequence | → [curriculum.md](curriculum.md) (55 KB) |
| **Look up phonograms, rules, or quick reference** | → [TEACHER-GUIDE.md](TEACHER-GUIDE.md) |
| **Contribute or modify content** | → [AGENTS.md](AGENTS.md) + [docs/BUILD.md § Development Workflow](docs/BUILD.md#development-workflow) |
| **Browse architecture decisions** | → [docs/agents/adr/](docs/agents/adr/) |

---

## Quick Start (Two Audiences)

### I'm a Teacher

1. Download the [latest release ZIP](#releases)
2. Extract and open `pdfs/stage-1/lesson-09-phonogram-a.pdf` (or whichever stage you start at)
3. Print the [phonogram chart](reference/phonogram-chart.html) and [spelling rules poster](reference/spelling-rules.html)
4. Read [docs/USE.md](docs/USE.md) for the daily workflow

The lesson PDFs are self-contained. Each `lesson-NN-*.pdf` pack includes a cover page with prep checklist, the teacher script, matched worksheet, and flash cards for review.

### I'm a Developer

```bash
git clone https://github.com/YOUR-USER/UncoveringtheLogic.git
cd UncoveringtheLogic

# One-time setup (Windows)
winget install Casey.Just MSYS2.MSYS2
"C:/msys64/usr/bin/pacman.exe" -S --noconfirm mingw-w64-x86_64-pango
pip install markdown weasyprint pypdf edge-tts

# Build everything
just build        # gen → render → packs (~80s)
just all          # + release ZIP (~85s)
```

Full instructions: [docs/BUILD.md](docs/BUILD.md).

---

## What's Inside

### Generated PDFs (~500 total, ~17 MB unpacked)

```
build/
├── stage-1/ ... stage-5/    # 248 lesson PDFs
├── worksheets/              # 178 practice sheets
│   ├── phonograms/          #   75 (one per phonogram)
│   ├── rules/               #   31 (one per rule)
│   ├── cards/               #   18 flash card sheets
│   └── blank/               #   3 reusable templates
├── readers/                 # 25 decodable story PDFs
└── curriculum.pdf           # Master reference (1 PDF)

packs/                       # 248 per-lesson bundles
└── stage-N/
    └── lesson-NN-title.pdf  # cover + lesson + worksheet + cards
```

### Source Files

```
framework/lesson-catalog.csv  # 248-row source of truth
scripts/generate-*.py         # 9 generators (data → Markdown)
framework/render.py           # Markdown → PDF
justfile                      # 25 build recipes
docs/BUILD.md                 # Build from source
docs/USE.md                   # Use the curriculum
```

### Plus

- **Phonogram trainer web game** — 4 modes (Flash, Match, Speed, Browse), self-contained HTML
- **74 audio MP3s** — neural TTS, phonogram sounds
- **8 printable HTML aids** — phonogram chart, rules poster, etc.

---

## Methodology Highlights

1. **Speech-to-print, not print-to-speech.** Start with the sound, find the written form.
2. **Teach ALL sounds from the start.** "a says /ă/ /ā/ /ä/" — never "a says /ă/" with more later.
3. **Spelling drives reading.** Spelling Analysis is the core routine.
4. **No sight words.** Every word can be decoded with phonograms + rules.
5. **Say-to-Spell is not optional.** Multi-syllable words need deliberate mispronunciation to reveal spelling.

Full philosophy: [TEACHER-GUIDE.md § Philosophy Reminders](TEACHER-GUIDE.md#philosophy-reminders).

---

## Project Structure

```
UncoveringtheLogic/
├── README.md                   ← You are here
├── justfile                    ← 25 build commands (try: `just`)
├── AGENTS.md                   ← AI agent session guide
├── TEACHER-GUIDE.md            ← Comprehensive teacher reference
├── curriculum.md               ← Scope & sequence (55 KB master)
├── CONTEXT.md                  ← Domain glossary
├── ROADMAP.md                  ← Open issues
├── CHANGELOG.md                ← Version history
│
├── docs/
│   ├── BUILD.md                ← Build from source (developers)
│   ├── USE.md                  ← Use the curriculum (teachers)
│   └── agents/
│       ├── INDEX.md            ← Progressive disclosure index
│       ├── adr/                ← Architecture Decision Records
│       └── learning/           ← Mental models
│
├── framework/                  ← Build tools (render.py, catalog CSV)
├── scripts/                    ← 9 generators + 2 builders
├── lessons/                    ← 248 generated lesson MDs
├── worksheets/                 ← 178 generated worksheet MDs
├── readers/                    ← 25 generated reader MDs
├── reference/                  ← 8 printable HTML aids
├── games/                      ← Web game + audio generators
├── images/                     ← 35 generated images
│
├── build/                      ← Rendered PDFs (gitignored)
├── packs/                      ← Per-lesson bundles (gitignored)
└── release.zip                 ← Distributable (gitignored)
```

---

## Releases

Download the latest release ZIP from the [Releases](../../releases) page.

Each release ZIP contains:
- All 248 lesson PDFs
- All 178 worksheet PDFs
- All 25 reader PDFs
- The full curriculum reference (1 PDF)
- The phonogram trainer web game
- 74 phonogram audio MP3s
- 8 printable HTML reference aids

**Total:** ~6 MB zipped, ~17 MB extracted.

---

## Contributing

Contributions welcome. The generator pattern means content changes flow through:

```
edit catalog / generator → run `just gen-lessons-stage N` → run `just render-stage N`
```

Read [AGENTS.md](AGENTS.md) for the AI agent session guide (covers generator pattern, drift watch, domain glossary).

Architectural decisions are recorded in [docs/agents/adr/](docs/agents/adr/) — append-only.

---

## License

Released under the **MIT License** — see [LICENSE](LICENSE).

## Credits

This project is an open-source adaptation of the methodology described in
[*Uncovering the Logic of English* by Denise Eide](https://logicofenglish.com/).
The phonograms, spelling rules, and instructional routines are derived from
that book and from the [Logic of English](https://logicofenglish.com/) curriculum.

**This project is not affiliated with, endorsed by, or sponsored by Logic of
English, Inc.** "Logic of English" and "Uncovering the Logic of English" are
trademarks of Logic of English, Inc. See [NOTICE](NOTICE) for the full
attribution statement.

### If you want the full commercial product

We encourage you to support the original authors if their commercial curriculum
fits your needs:

- **[*Uncovering the Logic of English* — Denise Eide (2012)](https://logicofenglish.com/)** — the foundational book.
- **[Logic of English, Inc.](https://logicofenglish.com/)** — official *Foundations* (Pre-K–Grade 2) and *Essentials* (Grades 3+) curriculum, printed materials, classroom kits, and training.
- **[Logic of English Facebook Group](https://www.facebook.com/groups/logicofenglish)** — active community.

### Attribution

- **Denise Eide** — Author of *Uncovering the Logic of English* and inventor of the methodology.
- **Logic of English, Inc.** — Publisher and curriculum developer.
- **Contributors** — See [git history](../../graphs/contributors).
- **Bundled font** — Atkinson Hyperlegible © Braille Institute of America, Inc., licensed under SIL OFL 1.1 (see [framework/fonts/OFL.txt](framework/fonts/OFL.txt)).
- **Built with:** Python, WeasyPrint, Markdown, MSYS2 GTK3, Just.
