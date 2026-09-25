# Typography rhythm

Turn the archetype into a scale, line-heights and spacing that produce consistent vertical rhythm.

## Scale

- Pick a ratio by archetype: dense-transactional ~1.125–1.2; neutral-product ~1.2–1.25; premium-modern/editorial ~1.25–1.333 with an extra display step; expressive ~1.414+ for display only.
- Keep **5–8 roles**: display, h1, h2, h3, body-lg, body, small/label, caption (+ mono). More sizes = drift.
- Mobile compresses the upper scale (display and h1 shrink most); body stays stable.
- Round to whole pixels or rem steps; tokens name roles (`type-display`, `type-body`), not sizes.

## Line-height and tracking by size

| Size | Line-height | Tracking (sans) |
|---|---|---|
| ≥ 64px | 0.95–1.1 (≥ 1.1 with Vietnamese) | −2% to −3% |
| 32–63px | 1.1–1.2 | −1% to −2% |
| 20–31px | 1.2–1.35 | 0 to −1% |
| 14–19px | 1.45–1.7 | 0 |
| ≤ 13px / caps labels | 1.3–1.5 | +2% to +8% for caps |

## Vertical rhythm

- Space above a heading > space below it (the heading belongs to what follows), roughly 2:1.
- Section spacing is a distinct, larger step than intra-group spacing; equal gaps everywhere flatten hierarchy.
- Align type blocks to the spacing scale rather than a strict baseline grid on the web.

## Responsive checks

At 320, 390, 768, 1280, 1440px: no overflow, headings ≤ 3–4 lines on mobile, measure within range, eyebrow/label wrapping acceptable.
