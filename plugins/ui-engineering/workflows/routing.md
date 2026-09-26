# UI Orchestration & Workflow Routing

The UI Orchestrator serves as the primary entry point for all UI engineering requests. It inspects repository context, classifies UI state, routes to the appropriate workflow, enforces preservation policies, and resolves required capabilities.

## Orchestration Flow

```text
User Request
    ↓
Inspect Repository / Context
    ↓
Determine UI State (GREENFIELD | PARTIAL_UI | EXISTING_UI | UNKNOWN)
    ↓
Workflow Router
    ├── Greenfield UI Workflow (workflows/greenfield-workflow.md)
    └── Existing UI/UX Workflow (workflows/existing-ui-workflow.md)
            + Hard Preservation Rules & Change Budget (L1 / L2 / L3)
    ↓
Load / Resolve Required Capabilities & Knowledge
    ↓
Execution Plan
    ↓
Implementation Handoff
    ↓
Validation Handoff
```

## Workflow Selection Matrix

| UI State | User Intent / Trigger | Target Workflow | Preservation Policy | Change Budget |
|---|---|---|---|---|
| `GREENFIELD` | New project or build from scratch | [Greenfield UI](greenfield-workflow.md) | `None` (AI design freedom grounded in domain) | `L3` (Full build authorized) |
| `EXISTING_UI` | "improve responsive", "fix a11y", spacing | [Existing UI/UX](existing-ui-workflow.md) | `PRESERVE FIRST`: Brand & palette LOCKED | `L1` (Safe refinement) |
| `EXISTING_UI` | "modernize UI", "làm đẹp", "make professional" | [Existing UI/UX](existing-ui-workflow.md) | Brand, palette & layout PROTECTED | `L1` (L3 denied without explicit prompt) |
| `EXISTING_UI` | Reorganize section/component layout | [Existing UI/UX](existing-ui-workflow.md) | Brand & palette LOCKED | `L2` (Justified only) |
| `EXISTING_UI` | "redesign toàn bộ", "đổi sang tông đen tím" | [Existing UI/UX](existing-ui-workflow.md) | Granular unlock for authorized properties | `L3` (Explicit permission granted) |
| `EXISTING_UI` | Fix button / single component | [Existing UI/UX](existing-ui-workflow.md) | Confined to local component scope | `L1` / `L2` (Global redesign blocked) |
| `PARTIAL_UI` | Prototype / partial scaffold | [Existing UI/UX](existing-ui-workflow.md) | Reconcile starter tokens with target design | `L2` (Extend starter UI) |
| `UNKNOWN` | Ambiguous / insufficient context | Context Inspection | Conservative preservation | Safe fallback; inspect before modifying |

## Precedence Hierarchy
When resolving design direction, component realization, or tokens:
1. **Explicit user instruction** (Highest priority)
2. **Existing brand identity**
3. **Existing design system**
4. **Existing UX / information architecture**
5. **Repository / framework constraints**
6. **Domain best practices**
7. **Design inspiration**
8. **AI preference** (Lowest priority)

See [preservation-rules.md](preservation-rules.md) for full change budget specifications.
