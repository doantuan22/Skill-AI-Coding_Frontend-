---
id: E36
name: Targeted mobile recapture
category: runtime-efficiency
project_state: iteration one has desktop/mobile evidence; code changed for mobile only
user_request: Recapture only mobile after the fix.
expected_route: iteration two request includes only mobile; old desktop remains historical
required_artifacts: [runtime-input, manifest.json, execution-report.json]
forbidden_behavior: [accept-stale-desktop-as-new, recapture-all-without-reason]
expected_context: [runtime-input, targeted-recapture-rule, evidence-retention]
success_conditions: [only-mobile-new-capture, old-evidence-not-relabeled]
failure_conditions: [stale-evidence-accepted, unnecessary-viewport-sweep]
---

Fixture: `runtime-fixtures/requests/two-viewports.json` with iteration two/mobile-only override.
