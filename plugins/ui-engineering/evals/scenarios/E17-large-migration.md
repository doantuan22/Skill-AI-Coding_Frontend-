---
id: E17
name: Large visual migration
category: migration
project_state: inconsistent-project with 30 pages
user_request: Migrate the application to a consistent design system.
expected_route: PHASE_2 / MIGRATE_EXISTING with representative pages and batches
required_artifacts: [CURRENT-DESIGN-SYSTEM, DESIGN-DIRECTION, DESIGN-SYSTEM, DESIGN-TOKENS, IMPLEMENTATION-MAP, FINAL-QUALITY-REPORT]
forbidden_behavior: [rewrite-all-at-once, migrate-without-representative-page, no-cross-page-review]
expected_context: [level-0, phase-2-router, chunking-strategy, design-system, selected-page-references]
success_conditions: [global-system, representative-pages, batch-handoffs, cross-page-qa]
failure_conditions: [unbounded-context, visual-drift, lock-violation]
---

Fixture: `fixtures/inconsistent-project`.

