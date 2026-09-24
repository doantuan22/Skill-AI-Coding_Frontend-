---
id: E14
name: One-page scope discipline
category: scope-control
project_state: simple-project
user_request: Improve only the login page.
expected_route: targeted phase based on requested change
required_artifacts: [TASK-SCOPE, targeted-page-artifact-or-review]
forbidden_behavior: [redesign-dashboard, alter-unrelated-pages, hidden-shared-impact]
expected_context: [level-0, execution-contract, selected-phase-router]
success_conditions: [scope-held, shared-impact-documented-if-needed]
failure_conditions: [scope-creep, unrelated-artifact-creation]
---

Fixture: `fixtures/simple-project`.

