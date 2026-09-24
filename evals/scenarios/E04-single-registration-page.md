---
id: E04
name: Single registration page
category: context-efficiency
project_state: simple-project
user_request: Add one registration page.
expected_route: PHASE_1 / EXTEND or NEW_UI / fast path
required_artifacts: [REQUIREMENT-SPEC, merged-page-flow-spec]
forbidden_behavior: [load-dashboard, load-tables, load-checkout, full-project-redesign]
expected_context: [level-0, phase-1-router, forms, onboarding-if-first-use]
success_conditions: [forms-only-context, minimal-artifacts, explicit-unknowns]
failure_conditions: [context-overload, unrelated-references, scope-creep]
---

Fixture: `fixtures/simple-project`.

