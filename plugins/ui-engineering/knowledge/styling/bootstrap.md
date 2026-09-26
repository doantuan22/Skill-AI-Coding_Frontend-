# Bootstrap UI Engineering Knowledge Pack

**Pack ID**: `styling.bootstrap`  
**Category**: `styling`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Grid & Layout Utilities
- **12-Column Grid**: Use `.container`, `.row`, and responsive `.col-{breakpoint}-{size}` (`col-12 col-md-6 col-lg-4`).
- **Flex & Spacing**: Use Bootstrap spacing utilities (`p-3`, `my-4`, `d-flex justify-content-between align-items-center`).

## 2. Hard Preservation & Anti-Fight Rule
- **Do NOT Fight Bootstrap**: Avoid writing hundreds of `!important` CSS overrides against Bootstrap primitives. Customize via Sass variables (`$theme-colors`, `$border-radius`) or targeted wrapper classes.
- **Do NOT Migrate Away**: Never rewrite Bootstrap code into Tailwind, MUI, or another framework unless the user explicitly requested a complete styling migration.
