# SaaS & AI Product Domain Design Pack

**Pack ID**: `domain.saas_ai`  
**Domain**: `saas_ai`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `saas`, `ai`, `b2b`, `cloud`, `platform`, `workspace`  

---

## 1. User Types & Operational Context
- **Primary Users**: Knowledge workers, developers, product managers, business analysts, team collaborators.
- **Key Psychology**: Efficiency-focused, task-driven, values clarity and predictable feedback, intolerant of confusing workflows or fake progress.

## 2. Domain Subtopics
- `public_surfaces`: Value proposition hero, feature breakdowns, transparent pricing tiers, documentation links.
- `dashboard`: Key metric cards, recent activity streams, quick action shortcuts, personalized operational feeds.
- `workspace`: Multi-pane layouts, persistent sidebars, collaborative canvases, resource tables.
- `onboarding`: Multi-step progress wizards, interactive product tours, sample data presets.
- `settings_billing`: Team member permissions, API keys, usage meter gauges, subscription tiers.
- `ai_interaction`: Prompt input bars, streaming token responses, response citations/sources, thumbs up/down feedback, regeneration controls.

## 3. Critical Flows
1. **Onboarding to First Value**: Sign up -> role selection -> guided quick start -> immediate tangible output.
2. **Dashboard Navigation**: Checking KPI summary -> filtering table of records -> drilling down to detailed view.
3. **AI Task Execution**: Typing prompt -> viewing generation progress -> inspecting citations/reasoning -> copying or modifying output.

## 4. Information Hierarchy & UX Patterns
- **Clear Information Density**: Balanced density (comfortable by default, compact option for heavy data tools).
- **Public vs Product Split**:
  - Marketing pages: High contrast, narrative flow, clear CTA ("Start Free Trial", "Book Demo").
  - App workspace: Utilitarian, predictable, toolbars close to canvas/editor, keyboard shortcut cues (`Cmd+K`).
- **AI UX Discipline**:
  - Distinct visual separation between user prompt and generated AI content.
  - Streaming feedback: Show pulsating cursor or loading indicator while generating.
  - Actionable output: Provide one-click "Copy", "Regenerate", "Insert", and "Provide Feedback" actions.

## 5. Required UI States
- `loading`: Skeleton loaders for charts and tables; streaming typewriter effect for AI text generation.
- `empty`: Actionable empty states with primary creation CTA ("Create your first project") and template shortcuts.
- `error`: Non-blocking toast notifications for network drops; inline retry buttons for failed AI generations.
- `plan_limit`: Gentle in-context upgrade nudges when reaching usage quotas without blocking current work abruptly.

## 6. Responsive & Accessibility Priorities
- **Responsive**: Collapsible navigation sidebar into a bottom drawer or hamburger menu; horizontally scrollable data tables with sticky primary column.
- **Accessibility**:
  - Keyboard navigation for command bars (`Cmd+K`) and data grids.
  - Announce completion of background generation via `aria-live="polite"`.
  - Accessible contrast for muted secondary metadata (dates, authors, tags).

## 7. Anti-Patterns to Avoid
- **Dark Gradient AI Slop**: Forcing dark neon purple gradients on every screen when the product is an enterprise SaaS tool.
- **Feature Overload Dashboard**: Cramming 25 unrelated metric widgets onto the home screen without hierarchy.
- **Unclear AI Disclaimers**: Hiding hallucinations without giving users tools to review sources or edit output.

## 8. Workflow Integration & Precedence
- **Greenfield**: Establishes dashboard layout shells, pricing tables, and onboarding flows.
- **Existing UI**: Subordinate to existing product design systems. Never force a consumer AI aesthetic onto a structured enterprise B2B dashboard.
