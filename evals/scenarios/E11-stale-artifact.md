---
id: E11
name: Stale downstream artifacts
category: change-impact
project_state: locked-project with requirement changed from v2 to v3
user_request: Add a new required booking constraint after Structure Lock.
expected_route: impact analysis then PHASE_1 review and new Structure Lock
required_artifacts: [ARTIFACT-REGISTRY, CHANGE-IMPACT, PHASE-1-REVIEW, STRUCTURE-LOCK-new-version]
forbidden_behavior: [reuse-stale-page-spec, continue-phase-2, silently-update-lock]
expected_context: [level-0, execution-contract, change-impact, rollback-matrix]
success_conditions: [downstream-needs-review, stale-detected, rerun-gate]
failure_conditions: [stale-artifact-usage, lock-violation]
---

Fixture: `fixtures/locked-project`.

