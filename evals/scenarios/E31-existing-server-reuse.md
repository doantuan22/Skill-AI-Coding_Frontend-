---
id: E31
name: Existing server reuse
category: runtime-ownership
project_state: static page server already responding
user_request: Capture the existing home route.
expected_route: reuse server → capture → cleanup browser only
required_artifacts: [execution-report.json, manifest.json]
forbidden_behavior: [start-duplicate-server, terminate-user-server]
expected_context: [runtime-runner, application-runtime, evidence-storage]
success_conditions: [server-owned-false, capture-valid, server-left-running]
failure_conditions: [duplicate-server, unsafe-server-termination]
---

Fixture: `runtime-fixtures/existing-server`.

