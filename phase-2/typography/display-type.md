# Display type

Display type creates the first impression and the page's scale contrast. It is used deliberately, not on every heading.

## Strategy decisions

| Decision | Options | Guidance |
|---|---|---|
| Scale | compact / large / oversized | Compact for apps and dense commerce; large for product marketing; oversized only for one moment (hero or chapter opener) with little copy. |
| Weight | light / regular / semibold / bold / heavy | Large sizes look heavier; semibold (600) often reads as bold at ≥ 48px. Light weights only with verified contrast and good rendering. |
| Tracking | negative / normal / positive | Negative on large sans (≈ −1% to −3%); serif display usually normal; spaced caps positive. |
| Line-height | 0.95–1.2 | Tighter as size increases; ≥ 1.1 for Vietnamese diacritics. |
| Case | sentence / title / uppercase | Sentence case is most readable; uppercase only for short labels/eyebrows. |
| Width | normal / condensed / wide | Condensed fits long words in large sizes and conveys urgency; wide conveys stability/luxury. Must match archetype. |
| Measure | ≤ ~12–20 words per headline | Use `text-wrap: balance` where supported for 2–3 line headings. |

## Fluid sizing

Use `clamp(min, preferred-vw-based, max)` for display so mobile does not inherit desktop size. Typical: hero display min 32–40px on mobile, max 64–112px on desktop depending on archetype. Verify at 320px width that no word overflows (long compound words, Vietnamese phrases, URLs).

## Rules

- Do **not** default to a giant hero heading. Large display requires a short, strong message and an archetype that wants scale (premium, editorial, expressive, portfolio). Developer, dense and app surfaces use compact display.
- One display size dominates per viewport; competing large headings flatten hierarchy.
- Gradient/clipped-text display is an exception requiring rationale and contrast verification.
- Display type animation follows [text-motion.md](../motion/text-motion.md) and must not delay reading.
