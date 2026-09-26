# Material UI (MUI) Knowledge Pack

**Pack ID**: `styling.mui`  
**Category**: `styling`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Theme & Component Overrides
- **ThemeProvider**: Respect the global `theme` object (`palette`, `typography`, `shape`, `components`).
- **`sx` Prop & `styled` API**: Use `sx={{ p: 2, display: 'flex', color: 'primary.main' }}` for one-off layouts, referencing theme tokens rather than raw hex colors.
- **Accessible Primitives**: Retain built-in MUI accessibility landmarks and ARIA bindings.

## 2. Preservation Rules
- **Do not switch styling engine**: Do not mix Tailwind classes into MUI components unless the project explicitly configured `@mui/material` with Tailwind integration.
- **Preserve theme tokens**: Do not change default primary/secondary theme colors without explicit user authorization.
