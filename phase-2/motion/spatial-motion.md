# Spatial motion

Spatial motion explains where something comes from and where it goes. Direction must match the interface's spatial model and the trigger.

| Pattern | Purpose | Good | Bad | Intensity / timing | Perf | A11y | Implementation |
|---|---|---|---|---|---|---|---|
| **modal enter/exit** | Focus shift to bounded task | Short confirmations, forms | Long workflows; bouncy scale on destructive dialogs | medium; 200–300ms enter, ~150–200ms exit; scale 0.96→1 + fade, backdrop fade | transform/opacity; backdrop blur is costly — avoid animating blur | Focus trap, return focus, `Esc`; reduced → fade only | Native `<dialog>` + CSS transitions (`@starting-style` / `allow-discrete` where supported) or existing component library |
| **drawer** | Secondary context from an edge | Filters, navigation, details | Primary content that should be a page | medium; 250–350ms | transform translateX/Y | Reduced → fade or instant; focus management as modal | Translate from the edge of its trigger/side |
| **expand/collapse** | Reveal detail in place | Rows, sections, cards | Animating `height` on large content repeatedly | low–medium; 150–250ms | Prefer `grid-template-rows: 0fr→1fr` or `interpolate-size` where supported; avoid JS height measurement loops | `aria-expanded`, content reachable; reduced → instant | CSS grid-rows technique |
| **popover / dropdown / tooltip** | Anchor content to trigger | Menus, pickers, tooltips | Large distance travel | low; 120–200ms; scale from trigger origin | transform | Tooltip delay ~300–500ms show, instant hide; keyboard accessible | `transform-origin` at trigger |
| **accordion** | Sequential disclosure | FAQ, specs, settings | Hiding critical/required info | low; 150–250ms | as expand/collapse | Proper button semantics; reduced → instant | `<details>`/`<summary>` or accessible button pattern |
| **shared spatial movement** | Continuity between states/pages (thumbnail → detail) | Gallery → detail, list → item | Every navigation; complex multi-element morphs without purpose | medium; 250–400ms | View Transitions API or library FLIP; limit elements | Reduced → crossfade/instant | `view-transition-name` on the shared element, progressive enhancement |

Rules: exit is faster than enter; interruptible transitions (reversing mid-way) are preferred over queued animations; never block input while an overlay animates in beyond ~100ms.
