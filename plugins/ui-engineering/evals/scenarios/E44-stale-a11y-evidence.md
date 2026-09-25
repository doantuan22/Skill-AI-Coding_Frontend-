---
id: E44
name: stale accessibility evidence
category: accessibility-staleness
project_state: page/component changed after prior scan
user_request: Finalize changed page.
expected_route: mark old evidence stale and require rescan
required_artifacts: [change-impact, ACCESSIBILITY-REPORT]
forbidden_behavior: [use-old-scan-for-gate]
expected_context: [change-impact, accessibility-gate]
success_conditions: [rescan-required]
failure_conditions: [stale-evidence-accepted]
---
