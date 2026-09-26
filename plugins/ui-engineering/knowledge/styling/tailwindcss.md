# Tailwind CSS UI Engineering Knowledge Pack

**Pack ID**: `styling.tailwindcss`  
**Category**: `styling`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Token Discipline & Utility Composition
- **Avoid Arbitrary Values**: Prefer theme tokens (`bg-primary`, `p-4`, `rounded-lg`) over hardcoded arbitrary values (e.g. `bg-[#2563eb]`, `w-[347px]`) unless adhering to an exact existing token.
- **Consistent Scales**: Use Tailwind's default spacing (`4`, `6`, `8`), color shades, and border radius scales to ensure visual rhythm.
- **Component Extraction**: When utility chains repeat identically across multiple components, extract them into a reusable component or `@apply` utility class.

## 2. Responsive & State Variants
- **Mobile-First Design**: Write default classes for mobile viewports, layering `sm:`, `md:`, `lg:`, `xl:` modifiers for larger screens.
- **Interactive States**: Always define `:hover`, `:focus-visible`, and `:active` variants for buttons and inputs.
- **Dark Mode**: If dark mode is active (`class` or `media`), maintain paired utilities (`bg-white dark:bg-slate-900`).

## 3. Existing UI Hard Preservation Rules
- **NEVER change theme colors, config palette, or brand tokens** in `tailwind.config.js` without explicit user permission.
- **Do not introduce arbitrary external styling engines** alongside an existing Tailwind installation.
