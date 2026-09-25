# Technical type

Covers code, commands, identifiers, metrics, prices, tables and specs.

## Monospace

- **Use for:** code blocks, inline code, CLI commands, API paths, hashes/IDs, keyboard shortcuts, fixed-width alignment needs.
- **May use for:** small metadata labels (versions, timestamps) in developer/technical archetypes as a deliberate voice, limited to one role.
- **Do not use for:** paragraphs, marketing headlines without technical meaning, navigation, buttons, whole UIs.
- Size mono ~0.9–0.95× body to match x-height; line-height 1.5–1.7 in code blocks; horizontal scroll inside code blocks, never page overflow.
- Code blocks need a copy action when commands are meant to be run.

## Numerals

| Context | Treatment | CSS |
|---|---|---|
| Tables, prices, metrics, timers, changing counters | tabular lining | `font-variant-numeric: tabular-nums lining-nums;` |
| Prose | proportional (default) | — |
| Editorial serif prose | oldstyle if the font supports it | `oldstyle-nums` |
| Fractions/ordinals | only if supported | `diagonal-fractions`, `ordinal` |

Right-align numeric table columns; align decimals where possible. Keep currency/unit formatting consistent and locale-correct (e.g., `1.250.000 ₫` for vi-VN).

## Metric typography

Large numbers (KPIs, specs, "10× faster") use display size with tabular numerals, a short label beneath/above, and a unit set smaller. A metric must be real and sourced; decorative "stats" are a composition tell (see [anti-slop/composition](../visual-language/anti-slop/composition.md)).
