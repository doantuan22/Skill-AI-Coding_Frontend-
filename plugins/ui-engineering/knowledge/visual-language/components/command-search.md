# Command, search and filter grammar

| Component | Design rules | States | Implementation guidance |
|---|---|---|---|
| **Command palette** | Centered near top, 560–720px wide; input first; results grouped (navigation, actions, recent); shortcut hints right-aligned in kbd style; one highlighted row | closed, empty (recent + suggestions), results, no results (suggest alternatives), running | Combobox + listbox semantics; open in under 150ms; do not animate results per keystroke; Escape closes and restores focus |
| **Search field** | Visible label or accessible name; leading search icon; clear button once text exists; suggestions anchored below | empty, typing, suggestions, submitted, no results, error | `type="search"`, debounce requests, keyboard selection of suggestions, `aria-live` result count |
| **Filters** | Facets grouped by meaning; applied filters shown as removable chips with a "clear all"; counts next to options when cheap | none applied, applied, loading results, zero results | URL reflects filters; on mobile use a sheet with an apply button and result count; `motion.m2-filter-transition` only for small result sets |
| **Pagination** | Current page clear; previous/next plus limited page numbers; show total when known | first, middle, last, loading | Use real links (`<a href>`) for crawlable lists; for infinite lists provide "load more" and keep footer reachable |
| **Breadcrumbs** | Show hierarchy, not history; current page not a link; truncate middle levels on small screens | default, truncated | `nav` with `aria-label="Breadcrumb"`, ordered list, `aria-current="page"` |

Anti-patterns: search hidden behind an icon on desktop when search is primary; filters that reset the query; palette as the only route to an action; chips in rainbow colors.
