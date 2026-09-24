# Motion principles

## Purposes

Every motion must serve at least one; otherwise remove it.

| Purpose | Example |
|---|---|
| Feedback | Button press, toggle, saved confirmation |
| Orientation | Drawer slides from its trigger side; page transition preserves context |
| Hierarchy | The primary element arrives first; secondary content follows |
| State change | Expand/collapse, loading → loaded, error appearing near its field |
| Storytelling | Scroll-linked product reveal explaining a sequence |

"It looks nice" is not a purpose; decorative loops need an explicit brand rationale and the lowest intensity.

## Intensity budget

| Level | Meaning | Examples |
|---|---|---|
| `LOW` | Barely noticed; ≤ 150ms; small distance/opacity | Hover color, focus ring, press scale 0.98 |
| `MEDIUM` | Noticed but brief; ≤ 400ms; moderate distance | Section fade-up, tab content switch, drawer |
| `HIGH` | A deliberate moment; scroll-linked or multi-step; large area | Cinematic hero, sticky storytelling, product reveal |

Rules:

- A page has **at most one `HIGH` region** (two on long storytelling pages if separated by low sections). Never every section `HIGH`.
- If the hero is `HIGH`, body sections are `LOW`/`MEDIUM` and controls stay subtle.
- App/dashboard/form surfaces: `LOW` everywhere; `MEDIUM` only for spatial overlays and meaningful state transitions.
- Entrance animation on ordinary content is limited to the first appearance of a section, not each element, and never re-triggers on scroll up.

Record the budget per region:

```yaml
motion_budget:
  hero: high
  sections: low-medium
  controls: low
  navigation: low
  decorative_loop: none
```

## Timing (by interaction type)

| Type | Duration range | Notes |
|---|---|---|
| Microinteraction (hover, press, focus, toggle) | 80–150ms | Press feedback can be 50–100ms; focus ring may be instant |
| Component transition (tabs, accordion, tooltip, dropdown) | 150–250ms | Scale with distance/size |
| Spatial transition (modal, drawer, sheet, page) | 200–350ms enter; exit ≈ 70–80% of enter | Larger surfaces take longer |
| Marketing entrance (section reveal) | 300–600ms | Stagger 40–80ms per item; total sequence ≤ ~800ms |
| Storytelling (scroll-linked) | tied to scroll, not time | Must be reversible and scrubbable |
| Text reveal (hero headline) | 400–900ms total | Content readable within ~1s |

Never use one global `transition: all 0.3s ease`. Transition specific properties; name durations as tokens (`motion-fast`, `motion-base`, `motion-slow`, `motion-story`).

## Easing

| Use | Easing |
|---|---|
| Entering / appearing | ease-out family, e.g., `cubic-bezier(0.2, 0, 0, 1)` or a stronger `cubic-bezier(0.16, 1, 0.3, 1)` for expressive |
| Exiting / dismissing | ease-in family, e.g., `cubic-bezier(0.4, 0, 1, 1)`, shorter duration |
| Moving on screen (A → B) | ease-in-out, e.g., `cubic-bezier(0.4, 0, 0.2, 1)` |
| Scroll-linked, progress, loaders | `linear` |
| Tactile/playful | spring (library spring if present, or CSS `linear()` approximation) with low overshoot |

Define 3–4 named easings; don't invent per component.

## Implementation strategy (order of preference)

1. **CSS transitions** on `transform`/`opacity`/`color` for state changes.
2. **CSS keyframes** for entrance/loading sequences.
3. **`IntersectionObserver`** to add a class once when a section enters the viewport (then unobserve).
4. **Native scroll-driven animation** (`animation-timeline: view()`/`scroll()`) inside `@supports`, with a static or IO-based fallback.
5. **View Transitions API** for spatial/page continuity as progressive enhancement.
6. **`requestAnimationFrame`** only for continuous, measured, scroll/pointer-linked effects that CSS cannot express; throttle and stop when off-screen.
7. **Existing project animation library** when present — use it consistently for the effects it already handles.
8. **New library** only with need + authorization + recorded justification.
