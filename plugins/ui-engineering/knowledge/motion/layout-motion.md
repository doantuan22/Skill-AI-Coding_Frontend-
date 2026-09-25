# M3 — Layout transitions

Layout transitions preserve object identity when elements move between layouts, views or pages. They are the main source of "transition continuity". Prefer the View Transitions API or an existing layout-animation library; never measure and set sizes every frame by hand.

Rules: keep the number of simultaneously morphing elements small (1 shared element plus a crossfade is usually enough); move focus to the new primary heading or item after the transition; reduced motion falls back to crossfade or instant swap.

```yaml
id: motion.m3-shared-element
name: Shared element
kind: motion
category: layout
tier: M3
purpose: Keep an object's identity as it moves from one view to another.
serves: [continuity, orientation]
trigger: Navigation or state change where the same object appears in both states.
behavior: The element morphs position and size between states while the rest crossfades.
duration: motion-normal to motion-expressive (250-450ms)
easing: cubic-bezier(0.4, 0, 0.2, 1)
spring: critically-damped
entrance: From the old geometry to the new.
exit: Reverse on back navigation.
interruption: New navigation cancels and snaps to the latest state.
responsive: One shared element on mobile; others crossfade.
reduced_motion: Crossfade or instant.
performance:
  cost: medium
  notes: Snapshots of large regions cost memory; keep shared elements few.
technology:
  preferred: [tech.view-transitions]
  alternatives: [tech.motion, tech.waapi]
intensity: medium
contexts: [application, commerce, content, marketing]
avoid_when: Unrelated views; every navigation in an app.
examples: Album cover becoming the player header.
```

```yaml
id: motion.m3-flip
name: FLIP transition
kind: motion
category: layout
tier: M3
purpose: Animate layout changes that CSS cannot transition (grid position, order, size).
serves: [continuity, state-change]
trigger: Any DOM layout change.
behavior: Measure first and last positions, invert with transform, play to identity.
duration: motion-normal (200-300ms)
easing: ease-in-out
spring: critically-damped
entrance: From previous geometry.
exit: n/a
interruption: Re-measure from the current visual position.
responsive: Same; limit element count on mobile.
reduced_motion: Instant layout change.
performance:
  cost: medium
  notes: One measurement pass per change; transform-only playback.
technology:
  preferred: [tech.waapi]
  alternatives: [tech.motion, tech.gsap]
intensity: low
contexts: [application, commerce]
avoid_when: Hundreds of elements or virtualized lists.
examples: Grid reflow after removing an item.
```

```yaml
id: motion.m3-list-to-detail
name: List to detail
kind: motion
category: layout
tier: M3
purpose: Show that the detail view is the item the user selected.
serves: [continuity, orientation]
trigger: Selecting a list item.
behavior: Item title/thumbnail becomes the detail header; detail content fades in.
duration: motion-normal (250-350ms)
easing: ease-in-out
spring: critically-damped
entrance: Detail enters from the item.
exit: Back returns to the item's position in the list, with scroll restored.
interruption: Back during transition reverses.
responsive: Mobile pushes a detail screen with the shared header.
reduced_motion: Instant or crossfade.
performance:
  cost: medium
  notes: Keep list scroll position; avoid re-rendering the list.
technology:
  preferred: [tech.view-transitions]
  alternatives: [tech.motion]
intensity: medium
contexts: [application, commerce]
avoid_when: Detail loads slowly (show skeleton instead of a stalled morph).
examples: Email list to message.
```

```yaml
id: motion.m3-card-to-modal
name: Card to modal
kind: motion
category: layout
tier: M3
purpose: Open a card's full content as a focused layer that clearly came from the card.
serves: [continuity, orientation]
trigger: Card activation.
behavior: Card expands into a modal; backdrop fades; content fills in.
duration: motion-normal to motion-expressive (300-400ms)
easing: cubic-bezier(0.2, 0, 0, 1)
spring: critically-damped
entrance: From the card geometry.
exit: Collapses back into the card.
interruption: Close during open reverses.
responsive: Full-screen sheet on mobile.
reduced_motion: Standard modal fade.
performance:
  cost: medium
  notes: Animate transform on a composited layer; load content after the morph starts.
technology:
  preferred: [tech.view-transitions]
  alternatives: [tech.motion, tech.waapi]
intensity: medium
contexts: [marketing, application]
avoid_when: Content needs its own URL and history entry.
examples: Case study card opening a preview.
```

```yaml
id: motion.m3-thumbnail-to-fullscreen
name: Thumbnail to fullscreen
kind: motion
category: layout
tier: M3
purpose: Enlarge media while keeping its identity.
serves: [continuity]
trigger: Thumbnail activation.
behavior: Image scales from its thumbnail position to fullscreen; UI fades in.
duration: motion-normal (250-350ms)
easing: cubic-bezier(0.2, 0, 0, 1)
spring: critically-damped
entrance: From the thumbnail rect.
exit: Returns to thumbnail; swipe down to close on touch.
interruption: Gesture takes over mid-transition.
responsive: Swipe navigation between images on touch.
reduced_motion: Fade.
performance:
  cost: medium
  notes: Use the already-loaded thumbnail as placeholder, swap to high-res after.
technology:
  preferred: [tech.view-transitions, tech.waapi]
  alternatives: [tech.motion]
intensity: medium
contexts: [commerce, content, marketing]
avoid_when: Images without higher-resolution versions.
examples: Product gallery lightbox.
```

```yaml
id: motion.m3-layout-reflow
name: Layout reflow
kind: motion
category: layout
tier: M3
purpose: Smooth unexpected size changes so users keep their place.
serves: [continuity, state-change]
trigger: Content inserted or resized (streamed AI output, expanding panels).
behavior: Surrounding content moves smoothly instead of jumping.
duration: motion-fast to motion-normal (150-250ms)
easing: ease-out
spring: critically-damped
entrance: New content fades in after space opens.
exit: Space closes after content fades.
interruption: Continuous updates re-target smoothly.
responsive: Same.
reduced_motion: Instant.
performance:
  cost: medium
  notes: Batch updates; streaming text should append without per-token layout animation.
technology:
  preferred: [tech.motion]
  alternatives: [tech.waapi, tech.view-transitions]
intensity: low
contexts: [application]
avoid_when: Reflow caused by late-loading assets (fix with reserved space, not animation).
examples: Answer panel growing as an AI response streams.
```

```yaml
id: motion.m3-animated-reorder
name: Animated reorder
kind: motion
category: layout
tier: M3
purpose: Show where items went after sorting or drag reorder.
serves: [continuity, feedback]
trigger: Sort change or drop.
behavior: Items slide to new positions.
duration: motion-normal (200-300ms)
easing: ease-in-out
spring: critically-damped
entrance: n/a
exit: n/a
interruption: New sort re-targets from current positions.
responsive: Same; fewer items animate on mobile.
reduced_motion: Instant reorder with announcement.
performance:
  cost: medium
  notes: Animate only visible rows.
technology:
  preferred: [tech.waapi]
  alternatives: [tech.motion, tech.view-transitions]
intensity: low
contexts: [application]
avoid_when: Large data tables sorted frequently.
examples: Kanban card dropped into a new position.
```

```yaml
id: motion.m3-navigation-morph
name: Navigation morph
kind: motion
category: layout
tier: M3
purpose: Transform one control into another to show they are related (button to menu, search to panel).
serves: [continuity, orientation]
trigger: Control activation.
behavior: The container morphs size and shape; content crossfades inside.
duration: motion-normal (250-350ms)
easing: cubic-bezier(0.2, 0, 0, 1)
spring: gentle
entrance: From the control.
exit: Back into the control.
interruption: Reverses.
responsive: On mobile, morph into a sheet.
reduced_motion: Crossfade.
performance:
  cost: medium
  notes: Transform-based morph; avoid animating border-radius on large surfaces every frame.
technology:
  preferred: [tech.motion]
  alternatives: [tech.view-transitions, tech.waapi]
intensity: medium
contexts: [application, marketing]
avoid_when: Standard menus where a dropdown suffices.
examples: Search button expanding into a search panel.
```

```yaml
id: motion.m3-cross-page-continuity
name: Cross-page continuity
kind: motion
category: layout
tier: M3
purpose: Make multi-page navigation feel like one continuous space.
serves: [continuity, orientation]
trigger: Same-origin navigation.
behavior: Persistent elements stay; page content crossfades or slides by direction.
duration: motion-normal (200-350ms)
easing: ease-in-out
spring: none
entrance: New page content from navigation direction.
exit: Old content out.
interruption: Browser navigation wins.
responsive: Crossfade only on mobile.
reduced_motion: No transition.
performance:
  cost: low
  notes: Cross-document view transitions are progressive enhancement.
technology:
  preferred: [tech.view-transitions]
  alternatives: [tech.motion]
intensity: low
contexts: [marketing, content, commerce]
avoid_when: Transitions that delay route changes or break back/forward cache.
examples: Portfolio project pages sharing a persistent header.
```
