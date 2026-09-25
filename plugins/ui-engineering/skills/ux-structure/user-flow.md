# User flow engine

Create `UX-FLOW.md` for each important journey. A flow has an ID, actor, entry point, intention, ordered steps, decisions, system responses, success exit, failure exit, and links to affected pages and use cases.

Model the happy path plus applicable alternative, error, empty, permission, and cancellation paths. Branches must name the next state; a sequence such as `A → B → C` without decisions or outcomes is insufficient. Use [references/feedback-states.md](references/feedback-states.md) when interaction outcomes need a shared pattern.
