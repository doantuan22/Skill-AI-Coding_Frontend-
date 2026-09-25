---
id: E29
name: Successful existing Playwright runtime
category: runtime-execution
project_state: playwright-ready static page with known route
user_request: Capture the home page at desktop and mobile.
expected_route: confirmed detector → runtime runner → COMPLETED evidence session
required_artifacts: [runtime-input, manifest.json, execution-report.json]
forbidden_behavior: [install-playwright, modify-config, fake-capture]
expected_context: [capability-detector, runtime-runner, viewport-registry]
success_conditions: [two-captures-exist, manifest-valid, status-completed]
failure_conditions: [false-runtime-pass, evidence-mismatch]
---

Fixture: `runtime-fixtures/playwright-ready`, `runtime-fixtures/static-page`.

