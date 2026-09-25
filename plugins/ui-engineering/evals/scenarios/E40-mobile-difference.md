---
id: E40
name: mobile-only accessibility difference
category: viewport-accessibility
project_state: desktop scan clear mobile violation
user_request: Check responsive page.
expected_route: viewport-specific evidence and unresolved mobile gate impact
required_artifacts: [per-viewport-axe-evidence]
forbidden_behavior: [desktop-pass-implies-mobile-pass]
expected_context: [viewport-registry, axe-runtime]
success_conditions: [mobile-finding-preserved]
failure_conditions: [wrong-viewport]
---
