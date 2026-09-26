# Phase 3 — Existing UI Analyzer & Preservation Guard

## 1. Role and Core Objectives
Phase 3 transforms the high-level preservation policies of Phase 1 and the structural detections of Phase 2 into a deep, evidence-based **Existing UI Analyzer & Preservation Guard**.
While Phase 2 answers *"What framework, styling, pages, components, and tokens exist in this repo?"*, Phase 3 answers:
- *"What is the active visual identity and brand aesthetic of this existing interface?"*
- *"How does the current layout operate (global shell vs. local component structure)?"*
- *"Are existing components internally consistent, or are there duplicate/conflicting variants?"*
- *"What user flows are active, and what critical UI states (loading, empty, error) are missing?"*
- *"What responsive hazards (fixed-width definitions) or accessibility gaps exist?"*
- *"What design invariants are strictly LOCKED or PROTECTED?"*
- *"Did the planned/implemented changes respect the preservation budget (L1/L2/L3) and user permissions?"*

---

## 2. Architecture & Pipeline

```text
repo_profile (Phase 2) + RepositorySnapshot
            ↓
    Existing UI Analyzer
        ├── Visual Identity Analyzer (Palette, typography, radius, shadows, density, visual language)
        ├── Layout Analyzer (Global app shell/nav vs. local card/form/section structure)
        ├── Component Consistency Analyzer (Canonical patterns, variants, radius/style anomalies)
        ├── UX Flow Analyzer (Auth, dashboard, CRUD, missing loading/empty/error states)
        ├── Responsive Analyzer (Breakpoints, fixed-width hazards, overflow risks, touch targets)
        ├── Accessibility Analyzer (Landmarks, form label association, headings, focus)
        └── Design System Extractor (Tokens, scales, component conventions, maturity classification)
            ↓
    Existing UI Profile (`existing_ui_profile`)
            ↓
    Preservation Profile Builder (Baseline invariants + granular user permission merging)
            ↓
    Preservation Guard / Evaluator (`evaluate_preservation`)
            ↓
    Pass | Warn | Fail (Violations, required vs. actual permissions, reason traces)
```

**Key Invariants**:
- **Read-only Observation**: Analyzes, extracts, classifies, and evaluates. Does *not* autonomously redesign or modify code.
- **Evidence-First**: Every extracted color, layout shell, or anomaly links to concrete file sources and deterministic confidence scores.
- **Strict Scope Confinement**: Local component or section tasks cannot trigger global layout or architectural mutations.
- **Single-Pass Reuse**: Leverages Phase 2 `repo_profile` and `RepositorySnapshot` without redundant filesystem traversals.

---

## 3. Specialized Analyzers

### A. Visual Identity Analyzer ([identity.py](../../plugins/ui-engineering/uiux/engine/existing_ui/identity.py))
- Extracts exact color roles: `primary`, `secondary`, `accent`, `neutral`, `surface`, `background`, and semantic status colors (`success`, `warning`, `error`, `info`).
- Resolves token values from CSS variables (`--color-primary: #2563eb`), Tailwind configs, and theme objects.
- Extracts typography: `font_family_base`, `font_family_heading`, `font_family_mono`, type scales, and weights.
- Extracts radius scale, elevation/shadow scale, and UI density (`compact`, `normal`, `spacious`).
- Identifies recurring visual language (`card-based modern interface`, `utility-driven modular design`, `minimalist accessible`).
- **Conflict Handling**: When multiple conflicting primary colors are detected across stylesheets, records conflicts and penalizes confidence.

### B. Layout Analyzer ([layout.py](../../plugins/ui-engineering/uiux/engine/existing_ui/layout.py))
- **Global Structure**: Detects app shells (`AppShell.tsx`, `layout.tsx`), global headers, persistent sidebars, footers, and main container boundaries.
- **Local Structure**: Identifies card patterns, form groupings, and section patterns.
- Distinguishes global from local structure to enforce L1/L2 vs. L3 change budgets accurately.
- Records container max-width conventions (`max-w-7xl`, `container`, `mx-auto`) and grid/flex systems.

### C. Component Consistency Analyzer ([components.py](../../plugins/ui-engineering/uiux/engine/existing_ui/components.py))
- Identifies canonical primitives (`Button`, `Input`, `Modal`, `Dialog`, `Badge`, `Card`).
- Extracts component variants (e.g., `default`, `primary`, `secondary`, `outline`).
- Flags anomalies and ad-hoc styling (e.g., raw `<button>` elements with inline custom classes bypassing the canonical Button component).
- Detects duplicated component implementations across different directories.
- Classifies consistency (`high`, `moderate`, `low`, `inconsistent`) and anomaly severity (`info`, `low`, `medium`, `high`).

### D. UX Flow Analyzer ([ux_flows.py](../../plugins/ui-engineering/uiux/engine/existing_ui/ux_flows.py))
- Identifies recognized application flows from routes and entrypoints: `authentication`, `dashboard`, `search_and_browse`, `crud_management`, `checkout`, `account_settings`.
- Audits state handling coverage: flags missing `loading` (skeletons/spinners), missing `error` feedback, and missing `empty` state views.
- Flags UX friction signals (e.g., destructive delete actions lacking confirmation dialogs).

### E. Responsive Analyzer ([responsive.py](../../plugins/ui-engineering/uiux/engine/existing_ui/responsive.py))
- Evaluates breakpoint declarations (`sm`, `md`, `lg`, `xl`) and stacking rules (`flex-col md:flex-row`).
- **Hazard Detection**: Flags hardcoded wide fixed widths (`width: 1200px`, `min-width: 900px`) that risk horizontal viewport overflow on mobile devices.
- Checks touch target sizes: flags sub-44px interactive controls.
- Detects mobile navigation patterns (collapsible drawers, sheets, hamburger menus).

### F. Accessibility Analyzer ([accessibility.py](../../plugins/ui-engineering/uiux/engine/existing_ui/accessibility.py))
- Reuses and aggregates accessibility standards without duplicating the runtime engine.
- Audits form label associations: flags `<input>` tags lacking `<label>`, `aria-label`, or `id`/`htmlFor` associations.
- Audits semantic HTML landmarks (`<main>`, `<nav>`, `<header>`, `<footer>`).
- Flags non-semantic clickable elements (`<div onClick=...>` without keyboard/role listeners).
- Audits heading hierarchy (e.g., multiple `<h1>` elements per page).

### G. Design System Extractor ([design_system.py](../../plugins/ui-engineering/uiux/engine/existing_ui/design_system.py))
- Compiles tokens, scales, and component conventions into a normalized design system model.
- Classifies **Design System Maturity**:
  - `mature`: Formal token source files + high component consistency + high confidence.
  - `partial`: Active styling conventions/Tailwind present without complete token architecture.
  - `fragmented`: Inconsistent component patterns and conflicting token declarations.
  - `unknown`: No token sources or unrecognized styling.

---

## 4. Preservation Profile & User Permission Merging ([preservation_profile.py](../../plugins/ui-engineering/uiux/engine/existing_ui/preservation_profile.py))

Constructs baseline preservation invariants conforming to [schemas/preservation-profile.schema.json](../../plugins/ui-engineering/schemas/preservation-profile.schema.json):
- `protected_design`:
  - `color_palette`: `policy: locked` (unlocked only with explicit permission) + baseline colors.
  - `brand_identity`: `policy: locked` (unlocked only with explicit branding permission).
  - `overall_layout_identity`: `policy: protected` (editable only with explicit layout permission).
  - `navigation_model`: `policy: protected` + baseline navigation items.
  - `information_architecture`: `policy: protected` + baseline route structure.
- `allowed_changes`:
  - `L1 (Safe Refinement)`: `policy: allowed` (spacing, typography scale, responsive, states, a11y, token alignment).
  - `L2 (Local Structural Change)`: `policy: justified_only` (requires explicit reason trace).
  - `L3 (Major Redesign)`: `policy: explicit_user_permission_only` (granted only when user explicitly authorizes).

### Granular Permission Enforcement
Permissions never leak or propagate:
- Granting `allow_layout_change` keeps `color_palette` strictly **LOCKED**.
- Granting `allow_palette_change` keeps `overall_layout_identity`, `navigation_model`, and `information_architecture` strictly **PROTECTED**.
- Vague prompts ("modernize the UI", "làm đẹp") grant **0** L3 permissions and keep all invariants locked.

---

## 5. Preservation Evaluator / Guard ([evaluator.py](../../plugins/ui-engineering/uiux/engine/existing_ui/evaluator.py))

Audits proposed changes against the baseline preservation profile:
1. **Palette Preservation**: Detects color shifts while locked -> `CRITICAL` violation (`PALETTE_PRESERVATION`).
   - *Micro-adjustments*: If `is_accessibility_contrast_adjustment = True`, small contrast tweaks are permitted with an informational warning rather than failing the build.
2. **Brand Preservation**: Detects brand token or visual language shifts -> `CRITICAL` violation.
3. **Layout Preservation**: Detects global layout shell rewrites while protected -> `HIGH` violation.
4. **Navigation Preservation**: Detects route alterations outside plan -> `HIGH` violation.
5. **Architecture Preservation**: Detects information architecture rewrites -> `CRITICAL` violation.
6. **Scope Confinement**: If task scope is `component` or `section`, any global layout or route change triggers `CRITICAL` violation (`SCOPE_CONFINEMENT`).
7. **L2 Justification Trace**: L2 local structural change without a valid `change_reason` triggers `MEDIUM` violation (`L2_JUSTIFICATION_TRACE`).
8. **L3 Permission Trace**: L3 major redesign without explicit user permission triggers `CRITICAL` violation (`L3_EXPLICIT_PERMISSION_TRACE`).

Output conforming to [schemas/preservation-evaluation.schema.json](../../plugins/ui-engineering/schemas/preservation-evaluation.schema.json):
- `status`: `"pass"` | `"warn"` | `"fail"`
- `violations`: `[ { rule, severity, affected_area, evidence, required_permission, actual_permission } ]`
- `warnings`: `[ ... ]`
- `checked_rules`: `[ ... ]`
- `summary`: Human-readable evaluation summary.

---

## 6. Monorepo Multi-App Support
When `is_monorepo = True`, `analyze_existing_ui` generates distinct profiles for each sub-application (e.g., `storefront` vs. `admin`) under `applications`. Sub-apps do not cross-contaminate color tokens, layouts, or component consistency.

---

## 7. Public Core API
Added to [uiux/api.py](../../plugins/ui-engineering/uiux/api.py):
- `analyze_existing_ui(project=".", repo_profile=None, options=None) -> dict`: Produces normalized `existing_ui_profile`.
- `build_preservation_profile(existing_ui_profile, permissions=None, requested_scope="global") -> dict`: Generates baseline preservation profile.
- `evaluate_preservation(baseline_profile, proposed_changes, permissions=None, requested_scope=None) -> dict`: Runs preservation guard audit.

CLI entrypoint: `python scripts/analyze_existing_ui.py [project] [--format json|summary|preservation]`.

---

## 8. Extension Boundaries (Phases 4, 6, 7)
Phase 3 establishes the analyzer and preservation guard. The following remain strictly deferred:
- **Phase 4**: Full Framework Knowledge Router & external knowledge pack indexing.
- **Phase 6**: Autonomous modification planner and AST code rewriting.
- **Phase 7**: Automated visual diff regression engine, runtime screenshot pixel clustering, and Critic/Repair loop.
