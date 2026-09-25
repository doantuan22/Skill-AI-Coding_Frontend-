# Body type

Body type carries comprehension and task completion. Its job is readability first; character comes second.

| Property | Reading content | App/product UI | Dense data/transactional |
|---|---|---|---|
| Size | 17–20px | 14–16px | 13–15px (never < 12px for essential text) |
| Line-height | 1.5–1.7 | 1.4–1.55 | 1.3–1.45 |
| Measure | 55–75ch (max ~80) | follows component | follows column |
| Weight | 400 (350–450 variable) | 400; 500 for labels | 400/500 |
| Paragraph spacing | 0.75–1em | component spacing | minimal |

## Rules

- Constrain reading measure with `max-width` in `ch`; full-width paragraphs on wide screens fail (`POOR_READING_MEASURE`).
- Mobile body is never smaller than desktop body for reading content; keep ≥ 16px for inputs to avoid mobile zoom.
- Secondary text reduces emphasis through color/size, not by dropping below contrast thresholds.
- Avoid justified text on the web unless hyphenation is enabled and language-supported; Vietnamese hyphenation support is limited, so prefer left-aligned.
- Links in body are distinguishable without color alone (underline or equivalent).
- Use `text-wrap: pretty` where supported to reduce orphans; never rely on it for layout.
