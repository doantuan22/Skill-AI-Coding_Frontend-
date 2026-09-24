---
id: E22
name: Browser capability without Playwright
category: execution-strategy
project_state: locked-project with agent browser capability and no Playwright
user_request: Inspect a responsive visual update.
expected_route: PHASE_2 execution request / existing browser-tool strategy
required_artifacts: [TOOL-CAPABILITY-MANIFEST, EXECUTION-REPORT, VISUAL-REVIEW]
forbidden_behavior: [install-playwright, change-package-json, fake-fallback]
expected_context: [level-0, execution-detection, execution-router, browser-contract]
success_conditions: [browser-tool-selected, evidence-plan, no-install]
failure_conditions: [unnecessary-tool-install, wrong-strategy]
---

Fixture: `fixtures/locked-project`.

