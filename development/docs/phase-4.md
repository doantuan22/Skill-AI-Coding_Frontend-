# Phase 4 — Knowledge Router + Framework Packs

## 1. Role and Core Objectives
Phase 4 implements the **Knowledge Router & Framework Packs** layer of the UI Engineering Plugin.
While previous phases solved repository understanding (Phase 2) and existing UI identity preservation (Phase 3), Phase 4 solves **context-efficiency and deterministic knowledge orchestration**:
- Instead of loading the entire 261-entry catalog or all design skills into every task, the Knowledge Router dynamically resolves a targeted, context-budgeted **Knowledge Load Plan**.
- The router is **not an LLM search engine**; it is a deterministic, framework-aware, task-aware, and preservation-aware orchestration layer.
- Combines:
  $$\text{Repo Profile} + \text{Existing UI Profile} + \text{Preservation Profile} + \text{Task Intent} \longrightarrow \text{Knowledge Load Plan}$$

---

## 2. Architecture & Pipeline

```text
User Request / Task
        ↓
UI Orchestrator (Phase 1)
        ↓
Repo Intelligence (Phase 2 repo_profile)
        ↓
Existing UI Analyzer (Phase 3 existing_ui_profile + preservation_profile)
        ↓
Knowledge Router (`uiux.engine.knowledge_router`)
    ├── Task Intent Classifier (15 canonical intents: responsive_fix, a11y_fix, form_ux, etc.)
    ├── Framework Pack Resolver (React, Next.js, Vue, Nuxt, Svelte, SvelteKit, HTML/CSS, Spring/Thymeleaf, Angular)
    ├── Styling & UI Library Resolver (Tailwind, Bootstrap, Plain CSS, CSS Modules, SCSS, styled-components, Emotion, MUI, shadcn/ui)
    ├── Design Skill Resolver (Responsive, Visual QA, UX Structure, Component Realization, Typography, etc.)
    ├── Preservation Knowledge Resolver (Invariants, locked palette, L1/L2/L3 change budgets)
    ├── Runtime Validation Resolver (Responsive viewport, a11y audit, form interaction, smoke test)
    └── Context Budget Manager (Priority sorting, weight points, deterministic pruning)
        ↓
Knowledge Load Plan (`knowledge_plan`)
```

---

## 3. Machine-Readable Contracts

### A. Input Contract (`knowledge_request`)
- `repo_profile`: Normalized repository intelligence profile from Phase 2.
- `existing_ui_profile`: Visual identity, layout, component consistency, and UX flows from Phase 3.
- `preservation_profile`: Baseline invariants and merged user permissions.
- `task_intent`: Canonical or user-provided intent.
- `user_request`: User prompt text.
- `workflow`: `"greenfield"` | `"existing-ui"` | `"unknown"`.
- `requested_scope`: `"global"` | `"page"` | `"section"` | `"component"` | `"local"`.
- `explicit_constraints`: Optional palette or structural restrictions.

### B. Output Contract (`knowledge_plan`)
Validated against [knowledge-plan.schema.json](../../plugins/ui-engineering/schemas/knowledge-plan.schema.json):
- `schema_version`: `1`
- `workflow`: Current workflow mode.
- `task_intent`: Canonical classified intent.
- `selected_packs`:
  - `framework`: List of resolved framework pack objects.
  - `styling`: Primary and secondary styling pack objects.
  - `ui_library`: Active component library pack objects (e.g. `shadcn_ui`).
  - `runtime`: Targeted runtime validation packs.
- `selected_skills`: Design skills relevant to the task and scope.
- `selected_knowledge`: Catalog knowledge entries or preservation invariants.
- `preservation_context`: Locked/protected invariants and allowed change level (`L1`, `L2`, `L3`).
- `excluded_knowledge`: Items pruned by the context budget manager with clear rationale.
- `load_order`: Deterministic sequence for loading knowledge.
- `context_budget`: Point usage, status (`within_budget` or `truncated_optional`), and priority buckets.
- `rationale`: Human-readable explanation of routing decisions.
- `diagnostics`: `warnings`, `conflicts`, `unsupported`.

---

## 4. Framework Packs Matrix

| Pack ID | Framework | Default Weight | Key UI Engineering Guidance |
| :--- | :--- | :---: | :--- |
| `framework.react` | React (>=16.8) | Medium | Component composition, local state placement, accessible form patterns, stable keys, and component preservation. |
| `framework.nextjs` | Next.js (>=12.0) | Medium | App Router vs Pages Router, Server/Client component boundaries (`"use client"`), `next/image`, `next/font`, and route preservation. |
| `framework.vue` | Vue 3 (>=3.0) | Medium | SFC `<script setup>`, Composition API reactivity, props/emits, scoped styles, and slots. |
| `framework.nuxt` | Nuxt (>=3.0) | Medium | File-system routing in `pages/`, `<NuxtLayout>`, `<NuxtPage>`, `<NuxtLink>`, and layout architecture preservation. |
| `framework.svelte` | Svelte (>=4.0) | Medium | Component reactivity, runes/declarations, compiler a11y adherence, and scoped CSS. |
| `framework.sveltekit` | SvelteKit (>=1.0) | Medium | `+layout.svelte`, `+page.svelte`, nested routing, and layout invariant preservation. |
| `framework.static_html` | Static HTML | Medium | Semantic HTML5 elements, progressive enhancement, CSS Grid/Flexbox, and no framework bloat. |
| `framework.spring_thymeleaf` | Spring + Thymeleaf | Medium | Template fragments (`th:replace`), form error binding (`#fields.hasErrors()`), and controller contract preservation. |
| `framework.angular` | Angular (>=14.0) | Medium | Standalone component conventions, reactive forms UI, and existing module structure preservation. |
| `framework.fallback` | Universal Fallback | Small | Universal frontend principles, accessible markup, and safe fallback rules when framework is unknown. |

---

## 5. Styling Packs Matrix & Composable Architecture

| Pack ID | System / Library | Weight | Core Focus |
| :--- | :--- | :---: | :--- |
| `styling.tailwindcss` | Tailwind CSS | Medium | Utility composition, theme token discipline, responsive modifiers, and locked palette preservation. |
| `styling.bootstrap` | Bootstrap | Medium | 12-column grid, responsive utilities, and anti-fight customization rules. |
| `styling.plain_css` | Plain CSS | Small | CSS custom properties (`:root`), Flexbox/Grid layouts, and modular class organization. |
| `styling.css_modules` | CSS Modules | Small | Locally scoped CSS classes, style composition, and camelCase naming conventions. |
| `styling.sass_scss` | Sass / SCSS | Small | Modern `@use`/`@forward` modules, variable structures, and nesting discipline. |
| `styling.styled_components` | styled-components | Medium | Theme-driven styled primitives, transient props, and CSS-in-JS preservation. |
| `styling.emotion` | Emotion | Medium | Emotion `css` prop, ThemeProvider tokens, and styled component conventions. |
| `styling.mui` | Material UI | Medium | ThemeProvider tokens, `sx` prop, component overrides, and accessible widget preservation. |
| `ui_library.shadcn_ui` | shadcn/ui | Medium | Radix primitives composition, `cn()` merging, custom variants reuse, and no blanket regeneration. |

**No Combinatorial Explosion**: Packs are composable independent units. A repository with Next.js + Tailwind + shadcn loads `framework.nextjs`, `styling.tailwindcss`, and `ui_library.shadcn_ui` without creating an unwieldy composite pack.

---

## 6. Context Budgeting & Prioritization Strategy

- **Budget Limit**: Default 25 points.
- **Weight Scale**:
  - `small`: 1 point
  - `medium`: 2 points
  - `large`: 4 points
- **Prioritization Hierarchy**:
  1. `critical`: Hard constraints and preservation invariants (`preservation.existing_ui_invariants`). **Never pruned.**
  2. `high`: Primary framework pack and primary styling pack. **Never pruned.**
  3. `high / medium`: Task-specific skills (`skill.responsive_interaction`, `skill.visual_qa`) and active runtime validation.
  4. `medium / low`: Optional catalog knowledge (layout patterns, motion recipes).
  5. `low`: Design inspiration (`skill.design_inspiration`). Pruned first when budget is exceeded.

---

## 7. Task Intent Classification & Scoped Routing

The classifier deterministically categorizes prompts into 15 canonical intents:
- `responsive_fix`: Routes `skill.responsive_interaction` and `runtime.responsive_viewport`. Excludes unrelated motion, typography inspiration, and landing page patterns.
- `accessibility_fix`: Routes `skill.visual_qa` and `runtime.accessibility_audit`.
- `component_refactor`: Confined to component scope; routes `skill.component_realization` without loading page-level architecture packs.
- `form_ux`: Routes `runtime.form_interaction`.
- `navigation_ux`: Routes `skill.ux_structure`.
- `page_redesign` / `full_redesign`:
  - If Existing UI and change level is `L1`: Suppresses major redesign knowledge, restricts to safe refinement.
  - If Greenfield or `L3` with explicit user permission: Loads `skill.ux_structure` and `skill.design_direction`.

---

## 8. Monorepo & Conflict Handling

- **Monorepo Scoping**: If the repository profile contains multiple applications (`storefront`, `admin`, `docs`), the router resolves knowledge exclusively for the targeted sub-application. Storefront's Next.js knowledge is never injected into an Admin task built in React + Bootstrap.
- **Conflict Handling**: If contradictory framework signals exist (e.g. legacy Vue templates inside a Next.js repo), the router picks the candidate with the highest evidence confidence, records the conflict in `diagnostics.conflicts`, and avoids loading multiple framework packs.

---

## 9. Domain Pack Extension Point (Phase 5 Boundary)

Phase 4 establishes the interface for domain packs via [domain_extension.py](../../plugins/ui-engineering/uiux/engine/knowledge_router/domain_extension.py):
- Known domain categories (`ecommerce`, `healthcare`, `fintech`, `saas`, `hospitality`, `devtools`) return stub metadata with `"status": "extension_point_phase_5"`.
- Resolving domain packs never crashes or leaks exceptions.
- Full domain design packs will be implemented in Phase 5.

---

## 10. Public API & CLI Reference

### Public API (`uiux.api`)
- `route_knowledge(request=None, **kwargs) -> dict`: Central routing entry point.
- `build_knowledge_plan(...) -> dict`: High-level convenience builder.
- `resolve_framework_pack(framework_name, version=None) -> dict | None`: Query framework pack metadata.

### CLI (`scripts/route_knowledge.py`)
```bash
python scripts/route_knowledge.py --project . --task "fix responsive dashboard" --format summary
```
Output:
```text
workflow: existing-ui
task_intent: responsive_fix
framework: framework.static_html
styling: styling.plain_css
selected:
  - preservation.existing_ui_invariants
  - framework.static_html
  - styling.plain_css
  - skill.responsive_interaction
  - skill.final_quality_gate
  - runtime.responsive_viewport
budget: 9/25 pts (within_budget)
```
