# Styled Components & CSS-in-JS Knowledge Pack

**Pack ID**: `styling.styled_components`  
**Category**: `styling`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Component Styling & Theme Integration
- **Theme Props**: Access theme tokens via `${({ theme }) => theme.colors.primary}` or `${({ theme }) => theme.spacing(2)}`.
- **Dynamic Props**: Pass transient props (`$isActive`) that should not be forwarded to DOM nodes.
- **Prevent Duplication**: Extract recurring styled primitives (Card, Container, Badge) rather than declaring duplicate styled literals across files.

## 2. Preservation Rules
- **Maintain CSS-in-JS Engine**: Do not migrate styled-components to Tailwind or plain CSS unless the task explicitly requests an engine migration.
- **Preserve Global Styles**: Keep `createGlobalStyle` definitions unmodified.
