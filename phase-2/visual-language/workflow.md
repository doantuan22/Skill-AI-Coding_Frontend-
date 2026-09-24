# Visual language workflow

1. Read active `DESIGN-DIRECTION.md`, `DESIGN-SYSTEM.md`, `DESIGN-TOKENS.md`, the Structure Lock, and relevant current-system/component artifacts.
2. For existing UI, extract representative components and classify `KEEP`, `REFINE`, `NORMALIZE`, or `REPLACE`; record the reason and blast radius in `VISUAL-GRAMMAR.md`.
3. Create or update [VISUAL-GRAMMAR.md](../../templates/VISUAL-GRAMMAR.md): color, type, surface, motion and selected component grammars, with approved exceptions.
4. Select targeted references: buttons, feedback, iconography, forms, navigation, data, overlays, status/states, or anti-slop/craft review. Do not load the whole module for a small change.
5. Hand off selected behavior to Component Specs; implement a representative component/page before broad normalization.
6. Run craft review, adversarial review where triggered, then browser visual QA and accessibility. A visual issue returns here; a semantic mismatch returns to Phase 1.

## Existing-system decision rules

- `KEEP`: coherent, accessible, task-fitting and consistent with direction; document it and do not restyle it.
- `REFINE`: sound pattern with local craft defects; make smallest focused correction.
- `NORMALIZE`: same responsibility has accidental variants; converge to an existing approved pattern/token.
- `REPLACE`: direction conflict, serious usability defect, or persistent drift; record evidence, migration scope and regression target.

