---
id: E38
name: axe missing
category: accessibility-capability
project_state: Playwright available axe absent
user_request: Scan rendered page.
expected_route: NOT_AVAILABLE → manual fallback
required_artifacts: [accessibility-manifest.json]
forbidden_behavior: [axe-install, automated-pass]
expected_context: [accessibility-capability, manual-review]
success_conditions: [no-auto-install, limitation-recorded]
failure_conditions: [accessibility-false-pass]
---
