---
id: E50
name: color character overuse
category: visual-language
project_state: dashboard uses primary hue in cards, borders, icons, shadows and all buttons
user_request: Reduce color noise while keeping semantic status clear.
expected_route: Phase 2 → color character and surface grammar → token-aware targeted implementation → QA
required_artifacts: [VISUAL-GRAMMAR, DESIGN-TOKENS, VISUAL-REVIEW]
forbidden_behavior: [change-semantic-meaning, replace-all-colors-with-grey, introduce-unapproved-palette]
expected_context: [visual-language/color-character, anti-slop/color, design-system]
success_conditions: [accent-frequency-defined, semantic-colors-preserved, neutral-structure-restored, contrast-reviewed]
failure_conditions: [color-character-drift, homogenous-color-goo, primary-everywhere]
---
