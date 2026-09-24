# M4 — Scroll choreography

For marketing, content and storytelling pages only; never for dashboards or forms. Scroll motion is the most expensive family in performance, accessibility and attention, so it must carry the narrative, not decorate it. Check [performance-safety.md](performance-safety.md) and [responsive-motion.md](responsive-motion.md) before implementing any entry here.

Rules:

- **Never hijack scroll.** Do not override wheel or touch speed or direction. Pinning is allowed; forced snapping through content is not.
- Scroll-linked effects are reversible and scrubbable. Nothing is a one-shot sequence tied to scroll position.
- One `HIGH` scroll region per page ([intensity budget](motion-principles.md#intensity-budget)). Parallax without a depth story is `UNJUSTIFIED_PARALLAX`.
- Mobile gets a simpler version or the static fallback by default.

```yaml
id: motion.m4-scroll-reveal
name: Scroll reveal
kind: motion
category: scroll
tier: M4
purpose: Pace reading by revealing each section once as it enters.
serves: [hierarchy]
trigger: Section crosses ~15-25 percent into the viewport, once.
behavior: Section header and key visual fade-up; not each child.
duration: motion-expressive (300-600ms)
easing: cubic-bezier(0.2, 0, 0, 1)
spring: none
entrance: Short upward distance.
exit: None.
interruption: Completes; unobserve after first reveal.
responsive: Smaller distance on mobile.
reduced_motion: None; content visible.
performance:
  cost: low
  notes: IntersectionObserver plus a class; content visible without JS.
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.motion, tech.gsap]
intensity: low
contexts: [marketing, content]
avoid_when: Apps, tables, forms; re-triggering; hiding content until JS runs.
examples: Feature sections arriving once while scrolling a landing page.
```

```yaml
id: motion.m4-parallax
name: Parallax
kind: motion
category: scroll
tier: M4
purpose: Express depth between foreground and background planes.
serves: [storytelling, brand-expression]
trigger: Scroll position within a section.
behavior: Background layer moves slower than foreground (factor 0.1-0.3).
duration: Scroll-linked
easing: linear
spring: none
entrance: n/a
exit: n/a
interruption: Follows scroll.
responsive: Disabled on touch and small viewports.
reduced_motion: Static.
performance:
  cost: medium
  notes: Transform on a composited layer via scroll-driven animation; never background-attachment fixed on mobile.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: medium
contexts: [marketing]
avoid_when: Text layers, several sections, dashboards, mobile.
examples: Product render drifting slightly slower than its caption.
```

```yaml
id: motion.m4-scroll-progress
name: Scroll progress
kind: motion
category: scroll
tier: M4
purpose: Show reading progress through long content.
serves: [orientation]
trigger: Document scroll.
behavior: Thin bar scales with scroll progress; or active section indicator.
duration: Scroll-linked
easing: linear
spring: none
entrance: Appears after the article starts.
exit: Hides at the end.
interruption: Follows scroll.
responsive: Same.
reduced_motion: Keep (it is informative, not decorative).
performance:
  cost: low
  notes: animation-timeline scroll() with transform scaleX; fallback via passive listener throttled with rAF.
technology:
  preferred: [tech.css]
  alternatives: [tech.native-js]
intensity: low
contexts: [content, marketing]
avoid_when: Short pages.
examples: Reading bar on a long article.
```

```yaml
id: motion.m4-sticky-reveal
name: Sticky reveal
kind: motion
category: scroll
tier: M4
purpose: Keep a visual in place while supporting text scrolls past, changing the visual state.
serves: [storytelling]
trigger: Step text entering the viewport.
behavior: Sticky visual crossfades or transforms to match the active step.
duration: motion-normal crossfades (250-400ms) per step
easing: ease-in-out
spring: none
entrance: Visual becomes sticky when the section starts.
exit: Unsticks at section end.
interruption: Scrolling back reverses states.
responsive: Mobile stacks steps with inline visuals.
reduced_motion: Stacked static steps.
performance:
  cost: medium
  notes: position sticky plus IntersectionObserver on steps; no scroll handlers.
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: medium
contexts: [marketing, content]
avoid_when: Fewer than three steps; long text in the sticky column.
examples: Workflow steps changing a product screenshot.
```

```yaml
id: motion.m4-pinned-section
name: Pinned section
kind: motion
category: scroll
tier: M4
purpose: Hold a scene in place while scroll scrubs a sequence within it.
serves: [storytelling]
trigger: Section reaches the top of the viewport.
behavior: Section pins for a scroll distance while an internal timeline scrubs.
duration: Scroll-linked over 100-300 percent of viewport height
easing: linear scrub
spring: none
entrance: Pins at section start.
exit: Releases at sequence end.
interruption: Scroll up scrubs backward.
responsive: Mobile shows the sequence as static steps or a short video with poster.
reduced_motion: Static sequence frames.
performance:
  cost: high
  notes: Pinning with heavy media causes jank; preload and keep layers few.
technology:
  preferred: [tech.gsap]
  alternatives: [tech.css, tech.motion]
intensity: high
contexts: [marketing]
avoid_when: Anything but the page's single high-intensity story; forms or reading.
examples: Product rotating through its features while pinned.
```

```yaml
id: motion.m4-horizontal-scroll
name: Horizontal scroll section
kind: motion
category: scroll
tier: M4
purpose: Present a sequence of comparable panels as a row.
serves: [storytelling, orientation]
trigger: User scrolls horizontally, or vertical scroll mapped while pinned.
behavior: Prefer native horizontal scroll with snap and visible controls; pinned vertical-to-horizontal mapping only with strong reason.
duration: Scroll-linked
easing: linear
spring: none
entrance: n/a
exit: n/a
interruption: Follows input.
responsive: Native swipe on touch.
reduced_motion: Normal list or native horizontal scroll without scrubbing.
performance:
  cost: medium
  notes: Pinned mapping is heavy; native scroll-snap is cheap.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap]
intensity: medium
contexts: [marketing, content]
avoid_when: Critical content hidden off-screen; scroll hijacking.
examples: Timeline of product generations.
```

```yaml
id: motion.m4-image-mask-reveal
name: Image mask reveal
kind: motion
category: scroll
tier: M4
purpose: Reveal a key image with an editorial wipe.
serves: [hierarchy, brand-expression]
trigger: Image enters viewport, once or scroll-linked.
behavior: clip-path inset opens from one side.
duration: motion-expressive (500-700ms) or scroll-linked
easing: cubic-bezier(0.16, 1, 0.3, 1)
spring: none
entrance: Wipe along reading direction.
exit: None.
interruption: Completes.
responsive: Fade on mobile.
reduced_motion: Image visible.
performance:
  cost: medium
  notes: Animate clip-path on a few images only.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap]
intensity: medium
contexts: [marketing, content]
avoid_when: Every image; galleries.
examples: Editorial feature image opening as the reader arrives.
```

```yaml
id: motion.m4-text-reveal
name: Text reveal
kind: motion
category: scroll
tier: M4
purpose: Pace a short headline statement for emphasis.
serves: [hierarchy, brand-expression]
trigger: Headline enters viewport once, or page load for the hero.
behavior: Lines or words rise from a mask; realizations in text-motion.md.
duration: 400-900ms total
easing: cubic-bezier(0.16, 1, 0.3, 1)
spring: none
entrance: By line or word in reading order.
exit: None.
interruption: Completes.
responsive: Line reveal only on mobile.
reduced_motion: Static text.
performance:
  cost: low
  notes: Few elements; split at render, not per frame.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: medium
contexts: [marketing]
avoid_when: Body copy, repeated headings, content users must act on.
examples: Hero statement revealing line by line.
```

```yaml
id: motion.m4-zoom-through
name: Zoom-through
kind: motion
category: scroll
tier: M4
purpose: Travel into an object or scene to transition to its detail.
serves: [storytelling, continuity]
trigger: Scroll within a pinned section.
behavior: Scale of a media layer increases until it fills the viewport and reveals the next scene.
duration: Scroll-linked over 100-200 percent viewport height
easing: linear scrub
spring: none
entrance: From framed object.
exit: Into the next section.
interruption: Scrub backward.
responsive: Replaced by a crossfade on mobile.
reduced_motion: Static crossfade or cut.
performance:
  cost: high
  notes: Large scaled images need adequate resolution and can be memory heavy.
technology:
  preferred: [tech.gsap]
  alternatives: [tech.css, tech.motion]
intensity: high
contexts: [marketing]
avoid_when: Low-quality media; vestibular-heavy audiences; multiple uses per page.
examples: Scrolling into a device screen that becomes the next section.
```

```yaml
id: motion.m4-layered-depth
name: Layered depth scroll
kind: motion
category: scroll
tier: M4
purpose: Build a composition layer by layer to explain structure.
serves: [storytelling, hierarchy]
trigger: Steps entering the viewport.
behavior: Layers of a diagram or product stack separate or assemble with small parallax.
duration: motion-normal per layer or scroll-linked
easing: ease-out or linear scrub
spring: none
entrance: Layers join in logical order.
exit: None.
interruption: Scroll back reverses.
responsive: All layers shown statically on mobile.
reduced_motion: Final assembled state plus labels.
performance:
  cost: medium
  notes: 3-5 layers maximum.
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: medium
contexts: [marketing]
avoid_when: Simple content without structure.
examples: Architecture diagram assembling its layers.
```

```yaml
id: motion.m4-scroll-storytelling
name: Scroll storytelling
kind: motion
category: scroll
tier: M4
purpose: Guide the reader through a multi-chapter narrative with scroll as the timeline.
serves: [storytelling]
trigger: Chapters entering the viewport.
behavior: Chapter-level transitions combining sticky visuals, reveals and state changes.
duration: Scroll-linked; chapter transitions motion-normal
easing: ease-in-out, linear scrub for scrubbed parts
spring: none
entrance: Each chapter introduces one idea.
exit: Chapter hands over to the next.
interruption: Fully reversible.
responsive: Mobile becomes a linear article with inline media.
reduced_motion: Linear article.
performance:
  cost: high
  notes: Budget the page; only one scrubbed sequence; lazy-load chapter media.
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: high
contexts: [marketing, content]
avoid_when: Content lacks a real sequence; users arrive with a task.
examples: Annual report or product story told in chapters.
```

```yaml
id: motion.m4-product-walkthrough
name: Product walkthrough
kind: motion
category: scroll
tier: M4
purpose: Demonstrate how the product works step by step using real UI.
serves: [storytelling, orientation]
trigger: Steps entering the viewport or step controls.
behavior: Product UI frame stays in view while states change per step; highlights point to the relevant area.
duration: motion-normal per step (250-400ms)
easing: ease-in-out
spring: none
entrance: First step visible immediately.
exit: Final step links to action.
interruption: Step controls or scroll change the active step.
responsive: Stacked steps with cropped UI on mobile.
reduced_motion: Static screenshots per step.
performance:
  cost: medium
  notes: Use real UI images or lightweight DOM replicas; avoid video when stills explain.
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.motion, tech.gsap]
intensity: medium
contexts: [marketing]
avoid_when: Product UI not ready or not self-explanatory.
examples: Three-step onboarding of an AI assistant shown with real screens.
```
