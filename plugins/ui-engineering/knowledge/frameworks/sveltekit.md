# SvelteKit UI Engineering Knowledge Pack

**Pack ID**: `framework.sveltekit`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Routing & Layout Structure
- **File Conventions**:
  - `+layout.svelte`: App shell and persistent layouts across child routes.
  - `+page.svelte`: Route view component.
  - `+error.svelte`: Contextual error boundary page.
- **Navigation**: Use native `<a>` tags with SvelteKit's client-side router (`data-sveltekit-preload-data`).

## 2. Page & Layout Data
- **Data Ingestion**: Render UI driven by `export let data` (or `$props()`) passed from `+page.ts` / `+page.server.ts`.
- **Preserve Routing Invariants**: Do not alter directory layout under `src/routes/` unless explicitly requested.
