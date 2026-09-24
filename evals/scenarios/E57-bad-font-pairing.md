---
id: E57
name: Bad font pairing
category: inspiration
project_state: fixture inspiration/bad-font-pairing
user_request: Clean up our typography.
expected_route: Phase 2 / EXTEND_EXISTING or POLISH → current type extraction → typography review → normalize → QA
required_artifacts: [CURRENT-DESIGN-SYSTEM, DESIGN-SYSTEM, VISUAL-REVIEW]
forbidden_behavior: [keep-script-face-for-body, add-another-family, rewrite-unrelated-components]
expected_context: [typography/typography-review, font-pairing, body-type, display-type]
success_conditions: [detect-excessive-font-families, detect-display-font-misuse, detect-mono-overuse, detect-poor-reading-measure, reduce-to-justified-pair]
failure_conditions: [excessive-font-families, display-font-misuse, mono-overuse, poor-reading-measure]
---

Fixture: [`fixtures/inspiration/bad-font-pairing`](../fixtures/inspiration/bad-font-pairing/README.md).

Expected result collapses six families to one family or one justified pair, with mono removed from nav/buttons.
