# M2 — Component transitions (spatial)

How a component appears, changes state, or reveals content. Direction matches the interface's spatial model and the trigger. Exits are faster than entrances; transitions are interruptible; input is never blocked for more than ~100ms while an overlay animates in.

```yaml
id: motion.m2-accordion
name: Accordion / expand-collapse
kind: motion
category: component
tier: M2
purpose: Reveal detail in place without losing context.
serves: [state-change]
trigger: Header activation (click, Enter, Space).
behavior: Height grows from 0 via grid-template-rows 0fr to 1fr; chevron rotates.
duration: motion-fast to motion-normal (150-250ms)
easing: ease-in-out
spring: none
entrance: Content fades in slightly after height starts.
exit: Faster collapse.
interruption: Reverses from the current size.
responsive: Same; long content may jump-scroll into view.
reduced_motion: Instant open/close.
performance:
  cost: low
  notes: Avoid JS height measurement loops; interpolate-size where supported.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application, marketing, content]
avoid_when: Hiding critical information (price, terms, required steps).
examples: FAQ answers; settings groups.
```

```yaml
id: motion.m2-modal
name: Modal enter/exit
kind: motion
category: component
tier: M2
purpose: Shift focus to a bounded task while keeping the page as context.
serves: [orientation, state-change]
trigger: Explicit user action.
behavior: Backdrop fades; dialog scales 0.96 to 1 with fade.
duration: motion-normal (200-300ms) in, 150-200ms out
easing: ease-out in, ease-in out
spring: critically-damped
entrance: From its trigger when spatially related, otherwise centered.
exit: Reverse, faster; focus returns to trigger.
interruption: Close during entrance reverses immediately.
responsive: Bottom sheet sliding up on mobile.
reduced_motion: Fade only.
performance:
  cost: low
  notes: Do not animate backdrop blur radius.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion, tech.waapi]
intensity: medium
contexts: [application, commerce, marketing]
avoid_when: Long workflows; bouncy scale on destructive confirmations.
examples: Confirm delete dialog.
```

```yaml
id: motion.m2-drawer
name: Drawer / sheet
kind: motion
category: component
tier: M2
purpose: Bring secondary context from an edge without leaving the page.
serves: [orientation, state-change]
trigger: Open filters, details, navigation, cart.
behavior: Translate from the edge; backdrop fades.
duration: motion-normal (250-350ms)
easing: ease-out in, ease-in out
spring: critically-damped
entrance: From the edge it belongs to.
exit: Back to the same edge; swipe-to-close follows the finger.
interruption: Drag follows input; release snaps open or closed.
responsive: Bottom sheet on mobile.
reduced_motion: Fade or instant.
performance:
  cost: low
  notes: Transform only.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: medium
contexts: [application, commerce]
avoid_when: Primary content that deserves a page.
examples: Cart drawer after add to bag.
```

```yaml
id: motion.m2-tabs
name: Tabs
kind: motion
category: component
tier: M2
purpose: Show which view is active and switch content without a page change.
serves: [state-change, orientation]
trigger: Tab activation.
behavior: Indicator slides to the active tab; content crossfades (optionally slides in the direction of the tab).
duration: motion-fast (150-250ms)
easing: ease-in-out
spring: critically-damped
entrance: New panel fades in.
exit: Old panel fades out faster.
interruption: Rapid switching jumps to the latest.
responsive: Scrollable tab list on mobile.
reduced_motion: Instant indicator and content swap.
performance:
  cost: low
  notes: Animate indicator with transform (translateX/scaleX).
technology:
  preferred: [tech.css]
  alternatives: [tech.motion, tech.view-transitions]
intensity: low
contexts: [application, marketing]
avoid_when: Content that must be compared simultaneously.
examples: Code sample tabs by language.
```

```yaml
id: motion.m2-dropdown
name: Dropdown / menu
kind: motion
category: component
tier: M2
purpose: Anchor a list of options to its trigger.
serves: [orientation]
trigger: Trigger activation.
behavior: Scale 0.96 to 1 and fade from the trigger origin.
duration: motion-fast (120-180ms)
easing: ease-out
spring: none
entrance: From the trigger edge.
exit: Faster fade.
interruption: Reverses.
responsive: Becomes a sheet or native select on mobile.
reduced_motion: Instant.
performance:
  cost: low
  notes: Transform-origin at trigger.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application, marketing, commerce]
avoid_when: Long distances or bouncy menus.
examples: Account menu.
```

```yaml
id: motion.m2-popover
name: Popover
kind: motion
category: component
tier: M2
purpose: Show contextual content attached to an element.
serves: [orientation]
trigger: Click or focus on the anchor.
behavior: Fade and 4-8px offset from the anchor side.
duration: motion-fast (120-200ms)
easing: ease-out
spring: none
entrance: From the anchor.
exit: Fade.
interruption: Reverses.
responsive: Sheet on small screens when content is large.
reduced_motion: Instant.
performance:
  cost: low
  notes: Transform and opacity.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application]
avoid_when: Tasks needing focus trapping (use a dialog).
examples: Date picker popover.
```

```yaml
id: motion.m2-carousel
name: Carousel slide
kind: motion
category: component
tier: M2
purpose: Browse equivalent items with spatial continuity.
serves: [orientation]
trigger: Next/previous, swipe, keyboard.
behavior: Track translates; follows the finger during swipe.
duration: motion-normal (250-350ms)
easing: ease-out; momentum on swipe
spring: critically-damped
entrance: From the direction of travel.
exit: Out the opposite direction.
interruption: New input takes over mid-animation.
responsive: Native scroll-snap on touch.
reduced_motion: Instant jump.
performance:
  cost: low
  notes: Prefer native scroll-snap over JS-driven transforms.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion, tech.native-js]
intensity: medium
contexts: [commerce, marketing, content]
avoid_when: Critical messages; auto-advance without pause.
examples: Product image gallery on mobile.
```

```yaml
id: motion.m2-notification
name: Notification / toast
kind: motion
category: component
tier: M2
purpose: Announce a non-blocking outcome without moving focus.
serves: [feedback, attention]
trigger: System event or completed action.
behavior: Slides from its screen edge with fade; stack shifts smoothly.
duration: motion-normal (200-300ms)
easing: ease-out in, ease-in out
spring: critically-damped
entrance: From the region edge (top or bottom).
exit: Fade/slide out; swipe to dismiss on touch.
interruption: Hover pauses auto-dismiss.
responsive: Full-width at bottom on mobile, above safe areas.
reduced_motion: Fade only.
performance:
  cost: low
  notes: Transform.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application, commerce]
avoid_when: Errors that need action (use inline or banner).
examples: Settings saved toast.
```

```yaml
id: motion.m2-command-palette
name: Command palette
kind: motion
category: component
tier: M2
purpose: Summon a fast keyboard surface with minimal delay.
serves: [feedback, orientation]
trigger: Shortcut (Ctrl/Cmd+K) or button.
behavior: Very fast fade and scale 0.98 to 1; results update without animation delay.
duration: motion-micro to motion-fast (80-150ms)
easing: ease-out
spring: none
entrance: Centered near the top.
exit: Instant or very fast fade.
interruption: Escape closes immediately.
responsive: Full-screen sheet on mobile.
reduced_motion: Instant.
performance:
  cost: low
  notes: Results list must not animate every keystroke.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application]
avoid_when: Slow, decorative openings that delay typing.
examples: Jump to project or run a command.
```

```yaml
id: motion.m2-card-expansion
name: Card expansion
kind: motion
category: component
tier: M2
purpose: Grow a card in place to reveal more detail.
serves: [state-change, continuity]
trigger: Card activation.
behavior: Card expands within the grid; neighbors reflow smoothly.
duration: motion-normal (250-350ms)
easing: ease-in-out
spring: critically-damped
entrance: Content appears after the expansion begins.
exit: Collapse reverses.
interruption: Reverses from current size.
responsive: Opens as a full-screen sheet on mobile.
reduced_motion: Instant expansion.
performance:
  cost: medium
  notes: Reflow of neighbors should use FLIP or layout animation, not animated width.
technology:
  preferred: [tech.view-transitions, tech.waapi]
  alternatives: [tech.motion]
intensity: medium
contexts: [marketing, application]
avoid_when: Detail that deserves its own page or URL.
examples: Feature tile expanding to show a demo.
```

```yaml
id: motion.m2-filter-transition
name: Filter transition
kind: motion
category: component
tier: M2
purpose: Show how a result set changes when filters change.
serves: [state-change, continuity]
trigger: Filter applied.
behavior: Removed items fade out, remaining items move to new positions, new items fade in.
duration: motion-fast to motion-normal (150-300ms)
easing: ease-in-out
spring: none
entrance: New items fade.
exit: Removed items fade quickly.
interruption: Latest filter wins; in-flight animations jump to end.
responsive: Simpler crossfade on mobile.
reduced_motion: Instant update with result count announced.
performance:
  cost: medium
  notes: Limit animated items to the visible ones; virtualized lists crossfade instead.
technology:
  preferred: [tech.view-transitions, tech.waapi]
  alternatives: [tech.motion, tech.gsap]
intensity: low
contexts: [commerce, application]
avoid_when: Large tables or data grids.
examples: Product grid after choosing a size filter.
```

```yaml
id: motion.m2-navigation-state
name: Navigation state
kind: motion
category: component
tier: M2
purpose: Show current location changes in navigation.
serves: [orientation, state-change]
trigger: Route or section change.
behavior: Active indicator slides to the new item; header condenses on scroll.
duration: motion-fast (150-250ms)
easing: ease-in-out
spring: critically-damped
entrance: n/a
exit: n/a
interruption: Latest state wins.
responsive: Mobile menu opens as a sheet or full-screen overlay.
reduced_motion: Instant indicator change.
performance:
  cost: low
  notes: Header condense via IntersectionObserver sentinel, not scroll handler.
technology:
  preferred: [tech.css, tech.native-js]
  alternatives: [tech.motion]
intensity: low
contexts: [application, marketing, content]
avoid_when: Navigation that bounces or delays route change.
examples: Sidebar active marker moving between items.
```
