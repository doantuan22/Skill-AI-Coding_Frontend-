# Phase 1 — UX structure engine

## Responsibility

Convert user requirements and existing project context into a reviewable, traceable structural handoff. This phase owns the decisions that the structure lock protects: actors, use cases, critical flows, pages, page responsibilities, sections, actions, states, required data, navigation relationships, and confirmed business constraints.

## Entry condition

The router has selected `PHASE_1`, and requirements plus enough project context to create the handoff are available.

## Inputs

- Raw user requirements
- Existing project context and relevant active artifacts, when present
- An active structure lock for an extension, when present

## Outputs

- A normalized requirement specification, then only the artifacts selected by [router.md](router.md)
- The required Phase 1 baseline: `UX-FLOW.md`, `PAGE-MAP.md`, `WIREFRAME-SPEC.md`, and `DESIGN-BRIEF.md`
- Supporting maps when needed: actors, use cases, IA, navigation, page specs, component map, state map, traceability matrix, current UX map, terminology registry, and review record

## Exit condition

All required outputs exist at active versions, traceability is sufficient for the selected scope, and Phase 1 review passes within three automatic structural iterations. The workflow can then create `STRUCTURE-LOCK.md`.

## Working method

1. Start with [router.md](router.md), normalize requirements, and inspect existing UX when applicable.
2. Progress through [workflow.md](workflow.md), loading a module only when its decision is needed.
3. Use templates as structured contracts, with stable IDs and explicit relationships rather than narrative-only output.
4. Review with [../review/phase-1-review.md](../review/phase-1-review.md), then issue the lock through [structure-lock.md](structure-lock.md).

Phase 1 does not perform visual design, CSS/frontend work, responsive implementation, visual testing, or accessibility implementation details.
