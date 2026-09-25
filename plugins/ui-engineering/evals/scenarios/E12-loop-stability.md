---
id: E12
name: Unresolvable review issue
category: loop-protection
project_state: simple-project
user_request: Complete a task with a requirement conflict that cannot be resolved from available context.
expected_route: relevant phase review then BLOCKED by max/no-progress rule
required_artifacts: [PHASE-1-REVIEW-or-PHASE-2-REVIEW, BLOCKED-REPORT]
forbidden_behavior: [infinite-loop, repeated-identical-fix, DONE]
expected_context: [level-0, execution-contract, review-file, rollback-matrix]
success_conditions: [iteration-tracked, issue-fingerprint, blocked-with-resume-condition]
failure_conditions: [loop-failure, premature-done]
---

Fixture: `fixtures/simple-project`.

