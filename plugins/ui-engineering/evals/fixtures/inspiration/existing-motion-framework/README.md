# Existing motion framework fixture

React + Vite marketing site. `package.json` has `framer-motion` (or equivalent `motion` package) in dependencies; `src/motion/presets.ts` exports `fadeUp`, `stagger`, durations and easings; components use `<motion.div variants={fadeUp}>` and `useReducedMotion()`.

User request: add a scroll-linked product reveal section and an animated feature switcher.
