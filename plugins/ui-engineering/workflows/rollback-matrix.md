# Rollback matrix

| Issue | Owner / rollback state | Required action |
|---|---|---|
| Wrong actor, permission, use case, business rule, required data, route/API semantics | Phase 1 | Stop Phase 2 decision; impact analysis; review and issue a new lock. |
| Missing page, page responsibility, flow conflict, navigation conflict | Phase 1 | Update structural artifacts and rerun Phase 1 review. |
| Invalid/missing Structure Lock for full Phase 2 | Phase 1 or `BLOCKED` | Route to Phase 1; block if requirements cannot support it. |
| Token inconsistency, component visual defect, responsive bug, visual drift | Phase 2 | Refine using current lock and rerun targeted Phase 2 review. |
| Accessibility defect without semantic change | Phase 2 | Correct realization and rerun relevant QA. |
| Upstream artifact stale after requirement change | Owning upstream phase | Mark impact, revalidate downstream, then rerun affected review. |
| No review progress / repeated issue | `BLOCKED` | Change strategy once; block after two no-progress iterations. |
| Missing input, tool, evidence, or contradictory requirement | `BLOCKED` | Record missing item and recommended resume state. |
