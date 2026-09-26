# Svelte UI Engineering Knowledge Pack

**Pack ID**: `framework.svelte`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Component & Reactivity Patterns
- **Reactivity**: Use standard Svelte reactivity primitives (Svelte 4 `$: ` or Svelte 5 runes `$state`, `$derived`, `$props` based on detected version).
- **Props & Bindings**: Declare props clearly; use `bind:value` only when two-way binding is appropriate for form controls.
- **Slots & Snippets**: Use `<slot />` or Svelte 5 `{#snippet}` for modular component composition.

## 2. Accessibility & Scoped Styles
- **Compiler Warnings**: Never ignore Svelte accessibility warnings (e.g., `a11y-click-events-have-key-events`, `a11y-missing-attribute`).
- **Scoped Styles**: Leverage Svelte's built-in component-scoped `<style>` blocks.
- **Preserve Architecture**: Keep existing component locations and naming patterns intact.
