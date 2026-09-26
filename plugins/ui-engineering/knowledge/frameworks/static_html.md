# HTML/CSS/JS UI Engineering Knowledge Pack

**Pack ID**: `framework.static_html`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Semantic HTML5 & Modern Layouts
- **Semantic Structure**: Use `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>` instead of unsemantic `<div>` soup.
- **Modern CSS Layouts**: Rely on CSS Grid (`display: grid`) and Flexbox (`display: flex`) with CSS variables (`var(--spacing-md)`) rather than floats or absolute positioning.
- **Responsive Meta**: Ensure `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present in HTML heads.

## 2. Progressive Enhancement & DOM Interaction
- **Progressive Enhancement**: Content should remain legible and functional even before JavaScript loads.
- **Targeted DOM Queries**: Use `document.querySelector` and event delegation. Avoid monolithic inline scripts.
- **Do Not Add Frameworks**: Never arbitrarily inject React, Vue, or heavy dependencies into a static HTML project.
