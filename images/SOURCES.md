# Image Sources & Provenance

This file documents the source, license, and generation provenance of
every image asset in `images/`. The project's main code and content is
released under the **MIT License**; however, the images themselves
require their own attribution record because they were generated with
third-party tools.

## Summary

- **All 35 PNGs** in this directory were generated with **Google Gemini**
  (Imagen 3 / image generation) in **August 2026**.
- All assets are released under the **MIT License** as part of the
  curriculum project (see [`../LICENSE`](../LICENSE)).
- The methodology of the curriculum is adapted from
  *Uncovering the Logic of English* by Denise Eide; the **illustrations
  are NOT derived from any Logic of English, Inc. artwork** (no
  Doodling Dragons, Whistling Whales, Knitting Knights, or any
  commercial product imagery is included or referenced).
- Style guidance followed the project's Montessori-style spec (see
  [`../framework/STYLE-GUIDE.md`](../framework/STYLE-GUIDE.md)):
  photorealistic, clean neutral background, natural lighting, sharp
  focus, no cartoon elements, no text overlays, no decorative borders.

## Per-Batch Provenance

### `images/animals/` (24 files)

**Generator:** Google Gemini (Imagen 3, image generation)
**Date:** 2026-08
**Purpose:** Reference photos for the 24 decodable-animal readers
**Style reference:** [`../framework/STYLE-GUIDE.md`](../framework/STYLE-GUIDE.md) § Animal Photos
**License:** MIT (per-batch)

Filenames (real animals, single subject each, neutral white/cream
background):
`beaver.png`, `bird.png`, `cat.png`, `dog.png`, `duck.png`, `eagle.png`,
`firefly.png`, `fish.png`, `fox.png`, `frog.png`, `goat.png`, `goose.png`,
`hen.png`, `horse.png`, `mouse.png`, `ostrich.png`, `pig.png`, `rabbit.png`,
`sheep.png`, `skunk.png`, `snail.png`, `snake.png`, `turtle.png`, `whale.png`.

### `images/illustrations/` (8 files)

**Generator:** Google Gemini (Imagen 3, image generation)
**Date:** 2026-08
**Purpose:** Story-scene illustrations for lesson-embedded readers
(stages 3-5). The "only exception" to the strict Montessori realism
rule — these show real animals doing human-coded activities, but
**rendered with naturalistic anatomy and realistic textures**.

Filenames (story illustrations, one per reader):
`cole-bike.png`, `firefly-night.png`, `fred-frog-cake.png`,
`gwen-goose-gift.png`, `jake-bakes-cake.png`, `ostrich-running.png`,
`sail-box.png`, `train.png`.

**License:** MIT (per-batch)

### `images/phonograms/` (2 files)

**Generator:** Google Gemini (Imagen 3, image generation)
**Date:** 2026-08
**Purpose:** Wall-chart posters for the phonogram catalog
**Style reference:** [`../framework/STYLE-GUIDE.md`](../framework/STYLE-GUIDE.md) § Wall Charts

Filenames: `all-single.png`, `all-multi.png`.

**License:** MIT (per-batch)

### `images/misc/` (1 file)

**Generator:** Google Gemini (Imagen 3, image generation)
**Date:** 2026-08
**Purpose:** Diacritical marks reference card
**Style reference:** [`../framework/STYLE-GUIDE.md`](../framework/STYLE-GUIDE.md) § Phonogram Cards

Filename: `diacritical-marks.png`.

**License:** MIT (per-batch)

## Auditing Prompts

The exact prompts used to generate each image are stored in
[`../framework/image-manifest.csv`](../framework/image-manifest.csv) —
the `prompt` column. To audit an image:

1. Read the `prompt` column in the manifest.
2. Cross-check that the image matches the prompt (manual review).
3. If the image was generated for a copyrighted-source work, remove
   it immediately and re-generate without the source reference.

## Third-Party Images

**None.** A repo-wide grep for `copyright|©|attribution|license|credit`
in `images/`, `assets/`, and `games/` returns zero matches (verified at
SOURCES.md creation). No clipart, no stock photos, no third-party
artwork is bundled.

## Future Audit Checklist

When adding new images, confirm:

- [ ] Generator tool is recorded in this file (and the manifest).
- [ ] Style spec in `framework/STYLE-GUIDE.md` is followed.
- [ ] No copyrighted source imagery is referenced in the prompt.
- [ ] Image is not derived from any Logic of English, Inc. product art.
- [ ] Image is properly licensed for redistribution (MIT default).

## Related

- [`../framework/image-manifest.csv`](../framework/image-manifest.csv) — machine-readable manifest with prompts
- [`../framework/STYLE-GUIDE.md`](../framework/STYLE-GUIDE.md) — image style guide
- [`../LICENSE`](../LICENSE) — project license
- [`../NOTICE`](../NOTICE) — full attribution statement
