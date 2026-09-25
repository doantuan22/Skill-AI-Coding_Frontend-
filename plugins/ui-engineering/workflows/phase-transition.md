# Phase transitions and rollback

## Required transitions

```text
INITIAL → ANALYZING → PHASE_1 → PHASE_1_REVIEW
PHASE_1_REVIEW (fail) → PHASE_1
PHASE_1_REVIEW (pass) → STRUCTURE_LOCKED → PHASE_2 → PHASE_2_REVIEW
PHASE_2_REVIEW (fail) → PHASE_2
PHASE_2_REVIEW (pass) → FINAL_REVIEW
FINAL_REVIEW (fail: implementation) → PHASE_2
FINAL_REVIEW (fail: structure) → PHASE_1
FINAL_REVIEW (pass) → DONE
```

Every non-`DONE` state may transition to `BLOCKED`. A blocked record must name the reason, evidence, affected artifacts, owner or required decision, and the state to resume from.

## Phase 1 to Structure Lock

Enter `PHASE_1_REVIEW` only when the router-selected artifacts are active, including `UX-FLOW.md`, `PAGE-MAP.md`, `WIREFRAME-SPEC.md`, and `DESIGN-BRIEF.md` for a normal structural handoff. `REQUIREMENT-SPEC.md`, a traceability record, and conditional actor/use-case/IA/navigation/page/component/state artifacts are required whenever their scope is present. On a passing review, create or update `STRUCTURE-LOCK.md`, set its status to `locked`, record the exact active artifact versions, and protect those versions. Only then enter `STRUCTURE_LOCKED`.

## Structure Lock to Phase 2

Enter Phase 2 only when the lock is active, names all required Phase 1 artifacts, and has no unresolved protected requirement. Phase 2 reads the locked Design Brief, Page Map, Page Spec, Wireframe Spec, Component Map, State Map, and Navigation Map or declared merged equivalents. It may refine visual or frontend realization that conforms to the lock. It must not change actors, use cases, business flows, pages, important business fields, routes, or APIs for aesthetic reasons.

## Rollback behavior

- A Phase 1 review failure returns to `PHASE_1`; revise the artifact that Phase 1 owns, increment its version, and review again.
- A Phase 2 review failure returns to `PHASE_2` when the lock remains satisfied.
- A Phase 2 or final review finding that changes structure returns to `PHASE_1`; supersede the old lock after a new Phase 1 review and issue a new lock version.
- Missing inputs, conflicting requirements, invalid locks, or unavailable project evidence go to `BLOCKED`. Do not proceed until resolution determines a valid resume state.
