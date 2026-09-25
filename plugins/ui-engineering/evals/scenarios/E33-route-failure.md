---
id: E33
name: Route failure
category: runtime-render
project_state: target route returns 404 or blank render
user_request: Capture the failed route and one independent valid route.
expected_route: record route error; preserve independent evidence; PARTIAL or FAILED
required_artifacts: [manifest.json, execution-report.json]
forbidden_behavior: [capture-failed-route-as-success, visual-pass]
expected_context: [runtime-runner, browser-contract, runtime-errors]
success_conditions: [error-structured, failed-capture-not-captured, honest-status]
failure_conditions: [false-runtime-pass, evidence-mismatch]
---

Fixture: `runtime-fixtures/broken-route`.

