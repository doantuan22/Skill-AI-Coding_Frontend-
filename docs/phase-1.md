# Phase 1 operation

Phase 1 starts by loading `SKILL.md`, `phase-1/README.md`, and `phase-1/router.md`. The router classifies the task as new UI, existing UI, redesign, extension, migration, or audit; it records project size, selected artifacts, relevant references, assumptions, and open questions. Existing interfaces first receive an observational `CURRENT-UX-MAP.md`.

Context is progressively loaded. The engine loads core modules in dependency order and only the page-type references that match the work; for example, a booking form uses form and checkout guidance while a dashboard uses dashboard, table, and navigation guidance. It never loads the entire reference directory merely because Phase 1 starts.

Artifacts flow from normalized requirements through actors/use cases, IA/navigation, flows, pages, components/states/wireframes, and traceability. The router may merge artifacts for a small scope, but all selected relationships must remain explicit. Large work is partitioned by role, domain, or flow after global IA/navigation, then checked for cross-flow and terminology consistency.

The Phase 1 review uses a documented three-iteration maximum. It passes only with no blockers or unresolved major structural issues, complete required use-case/state coverage, and a valid artifact contract. Pass produces a Design Brief and Structure Lock. The lock lists exact active artifact versions and protected semantics; Phase 2 receives those locked artifacts and may refine visual realization only, returning structural discoveries to Phase 1.
