# Stack strategy

| Stack | Prefer |
|---|---|
| Plain HTML/CSS/JS | Tokens, base, layout, components, utilities, then pages; semantic elements first. |
| Tailwind | Theme tokens, shared component patterns, and disciplined utilities; avoid repeated arbitrary values. |
| Bootstrap | Variables, existing utilities, component overrides, then minimal custom CSS. |
| Component framework | Existing project architecture, shared primitives, and established styling/theme mechanism. |

Use `header`, `nav`, `main`, `section`, `article`, `form`, `label`, `button`, `table`, and `dialog` for their purpose rather than a div-only implementation. Do not rewrite a project for a preferred framework.
