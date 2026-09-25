# Font pairing

Pair only when a second family has a job the first cannot do. Default is one family.

## Strategies

| Strategy | When | Rules |
|---|---|---|
| **Single-family system** | Most products; neutral-product, dense-transactional, minimal | Hierarchy from size, weight and tracking; 2–3 weights. |
| **Variable family with optical hierarchy** | premium-modern; families with `opsz`/`wdth` axes | Display uses higher optical size/tighter tracking; body uses text optical size. Counts as one family. |
| **Display + body (sans + sans)** | expressive-marketing, consumer-tech | Families must differ clearly in one axis (width, geometry, contrast); similar-but-different sans pairs read as a mistake. Display ≥ 24–28px only. |
| **Serif display + sans body** | editorial, luxury, premium storytelling | Match x-height and proportion roughly; serif only for display/pull quotes; UI controls stay sans. |
| **Serif throughout** | long-form reading products | Body serif must be a text-optimized design; UI chrome may remain sans. |
| **Sans + mono accent** | developer, technical | Mono only for code, commands, IDs, metrics labels or deliberate metadata; never paragraphs. Harmonize x-height; mono often needs ~0.9–0.95× size. |

## Limits

- ≤ 2 families per product (plus mono when `developer`/`technical` justifies it = max 3).
- ≤ 4 weights in active use across all families.
- One italic role at most (emphasis or editorial voice), defined.

## Detect

| Code | Signal |
|---|---|
| `EXCESSIVE_FONT_FAMILIES` | > 2 non-mono families, or 3 including mono without technical content; fonts introduced per section. |
| arbitrary pairing (reported as `TYPE_STYLE_DRIFT` or `TYPOGRAPHY_CHARACTER_MISSING`) | Two families without a recorded job for each; two near-identical sans; display and body from conflicting archetypes (e.g., playful rounded display + luxury serif body). |
| `DISPLAY_FONT_MISUSE` | Display/decorative face used for paragraphs, form labels, buttons in dense UI, or below ~20px. |
| `MONO_OVERUSE` | Mono used for body copy, headings without technical meaning, or entire UI to look "techy". |

## Record

```yaml
pairing:
  strategy: serif display + sans body
  display: {family: Newsreader, job: editorial headlines and pull quotes, min_size: 28px}
  body: {family: Source Sans 3, job: reading, UI, controls}
  mono: none
  reason: editorial-product; serif carries authorship, sans keeps UI legible
```
