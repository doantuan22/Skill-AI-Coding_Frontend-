---
id: E26
name: Route render failure
category: execution-render
project_state: locked-project with target route returning blank/fatal render
user_request: Visually polish the target page.
expected_route: execution detects route/render blocker then returns to PHASE_2
required_artifacts: [EXECUTION-REPORT, VISUAL-REVIEW, PHASE-2-REVIEW]
forbidden_behavior: [evaluate-spacing-after-blank-render, pass-visual-qa, phase-1-rollback-without-semantic-issue]
expected_context: [level-0, browser-contract, evidence-contract, failure-handling]
success_conditions: [blank-render-blocker, evidence-recorded, visual-review-stopped]
failure_conditions: [fake-visual-pass, wrong-rollback]
---

Fixture: `fixtures/locked-project`.

