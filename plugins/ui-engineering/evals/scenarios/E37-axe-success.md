---
id: E37
name: axe available successful scan
category: accessibility-runtime
project_state: local Playwright and axe available
user_request: Scan accessible page.
expected_route: axe scan → COMPLETED manifest → manual gate still required
required_artifacts: [accessibility-manifest.json]
forbidden_behavior: [overall-pass-from-axe-alone]
expected_context: [accessibility-capability, axe-runtime]
success_conditions: [scan-evidence, no-critical-serious, automated-completed]
failure_conditions: [accessibility-false-pass]
---
