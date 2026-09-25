# Motion System

- Status: draft
- Version: v1
- Structure Lock version:
- Inputs: Design Direction / Design Inspiration / Visual Grammar versions
- Existing motion implementation: none / CSS / library (name, version) — reuse decision:

Owner of temporal behavior (see [Motion Engine](../knowledge/motion/README.md)). Duration and easing **values** live in `DESIGN-TOKENS.md`; this file references token names. Low-budget app work may record only the `motion_character` block inside `VISUAL-GRAMMAR.md`.

## Character

```yaml
motion_character:
  base:                 # minimal | snappy | soft | cinematic | expressive-controlled | playful | technical
  microinteraction:
  hero:
  navigation:
  scroll_storytelling:
  decorative_loop:      # none | rare (+ rationale)
  reason:
```

## Intensity budget

| Region / pattern | Intensity (`LOW`/`MEDIUM`/`HIGH`) | Purpose | Notes |
|---|---|---|---|

Rule: ≤ 1 `HIGH` region (2 on long storytelling pages with separation).

## Timing and easing

| Interaction type | Duration token | Easing token | Range rationale |
|---|---|---|---|
| Microinteraction | | | |
| Component transition | | | |
| Spatial (enter / exit) | | | |
| Marketing entrance / stagger | | | |
| Storytelling (scroll-linked) | n/a (scroll) | linear | |

## Vocabulary in use

| Family | Pattern | Where | Purpose | Implementation (CSS / IO / scroll-timeline / VT API / rAF / existing lib) |
|---|---|---|---|---|
| Entrance | | | | |
| Microinteraction | | | | |
| Spatial | | | | |
| Scroll | | | | |
| Typography | | | | |

## Reduced motion

| Pattern | Reduced equivalent | Verified |
|---|---|---|

Content visible without JS and under `reduce`: yes / no

## Performance safety

- Animated properties limited to transform/opacity: yes / exceptions:
- Scroll handling strategy:
- Off-screen/hidden-tab pausing:
- New dependency added: none / name + authorization + justification
