---
id: E13
name: Repeated issue fingerprint
category: loop-protection
project_state: locked-project
user_request: Resolve a responsive issue that reappears after the same attempted fix.
expected_route: PHASE_2 targeted review then strategy change or BLOCKED
required_artifacts: [VISUAL-REVIEW, PHASE-2-REVIEW, BLOCKED-REPORT-if-no-progress]
forbidden_behavior: [repeat-same-fix-indefinitely, ignore-regression]
expected_context: [level-0, execution-contract, phase-2, responsive-review]
success_conditions: [fingerprint-compared, progress-delta-recorded, strategy-changed]
failure_conditions: [loop-failure, unresolved-blocker-hidden]
---

Fixture: `fixtures/locked-project`.

