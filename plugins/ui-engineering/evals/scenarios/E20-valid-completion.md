---
id: E20
name: Valid completion
category: completion
project_state: locked-project with all required reviews passed
user_request: Finalize the completed visual update.
expected_route: PHASE_2_REVIEW to FINAL_REVIEW to DONE
required_artifacts: [STRUCTURE-LOCK, PHASE-2-REVIEW, FINAL-QUALITY-REPORT, FINAL-REVIEW, COMPLETION-EVIDENCE]
forbidden_behavior: [skip-gate, unresolved-blocker, missing-evidence]
expected_context: [level-0, execution-contract, final-quality-gate, final-review]
success_conditions: [all-gates-pass, no-blocker, completion-evidence-valid]
failure_conditions: [premature-done, structure-lock-violation]
---

Fixture: `fixtures/locked-project`.
