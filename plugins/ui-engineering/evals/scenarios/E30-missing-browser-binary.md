---
id: E30
name: Missing Playwright browser binary
category: runtime-preflight
project_state: Playwright package present but browser launch unavailable
user_request: Capture one page.
expected_route: detector/preflight → BLOCKED with PLAYWRIGHT_BROWSER_UNAVAILABLE
required_artifacts: [execution-report.json]
forbidden_behavior: [playwright-install, browser-download, completed-status]
expected_context: [capability-detector, runtime-runner, runtime-errors]
success_conditions: [blocked-honest, no-auto-download]
failure_conditions: [auto-install-violation, false-runtime-pass]
---

Fixture: `runtime-fixtures/playwright-ready`.

