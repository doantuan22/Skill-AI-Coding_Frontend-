# shadcn/ui Component & Styling Knowledge Pack

**Pack ID**: `ui_library.shadcn_ui`  
**Category**: `ui_library`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Composition & Radix Primitives
- **Unstyled Primitives**: Components are built on Radix UI primitives (`@radix-ui/react-*`), providing full keyboard navigation, ARIA states, and focus trapping out-of-the-box.
- **Class Merging**: Always use the project's `cn(...)` utility (combining `clsx` and `tailwind-merge`) when extending component styles:
  ```tsx
  className={cn("base-classes", variantClasses, className)}
  ```

## 2. Hard Preservation Rules
- **No Blanket Re-Generation**: Do NOT run CLI commands that regenerate or overwrite customized components in `components/ui/`.
- **Preserve Existing Customizations**: If the team has added custom variants (e.g. `variant="gradient"`, `size="xl"` in `buttonVariants`), preserve and reuse them.
- **Preserve CSS Variables**: Rely on existing HSL CSS custom properties (`--background`, `--foreground`, `--primary`, `--radius`).
