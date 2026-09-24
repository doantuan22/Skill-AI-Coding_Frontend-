# Reference loading

## Levels

| Level | Load | Rule |
|---|---|---|
| 0 — Core | `SKILL.md`, routing, execution contract | Start here; never scan the full skill for orientation. |
| 1 — Phase | Selected phase README/workflow and relevant state/transition | Load after routing only. |
| 2 — Domain | A specific forms, tables, dashboard, navigation, token, or QA reference | Require a router/task trigger. |
| 3 — Deep | Narrow reference for an explicit issue, exception, or user request | Load only after lower levels cannot resolve it. |

Record a manifest for large work: core files, active artifacts, selected references, excluded references, and why. Do not create a manifest for a small task unless it prevents a real ambiguity.

## Trigger rule

Use [reference-index.md](reference-index.md) instead of scanning reference directories. A reference is loaded only when its trigger is present; listed exclusions are positive reasons not to load it. Reuse the current manifest/phase context within a batch and do not reread confirmed artifacts without an invalidation signal.
