# State machine

`BLOCKED` is an interrupt state reachable whenever a required input is missing, contradictory, invalid, or cannot be verified. It is not a substitute for ignoring a gate.

| State | Enter when | Required active artifacts | Leave when | Next state / rollback |
|---|---|---|---|---|
| `INITIAL` | Work is received and no workflow state is established. | User task or project context. | Initial context can be inspected. | `ANALYZING`; `BLOCKED` if context is unavailable. |
| `ANALYZING` | Initial context is available. | Project context; inventory of existing artifacts. | A valid route and required inputs are identified. | `PHASE_1`, `PHASE_2`, or `FINAL_REVIEW` as routing permits; `BLOCKED`. |
| `PHASE_1` | New structure is required, or structural change was requested. | Requirements; router-selected Phase 1 artifacts. | Baseline handoff plus all scope-required supporting artifacts are ready for review. | `PHASE_1_REVIEW`; `BLOCKED`. |
| `PHASE_1_REVIEW` | Phase 1 handoff set exists. | Baseline and router-selected supporting artifacts; review record. | Review passes within three automatic iterations or identifies an owner/action. | pass: `STRUCTURE_LOCKED`; fail: `PHASE_1`; `BLOCKED` if unresolved. |
| `STRUCTURE_LOCKED` | Phase 1 review passed and the lock contract is issued. | Valid active `STRUCTURE-LOCK.md` plus locked Phase 1 artifacts. | Phase 2 work is authorized. | `PHASE_2`; structural change: `PHASE_1`; invalid lock: `BLOCKED`. |
| `PHASE_2` | Valid structure lock exists. | Structure lock; referenced locked artifacts; router-selected direction/system/implementation artifacts. | Rendered output and required Phase 2 evidence are ready for review. | `PHASE_2_REVIEW`; structural discovery: `PHASE_1`; `BLOCKED`. |
| `PHASE_2_REVIEW` | Phase 2 output is available. | Structure lock; router-selected Phase 2 artifacts; rendered implementation; review evidence. | Review and final quality gate pass or identify an owner/action. | pass: `FINAL_REVIEW`; fail: `PHASE_2`; structural issue: `PHASE_1`; `BLOCKED`. |
| `FINAL_REVIEW` | Phase 2 review passed or an audit is validly routed here. | Structure lock, Phase 2 output, final-review record. | Final review records a pass or actionable result. | pass: `DONE`; implementation issue: `PHASE_2`; structural issue: `PHASE_1`; `BLOCKED`. |
| `DONE` | Final review passed. | `FINAL-REVIEW.md` with status `passed`. | A new request changes scope. | Small visual-only change: `PHASE_2`; structural change: `PHASE_1`. |
| `BLOCKED` | A contract cannot be met. | Blocker record: reason, issue fingerprint, affected phase, last valid artifact/version, evidence, rollback target, and missing input/tool/decision. | Missing or conflicting input is resolved and route re-evaluated. | The documented rollback target; normally `ANALYZING`, `PHASE_1`, or `PHASE_2`. |

When resuming from `BLOCKED`, retain valid artifacts but revalidate their versions and lock status before progressing.
