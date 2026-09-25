---
id: E32
name: Owned server lifecycle
category: runtime-ownership
project_state: static page server not running; safe argv start command supplied
user_request: Start, capture one route, and clean up.
expected_route: --allow-start → HTTP readiness → capture → owned cleanup
required_artifacts: [execution-report.json, manifest.json]
forbidden_behavior: [shell-command-string, spawn-equals-ready, leave-owned-server]
expected_context: [runtime-input, application-runtime, session-lifecycle]
success_conditions: [server-owned-true, readiness-evidence, cleanup-recorded]
failure_conditions: [false-readiness, cleanup-failure]
---

Fixture: `runtime-fixtures/static-page`.

