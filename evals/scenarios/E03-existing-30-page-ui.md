---
id: E03
name: Existing thirty-page UI
category: extraction-and-migration
project_state: large-existing-project
user_request: Normalize UX across an existing thirty-page application.
expected_route: PHASE_1 / EXISTING_UI with extraction and chunk processing
required_artifacts: [CURRENT-UX-MAP, REQUIREMENT-SPEC, ARTIFACT-REGISTRY, TASK-SCOPE]
forbidden_behavior: [rewrite-everything, ignore-existing-artifacts, one-large-context]
expected_context: [level-0, phase-1-router, current-ux-extraction, chunking-strategy]
success_conditions: [extract-before-change, reuse, batch-plan]
failure_conditions: [blind-rewrite, duplicate-artifacts, no-impact-analysis]
---

Fixture: `fixtures/large-existing-project`.

