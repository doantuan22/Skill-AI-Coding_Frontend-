---
id: E59
name: Reduced-motion requirement
category: inspiration
project_state: fixture inspiration/missing-reduced-motion
user_request: Review the motion on this page before release.
expected_route: Phase 2 / POLISH → motion review → reduced-motion equivalents → accessibility path → QA
required_artifacts: [MOTION-SYSTEM, VISUAL-REVIEW, ACCESSIBILITY-REVIEW]
forbidden_behavior: [treat-reduced-motion-as-optional, remove-all-motion-globally-as-only-fix, leave-content-hidden-without-js]
expected_context: [motion/reduced-motion, motion-review, spatial-motion, scroll-motion, text-motion]
success_conditions: [detect-motion-without-reduced-mode, per-pattern-equivalents, content-visible-without-js, sticky-story-static-fallback]
failure_conditions: [motion-without-reduced-mode, premature-done]
---

Fixture: [`fixtures/inspiration/missing-reduced-motion`](../fixtures/inspiration/missing-reduced-motion/README.md).

Existing purposeful motion is kept; equivalents are added per pattern.
