---
id: E58
name: Motion overuse
category: inspiration
project_state: fixture inspiration/motion-overuse
user_request: The page feels chaotic; fix the animations.
expected_route: Phase 2 / POLISH → motion review → character + budget → targeted rewrite of motion layer → reduced motion → QA
required_artifacts: [MOTION-SYSTEM, VISUAL-REVIEW]
forbidden_behavior: [remove-all-feedback-motion, add-animation-library, change-locked-content]
expected_context: [motion/motion-review, motion-principles, performance-safety, reduced-motion, scroll-motion]
success_conditions: [detect-everything-animated, detect-scroll-jank-risk, detect-unjustified-parallax, replace-transition-all, io-instead-of-scroll-handler, single-high-region]
failure_conditions: [everything-animated, excessive-entrance-animation, motion-for-decoration, scroll-jank-risk, motion-without-reduced-mode]
---

Fixture: [`fixtures/inspiration/motion-overuse`](../fixtures/inspiration/motion-overuse/README.md).

Motion intensity must be reduced while keeping purposeful feedback.
