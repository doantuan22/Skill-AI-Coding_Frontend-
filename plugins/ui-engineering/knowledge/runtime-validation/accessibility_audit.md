# Accessibility Audit Validation Knowledge

**Knowledge ID**: `runtime.accessibility_audit`  
**Category**: `runtime`  
**Priority**: `medium`  
**Status**: Active  

---

## 1. Automated axe Core Checks
- Contrast: Verify 4.5:1 text-to-background contrast ratio (3:1 for large text).
- Label association: Ensure all `<input>`, `<select>`, `<textarea>` have linked `<label>` or `aria-label`.
- Landmarks: Confirm presence of `<main>` and unique `aria-label` for `<nav>` elements.

## 2. Keyboard & Focus Flow
- Tab order follows visual flow left-to-right, top-to-bottom.
- Focused elements display visible outline (`:focus-visible`).
- Modal dialogs trap focus and release upon dismissal with `Escape`.
