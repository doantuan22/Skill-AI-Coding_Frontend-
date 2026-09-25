# Reduced motion

Reduced motion is a requirement, not optional polish. Every motion decision records its reduced equivalent before implementation.

## Rules

1. Respect `prefers-reduced-motion: reduce` for all non-essential motion.
2. **Reduce, don't necessarily remove:** replace movement (translate, scale, parallax, rotation, zoom) with opacity changes or instant state changes; keep essential feedback (focus, state change, progress) perceivable.
3. Remove entirely under reduce: parallax, scroll-linked transforms, auto-playing loops, character/word reveals, large-area scaling, background video autoplay (show poster + play control).
4. Content must be fully visible and operable in the reduced state (no content stuck at `opacity: 0` because an observer or animation never ran).
5. Any auto-moving content lasting > 5 seconds needs a pause/stop control regardless of preference (WCAG 2.2.2).
6. If an existing library is used, use its reduced-motion hook/config (e.g., a `useReducedMotion`-style API or `matchMedia` check) consistently.

## Pattern

```css
/* default: no motion-dependent visibility */
.reveal { opacity: 1; }

@media (prefers-reduced-motion: no-preference) {
  .js .reveal { opacity: 0; transform: translateY(16px);
    transition: opacity var(--motion-slow) var(--ease-out), transform var(--motion-slow) var(--ease-out); }
  .js .reveal.is-visible { opacity: 1; transform: none; }
}
```

Motion is opt-in under `no-preference`; the default is the static, complete state. A global `* { animation: none !important }` reset is acceptable as a safety net but does not replace per-pattern equivalents (it can hide content left at initial keyframes).

## Equivalents table

| Motion | Reduced equivalent |
|---|---|
| fade-up / slide / scale entrance | opacity only (short) or none |
| modal/drawer slide | fade |
| expand/collapse | instant |
| parallax / image scale / progress-linked | static final state |
| sticky storytelling | stacked static steps |
| text reveals / rotating headline | static text |
| counter | final value |
| hover lift | color/shadow change only |
| loaders | keep (essential), prefer non-spinning indicators if possible |

Missing strategy is `MOTION_WITHOUT_REDUCED_MODE` (MAJOR; BLOCKER when it causes vestibular-risk effects like parallax/zoom or hides content).
