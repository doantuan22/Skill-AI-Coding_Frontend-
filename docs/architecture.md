# Architecture

The skill is deliberately split into orchestration, phase ownership, review gates, templates, and supporting documentation.

```text
SKILL.md (entry point and controller)
├─ workflow/ (routing, state, transitions, contracts, execution hardening)
├─ phase-1/ (router, UX structure engine, selectively loaded references)
├─ phase-2/ (router, eight frontend design engines, visual language, design inspiration,
│            typography, motion, web patterns, design knowledge system, capability resolver;
│            all selectively loaded)
├─ review/ (gate-specific loops)
├─ templates/ (artifact shapes and hardening records)
├─ evals/ (agent-agnostic evaluation framework and fixtures)
├─ execution/ (capability-driven rendered UI verification contracts)
├─ uiux/ (platform-neutral Python core: core foundation, knowledge, engine, runtime, evals, tooling, Core API)
├─ scripts/ (backward-compatible CLIs + unified CLI scripts/uiux_cli.py)
├─ plugin/ (plugin layer: manifest, adapters, packaging boundary; the core never depends on it)
└─ tests/ (standard-library test suite; not packaged)
```

`SKILL.md` remains a router. Each operational state loads only the relevant file(s), which keeps context narrow and makes future specialization additive. `workflow/` is the source of truth for lifecycle behavior; phase folders define responsibilities without embedding specialist methods; review files define gates; templates carry stable handoff metadata.

Phase 1 begins with [phase-1/router.md](../phase-1/router.md), which classifies the task and selects the smallest sufficient artifact set and relevant references. Its ordered engine is documented in [phase-1/workflow.md](../phase-1/workflow.md). This keeps page-type guidance out of the base context while preserving a structured path from normalized requirement to actors, use cases, IA, navigation, flows, page specifications, components, states, wireframes, review, brief, and lock.

Phase 2 begins with [phase-2/router.md](../phase-2/router.md), which validates the Structure Lock, classifies visual work, identifies the frontend stack, and selects relevant engines and references. Its eight engines progress from direction and design intelligence to system/tokens, components, stack-conforming implementation, responsive interaction, visual QA, and final quality gating. The full operating model is in [docs/phase-2.md](phase-2.md).

The central invariant is the structure lock: Phase 1 produces and owns structural decisions, then the lock freezes their active versions for Phase 2. If later work needs a structural change, workflow rolls back to Phase 1 and issues a new lock after review. This preserves a one-way artifact dependency graph and prevents Phase 2 from bypassing UX structure.

The execution hardening layer runs after routing and before phase work. It selects minimum sufficient context, resolves active/locked artifacts, prevents duplicate creation and re-analysis, detects stale downstream work, constrains scope, and protects review loops/completion. The evaluation layer is agent-agnostic: fixtures and E01–E28 scenarios test workflow and execution contracts without requiring a browser runtime. See [docs/hardening.md](hardening.md) and [evals/README.md](../evals/README.md).

The execution layer is selected only for rendered UI work when capability warrants it. It is independent of any agent API: adapters implement a browser contract, Playwright is reused only when already present, and manual fallback reports limitation honestly. Evidence flows into Phase 2 visual review and the final quality gate. See [docs/execution-layer.md](execution-layer.md).

Browser runtime evidence may feed the accessibility runtime: local axe scan evidence plus manual review flows through the Accessibility Gate before Final Quality Gate. It reuses execution session/server/viewport contracts and does not create a second browser lifecycle. See [docs/accessibility-runtime.md](accessibility-runtime.md).

The Design Knowledge System adds a knowledge layer (structured, schema-validated catalogs), a reasoning bridge (Capability Resolver), implementation intelligence (technology resolver, performance budget) and outcome evaluation (E65–E80 with a static analyzer and optional runtime motion probes). See [design-knowledge-system.md](design-knowledge-system.md).

The repository is plugin-ready: a layered `uiux` package exposes a public Core API, knowledge and tool registries, and portable resource discovery and configuration, while `plugin/` holds only integration metadata. See [plugin-architecture.md](plugin-architecture.md).
