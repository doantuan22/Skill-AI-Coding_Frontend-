# Motion & Interaction Engine

Motion must communicate, orient, or support storytelling. This module decides **motion character, intensity budget, timing/easing, vocabulary, reduced-motion behavior, and implementation strategy**, then reviews the result. It owns temporal behavior; it does not own static composition (Web Patterns) or tokens (Design System).

## Position

Runs after Visual Grammar and before Web Pattern selection is finalized (pattern choice and motion budget are checked together), then feeds Component Specs. Output goes to [MOTION-SYSTEM.md](../../templates/MOTION-SYSTEM.md) for landing/marketing/storytelling or any medium/high budget work; for low-budget app work, a `motion_character` block in `VISUAL-GRAMMAR.md` is enough. Duration/easing **values** live in `DESIGN-TOKENS.md`; MOTION-SYSTEM references token names.

## Files

| File | Load when |
|---|---|
| [motion-principles.md](motion-principles.md) | Always, when motion is in scope: purposes, intensity budget, timing, easing, implementation strategy |
| [motion-character.md](motion-character.md) | Choosing the motion personality |
| [motion-vocabulary.md](motion-vocabulary.md) | Choosing entrance patterns and the vocabulary index |
| [microinteractions.md](microinteractions.md) | Controls, hover/press/focus, feedback |
| [spatial-motion.md](spatial-motion.md) | Modals, drawers, popovers, expand/collapse, shared movement |
| [scroll-motion.md](scroll-motion.md) | Landing/storytelling scroll effects |
| [text-motion.md](text-motion.md) | Headline/line/word/metric reveals |
| [reduced-motion.md](reduced-motion.md) | Always, when any motion exists |
| [performance-safety.md](performance-safety.md) | Any scroll-linked, continuous, or large-area motion |
| [motion-review.md](motion-review.md) | Review of rendered motion |

Progressive disclosure: dashboards/forms load principles + microinteractions (+ spatial if overlays) + reduced-motion only. Scroll and text motion are for marketing/storytelling pages.

## Dependencies

- Prefer CSS transitions/transforms/keyframes, `IntersectionObserver`, `requestAnimationFrame` when justified, and native scroll-driven animation or View Transitions as progressive enhancement.
- **Reuse** an animation library already present in the project (GSAP, Framer Motion/Motion, Anime.js, etc.) instead of adding another or mixing systems.
- Do **not** add GSAP, Framer Motion, Anime.js, Three.js, Lottie or similar unless the need cannot be met natively *and* the task authorizes a new dependency. Record the justification.
