# Montessori Image Style Guide

Apply to every image in this project. Give this to your image generator as a global pre-prompt.

---

## Universal Rules (all images)

- **Photorealistic or naturalistic illustration. NEVER cartoon.**
- Clean, uncluttered background — white, cream, or soft neutral tone
- Natural soft lighting, sharp focus on the subject
- True-to-life colors and proportions
- No text overlays, no watermarks, no decorative borders or frames
- One clear subject per image
- Print-ready at stated resolution (minimum 300dpi equivalent)
- Consistent warm-neutral color temperature across the entire set
- No lens flare, no heavy filters, no artificial bokeh

## Animal Photos (images/animals/*.png)

- Real animals in natural poses — **not anthropomorphized, no human clothing**
- Neutral background (white, cream, or very soft natural blur)
- The animal should fill ~60-70% of the frame
- Sharp focus on the eyes/face
- Examples: a real frog on a leaf, a real dog sitting, a real fish swimming
- These serve as character reference images for the readers — the same animal appears in illustrations doing story activities, but here they are depicted as real animals

## Reader Illustrations (images/illustrations/*.png)

- Animals doing human-coded activities (baking, holding objects, using tools) — this is the **only** exception to strict Montessori realism
- **BUT:** the animals must be rendered with naturalistic anatomy, real animal textures (fur, feathers, scales), and realistic proportions
- Think: a real frog standing at a counter with a mixing bowl. The frog looks like a photograph of a real frog — it just happens to be in a kitchen scene
- Soft, warm storybook lighting — golden hour or cozy interior
- No exaggerated facial expressions, no cartoon squash-and-stretch
- Children characters: realistic children with natural proportions, not stylized

## Phonogram Cards (images/phonograms/*.png)

- White background (#FFFFFF)
- Large typography in Georgia serif font, navy blue (#2a5c8a)
- Centered layout with generous whitespace
- Sounds below the phonogram in smaller type
- Example words in light gray (#888) below sounds
- No decorative elements, no borders, no gradients
- Clean, minimalist — these are reference cards, not posters

## Wall Charts (images/phonograms/all-*.png)

- White background
- Grid layout with 5-6 columns
- Each cell: phonogram in navy blue Georgia, sounds below in smaller type
- Generous padding between cells
- Print-friendly: high contrast, no color backgrounds
- Font sizes: phonogram ~60pt, sounds ~14pt

## Aspect Ratios & Sizes

| Type | Size | Ratio |
|------|------|-------|
| Phonogram cards | 800×600 | 4:3 |
| Animal photos | 1200×900 | 4:3 |
| Reader illustrations | 1200×900 | 4:3 |
| Wall charts | 2400×1800 | 4:3 |
| Worksheets | 1600×1200 | 4:3 |

## Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Primary accent | Navy blue | #2a5c8a |
| Body text | Near-black | #111111 |
| Muted text | Warm gray | #555555 |
| Light text | Light gray | #888888 |
| Background | Off-white | #fffff8 |
| Card background | Warm white | #f7f7f2 |
| Warm-up box | Pale blue | #eef6ff |
| Success green | Forest green | #2a7d2a |
| Rule lines | Light gray | #dddddd |

---

**Pre-prompt for image generator:**

> Generate a [type] image in Montessori educational style: photorealistic, clean neutral background, natural lighting, sharp focus, true-to-life colors, no cartoon elements, no text overlays, no decorative borders. Print-ready at stated resolution. Consistent warm-neutral color temperature.
