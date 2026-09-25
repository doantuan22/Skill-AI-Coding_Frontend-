# Workflow overview

This workflow separates decisions about product structure from decisions about visual and frontend realization. It operates as a gated state machine, not as a linear checklist: reviews may return work to the phase that owns the issue.

```text
User requirement
  → analysis
  → Phase 1: UX / structure
  → Phase 1 review
  → structure lock
  → Phase 2: frontend / visual design
  → Phase 2 review
  → final review
  → done
```

Phase 1 owns structural artifacts. Phase 2 consumes their locked version and owns implementation-facing artifacts. The review stages validate the handoff; the structure lock makes it explicit and auditable.

Read [routing.md](routing.md) to choose the start, [state-machine.md](state-machine.md) for the lifecycle, [artifact-contract.md](artifact-contract.md) for ownership, and [phase-transition.md](phase-transition.md) before crossing a gate.

