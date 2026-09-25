# Button grammar

Define only variants required by the locked flow: primary, secondary, tertiary/ghost, destructive, icon-only and link-like action. For every allowed variant specify height, horizontal padding, radius/shape, label weight, icon size/gap, border, elevation and default/hover/focus-visible/pressed/disabled/loading states in the Visual Grammar and Component Spec.

| Variant | Role | Rules |
|---|---|---|
| primary | one dominant next action per local decision | strongest contrast; do not use for all actions |
| secondary | alternate meaningful action | visible but clearly subordinate |
| tertiary / ghost | low-emphasis contextual action | retain target, focus and hover clarity without fake prominence |
| destructive | irreversible/risky action | explicit destructive semantic; never rely on red alone |
| icon-only | familiar, space-constrained action | accessible name, target size and tooltip when label is otherwise unclear |
| link-like | navigation, not command | behaves and reads as navigation |

Detect unexplained pill shapes, gradient CTAs, colored glow shadows, inconsistent icon placement, primary-everywhere hierarchy, and incompatible radius/weight. Do not turn every control into the same rounded rectangle.

