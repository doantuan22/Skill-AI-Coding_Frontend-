# Routing

Start by inventorying the project, its active artifact versions, and any structure lock. Never infer a bypass from the presence of implementation files alone.

| Situation | Route | Gate |
|---|---|---|
| Completely new project | `INITIAL → ANALYZING → PHASE_1` | Requirements and project context must be available. |
| Existing UX structure, no visual/frontend delivery | `ANALYZING → PHASE_2` | All required Phase 1 artifacts and a valid current structure lock must exist. Otherwise route to `PHASE_1`. |
| Existing UI that needs redesign | `ANALYZING → PHASE_1` | Review the existing structure before visual work; issue a new lock after Phase 1 review. |
| Completed UI requiring audit only | `ANALYZING → FINAL_REVIEW` | Existing output, relevant lock, and sufficient evidence must be available. If the audit finds structural issues, roll back to `PHASE_1`. |
| Small visual-only adjustment | `ANALYZING → PHASE_2` | Confirm it stays within the active structure lock. If not, route to `PHASE_1`. |

If requirements conflict, required artifacts are absent, versions are ambiguous, a lock is invalid, the project cannot be evaluated, or Phase 2 reveals a business change, enter `BLOCKED`, record the issue, then follow the rollback behavior in [phase-transition.md](phase-transition.md).

