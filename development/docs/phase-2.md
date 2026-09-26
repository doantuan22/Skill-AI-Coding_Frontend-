# Phase 2 — Repo & Framework Intelligence

## 1. Role and Core Objectives
Phase 2 transforms heuristic repository scanning into a structured, machine-readable **Repo & Framework Intelligence** layer.
Before the UI Orchestrator routes tasks or selects knowledge packs, Repo Intelligence inspects the codebase to extract concrete evidence and confidence scores.

### Architecture Pipeline
```text
User Request / Project Context
            ↓
    UI Orchestrator
            ↓
    Repo Intelligence (Single-Pass Snapshot)
        ├── RepositorySnapshot (Bounded, single-pass inspection, ignore rules)
        ├── Framework Detector
        ├── Styling Detector (Multi-system support + usage penalties)
        ├── Route / Page Detector (Framework-adaptive)
        ├── Component Inventory (Shared, layouts, primitives, wrappers)
        ├── Design Token Detector (CSS custom properties, themes, Tailwind)
        ├── Runtime Capability Detector (Read-only commands, Playwright readiness)
        └── UI State Detector (RepositoryUIStateDetector)
            ↓
    Normalized Repo Profile (`repo_profile`)
            ↓
    Workflow Router (Greenfield / Existing UI / Safe Fallback)
```

**Key Invariants**:
- **Read-only**: Never runs destructive commands, never auto-installs packages or browser drivers, never modifies target projects.
- **Deterministic**: Same input signals always generate identical profiles and confidence values.
- **Evidence-First**: Every detection includes concrete evidence lines and deterministic confidence numbers.
- **No Hallucination**: Missing runtime scripts, framework versions, or commands resolve to `null`/`unknown` rather than guesswork.
- **Boundary Preservation**: Repo Intelligence provides facts, signals, and inventory; it does *not* make visual or design direction decisions.

---

## 2. Normalized Repository Snapshot (`RepositorySnapshot`)
All detectors consume a shared in-memory `RepositorySnapshot` instead of walking the filesystem independently:
- **Bounded Scanning**: Limits traversal to configurable boundaries (default 5,000 files, max 50KB per inspected text sample).
- **Strict Ignore Rules**: Automatically ignores build artifacts and external vendor directories:
  `node_modules`, `dist`, `build`, `.next`, `.nuxt`, `coverage`, `.git`, `__pycache__`, `.cache`, `out`, `vendor`, `.turbo`, `.svelte-kit`, `.output`, `target`, `bin`, `obj`.
- **Monorepo Detection**: Detects `pnpm-workspace.yaml`, `lerna.json`, or sub-package directories (`apps/*`, `packages/*`) to avoid collapsing multiple applications into a single root.

---

## 3. Specialized Detectors

### A. Framework Detector ([framework.py](../../plugins/ui-engineering/uiux/engine/repo_intelligence/framework.py))
Detects frontend stacks with confidence and evidence:
- **React**: `package.json` (`react`), Vite config, JSX/TSX conventions.
- **Next.js**: `next` in dependencies, `next.config.*`, App Router (`app/`) or Pages Router (`pages/`).
- **Vue**: `vue` dependency, `vite.config.*` with `@vitejs/plugin-vue`, `.vue` SFCs.
- **Nuxt**: `nuxt` dependency, `nuxt.config.*`.
- **Svelte / SvelteKit**: `svelte`, `@sveltejs/kit`, `svelte.config.*`, `routes/**/+page.svelte`.
- **Angular**: `@angular/core`, `angular.json`.
- **Spring Boot + Thymeleaf**: `pom.xml` / `build.gradle` declaring `spring-boot-starter-thymeleaf`, `src/main/resources/templates/*.html`.
- **Static HTML/CSS/JS**: Standalone `.html` entry files without dynamic framework dependencies.
- **Unknown**: Insufficient evidence or conflicting signals.

### B. Styling Detector ([styling.py](../../plugins/ui-engineering/uiux/engine/repo_intelligence/styling.py))
Recognizes styling paradigms with multi-system support:
- `plain_css`, `css_modules`, `sass_scss`, `tailwindcss`, `bootstrap`, `styled_components`, `emotion`, `mui`, `shadcn_ui`.
- **Multi-System Ranking**: Identifies `primary` and `secondary` systems (e.g., Tailwind CSS + CSS Modules).
- **Usage Penalty (Case 8)**: If a styling library (e.g. Bootstrap) is declared in `package.json` but has zero source usages or classes in components, its confidence is heavily penalized (<= 0.35) and an explicit `WARNING` evidence is generated.

### C. Route & Page Detector ([routes.py](../../plugins/ui-engineering/uiux/engine/repo_intelligence/routes.py))
Inventories routes, layouts, and page entrypoints:
- **Next.js App Router**: Strips route groups `(group)` to map canonical paths, detects associated `layout.*`.
- **Next.js Pages Router & Nuxt**: Normalizes index and dynamic parameter routes `[param]` -> `:param`.
- **SvelteKit**: Maps `routes/**/+page.svelte` and associates `+layout.svelte`.
- **Thymeleaf**: Normalizes templates to server-rendered routes.
- **Static HTML**: Inventories standalone HTML documents.
- **Client Routers**: Detects route definitions in React Router or client entrypoints (`App.tsx`, `routes.tsx`).

### D. Component Inventory ([components.py](../../plugins/ui-engineering/uiux/engine/repo_intelligence/components.py))
Categorizes component files without destructive modifications:
- **Shared Components**: Located in `components/`, `ui/`, `common/`, `shared/`.
- **Layouts**: Headers, footers, sidebars, navigation bars, app shells.
- **Primitives**: Buttons, inputs, modals, cards, badges, dropdowns, tags, selects.
- **Page-Specific Components**: Components residing directly in page or view folders.
- **Library Wrappers**: Custom adapters wrapping Radix UI, MUI, Chakra, AntD, or Lucide.
- **Possible Duplicates**: Components sharing identical names across multiple directories.

### E. Design Token Detector ([tokens.py](../../plugins/ui-engineering/uiux/engine/repo_intelligence/tokens.py))
Extracts code-level token signals:
- **CSS Variables**: Extracts `--color-*`, `--font-*`, `--spacing-*`, `--radius-*`, `--shadow-*` from `:root` or stylesheets.
- **Theme Objects**: Analyzes JavaScript/TypeScript theme configurations (colors, typography scales, breakpoints).
- **Tailwind Theme**: Inspects `tailwind.config.*` for extended colors and theme scales.

### F. Runtime Capability Detector ([runtime.py](../../plugins/ui-engineering/uiux/engine/repo_intelligence/runtime.py))
Read-only inspection of repository scripts and build tools:
- Detects package manager (`npm`, `pnpm`, `yarn`, `bun`, `maven`, `gradle`).
- Extracts verified `dev_command`, `build_command`, `test_command`, `lint_command`, and `typecheck_command` from `package.json` scripts or build files. Missing commands return `null` and are never fabricated.
- Inspects Playwright readiness: `playwright_available = true` if Playwright is declared or configured; otherwise `false` without triggering installation.

---

## 4. UI State Classification (`RepositoryUIStateDetector`)
Replaces simple heuristic scanning with an intelligence-backed classification adhering to the Phase 1 `UIStateDetector` contract:
- **`GREENFIELD`**: 0 UI components, pages, or styling (or brand-new empty repository).
- **`PARTIAL_UI`**: 1–2 scaffold files, minimal components, and no established design system.
- **`EXISTING_UI`**: Substantial footprint (>=2 components or pages, active styling system, tokens detected).
- **`UNKNOWN`**: Ambiguous, corrupt, or insufficient evidence.

```json
"existing_ui_state": {
  "value": "EXISTING_UI",
  "confidence": 0.95,
  "evidence": [
    "Mature UI footprint: 5 components, 3 routes/pages, active tailwindcss styling."
  ]
}
```

---

## 5. Machine-Readable Profile Contract (`repo-profile.schema.json`)
The complete analysis produces a single validated JSON structure conforming to [schemas/repo-profile.schema.json](../../plugins/ui-engineering/schemas/repo-profile.schema.json):
- `schema_version`: `1`
- `framework`: `{ name, version, confidence, evidence, conflicting_signals }`
- `styling_system`: `{ primary, secondary, detected, confidence, evidence }`
- `ui_library`: `{ name, version, confidence, evidence }`
- `icon_library`: `{ name, confidence }`
- `motion_library`: `{ name, confidence }`
- `routes`: `[ { path, source_file, page_component, layout, confidence } ]`
- `pages`: `[ { id, file, route, type } ]`
- `components`: `{ shared, layouts, primitives, page_specific, library_wrappers, possible_duplicates, total_count }`
- `design_tokens`: `{ sources, colors, typography, spacing, radius, shadows, breakpoints, confidence }`
- `existing_ui_state`: `{ value, confidence, evidence }`
- `runtime`: `{ package_manager, install_command, dev_command, build_command, test_command, lint_command, typecheck_command, browser_validation, playwright_available, commands_source, confidence }`
- `repository_signals`: `{ is_monorepo, apps, ui_density, total_files, ui_files_count }`
- `conflicts`: `[ ... ]`
- `diagnostics`: `{ warnings, detector_failures, unsupported_signals }`
- `overall_confidence`: Number between 0.0 and 1.0.

---

## 6. Phase 1 Orchestrator Integration
The UI Orchestrator (`uiux.api.orchestrate_ui`) consumes `repo_profile` seamlessly via `get_ui_state_detector()`.
- Backward compatibility is preserved: if repository context is purely heuristic or synthetic, `HeuristicUIStateDetector` remains available as a fallback.
- **Preservation Hard Rules Unchanged**: Phase 2 detection feeding `EXISTING_UI` into Orchestrator triggers exact Phase 1 preservation constraints (palette locked, L1/L2 permissions, L3 denied without explicit instruction).

---

## 7. Phase 3 Extension Boundary
Phase 2 strictly isolates code-level extraction. The following are deliberately deferred to **Phase 3 (Existing UI Analyzer & Preservation Guard)**:
- Screenshot-based visual identity extraction.
- Pixel-level palette clustering and color harmony inference.
- Visual diff rendering between baseline and proposed changes.
- Deep UX flow friction and cognitive walkthrough analysis.
- Full before/after preservation policy audit.
