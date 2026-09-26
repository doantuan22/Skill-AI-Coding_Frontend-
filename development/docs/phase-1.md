# Phase 1 — UI Orchestrator & Workflow Split

## 1. Role and Core Objectives
Phase 1 establishes the unified UI Orchestrator as the primary entry point for all frontend/UI engineering tasks.
Instead of directly diving into implementation or visual styling, requests pass through the orchestrator to:
1. Inspect repository context and determine UI state (`GREENFIELD`, `PARTIAL_UI`, `EXISTING_UI`, `UNKNOWN`).
2. Route into one of two dedicated workflow tracks:
   - **Greenfield UI Workflow**: For projects without significant existing UI or explicit rebuilds from scratch.
   - **Existing UI/UX Workflow**: For codebases with established UI components, stylesheets, or layouts.
3. Enforce the **Hard Preservation Rule** (`PRESERVE FIRST → IMPROVE SECOND → REDESIGN ONLY WHEN EXPLICITLY REQUESTED`).
4. Evaluate the **Change Budget (L1 / L2 / L3)** with granular permission enforcement.
5. Resolve required capabilities and knowledge categories.
6. Produce an actionable plan and handoff to implementation and validation.

```text
User Request
    ↓
Inspect repository / context
    ↓
Determine UI state
    ↓
Route workflow
    ├── Greenfield UI
    └── Existing UI/UX (+ hard preservation rules)
    ↓
Load / select required capabilities
    ↓
Plan
    ↓
Implementation handoff
    ↓
Validation handoff
```

## 2. Dedicated Workflows

### A. Greenfield Workflow ([workflows/greenfield-workflow.md](../../plugins/ui-engineering/workflows/greenfield-workflow.md))
- Flow: `Requirement → Product/domain understanding → Page inventory → UX flow → Design direction → Design system → Implementation → Validation`.
- **Design Freedom**: If user has not specified a style, color palette, or typography, the AI selects them based on product type, domain, target user, use case, and content density (never arbitrary AI preference).
- **User Constraints**: Any user-specified color, style, or framework takes top precedence.
- **Multi-page Gate**: Page inventory, UX flow, and minimal design system must be established before multi-page coding.

### B. Existing UI/UX Workflow ([workflows/existing-ui-workflow.md](../../plugins/ui-engineering/workflows/existing-ui-workflow.md))
- Hard rule: **PRESERVE FIRST → IMPROVE SECOND → REDESIGN ONLY WHEN EXPLICITLY REQUESTED**.
- **Defaults**:
  - `color_palette`: LOCKED
  - `brand_identity`: LOCKED
  - `overall_layout_identity`: PROTECTED
  - `navigation_model`: PROTECTED
  - `information_architecture`: PROTECTED
  - `component_structure`: CONTROLLED
  - `spacing / alignment / hierarchy`: ALLOWED (L1)
  - `responsive / a11y / consistency`: ALLOWED (L1)
- Vague prompts ("modernize UI", "làm đẹp", "make professional") DO NOT authorize palette change, branding swap, or architecture redesign.

## 3. Change Budget & Permission Model (L1 / L2 / L3)
- **L1 (Safe Refinement)**: Spacing, typography scale, responsive breakpoints, states, a11y, token alignment. *Default: ALLOWED*.
- **L2 (Local Structural Change)**: Component layout, section arrangement, form flow, card structure. *Default: ALLOWED ONLY WITH CLEAR UX/TECHNICAL JUSTIFICATION*.
- **L3 (Major Redesign)**: Global palette, branding, page architecture, rebuild from scratch. *Default: DENIED*. Requires explicit user permission.
- **Granular Permissions**:
  - Layout permission != Palette permission.
  - Palette permission != Full architecture rebuild.
  - Local component scope != Global redesign.

## 4. Precedence Hierarchy
1. Explicit user instruction
2. Existing brand identity
3. Existing design system
4. Existing UX / information architecture
5. Repository / framework constraints
6. Domain best practices
7. Design inspiration
8. AI preference

*Note on Case 12*: When domain/design inspiration suggests a different visual style, Existing Brand Identity (2) and Existing Design System (3) strictly overrule Design Inspiration (7).

## 5. Extension Point for Phase 2
Phase 1 implements `UIStateDetector` with a deterministic heuristic (`HeuristicUIStateDetector`).
In Phase 2, this interface will be extended with full Framework & Repo Intelligence (AST component graph, design token detectors, and route scanners) without altering orchestrator contracts or workflow routing.
