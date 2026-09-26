# Existing UI/UX Workflow

## Trigger Conditions
Use the Existing UI/UX Workflow when:
- The repository already has established UI components, styles, design tokens, or pages (`ui_state == "EXISTING_UI"` or `"PARTIAL_UI"`); AND
- The user has not explicitly requested a full rebuild from scratch.

## Hard Preservation Rule (MANDATORY)

```text
PRESERVE FIRST
    ↓
IMPROVE SECOND
    ↓
REDESIGN ONLY WHEN EXPLICITLY REQUESTED
```

The primary duty of the agent in an existing codebase is to protect established brand identity, design tokens, and user muscle memory while improving consistency, responsiveness, and accessibility.

## Default Protection Matrix

| Property | Default State | Policy |
|---|---|---|
| **Color palette / brand colors** | `LOCKED` | Must NOT be modified or replaced without explicit user permission. |
| **Brand identity & typography** | `LOCKED` | Brand font families, voice, and visual character are strictly maintained. |
| **Overall layout identity** | `PROTECTED` | Header, sidebar, content grid structure are preserved. |
| **Navigation model** | `PROTECTED` | Route structure, URLs, tab models, and primary nav hierarchy are preserved. |
| **Information architecture** | `PROTECTED` | Page hierarchies and entity relationships cannot be arbitrarily restructured. |
| **Component structure** | `CONTROLLED` | Existing component APIs and variants are reused and extended, not rewritten. |
| **Spacing / alignment / hierarchy**| `ALLOWED` | Refining rhythm, alignment bugs, padding inconsistencies is allowed (L1). |
| **Responsive / accessibility** | `ALLOWED` | Adding mobile breakpoints, fixing WCAG AA contrast, keyboard navigation is allowed (L1). |
| **Semantic states & feedback** | `ALLOWED WITH PRESERVATION` | Adding hover, focus, error, loading states using existing color tokens is allowed (L1). |

## Vague Improvement Trap

Requests containing phrases such as:
- *"modernize UI"*
- *"làm đẹp giao diện"*
- *"nâng cấp UI/UX"*
- *"đồng bộ giao diện"*
- *"make it more professional / cleaner / prettier"*

**MUST NEVER** be interpreted as permission to:
- Change the color palette or brand colors
- Introduce an unrequested visual theme or style family
- Execute a full page or global redesign
- Rewrite navigation or information architecture
- Swap out the UI framework or component library

Such requests only authorize **L1 Safe Refinements** (or **L2 Local Structural Changes** when accompanied by technical/UX justification).

## Change Budget Model (L1 / L2 / L3)

### L1 – Safe Refinement (Default: `ALLOWED`)
- Spacing, padding, margins, visual alignment
- Typography scale adherence and hierarchy clarity
- Responsive adaptability (mobile/tablet/desktop)
- Component states (hover, active, focus-visible, disabled, loading, empty)
- Accessibility fixes (color contrast, ARIA labels, focus traps)
- Consistency alignment with existing design tokens

### L2 – Local Structural Change (Default: `JUSTIFIED ONLY`)
- Internal component layout reorganization
- Section arrangement within an existing page
- Form step grouping or field flow clarification
- Card internal hierarchy adjustments
- Local breadcrumb or in-page navigation details
- *Condition*: Requires explicit UX rationale or technical necessity documented in task scope.

### L3 – Major Redesign (Default: `DENIED`)
- Global color palette change or new color system
- Brand visual language overhaul
- Page architecture or global layout rebuilding
- Global navigation hierarchy restructuring
- Full component library replacement or framework swap
- *Condition*: **DENIED by default**. Allowed **ONLY** when explicit, unambiguous user permission is granted.

## Execution Flow for Existing UI

1. **Extraction / Observation**: Inspect current components, styling conventions, design tokens, and layout (`CURRENT-UX-MAP.md`).
2. **Scope Isolation**: Determine if the task is global, page-level, or local component-level. Local component tasks are strictly isolated from global redesign.
3. **Change Budget Determination**: Verify permissions for L1, L2, or L3 based on explicit user prompt.
4. **Targeted Improvement**: Apply refinements using existing design system tokens and component patterns.
5. **Preservation & Non-regression Gate**: Validate that brand colors, fonts, and layout invariants are intact before marking complete.
