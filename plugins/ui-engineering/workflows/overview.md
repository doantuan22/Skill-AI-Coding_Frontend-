# Workflow Overview

This workflow provides a unified UI Orchestrator that routes between two dedicated tracks based on the detected UI state:

1. **Greenfield UI Workflow** ([greenfield-workflow.md](greenfield-workflow.md)): Used for brand-new applications or rebuilding from scratch. AI exercises grounded design freedom (domain, target users, density) unless explicit constraints are provided. Multi-page builds require page inventory and UX flow prior to implementation.
2. **Existing UI/UX Workflow** ([existing-ui-workflow.md](existing-ui-workflow.md)): Used when UI components, layouts, or stylesheets exist. Strictly enforces **PRESERVE FIRST → IMPROVE SECOND → REDESIGN ONLY WHEN EXPLICITLY REQUESTED**. Employs the L1/L2/L3 change budget model and granular permission enforcement ([preservation-rules.md](preservation-rules.md)).

```text
User Request
    ↓
UI Orchestrator (inspects repo, determines UI state)
    ↓
Workflow Router
    ├── Greenfield UI (Requirement → IA/Pages → Flows → Direction → Tokens → Implementation → QA)
    └── Existing UI/UX (Observation → Scope Isolation → L1/L2/L3 Budget → Refinement → Preservation Gate)
    ↓
Implementation Handoff
    ↓
Validation & Quality Gates
```

Read [routing.md](routing.md) to choose the entry state, [state-machine.md](state-machine.md) for the lifecycle, [artifact-contract.md](artifact-contract.md) for ownership, and [preservation-rules.md](preservation-rules.md) for change budgets.
