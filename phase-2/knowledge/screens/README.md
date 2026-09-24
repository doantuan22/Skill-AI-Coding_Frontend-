# Screen Pattern Library

Knowledge about common screen types: reference anatomy, hierarchy, actions, states, layout, interaction, motion, responsive and accessibility behavior, common mistakes and variants.

## Phase boundary

- **Phase 1 owns the locked anatomy.** Which regions, fields, actions and states a screen has is decided in Phase 1 (`PAGE-SPEC`, `WIREFRAME-SPEC`, `STATE-MAP`). Where a Phase 1 reference exists (`phase_1_reference`), it is the structural source; the anatomy here is a checklist, not an override.
- **Phase 1 may consult** the `anatomy`, `hierarchy`, `primary_actions` and `states` fields for screen types that have no Phase 1 reference (e.g., AI copilot, kanban). This is read-only.
- **Phase 2 uses** `layout`, `interaction`, `motion`, `responsive`, `accessibility`, `compatible_layouts`, `key_interactions` and `key_motion` to realize the locked screen. Adding or removing regions or actions in Phase 2 is a rollback request, not a pattern choice.

| File | Screens |
|---|---|
| [app-core.md](app-core.md) | dashboard, analytics, workspace, admin, list, detail, data table, kanban, calendar, file browser, editor |
| [account-commerce.md](account-commerce.md) | settings, onboarding, authentication, profile, billing, pricing, checkout, notifications, activity |
| [search-ai.md](search-ai.md) | search, command palette, chat, AI chat, AI copilot |
| [states.md](states.md) | empty state, error state, loading state |

Schema: [schema.md](../schema.md#screen).
