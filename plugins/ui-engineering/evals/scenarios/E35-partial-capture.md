---
id: E35
name: Partial capture preservation
category: runtime-evidence
project_state: desktop capture succeeds and mobile screenshot fails
user_request: Capture desktop and mobile.
expected_route: preserve desktop evidence, record mobile SCREENSHOT_FAILURE, return PARTIAL
required_artifacts: [manifest.json, execution-report.json]
forbidden_behavior: [delete-desktop-evidence, mark-mobile-captured, completed-status]
expected_context: [runtime-runner, evidence-storage, runtime-errors]
success_conditions: [partial-status, completed-evidence-retained, failed-item-explicit]
failure_conditions: [partial-evidence-loss, false-runtime-pass]
---

Fixture: `runtime-fixtures/evidence-valid` adapted with one failed capture.

