# CSS Modules Knowledge Pack

**Pack ID**: `styling.css_modules`  
**Category**: `styling`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Scoped Classes & Composition
- **Class Mapping**: Import styles as `styles from './Component.module.css'` and access via `styles.className`.
- **CSS Composition**: Use `composes: baseButton from './common.module.css'` to share styles without polluting the global scope.
- **Naming Convention**: Follow existing camelCase or kebab-case conventions used in the project.
