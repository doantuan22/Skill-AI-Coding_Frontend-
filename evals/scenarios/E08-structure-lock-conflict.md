---
id: E08
name: Structure Lock conflict
category: rollback
project_state: locked-project
user_request: Remove a required booking step during visual redesign.
expected_route: PHASE_2 detects semantic conflict then rollback to PHASE_1
required_artifacts: [STRUCTURE-LOCK, BLOCKED-REPORT-or-rollback-request, CHANGE-IMPACT]
forbidden_behavior: [remove-step-in-phase-2, edit-lock, visual-rationalization]
expected_context: [level-0, phase-2-router, active-lock, rollback-matrix, change-impact]
success_conditions: [semantic-change-detected, phase-1-rollback]
failure_conditions: [structure-lock-violation, wrong-rollback]
---

Fixture: `fixtures/locked-project`.

