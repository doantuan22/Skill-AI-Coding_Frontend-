# Design System

- Status: draft
- Version: v1
- Owner: Phase 2
- Structure Lock version:

## Foundations

| Area | Direction / token source | Constraints |
|---|---|---|
| Color | | Semantic interaction and feedback states |
| Typography | | Family, scale, weight, line-height, tracking |
| Spacing | | Scale and density |
| Radius / borders / elevation | | Surface language |
| Grid / container / breakpoints | | Responsive strategy |
| Iconography / imagery | | Existing library, crop/loading behavior |
| Motion | | Purpose, durations, reduced motion; behavior in `MOTION-SYSTEM.md` when in scope |
| States | | Focus, disabled, loading, feedback |

## Typography system

Owned by [Typography Intelligence](../skills/typography/README.md); values map to `DESIGN-TOKENS.md`.

```yaml
typography_character:
  archetype:              # neutral-product | premium-modern | editorial | technical | developer | friendly-consumer | luxury | dense-transactional | expressive-marketing
  secondary_scope:        # none | scoped voice + region
  reason:
pairing_strategy:         # single-family | variable-optical | display+body | serif-display+sans-body | sans+mono
numerals:                 # tabular contexts / proportional contexts
```

| Family | Role / job | Class | Source (existing / system / licensed web font) | License | Weights | Language coverage verified (e.g., Vietnamese) | Loading + fallback |
|---|---|---|---|---|---|---|---|

| Role | Size (mobile → desktop) | Weight | Line-height | Tracking | Measure / notes |
|---|---|---|---|---|---|
| Display | | | | | |
| H1–H3 | | | | | |
| Body | | | | | |
| Small / label | | | | | |
| Mono | | | | | |

## Component contracts

| Component | Purpose | Variants / sizes | Required states | Tokens | Responsive / accessibility constraints |
|---|---|---|---|---|---|

_This document is the Phase 2 source of truth; map values to `DESIGN-TOKENS.md` and the existing frontend stack._

