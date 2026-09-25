---
id: E27
name: Mobile-only regression
category: viewport-coverage
project_state: locked-project with an existing desktop capture and mobile defect
user_request: Fix the mobile layout regression.
expected_route: PHASE_2 targeted mobile recapture plus justified regression viewport
required_artifacts: [EXECUTION-REPORT, VISUAL-REVIEW]
forbidden_behavior: [full-route-viewport-sweep, ignore-mobile-evidence, semantic-flow-change]
expected_context: [level-0, execution-router, viewport-registry, responsive-review]
success_conditions: [mobile-targeted-evidence, delta-review, limited-regression-check]
failure_conditions: [wrong-viewport, context-overload, structure-lock-violation]
---

Fixture: `fixtures/locked-project`.

