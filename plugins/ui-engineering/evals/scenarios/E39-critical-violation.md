---
id: E39
name: critical violation
category: accessibility-gate
project_state: axe critical finding
user_request: Finalize page.
expected_route: evidence → gate FAIL → DONE forbidden
required_artifacts: [accessibility-manifest.json, ACCESSIBILITY-REPORT]
forbidden_behavior: [dismiss-critical, done]
expected_context: [issue-model, accessibility-gate]
success_conditions: [critical-preserved, gate-fail]
failure_conditions: [gate-bypass]
---
