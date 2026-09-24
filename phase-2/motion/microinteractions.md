# Microinteractions

Fast, low-intensity feedback on controls. They must match the [button](../visual-language/components/buttons.md) and [forms](../visual-language/components/forms-controls.md) grammar and share timing tokens.

| Pattern | Purpose | Good | Bad | Intensity / timing | Perf | A11y | Implementation |
|---|---|---|---|---|---|---|---|
| **hover shift** (color/background) | Affordance | Buttons, links, rows | Only feedback on touch devices (hover absent) | low, 100–150ms | color/background cheap | Must not be the only state cue; pair with focus-visible | `transition: background-color, color` |
| **hover lift** (translateY −1/−2px, shadow) | Indicates clickable surface | Clickable cards that navigate | Non-interactive cards; buttons in dense UI; every element | low, 150ms | transform + opacity of a pre-rendered shadow layer | Reduced → no translate | Animate a pseudo-element's opacity for shadow |
| **press response** (scale 0.97–0.98 / darken) | Tactile confirmation | Primary buttons, toggles, mobile taps | Large surfaces (scaling blurs text) | low, 50–100ms | transform | Safe | `:active { transform: scale(.98) }` |
| **underline transition** | Link affordance | Editorial/text links, nav | Replacing a missing underline with hover-only | low, 150ms | `text-decoration-color`/`background-size` | Underline must be present at rest for body links | Animate thickness/offset or background-size |
| **icon transform** (chevron rotate, menu→close) | State change legibility | Disclosure, menus | Spinning decorative icons | low, 150–200ms | transform | Reduced → instant swap | Rotate via transform; `aria-expanded` owns semantics |
| **button feedback** (loading, success) | Async state | Submit, save | Removing the label so width jumps | medium, 150–250ms | avoid width animation; reserve space | Announce via `aria-live`/status; keep disabled semantics correct | Keep min-width; swap content with opacity |
| **focus transition** | Show focus | All interactive controls | Delayed/animated-in focus ring that is invisible at first | low, 0–100ms | outline/box-shadow | Focus must be visible immediately; never animate from invisible for > 100ms | `:focus-visible` ring; optional quick fade |

Rules:

- Transition named properties only; no `all`.
- Hover effects are enhancements: wrap strong hover movement in `@media (hover: hover) and (pointer: fine)`.
- Equivalent controls share identical microinteractions (component personality).
