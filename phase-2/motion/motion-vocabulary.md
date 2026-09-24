# Motion vocabulary

A structured vocabulary, not an effect catalog. Each entry states purpose, fit, intensity, performance, accessibility, and implementation. Families are detailed in their own files:

| Family | File |
|---|---|
| Entrance | this file |
| Microinteraction | [microinteractions.md](microinteractions.md) |
| Spatial | [spatial-motion.md](spatial-motion.md) |
| Scroll | [scroll-motion.md](scroll-motion.md) |
| Typography | [text-motion.md](text-motion.md) |

Reduced-motion equivalents for every entry are defined in [reduced-motion.md](reduced-motion.md).

## Entrance

### fade
- **Purpose:** soften appearance of content that loads or reveals. **Intensity:** low.
- **Good:** async content replacing skeletons; toasts; images after load. **Bad:** above-the-fold primary content on page load (delays reading).
- **Perf:** opacity only — cheap. **A11y:** safe; keep short. **Impl:** CSS transition on `opacity` 150–300ms.

### fade-up
- **Purpose:** signal section order on first scroll into view. **Intensity:** low–medium.
- **Good:** marketing sections, once per section. **Bad:** every card/paragraph; app screens; re-triggering on scroll-up.
- **Perf:** `transform: translateY(8–24px)` + opacity. **A11y:** reduced → opacity-only or none. **Impl:** IntersectionObserver adds `.is-visible` once; content visible without JS (`.js` class gate).

### slide
- **Purpose:** communicate origin/direction (panel from edge, carousel item). **Intensity:** medium.
- **Good:** drawers, step transitions where direction has meaning. **Bad:** generic content entrance from random sides.
- **Perf:** transform. **A11y:** reduced → fade. **Impl:** direction matches spatial model.

### scale
- **Purpose:** emphasize an object emerging from a point (popover from trigger, product focus). **Intensity:** low (0.96–1) to high (product reveal).
- **Good:** popovers, menus, hero product. **Bad:** text blocks (blurry scaling), large backgrounds.
- **Perf:** transform; avoid scaling huge layers continuously. **A11y:** reduced → fade.

### clip reveal / mask reveal
- **Purpose:** editorial/cinematic reveal of media or headlines. **Intensity:** medium–high.
- **Good:** one hero image or chapter opener. **Bad:** repeated on every image; text that must be read immediately.
- **Perf:** `clip-path` animation is moderately expensive; limit area and count. **A11y:** reduced → show final state. **Impl:** `clip-path: inset()` transition or keyframes.

### stagger
- **Purpose:** express order within a group. **Intensity:** adds one level to its members.
- **Good:** 3–6 related items appearing together. **Bad:** long lists, tables, grids > ~8 items (stagger caps; remaining items appear together).
- **Perf:** fine with transform/opacity. **A11y:** reduced → no stagger. **Impl:** CSS custom property `--i` × 40–80ms delay; cap total ≤ ~400–600ms.

## Selection rule

Choose the **least intense** entry that achieves the purpose. Content must be readable and operable without waiting for any entrance.
