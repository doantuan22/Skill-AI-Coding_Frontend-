---
id: E21
name: Existing Playwright setup
category: execution-capability
project_state: execution-playwright-project
user_request: Verify a rendered page after a visual update.
expected_route: PHASE_2 execution request / existing Playwright adapter
required_artifacts: [TOOL-CAPABILITY-MANIFEST, EXECUTION-REPORT, VISUAL-REVIEW]
forbidden_behavior: [npm-install-playwright, overwrite-config, create-new-e2e-framework]
expected_context: [level-0, execution-detection, execution-router, playwright-adapter]
success_conditions: [playwright-detected, existing-config-reused, no-install]
failure_conditions: [unnecessary-tool-install, capability-misdetection]
---

Fixture: `fixtures/execution-playwright-project`.

