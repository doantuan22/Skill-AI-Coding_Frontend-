---
id: E43
name: targeted accessibility rescan
category: accessibility-efficiency
project_state: mobile label fixed after iteration one
user_request: Rescan mobile only.
expected_route: iteration two mobile-only evidence
required_artifacts: [new-axe-file, accessibility-manifest.json]
forbidden_behavior: [full-unneeded-rescan, relabel-old-evidence]
expected_context: [targeted-rescan, retention]
success_conditions: [new-mobile-evidence, historical-old-evidence]
failure_conditions: [stale-evidence-accepted]
---
