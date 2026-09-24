---
name: ui-ux-workflow
description: Orchestrate a two-phase web UI/UX delivery workflow with structure locking, artifact contracts, and review gates. Use for new interface work, redesigns, or UI audits; do not use it for standalone visual styling guidance.
---

# UI/UX Workflow Engine

## Purpose and role

Act as the workflow controller for web UI/UX work. Establish the project state, select a valid entry point, and preserve the boundary between UX structure and visual/frontend delivery. Phase 1 defines the complete structural handoff; Phase 2 remains out of scope for structural decisions.

## Operating loop

1. Inspect the project and active artifacts.
2. Read [workflow/execution-contract.md](workflow/execution-contract.md) and [workflow/routing.md](workflow/routing.md) to select an entry state.
3. Follow [workflow/state-machine.md](workflow/state-machine.md) and load the relevant phase or review file.
4. Create or update only artifacts authorized for that state, using the templates as starting points.
5. Run the state-specific review loop and apply [workflow/phase-transition.md](workflow/phase-transition.md).
6. Stop at `BLOCKED` when a required contract cannot be satisfied; record the reason and rollback target.

The valid happy path is `INITIAL → ANALYZING → PHASE_1 → PHASE_1_REVIEW → STRUCTURE_LOCKED → PHASE_2 → PHASE_2_REVIEW → FINAL_REVIEW → DONE`.

## Phase routing and loading

- For routing, load this file and [workflow/routing.md](workflow/routing.md).
- In Phase 1, load [phase-1/router.md](phase-1/router.md) after [phase-1/README.md](phase-1/README.md). The router selects the task path, required artifacts, and only the relevant references; then follow [phase-1/workflow.md](phase-1/workflow.md).
- For the structure gate, load [workflow/phase-transition.md](workflow/phase-transition.md) and [templates/STRUCTURE-LOCK.md](templates/STRUCTURE-LOCK.md).
- In Phase 2, load [phase-2/README.md](phase-2/README.md), the active `STRUCTURE-LOCK.md`, and [phase-2/router.md](phase-2/router.md). The router verifies inputs and selects only the relevant engine modules, artifacts, and references, including Visual Language only when visual behavior/craft is in scope.
- For review, load the applicable file in [review/](review/) and the artifacts it names. For final review, also load [review/final-review.md](review/final-review.md).

Executable tools (capability resolver, knowledge retrieval, technology resolver, quality analyzer, runtime runner, evals, validation) are listed in `uiux/core/tools.json` and run with `python scripts/uiux_cli.py call <tool-id>`; see [docs/plugin-architecture.md](docs/plugin-architecture.md).

Do not load the entire skill directory by default. Detailed contracts are in [workflow/artifact-contract.md](workflow/artifact-contract.md); the architectural rationale is in [docs/architecture.md](docs/architecture.md).

## Global execution invariants

- Load the minimum sufficient context by following [workflow/reference-loading.md](workflow/reference-loading.md); reuse validated artifacts rather than rediscovering them.
- Discover the active artifact before creating a new one. Respect `LOCKED > ACTIVE > DRAFT > SUPERSEDED`, and never create ad-hoc duplicate filenames.
- Keep work within explicit scope. Record unknown business rules as questions or assumptions, not facts.
- Review loops must show material progress. Stop after the configured limit or two consecutive no-progress iterations and enter `BLOCKED` with the required record.
- `DONE` needs gate and scope evidence, not merely valid Markdown or compiling code. See [workflow/execution-contract.md](workflow/execution-contract.md).

For rendered UI changes, decide execution need with [workflow/execution-requirement.md](workflow/execution-requirement.md). Detect capability before choosing strategy, reuse existing browser/runtime tooling before adding anything, and never claim browser verification without actual evidence.

Accessibility is not proven by axe alone. Never install accessibility tooling or fake manual verification; when required, the rendered UI must satisfy the [Accessibility Gate](execution/accessibility/gate.md).

Tokens alone do not define visual quality. Rendered UI must follow an approved Visual Grammar when visual realization changes. Avoid generic AI UI through intentional craft and adversarial review, not blanket style bans; preserve an existing coherent system unless a documented rationale justifies change.

A strong interface needs intentional inspiration, not random styling: select design DNA with [Design Inspiration](phase-2/design-inspiration/README.md), and choose composition from content and product intent via the [Web Pattern Library](phase-2/web-patterns/README.md). References provide design DNA, not templates to clone. Typography is part of product character, not merely font sizing ([Typography Intelligence](phase-2/typography/README.md)). Motion must communicate, orient, or support storytelling, within a budget and with a reduced-motion equivalent ([Motion Engine](phase-2/motion/README.md)).

Design decisions come from the [Design Knowledge System](phase-2/knowledge/README.md) through the [Capability Resolver](phase-2/capability-resolver/README.md): declare brand, product, audience, density, interaction model, content and intensity first, then retrieve only the resolved entries. Every chosen style, layout, motion, interaction, effect and technology needs a *why* and a *why not*. Premium does not mean more effects; prefer the simplest technology that meets the need, and never add a dependency or asset automatically.

## Phase 1 boundary

Phase 1 resolves what exists, why, who uses it, where it lives, how users move through it, what information and actions each screen needs, and what happens next. It creates a specification-driven structural handoff, not visual styling. Do not choose colors, typography, visual effects, CSS, component appearance, or frontend implementation here.

Phase 1 must not invent business rules or change backend, authentication, API, database, or route contracts. Record unsupported assumptions, dependencies, and open questions. Explicit user requirements override general UX recommendations unless they cause a serious logical conflict.

## Non-negotiable gates

- Phase 2 may start only from `STRUCTURE_LOCKED` with a valid, active structure lock.
- A locked structural artifact is not changed in Phase 2. A requested business, actor, flow, page, field, route, or API change returns work to Phase 1.
- A phase exits only after its review passes and its required artifacts exist.
- `DONE` requires a passed final review and `FINAL-REVIEW.md`.

Phase 2 must produce rendered evidence, not merely compiling code. It may return implementation/visual issues to Phase 2, but it must send a semantic, business, flow, actor, permission, required-data, route, or API mismatch back to Phase 1 without editing the lock.
