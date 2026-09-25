# Phase 1 workflow

Use this sequence as a dependency order; omit or merge optional artifacts only when [router.md](router.md) permits it.

```text
Requirement normalizer → project / current-UX extractor → actors → use cases
→ decision prompts → IA → navigation → flows → pages → page specs
→ component structure → state model → wireframes → anti-pattern check
→ Phase 1 review → design brief → structure lock
```

## Core steps

| Step | Load | Produce or update | Decision gate |
|---|---|---|---|
| Normalize | [requirement-analysis.md](requirement-analysis.md) | `REQUIREMENT-SPEC.md` | Unknown business rules remain explicit. |
| Understand current state | [current-ux-extraction.md](current-ux-extraction.md) when existing UI exists | `CURRENT-UX-MAP.md` | Record structure; do not assess visual style. |
| Model users and intent | [actor-analysis.md](actor-analysis.md), [use-case-mapping.md](use-case-mapping.md) | `ACTOR-MAP.md`, `USE-CASE-MAP.md` | Each required goal has an accountable actor. |
| Model system structure | [information-architecture.md](information-architecture.md), [user-flow.md](user-flow.md) | IA, navigation, flow maps | Required flows include non-happy paths. |
| Specify screens | [page-architecture.md](page-architecture.md), [component-structure.md](component-structure.md), [state-model.md](state-model.md), [wireframe-engine.md](wireframe-engine.md) | Page, component, state, wireframe artifacts | Every page has one clear responsibility. |
| Verify and hand off | [../review/phase-1-review.md../../review/phase-1-review.md, [structure-lock.md](structure-lock.md) | Review, brief, lock | No blocker or unresolved major structural issue. |

For a project with 30+ pages, multiple roles, or complex flows, establish global IA and navigation first, then process one role, domain, or flow at a time. Run cross-flow consistency before the final Phase 1 review. A small project may merge Actor + Use Case, Page Map + Navigation, or Page Spec + Wireframe, but must retain their information and traceability.
