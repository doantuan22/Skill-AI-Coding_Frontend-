# Greenfield UI Workflow

## Trigger Conditions
Use the Greenfield UI Workflow when:
- The repository has no significant existing UI/UX (`ui_state == "GREENFIELD"`); OR
- The user explicitly instructs building a new interface from scratch (e.g., "xây lại từ đầu", "rebuild from scratch", "new app").

## Execution Flow

```text
Requirement
    ↓
Product / Domain Understanding
    ↓
Page Inventory
    ↓
UX Flow
    ↓
Design Direction
    ↓
Design System (Tokens / Palette / Typography)
    ↓
Implementation (Component Realization)
    ↓
Validation (Accessibility Gate / Visual QA)
```

1. **Requirement Analysis**: Normalize intent, identify core user personas, key use cases, and functional scope.
2. **Product / Domain Understanding**: Determine domain constraints (e.g., fintech, developer tool, luxury e-commerce, consumer app) and target user expectations.
3. **Page Inventory & Information Architecture**: Enumerate every screen/route required. Multi-page projects must document the inventory before code implementation.
4. **UX Flow**: Define user journey, primary task paths, edge cases, error states, and empty states.
5. **Design Direction & Inspiration**: Establish visual character, mood, tone, and reference DNA (via `skills/design-direction` and `skills/design-inspiration`).
6. **Design System & Tokens**: Select color palette, typographic hierarchy, elevation, spacing scale, and radius system (via `skills/design-system` and `skills/typography`).
7. **Implementation**: Build UI components, layouts, and pages cleanly adhering to the design tokens and structural contract.
8. **Validation**: Execute Accessibility Gate, responsive checks across mobile/tablet/desktop, and visual QA review.

## Invariant Rules

1. **Design Freedom Policy**:
   - If the user has NOT specified a style, color palette, or typography, the AI is granted design freedom to select them.
   - Selection MUST be rigorously grounded in:
     - **Product type** (e.g., analytics dashboard vs. marketing showcase)
     - **Domain** (e.g., healthcare, fintech, creative agency)
     - **Target user** (e.g., engineers, casual consumers, executives)
     - **Use case** (e.g., high-frequency data entry vs. exploratory reading)
     - **Content density** (compact, comfortable, spacious)
   - The AI must NEVER choose arbitrarily or randomly based on personal AI preference. Every choice requires a *why* and *why not*.

2. **User Constraint Precedence**:
   - If the user specifies any color, palette, typography, visual style, or framework, the **explicit user instruction has highest priority** (Precedence Level 1).
   - The AI cannot overwrite or ignore user-specified constraints in favor of catalog recommendations.

3. **Multi-Page Gate**:
   - Prior to implementing code across multiple pages, the AI must establish:
     - Page Inventory (`PAGE-MAP.md`)
     - UX Flow (`UX-FLOW.md`)
     - Minimal Design System / Tokens (`DESIGN-TOKENS.md` / `DESIGN-SYSTEM.md`)
