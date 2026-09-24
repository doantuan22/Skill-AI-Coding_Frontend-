# Phase 1 router

Inspect requirements, project context, active artifact versions, and any structure lock. Select one task path before loading specialized references.

| Task type | Starting work | Minimum artifact set | Typical references |
|---|---|---|---|
| `NEW_UI` | Normalize → actors → IA → flows → pages | Requirement, actors/use cases as needed, flows, pages, wireframes, brief | `information-architecture`, `navigation`, plus page-type references |
| `EXISTING_UI` | Extract current UX → normalize delta → audit or rebuild | Current UX map, requirement, impacted maps | `navigation`, `anti-patterns`, relevant page-type references |
| `REDESIGN` | Extract → audit structural gaps → rebuild impacted structure | Current UX map, impacted flows/pages, review | Relevant page-type references and `anti-patterns` |
| `EXTEND` | Read lock → add use case → update impacted artifacts | Requirement delta, impacted maps, new lock version | References for added page or flow type |
| `MIGRATION` | Extract all structure → normalize → model and lock | Current UX map, core maps, review | `navigation`, `information-architecture`, relevant types |
| `AUDIT` | Extract → review → issue report | Current UX map, review record | `anti-patterns` and relevant types |

## Reference selection

Load `references/decision-prompts.md`, `principle-cards.md`, `anti-patterns.md`, and `wireframe-rules.md` only at their relevant decision or review step. Load exactly the page-type reference needed:

| Signal | Load |
|---|---|
| Form, registration, data collection | `forms.md`; add `onboarding.md` for first-use setup |
| Search, filtering, discovery | `search-filter.md` |
| Data list, bulk actions, operational records | `tables.md` |
| Status overview, monitoring, prioritization | `dashboard.md` |
| Purchase, booking, payment, confirmation | `checkout.md` |
| Account or preference management | `settings.md` |
| Destructive operation | `destructive-actions.md` |
| Important feedback, errors, permissions | `feedback-states.md` |

If an artifact, lock, or requirement is ambiguous, enter `BLOCKED` rather than guessing. Router output should state task type, project size, selected artifacts, selected references, assumptions, and unresolved questions.
