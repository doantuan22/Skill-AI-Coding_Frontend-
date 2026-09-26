# Phase 6 – Implementation Planning & Controlled Editing

## 1. Overview & Core Principles

Phase 6 introduces a deterministic, machine-readable **Implementation Planning & Controlled Editing** system to the UI Engineering Plugin. 

Prior phases (Phases 1–5) established full comprehension of user intent, Greenfield vs Existing UI workflows, framework/styling architectures, design identity preservation invariants, framework knowledge packs, and domain UI states. Phase 6 bridges comprehension to safe execution by answering:

- **What** is the AI authorized to edit?
- **Where** are the edits bounded?
- **In what order** must the changes be applied?
- **Which changes exceed scope?**
- **Which changes require concrete engineering justification (L2)?**
- **Which changes require explicit user authorization (L3)?**
- **What is the maximum allowed blast radius?**
- **How can changes be rolled back if validation fails?**
- **What runtime evidence is required before concluding work?**

### The Core Principle
```text
PLAN FIRST → VALIDATE SCOPE → EDIT WITHIN BUDGET → VERIFY → STOP WHEN GOAL IS MET
```

The system strictly avoids turning the agent into an unconstrained autonomous refactoring engine. Edits are bounded, tracked, and verified against an approved plan.

---

## 2. Pipeline Architecture

```text
User Request
    ↓
UI Orchestrator
    ↓
Repo Intelligence (repo_profile)
    ↓
Existing UI / Preservation Analysis (existing_ui_profile, preservation_profile)
    ↓
Knowledge Router & Domain Packs (knowledge_plan)
    ↓
Modification Planner (uiux.api.plan_modification)
    ├── Scope Resolver (scope_resolver.py)
    ├── Affected Surface Resolver (surface_resolver.py)
    ├── Change Classifier & Permission Gates (change_classifier.py)
    ├── Blast Radius Calculator (blast_radius.py)
    └── Step Planner, Rollback & Validation (step_planner.py)
    ↓
Permission & Scope Gate (uiux.api.evaluate_plan_permissions)
    ├── READY: Proceed to bounded execution
    ├── BLOCKED: Policy violation (e.g., locked palette, route deletion)
    ├── NEEDS_PERMISSION: Requires explicit user instruction (unauthorized L3)
    ├── INSUFFICIENT_CONTEXT: Ambiguous monorepo target application
    └── READ_ONLY: Audit-only mode
    ↓
Controlled Editing Engine (uiux.api.compare_plan_to_changes)
    ├── Enforce allowed_files and allowed_components
    ├── Reject out-of-plan file creations / deletions
    ├── Detect plan drift (files, change levels, routes, tokens)
    └── Produce machine-readable ChangeManifest
    ↓
Validation Handoff Contract
    └── Hand off to runtime / evidence infrastructure (viewports, interactions, a11y, preservation)
```

---

## 3. Machine-Readable Contracts & Schemas

### 3.1 Modification Plan (`modification-plan.schema.json`)
Every editing task must produce a machine-readable plan matching `plugins/ui-engineering/schemas/modification-plan.schema.json`:
- `schema_version`: Version number (1).
- `plan_id`: Unique identifier (`plan_...`).
- `request`: Normalized user goal, task intent, requested scope.
- `workflow`: `greenfield` or `existing-ui`.
- `repository`: Application root, framework, styling system, UI library.
- `constraints`: Explicit user constraints, repository constraints, framework constraints.
- `preservation`: Protected properties, max allowed level, granular permissions (`palette`, `brand`, `layout`, `navigation`).
- `knowledge`: Selected framework/domain packs and design skills.
- `affected_surface`: Concrete list of files, pages, components, tokens, routes, protected files.
- `change_classification`: Overall level (`L1`, `L2`, `L3`) and list of individual changes with reasons, evidence, justifications, and permission traces.
- `implementation_steps`: Ordered execution steps with explicit dependencies, risks, and expected outcomes.
- `execution_batches`: Phased batches (`batch_a` tokens -> `batch_b` structure -> `batch_c` states -> `batch_d` validation).
- `validation`: Required checks, affected viewports, interactions, accessibility checks, preservation invariants.
- `blast_radius`: `allowed_files`, `allowed_components`, `protected_files`, `protected_tokens`, `protected_routes`, `max_scope`, `estimated_risk`.
- `rollback`: Strategy (`file_restore_with_checkpoints`) and checkpoints.
- `risks`: Qualitative ratings (`low`, `medium`, `high`) for regression, architecture, preservation, and runtime.
- `status`: `ready`, `blocked`, `needs_permission`, `insufficient_context`, `read_only`.
- `status_reasons`: Deterministic audit log explaining status determination.

### 3.2 Change Manifest (`change-manifest.schema.json`)
Post-execution auditing compares planned vs actual changes matching `plugins/ui-engineering/schemas/change-manifest.schema.json`:
- `manifest_id`: Unique identifier (`manifest_...`).
- `plan_id`: Associated plan ID.
- `modified_files`: Files modified during implementation.
- `created_files`: Files created during implementation.
- `deleted_files`: Files deleted during implementation.
- `changed_components`: Components impacted.
- `changed_tokens`: Tokens modified.
- `changed_routes`: Routes touched.
- `actual_change_levels`: Observed change levels.
- `unexpected_changes`: Unauthorized files, operations, or level escalations.
- `drift_detected`: Boolean indicating whether actual execution drifted from the plan.
- `status`: `passed` or `failed`.
- `validation_required`: Validation checks required for the actual modified surface.

---

## 4. Key Subsystems & Policies

### 4.1 Scope Resolution & User Goal Normalization
The `ScopeResolver` normalizes vague user requests into strict scope boundaries:
- `global`: Full product or multi-application scope.
- `application`: Specific application inside a monorepo.
- `page`: Specific page or route subset.
- `section`: Major layout container or landmark (e.g. navbar, sidebar, footer).
- `component`: Individual UI component (e.g. Button, Card, Dialog).
- `token`: Design system tokens and styling primitives.
- `local`: Isolated single-file fix.

**Goal Normalization Rules**:
- "Fix mobile navbar" → `section` scope, NOT a site-wide navigation overhaul.
- "Improve checkout UX" → `page` scope, NOT an ecommerce design system rebuild.
- "Modernize the UI" → Vague enhancement: does NOT grant L3 permissions or expand scope.

### 4.2 L1 / L2 / L3 Permission & Justification Gates
1. **L1 (Safe Refinement)**:
   - Spacing, alignment, responsive fixes, typography scale, states, accessibility, visual consistency.
   - **Allowed by default**.
2. **L2 (Local Structural Change)**:
   - Reordering sections, grouping form fields, altering local layout hierarchy.
   - **Mandatory Justification**: Must contain `issue`, `evidence`, `why_L1_is_insufficient`, and `expected_improvement`. Subjective aesthetic rationales ("looks nicer", "trông đẹp hơn", "modern feel") are **strictly rejected**.
3. **L3 (Major Redesign)**:
   - Palette changes, rebranding, page architecture overhauls, navigation restructuring.
   - **Mandatory Explicit Permission**: Requires unambiguous user instruction. Granular permissions are strictly isolated: granting layout redesign does NOT grant palette or brand changes.

### 4.3 Blast Radius & Protection Envelopes
Every plan computes a strict envelope:
- `allowed_files`: Explicit list of files authorized for modification.
- `protected_files`: Files strictly off-limits (e.g., `theme.ts`, `tailwind.config.js` when palette is locked; router configurations when navigation is locked).
- `protected_tokens`: Global color palette and brand definitions.
- `protected_routes`: Route paths that must not be renamed or deleted.

### 4.4 Shared-First but Safe
- When a defect repeats across multiple pages due to a shared primitive (e.g., Button focus ring), the planner targets the shared component.
- If a shared component API modification breaks compatibility (prop rename, prop deletion, variant removal), regression risk is automatically escalated to `high`.
- When an issue is isolated to a single page's custom implementation, shared component refactoring is suppressed to prevent unintended cross-app side effects.

### 4.5 Policy Invariants
1. **No Unsolicited Framework Migration**: Prohibits switching from React to Vue, Next.js to Nuxt, etc., unless explicitly ordered by the user.
2. **No Unsolicited UI Library Swapping**: Prohibits swapping Tailwind for Bootstrap, plain CSS for MUI, etc.
3. **Strict Business Logic Boundaries**: Prohibits modifying backend services, database schemas, SQL queries, payment processing, or domain business logic under the guise of UI tasks.
4. **New Dependency Policy**: Prohibits adding dependencies (e.g., `lodash`, `moment`, `styled-components`) when framework primitives suffice. Any justified dependency is recorded in the plan and never auto-installed.
5. **Audit-Only & Plan-Only Modes**:
   - `task_intent = "audit_only"` → Plan status is `read_only`; editing is prohibited.
   - `plan_only = true` → Generates and validates the plan for review without touching code.

---

## 5. Public Python API & CLI

Phase 6 exposes 5 functions via `uiux.api`:

```python
from uiux import api

# 1. Generate a machine-readable Modification Plan
plan = api.plan_modification(
    user_request="Improve responsive navbar on mobile",
    workflow="existing-ui",
    repo_profile=repo_profile,
    existing_ui_profile=existing_ui_profile,
    preservation_profile=preservation_profile,
    knowledge_plan=knowledge_plan,
)

# 2. Validate structural integrity of a plan
val_result = api.validate_modification_plan(plan)

# 3. Evaluate permission compliance
perm_result = api.evaluate_plan_permissions(plan)

# 4. Extract validation handoff contract
handoff = api.build_validation_handoff(plan)

# 5. Compare plan against actual implementation changes (plan drift detection)
manifest = api.compare_plan_to_changes(
    plan,
    actual_changes={"modified_files": ["src/components/Navbar.tsx"]}
)
```

### CLI Tooling
```bash
python scripts/plan_modification.py \
  --request "Fix button spacing on checkout" \
  --workflow existing-ui \
  --format summary
```

---

## 6. Phase 7 Extension Boundary

Phase 6 intentionally does NOT implement:
- Autonomous runtime critic or repair loop.
- Visual screenshot AI critic.
- Multi-iteration automatic code patch and fix cycles.

Phase 6 establishes the authoritative **Validation Handoff** contract (`validation` block in `ModificationPlan`) and **Plan Drift Detection** (`compare_plan_to_changes`), providing the structured foundation for Phase 7 to execute runtime critiques and targeted repairs.
