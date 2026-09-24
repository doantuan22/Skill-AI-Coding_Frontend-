# Scroll motion

For marketing and storytelling pages only. Scroll motion is the most expensive in performance, accessibility and attention; it must carry narrative, not decoration. Check [performance-safety.md](performance-safety.md) before implementing any entry here.

| Pattern | Purpose | Good | Bad | Intensity | Perf | A11y | Implementation |
|---|---|---|---|---|---|---|---|
| **section reveal** | Pace reading order | Marketing sections, once | App screens; re-triggering; hiding content until JS runs | low–medium | IO + transform/opacity | Reduced → none; content visible without JS | IO adds class once, unobserve |
| **sticky storytelling** | Explain a sequence while a visual stays in place | 3–6 steps each changing one visual state | One or two steps; long text in sticky column; mobile without fallback | high | `position: sticky`; swap states via IO, not scroll handlers | Every step readable as normal content; reduced → static stacked steps | Sticky visual + IO-observed step list; stack on mobile |
| **parallax** | Depth between foreground/background | Rare atmospheric hero with layered media | Text layers; multiple parallax sections; mobile | medium–high | Can cause jank; native scroll-timeline or transform only; never `background-attachment: fixed` on mobile | Vestibular risk → disable on reduced motion | `animation-timeline: scroll()` in `@supports`; fallback static |
| **image scale** | Emphasize media as it enters | Hero or chapter media | Every image | medium | transform scale on a single layer | Reduced → static | `animation-timeline: view()` with fallback |
| **progress-linked transformation** | Show a process (assembly, data flow) tied to scroll | Product anatomy, pipeline explanation | Content that should be readable at any scroll position only | high | Linear easing; limited elements; precompute | Reduced → final state + stepwise static illustrations | Scroll-driven animation or rAF with IO gating |
| **horizontal storytelling** | Sequence of comparable panels | Galleries, timelines | Critical content (hidden overflow), mobile scroll hijacking | high | Pinned horizontal sections are heavy | Must remain keyboard-accessible; reduced → normal vertical list | Prefer native horizontal scroll-snap with visible controls over scroll hijacking |
| **layered reveal** | Build complexity gradually (diagram layers) | Technical architecture, product layers | Simple content | medium | Few layers | Reduced → all layers shown | IO steps adding layers |

Rules:

- **Never hijack scroll** (overriding wheel/touch speed or direction).
- Scroll-linked effects must be reversible and scrubbable; no one-shot sequences tied to scroll position.
- One `HIGH` scroll region per page ([intensity budget](motion-principles.md#intensity-budget)); `UNJUSTIFIED_PARALLAX` when parallax has no depth story.
- Mobile gets a simpler version or the static fallback by default.
