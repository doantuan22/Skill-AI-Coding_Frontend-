# Phase 5 — Domain Design Packs

## 1. Role and Core Objectives
Phase 5 introduces **Product & Domain Intelligence** to the UI Engineering Plugin.
While previous phases established repository analysis (Phase 2), existing UI visual identity preservation (Phase 3), and framework/styling routing (Phase 4), Phase 5 ensures the AI engineer understands the specific **domain semantics, user expectations, critical flows, required states, and anti-patterns** of the product it is designing or refactoring.

Key principles:
- **Product Semantics over Generic UI**: A checkout flow, a hotel room rate matrix, a patient vitals board, and a terminal log viewer have distinct information densities, trust requirements, and UX conventions.
- **Evidence-Based, Multi-Signal Classification**: Domain selection is deterministic, combining route patterns, component names, vocabulary signals, and explicit user declarations. No LLM "taste" or arbitrary guesswork.
- **Not a Rigid Template**: Domain Packs never prescribe fixed visual styling (e.g. "hero must be 720px" or "primary button must be blue"). They provide information hierarchy, state requirements, trust patterns, and UX conventions. Visual realization remains governed by the Design System, Existing UI Identity, and User Constraints.
- **Context-Budgeted Subtopics**: Tasks that only touch a local button or checkout flow do not load unrelated catalog flows. Subtopics allow fine-grained, task-aware loading.
- **Strict Preservation Precedence**: Domain Pack guidance operates at **Level 6** of the Precedence Hierarchy. It can **NEVER** override existing brand identity, locked palettes, or framework constraints.

---

## 2. Architecture & Pipeline

```text
User Request
    ↓
UI Orchestrator (Phase 1)
    ↓
Repo Intelligence (Phase 2 repo_profile)
    ↓
Existing UI Analyzer (Phase 3 existing_ui_profile + preservation_profile)
    ↓
Task Intent Classifier (Phase 4 task_intent)
    ↓
Domain Intelligence (`uiux.engine.knowledge_router.domain_classifier`)
    ├── User Explicit Declaration (Highest precedence: 1.0 confidence)
    ├── Monorepo Scope Filter (`requested_scope` per application)
    ├── Multi-Signal Classifier (Routes + Components + Vocabulary)
    └── Domain Candidates (Primary + optional Secondary)
        ↓
Domain Pack Resolver (`uiux.engine.knowledge_router.domain_registry`)
    ├── Subtopic Query (`query_domain_subtopics`)
    ├── Critical Flows & Required States
    ├── Anti-Patterns & Trust Patterns
    └── Recommended Runtime Validation Mapping
        ↓
Knowledge Router (`uiux.engine.knowledge_router.router`)
    ├── Framework Pack (Version-Hardened)
    ├── Styling & UI Library Packs
    ├── Domain Pack (Primary + Secondary)
    ├── Relevant Design Skills
    ├── Preservation Invariants (Protected)
    └── Runtime Validation Packs
        ↓
Context Budget Manager (`uiux.engine.knowledge_router.budget`)
    └── Deterministic Pruning (Drops low/medium before high/critical)
        ↓
Context-Bounded Knowledge Plan (`knowledge_plan`)
```

---

## 3. Precedence Hierarchy (Rule 19)

Domain Intelligence strictly adheres to the established 8-level precedence hierarchy:

1. **Explicit user instruction** (e.g. "monochrome bank dashboard")
2. **Existing brand identity** (e.g. locked `#e11d48` primary color)
3. **Existing design system** (e.g. typography, token scale, spacing)
4. **Existing UX / information architecture** (e.g. global nav, routing structure)
5. **Repository / framework constraints** (e.g. Next.js 14 App Router rules)
6. **Domain best practices** (Domain Design Pack — Phase 5)
7. **Design inspiration** (e.g. editorial or brutalist aesthetic)
8. **AI preference** (Lowest priority, easily overridden)

> **Inviolable Invariant**: Domain best practices sit at Level 6. On an Existing UI project with a locked palette, domain knowledge **CANNOT** recolor the brand (e.g., cannot turn a red hotel website into blue travel colors, or force a healthcare dashboard into generic medical teal).

---

## 4. The 8 Mandatory Domain Design Packs

All 8 Domain Packs are implemented as machine-readable registry metadata ([domain_registry.py](file:///d:/Skill_AIcoding_Frontend/plugins/ui-engineering/uiux/engine/knowledge_router/domain_registry.py)) and comprehensive design guidance documents ([knowledge/domain-packs/](file:///d:/Skill_AIcoding_Frontend/plugins/ui-engineering/knowledge/domain-packs/)):

| Pack ID | Canonical Domain | Key Flows & Focus | Subtopics |
| :--- | :--- | :--- | :--- |
| `domain.ecommerce` | E-Commerce | Product cards, cart review, multi-step checkout, stock states, order tracking | `discovery`, `listing`, `product_detail`, `cart`, `checkout`, `order_state`, `trust` |
| `domain.beauty_fashion` | Beauty & Fashion | Editorial commerce, lookbooks, shade swatches, size guides, fit recommenders | `editorial_commerce`, `visual_browsing`, `variant_selection`, `product_storytelling`, `recommendations` |
| `domain.saas_ai` | SaaS & AI Products | Value props, pricing tables, workspaces, prompt inputs, streaming outputs | `public_surfaces`, `onboarding`, `dashboard`, `workspace`, `settings_billing`, `ai_interaction` |
| `domain.developer_tool` | Developer Tools | Dense CLI/logs, terminal viewports, error stack traces, syntax readability | `dense_information`, `code_terminal`, `diagnostics_logs`, `config_flows`, `documentation_ui` |
| `domain.hospitality_travel` | Hospitality & Travel | Date range selection, guest counters, room types, price breakdowns, vouchers | `search`, `date_guest`, `property_detail`, `room_selection`, `booking`, `confirmation` |
| `domain.healthcare` | Healthcare & HealthTech | Patient headers, vitals monitoring, appointment schedules, dosage visibility | `patient_records`, `appointment_scheduling`, `clinical_data_display`, `forms_entry`, `status_visibility` |
| `domain.finance_fintech` | Finance & FinTech | Balances, funds transfer, masked cards, audit records, explicit transaction confirmation | `dashboard_overview`, `transaction_clarity`, `transfer_flow`, `cards_wallets`, `audit_security` |
| `domain.portfolio_agency` | Portfolio & Agency | Case studies, outcome metrics, client showcase, contact conversion, restrained motion | `hero_narrative`, `project_showcase`, `case_study_detail`, `services_outcomes`, `contact_conversion` |

---

## 5. Domain Classification Model

The `classify_domain` function ([domain_classifier.py](file:///d:/Skill_AIcoding_Frontend/plugins/ui-engineering/uiux/engine/knowledge_router/domain_classifier.py)) uses composite evidence:
1. **Explicit Precedence**: If user declares `domain="ecommerce"` or `"hotel"`, confidence is `1.0` and source is `"explicit"`.
2. **Monorepo Scoping**: If project contains multiple sub-applications (`applications: { storefront: ..., admin: ..., docs: ... }`), domain classification targets the requested application scope rather than homogenizing the entire monorepo.
3. **Multi-Signal Score**:
   - Request vocabulary (e.g. "cart", "checkout", "vitals", "terminal")
   - Detected routes & pages (e.g. `/products`, `/rooms`, `/patients`, `/logs`)
   - Detected component names (e.g. `ProductCard`, `DateRangePicker`, `VitalSignsCard`, `CodeBlock`)
4. **Safeguard against Over-Inference**: Single weak route matches (e.g. just `/pricing` or just `/products` in a documentation site) cannot trigger a domain pack without supporting signals.
5. **Multi-Domain Detection**:
   - Exactly **1 primary domain** is selected.
   - At most **1 secondary domain** is allowed if strong secondary evidence exists (e.g. Beauty E-Commerce: Primary = `ecommerce`, Secondary = `beauty_fashion`).
   - Weak secondary evidence is discarded to prevent context bloat.
6. **Safe Fallback**: Unrecognized domains or weak evidence fall back to `"general"` with confidence `0.30` without crashing.

---

## 6. Task-Aware Subtopic Routing

Loading entire domain documents for local tasks bloats context windows.
`query_domain_subtopics(domain_name, user_request, task_intent)` selects only subtopics matching the current task:

- **Local / Minor Tasks** (e.g. `user_request="fix button alignment on product card"`):
  - Subtopics: `[]` (empty)
  - Domain pack weight: `"small"` (1 point)
  - Full checkout or discovery flows are **NOT** dumped into context.
- **Specific Flow Tasks** (e.g. `user_request="Redesign the checkout payment flow and order summary"`):
  - Subtopics: `["checkout", "cart", "trust"]`
  - Domain pack weight: `"medium"` (2 points)
- **Comprehensive Page Tasks** (e.g. `user_request="Full redesign of the entire landing page"`):
  - Subtopics: top 3 core subtopics (e.g. `["discovery", "listing", "product_detail"]`).

---

## 7. Context Budget & Pruning Integration

Domain packs are fully integrated into `ContextBudgetManager`:
- Domain packs are categorized as `category: "domain"`, `required: False`.
- Primary domain priority is `"high"`; secondary domain priority is `"medium"`.
- When context budget is exceeded:
  1. Low-priority optional items are pruned first.
  2. Secondary domain packs (`priority: "medium"`) are pruned next.
  3. Primary domain pack (`priority: "high"`) is pruned only if budget is severely constrained.
  4. **Preservation invariants (`priority: "critical"`) and required framework packs are NEVER pruned** to accommodate domain packs.

---

## 8. Greenfield vs. Existing UI Behavior

### Greenfield Workflow
- Domain packs influence visual hierarchy, page inventory, default flow structure, and required UI states.
- Domain guidance never overrides explicit user constraints (e.g. if user asks for a "monochrome healthcare dashboard", the UI respects the monochrome instruction while maintaining high-contrast accessibility and patient data clarity).

### Existing UI Workflow
- Domain packs **CANNOT** alter existing brand colors, typography scales, design system tokens, or global navigation structures.
- Domain packs are used exclusively to:
  - Identify missing UX states (loading skeletons, empty search, error boundaries, payment pending).
  - Enhance information hierarchy (e.g. date context clarity in hotels, fee visibility in fintech).
  - Prevent domain-specific anti-patterns (e.g. hidden charges, ambiguous CTAs, obscured numbers).

---

## 9. Phase 4 Hardening Verification

Phase 4 framework version compatibility has been verified and hardened:
- Framework metadata defines `version_features` (e.g. Angular `@if`/`@for` control flow requires `>= 17.0.0`, Svelte runes require `>= 5.0.0`, Vue Composition API setup requires `>= 3.0.0`, Next.js App Router requires `>= 13.0.0`).
- When framework version is unknown or incompatible, the Knowledge Router automatically assigns the `"generic_safe"` guidance tier, suppressing version-incompatible APIs.
- When framework version is known and compatible, the router assigns the `"standard"` guidance tier with active feature flags.

---

## 10. Phase 6 Extension Boundary

Phase 5 strictly establishes the domain intelligence, classification, and knowledge routing layer.
The following capabilities are deliberately left to subsequent phases:
- **Phase 6**: Modification Planner, Code Editing Engine, controlled patch generation.
- **Phase 7**: Runtime Critic, automated visual regression detection, self-repair loops.
- **Phase 8/9**: Package marketplace distribution, external ecosystem adapters.
