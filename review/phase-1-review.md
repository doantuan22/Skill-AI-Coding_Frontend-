# Phase 1 review loop

Run this loop after the router-selected artifacts exist:

```text
Build → self review → issue detection → classify → refine → review again
```

Use `PHASE-1-REVIEW.md` to record each iteration. Review requirement coverage, actor coverage, use-case coverage, flow completeness, IA, navigation, page responsibility, action hierarchy, content hierarchy, state coverage, error and empty paths, business constraints, component reuse, complexity, cognitive load, and consistency.

Classify findings as `BLOCKER`, `MAJOR`, `MINOR`, or `NOTE`. A blocker is a missing required use case, invalid contract, unresolvable requirement conflict, or issue that prevents a safe handoff. A major is an unresolved structural issue, such as an unrecoverable failure path. Minor issues may remain documented only when they do not affect required flows or the artifact contract.

The loop passes only when there is no blocker, no unresolved major structural issue, required use cases and states are covered, and the contract is valid. At most three automatic structural iterations are allowed. If a blocker remains after iteration three, enter `BLOCKED`, record the reason/evidence/affected artifacts, and name the rollback state. A passing review authorizes the design brief and Structure Lock; a failed review returns to `PHASE_1`.
