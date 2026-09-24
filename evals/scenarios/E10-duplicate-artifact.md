---
id: E10
name: Active artifact reuse
category: artifact-lifecycle
project_state: simple-project with PAGE-MAP active v3
user_request: Add one related page to the service flow.
expected_route: PHASE_1 / EXTEND with artifact discovery
required_artifacts: [ARTIFACT-REGISTRY, PAGE-MAP-v3-update, CHANGE-IMPACT]
forbidden_behavior: [create-PAGE-MAP-v2, create-NEW-PAGE-MAP, ignore-active-v3]
expected_context: [level-0, execution-contract, artifact-contract, phase-1-router]
success_conditions: [reuse-active-artifact, version-increment, targeted-review]
failure_conditions: [duplicate-artifact, stale-artifact-usage]
---

Fixture: `fixtures/simple-project`.

