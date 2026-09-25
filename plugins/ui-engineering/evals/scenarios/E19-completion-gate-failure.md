---
id: E19
name: Completion gate failure
category: completion
project_state: locked-project with unresolved major responsive issue
user_request: Finalize the visual update.
expected_route: PHASE_2 review or BLOCKED; not DONE
required_artifacts: [PHASE-2-REVIEW, FINAL-QUALITY-REPORT-or-BLOCKED-REPORT]
forbidden_behavior: [mark-done, omit-major-issue, compile-equals-success]
expected_context: [level-0, execution-contract, phase-2-review, final-quality-gate]
success_conditions: [major-issue-prevents-completion, evidence-recorded]
failure_conditions: [premature-done]
---

Fixture: `fixtures/locked-project`.

