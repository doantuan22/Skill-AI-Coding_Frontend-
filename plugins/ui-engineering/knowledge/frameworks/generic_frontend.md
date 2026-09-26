# Generic Frontend UI Engineering Fallback Pack

**Pack ID**: `framework.fallback`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Universal Frontend Principles
- **Semantic Structure**: Always use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<button>`, `<input>`, `<footer>`).
- **Responsive Layout**: Use Flexbox and CSS Grid with relative units (`rem`, `%`, `vh/vw`) to adapt across viewports.
- **A11y Baseline**: Ensure 4.5:1 text contrast (WCAG AA), visible keyboard `:focus-visible` outlines, and explicit form input labels.
- **Graceful Fallback**: When framework is unknown or custom, never hallucinate framework-specific abstractions (like React JSX or Vue directives); rely on standard web platform APIs.
