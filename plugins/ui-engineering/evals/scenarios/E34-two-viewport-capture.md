---
id: E34
name: Desktop and mobile capture
category: runtime-evidence
project_state: working static page and Playwright runtime
user_request: Capture one page at desktop and mobile.
expected_route: viewport loop produces two deterministic PNG records
required_artifacts: [manifest.json, execution-report.json]
forbidden_behavior: [raw-unnamed-viewport, missing-dimension-metadata]
expected_context: [runtime-input, viewport-registry, evidence-schema]
success_conditions: [two-files, desktop-mobile-dimensions-correct, manifest-valid]
failure_conditions: [wrong-viewport, missing-evidence]
---

Fixture: `runtime-fixtures/requests/two-viewports.json`.

