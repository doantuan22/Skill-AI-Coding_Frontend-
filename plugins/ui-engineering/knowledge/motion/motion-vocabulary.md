# Motion vocabulary

A structured vocabulary, not an effect catalog. Every entry states purpose, trigger, behavior, timing, interruption, responsive and reduced-motion behavior, cost and technology. Grammar and budgets: [motion-principles.md](motion-principles.md).

| Tier | File | Entries |
|---|---|---|
| primitive | this file | fade, fade-up, slide, scale, clip reveal, stagger, ambient drift |
| M1 Micro motion | [microinteractions.md](microinteractions.md) | hover, press, focus, toggle, checkbox, icon transition, tooltip, loading, success, error, skeleton, progress, button feedback |
| M2 Component transition | [spatial-motion.md](spatial-motion.md) | accordion, modal, drawer, tabs, dropdown, popover, carousel, notification, command palette, card expansion, filter transition, navigation state |
| M3 Layout transition | [layout-motion.md](layout-motion.md) | shared element, FLIP, list → detail, card → modal, thumbnail → fullscreen, layout reflow, animated reorder, navigation morph, cross-page continuity |
| M4 Scroll choreography | [scroll-motion.md](scroll-motion.md), [text-motion.md](text-motion.md) | scroll reveal, parallax, scroll progress, sticky reveal, pinned section, horizontal scroll, image mask reveal, text reveal, zoom-through, layered depth, scroll storytelling, product walkthrough; line/word/character/rotating/counter text motion |
| M5 Cinematic / immersive | [cinematic-motion.md](cinematic-motion.md) | cinematic hero, 3D sequence, camera motion, WebGL transition, particle interaction, cursor-reactive scene, physics interaction, SVG morph, interactive shader, spatial navigation |

Responsive and low-power behavior across tiers: [responsive-motion.md](responsive-motion.md). Reduced-motion equivalents: [reduced-motion.md](reduced-motion.md).

**Selection rule:** choose the least intense entry that achieves the purpose. Content must be readable and operable without waiting for any motion.

## Primitives

```yaml
id: motion.fade
name: Fade
kind: motion
category: entrance
tier: primitive
purpose: Soften the appearance or disappearance of content without implying direction.
serves: [state-change, feedback]
trigger: Content load, state change, overlay open/close.
behavior: Opacity 0 to 1 (or reverse).
duration: motion-fast to motion-normal (150-300ms)
easing: ease-out in, ease-in out
spring: none
entrance: Opacity from 0.
exit: Opacity to 0, about 70 percent of entrance duration.
interruption: Reverses from current opacity.
responsive: Same on all devices.
reduced_motion: Keep (opacity is safe) or make instant.
performance:
  cost: low
  notes: Compositor-only.
technology:
  preferred: [tech.css]
  alternatives: [tech.waapi]
intensity: low
contexts: [marketing, application, content, commerce]
avoid_when: Primary above-the-fold content on first paint (delays reading).
examples: Async content replacing a skeleton; toast appearing.
```

```yaml
id: motion.fade-up
name: Fade-up (fade-rise)
kind: motion
category: entrance
tier: primitive
purpose: Signal section order as content first enters the viewport.
serves: [hierarchy]
trigger: Section enters viewport once.
behavior: Opacity 0 to 1 with translateY 8-24px to 0.
duration: motion-expressive (300-600ms), stagger 40-80ms
easing: cubic-bezier(0.2, 0, 0, 1)
spring: none
entrance: From below, short distance.
exit: None; never re-triggers.
interruption: Completes; no reverse on scroll up.
responsive: Distance reduced to 8-12px on mobile.
reduced_motion: Opacity only or no animation.
performance:
  cost: low
  notes: Transform and opacity only; IntersectionObserver trigger.
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [marketing, content]
avoid_when: Every card or paragraph; app screens; content needed immediately.
examples: Feature section header and visual arriving once on scroll.
```

```yaml
id: motion.slide
name: Slide
kind: motion
category: entrance
tier: primitive
purpose: Communicate origin or direction (panel from an edge, next step).
serves: [orientation]
trigger: Panel open, step change, carousel item change.
behavior: Translate along one axis from the origin edge.
duration: motion-normal (200-350ms)
easing: ease-out in, ease-in out
spring: critically-damped if a library is present
entrance: From the side the element lives on.
exit: Back toward the origin.
interruption: Reverses from the current position.
responsive: Mobile sheets slide from the bottom.
reduced_motion: Fade instead.
performance:
  cost: low
  notes: Transform only.
technology:
  preferred: [tech.css]
  alternatives: [tech.waapi, tech.motion]
intensity: medium
contexts: [application, marketing, commerce]
avoid_when: Generic content entrance from random sides.
examples: Drawer from the right; wizard step forward.
```

```yaml
id: motion.scale
name: Scale
kind: motion
category: entrance
tier: primitive
purpose: Show an object emerging from a point (trigger or focus).
serves: [orientation, attention]
trigger: Popover/menu open; product focus.
behavior: Scale 0.95-0.98 to 1 with fade from the trigger origin.
duration: motion-fast (120-200ms) for UI; expressive for product moments
easing: ease-out
spring: gentle for playful styles
entrance: From transform-origin at the trigger.
exit: Scale down slightly with fade, faster.
interruption: Reverses.
responsive: Same.
reduced_motion: Fade only.
performance:
  cost: low
  notes: Avoid scaling text-heavy or very large layers continuously.
technology:
  preferred: [tech.css]
  alternatives: [tech.waapi]
intensity: low
contexts: [application, marketing, commerce]
avoid_when: Text blocks or large backgrounds.
examples: Dropdown opening from its button.
```

```yaml
id: motion.clip-reveal
name: Clip / mask reveal
kind: motion
category: entrance
tier: primitive
purpose: Editorial or cinematic reveal of media or headlines.
serves: [hierarchy, brand-expression]
trigger: Chapter/section enters viewport once.
behavior: clip-path inset animates from closed to open.
duration: motion-expressive (400-700ms)
easing: cubic-bezier(0.16, 1, 0.3, 1)
spring: none
entrance: Wipe along the reading direction.
exit: None.
interruption: Completes.
responsive: Shorter on mobile or replaced by fade.
reduced_motion: Show final state.
performance:
  cost: medium
  notes: clip-path animation repaints; limit to one or two elements per view.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap]
intensity: medium
contexts: [marketing, content]
avoid_when: Repeated on every image; text users must read immediately.
examples: Chapter-opening photograph wiping in.
```

```yaml
id: motion.stagger
name: Stagger
kind: motion
category: entrance
tier: primitive
purpose: Express order within a small group.
serves: [hierarchy]
trigger: Group enters or is revealed.
behavior: Members start with incremental delays.
duration: 40-80ms per item, total 400-600ms maximum
easing: Inherits the member motion.
spring: none
entrance: Order follows reading order.
exit: All together.
interruption: Remaining items appear immediately.
responsive: Fewer steps on mobile.
reduced_motion: No stagger.
performance:
  cost: low
  notes: CSS custom property index times delay.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion, tech.gsap]
intensity: low
contexts: [marketing, application]
avoid_when: Lists over ~8 items, tables, grids of data.
examples: Three pricing tiers appearing in order.
```

```yaml
id: motion.ambient-drift
name: Ambient drift
kind: motion
category: ambient
tier: primitive
purpose: Give a signature surface a sense of life without demanding attention.
serves: [brand-expression]
trigger: Continuous while visible.
behavior: Very slow translation, rotation or opacity drift of a background light or gradient layer.
duration: 15-40s per cycle
easing: ease-in-out or linear
spring: none
entrance: Starts already in motion.
exit: Pauses when off-screen or when the tab is hidden.
interruption: Pauses during user interaction with foreground elements if distracting.
responsive: Static on mobile and low-power.
reduced_motion: Static.
performance:
  cost: medium
  notes: Must animate a transformed composited layer only; pause off-screen.
technology:
  preferred: [tech.css]
  alternatives: [tech.native-js]
intensity: low
contexts: [marketing]
avoid_when: Behind text, in apps, or more than one per page.
examples: Slow drift of a radial light behind a product hero.
```
