# React UI Engineering Knowledge Pack

**Pack ID**: `framework.react`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Core Component Composition
- **Composition over Inheritance**: Assemble complex UIs by nesting focused, single-responsibility components rather than passing excessive boolean configuration flags.
- **Children & Slots**: Use `children` or explicit render props/elements (`slotLeft`, `actionSlot`) for flexible UI layout composition.
- **Preserve Component Architecture**: When extending an existing codebase, mirror the existing component folder structure (e.g. `components/ui/` vs `components/common/`) and naming conventions (`PascalCase.tsx`).

## 2. State Placement & UI Form Discipline
- **Localize State**: Keep UI state as close as possible to where it is consumed. Do not hoist toggle, accordion, or input focus states into global stores (Redux/Zustand) unless multiple distant components require synchronization.
- **Controlled vs Uncontrolled**:
  - Prefer controlled inputs for dynamic form validation, multi-step wizards, or when submit actions depend on real-time validity.
  - Use uncontrolled inputs with `ref` or native `FormData` for simple submit-and-forget forms to minimize re-renders.
- **Form UX States**: Always render explicit visual feedback for `submitting` (disabled button + spinner), `error` (inline message associated with input), and `success`.

## 3. Responsive & Accessibility Conventions
- **Accessible Primitives**:
  - Ensure every interactive element is a `<button>`, `<a>`, or `<input>`. Never attach `onClick` to `<div>` without `role="button"`, `tabIndex={0}`, and `onKeyDown`.
  - Always link form `<label htmlFor={id}>` to `<input id={id}>`.
- **Responsive Layout**: Build components that adapt to parent container width using Flexbox, CSS Grid, and responsive utility classes (`sm:`, `md:`, `lg:`).

## 4. Performance & Rendering Safety
- **Stable Keys**: Always use unique, stable identifiers for `key` props in lists (e.g., `item.id`). Never use array index when items can be filtered, reordered, or deleted.
- **Avoid Render Loops**: Ensure `useEffect` dependencies are primitives or memoized (`useCallback`, `useMemo`) when referencing functions or objects.

## 5. Existing UI Hard Preservation Rules
- **Do not introduce new state management libraries** without explicit user permission.
- **Preserve existing hook conventions** (e.g., custom form hooks, design token hooks).
