# Form and control grammar

Keep field height, label relationship, help/error placement, required indication, border/focus behavior and validation feedback consistent. Use control variants to express input type, not decoration. Inline errors stay with the field; submission/system outcomes follow feedback grammar. States must remain identifiable without color alone.

| Control | Rules |
|---|---|
| Text input | Visible label, 16px+ text on mobile, helper/error below, focus ring distinct from error state |
| Select | Native `select` for short, simple lists; custom listbox only when options need rich content, with full keyboard support |
| Combobox | For long or searchable lists; typed filtering, highlighted match, "no results" row, ARIA combobox pattern |
| Upload field | Browse button plus optional drop zone; see [data-display.md](data-display.md) |

Micro motion for controls follows [M1 micro motion](../../motion/microinteractions.md).
