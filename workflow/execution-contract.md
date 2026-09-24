# Global execution contract

Apply this contract to every task before loading a phase engine.

## Intake and scope

1. Capture the request, explicit scope, phase/mode signal, and project state. For large/complex work, create `TASK-SCOPE.md`; create `CONTEXT-MANIFEST.md` only when its traceability benefit exceeds its cost.
2. Do not expand one-page or visual-only work into unrelated redesign. Record the impact if a shared artifact/component must change.
3. Treat unknown business behavior, permissions, payment logic, approval, backend rules, routes, and APIs as `UNKNOWN` or explicit `ASSUMPTION`; never lock an invention.

## Discovery, reuse, and versions

1. Before creating or reading an artifact, consult the active project artifact registry or discover its equivalent.
2. Reuse a `VALIDATED` artifact; read a `LOCKED` artifact as immutable; update an `ACTIVE` artifact only in its owning phase; send `NEEDS_REVIEW`, `STALE`, or `INVALID` artifacts through impact analysis.
3. Resolve conflicting candidates by `LOCKED > ACTIVE > DRAFT > SUPERSEDED`. The lock’s named version wins over timestamp or filename. Each artifact type has one active version; increment its version in place/registry rather than inventing suffix files.
4. Do not re-analyze validated upstream structure. Trust it unless an observed conflict, stale dependency, invalidation, or user-requested structural change requires escalation.

## Context and routing

Load Level 0 first: `SKILL.md`, routing, this contract. Load Level 1 only for the selected phase: its README/workflow plus relevant transition. Load Level 2 only through a matching reference trigger. Load Level 3 only for a concrete issue, unusual constraint, or explicit request. See [reference-loading.md](reference-loading.md) and [reference-index.md](reference-index.md).

Route through the state machine. Before changing an important artifact, use [change-impact.md](change-impact.md). Phase 1 may not produce final visual styling; Phase 2 may not modify semantic UX structure and must validate Structure Lock before every mode.

For a small task (one page, one form, one component, or minor polish), use the fast path: scope → minimum artifact/lock check → relevant rules → execution → targeted review. Do not generate the full artifact set unless the scope makes it necessary.

## Review, rollback, blocked, completion

Review deltas only: new, unresolved, and regressed issues. Track each issue by type, artifact/page, location, and root cause. If the issue set does not materially improve for two consecutive no-progress iterations, change strategy or enter `BLOCKED`; never repeat an identical fix indefinitely. Use [rollback-matrix.md](rollback-matrix.md), not intuition alone.

A `BLOCKED` record contains reason, blocking issue/fingerprint, affected phase, last valid artifact/version, recommended rollback, and missing input/tool/decision. `DONE` requires applicable phase gates, valid required artifacts, no blocker or unresolved major issue, Structure Lock compliance, and scope coverage. Use `COMPLETION-EVIDENCE.md` for large work.
