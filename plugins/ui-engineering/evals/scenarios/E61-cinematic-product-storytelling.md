---
id: E61
name: Cinematic product storytelling
category: inspiration
project_state: fixture inspiration/premium-landing
user_request: Tell the product story in a cinematic way.
expected_route: Phase 2 → inspiration (premium-product) → storytelling pattern (progressive product reveal) → motion (cinematic hero, budgeted) → performance safety → QA
required_artifacts: [DESIGN-INSPIRATION, MOTION-SYSTEM, VISUAL-REVIEW]
forbidden_behavior: [feature-cards-only, multiple-high-regions-adjacent, scroll-hijacking, add-animation-library-without-authorization]
expected_context: [web-patterns/storytelling, web-patterns/hero, motion/scroll-motion, motion/performance-safety, motion/reduced-motion, web-patterns/motion-composition]
success_conditions: [narrative-pattern-selected, specs-still-accessible, native-or-io-scroll-strategy, mobile-simplification, reduced-motion-static-steps]
failure_conditions: [pattern-misuse, scroll-jank-risk, motion-without-reduced-mode, everything-animated]
---

Fixture: [`fixtures/inspiration/premium-landing`](../fixtures/inspiration/premium-landing/README.md).

Cinematic does not mean everything moves: one high region, calm elsewhere.
