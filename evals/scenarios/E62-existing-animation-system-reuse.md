---
id: E62
name: Existing animation system reuse
category: inspiration
project_state: fixture inspiration/existing-motion-framework
user_request: Add a scroll-linked product reveal and an animated feature switcher.
expected_route: Phase 2 / EXTEND_EXISTING → capability/stack inspection → motion character from existing presets → implement with existing library → QA
required_artifacts: [VISUAL-GRAMMAR, VISUAL-REVIEW]
forbidden_behavior: [add-gsap-or-second-library, bypass-existing-presets, ignore-useReducedMotion]
expected_context: [motion/README, motion-principles, scroll-motion, reduced-motion, product-showcase/interaction-patterns]
success_conditions: [reuse-existing-library-and-presets, respect-existing-reduced-motion-hook, feature-switcher-accessible]
failure_conditions: [unnecessary-dependency, motion-style-drift]
---

Fixture: [`fixtures/inspiration/existing-motion-framework`](../fixtures/inspiration/existing-motion-framework/README.md).

The project's existing motion framework is reused; no second animation system is added.
