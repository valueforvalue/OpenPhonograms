# Docs Index — 3-Tier Progressive Disclosure

Token budgets enforced. Read tier-0 every session.

---

## Tier 0 — Every Session (~5K tokens total)

| Doc | Tokens | Purpose |
|-----|--------|---------|
| `AGENTS.md` | ~300 | Session-start guide, key files, generator pattern, drift watch |
| `CONTEXT.md` | ~600 | Domain glossary: phonogram, say-to-spell, decodable, etc. |
| `TEACHER-GUIDE.md` | ~2,500 | Human + agent entry point, file map, stage overviews |
| `curriculum.md` (first 200 lines) | ~2,000 | Scope & sequence, core principles |

## Tier 1 — By Role (~5K each)

| Doc | Role | Purpose |
|-----|------|---------|
| `curriculum.md` (full) | Content authors | All 75 PGs, 31 rules, methodology |
| `framework/STYLE-GUIDE.md` | Image/asset creators | Montessori image rules |
| `framework/README.md` | Toolchain users | render.py, generate.py, image-check.py |
| `docs/agents/learning/logic-of-english.md` | New contributors | 5-min mental model of LoE methodology |

## Tier 2 — On Demand

| Doc | When to read |
|-----|-------------|
| `framework/render.py` (source) | Debugging PDF output |
| `scripts/generate-stage*.py` (source) | Adding/modifying lesson content |
| `framework/lesson-catalog.csv` | Querying lesson metadata |
| `framework/image-manifest.csv` | Adding new images |
| `reference/*.html` | Printing classroom aids |
| `games/phonogram-trainer.html` (source) | Modifying the web game |

## ADR Directory

`docs/agents/adr/` — Architecture Decision Records. Append-only.

| ADR | Status |
|-----|--------|
| 0001-print-first.md | Accepted |
| 0002-css-phonogram-cards.md | Accepted |
| 0003-generator-as-source.md | Accepted |
