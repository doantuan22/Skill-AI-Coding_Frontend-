# M1 — Micro motion

Fast, low-intensity feedback on a single control. Must match the [button](../visual-language/components/buttons.md) and [form](../visual-language/components/forms-controls.md) grammar and share timing tokens. Rules:

- Transition named properties only; never `transition: all`.
- Hover effects are enhancements; wrap movement in `@media (hover: hover) and (pointer: fine)`. Every hover affordance has a focus-visible and touch equivalent.
- Equivalent controls share identical micro motion.

```yaml
id: motion.m1-hover
name: Hover feedback
kind: motion
category: micro
tier: M1
purpose: Confirm an element is interactive before it is pressed.
serves: [feedback]
trigger: Pointer enters an interactive element (fine pointers).
behavior: Background/color shift; optional 1-2px lift for clickable cards.
duration: motion-fast (100-150ms)
easing: ease-out
spring: none
entrance: Immediate on pointer enter.
exit: Slightly faster on pointer leave.
interruption: Reverses from current value.
responsive: No movement on touch; focus and press states carry feedback.
reduced_motion: Color change only, no translate.
performance:
  cost: low
  notes: Animate color/opacity or transform; animate a shadow layer's opacity, not box-shadow.
technology:
  preferred: [tech.css]
  alternatives: []
intensity: low
contexts: [marketing, application, content, commerce]
avoid_when: Non-interactive cards; scale-and-rotate hovers; hover as the only affordance.
examples: Row highlight in a table; link underline thickening.
```

```yaml
id: motion.m1-press
name: Press response
kind: motion
category: micro
tier: M1
purpose: Tactile confirmation that input was received.
serves: [feedback]
trigger: Pointer down, touch start, Enter/Space.
behavior: Scale 0.97-0.98 or darken; tactile styles move into the shadow.
duration: motion-micro (50-100ms)
easing: ease-out
spring: gentle release in tactile/playful styles
entrance: On press.
exit: On release, spring back.
interruption: Release at any point restores.
responsive: Essential on touch where hover is absent.
reduced_motion: Color/darken only.
performance:
  cost: low
  notes: Transform only.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [marketing, application, commerce]
avoid_when: Large surfaces where scaling blurs text.
examples: Primary button compresses slightly on click.
```

```yaml
id: motion.m1-focus
name: Focus transition
kind: motion
category: micro
tier: M1
purpose: Make keyboard focus immediately visible.
serves: [feedback, orientation]
trigger: focus-visible.
behavior: Focus ring appears; optional very fast fade or offset change.
duration: 0-100ms
easing: ease-out
spring: none
entrance: Visible immediately.
exit: Immediate.
interruption: n/a
responsive: Same.
reduced_motion: Instant.
performance:
  cost: none
  notes: Outline or box-shadow.
technology:
  preferred: [tech.css]
  alternatives: []
intensity: low
contexts: [marketing, application, content, commerce]
avoid_when: Never avoid focus; avoid slow animated-in rings.
examples: Ring on a nav link when tabbing.
```

```yaml
id: motion.m1-toggle
name: Toggle switch
kind: motion
category: micro
tier: M1
purpose: Show the on/off state change and its direction.
serves: [feedback, state-change]
trigger: Click, tap, Space.
behavior: Thumb travels; track color changes.
duration: motion-fast (120-180ms)
easing: ease-in-out; gentle spring in playful styles
spring: gentle
entrance: n/a
exit: n/a
interruption: Rapid toggling reverses from the current position.
responsive: Larger hit area on touch.
reduced_motion: Instant position change with color.
performance:
  cost: low
  notes: Transform on the thumb.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application, marketing]
avoid_when: Settings that apply only after saving (use a checkbox).
examples: Dark mode switch.
```

```yaml
id: motion.m1-checkbox
name: Checkbox check
kind: motion
category: micro
tier: M1
purpose: Confirm selection or completion.
serves: [feedback, delight]
trigger: Check/uncheck.
behavior: Checkmark draws (stroke-dashoffset) or scales in; box fills.
duration: motion-fast (120-200ms)
easing: ease-out
spring: gentle in playful styles
entrance: Stroke draws in reading direction.
exit: Fade out quickly.
interruption: Reverses.
responsive: Same.
reduced_motion: Instant check.
performance:
  cost: low
  notes: SVG stroke animation is cheap.
technology:
  preferred: [tech.css, tech.svg]
  alternatives: []
intensity: low
contexts: [application]
avoid_when: Bulk selection of hundreds of rows (no per-item animation).
examples: Task completion in a to-do list.
```

```yaml
id: motion.m1-icon-transition
name: Icon transition
kind: motion
category: micro
tier: M1
purpose: Make an icon's state change legible (menu to close, chevron rotate, play to pause).
serves: [state-change]
trigger: State change of the control.
behavior: Rotate or morph between two icon states.
duration: motion-fast (150-200ms)
easing: ease-in-out
spring: none
entrance: n/a
exit: n/a
interruption: Reverses.
responsive: Same.
reduced_motion: Instant swap.
performance:
  cost: low
  notes: Transform; SVG path morph only between compatible paths.
technology:
  preferred: [tech.css, tech.svg]
  alternatives: [tech.rive]
intensity: low
contexts: [application, marketing]
avoid_when: Spinning decorative icons.
examples: Accordion chevron rotating 180 degrees.
```

```yaml
id: motion.m1-tooltip
name: Tooltip
kind: motion
category: micro
tier: M1
purpose: Reveal supplementary label without distraction.
serves: [feedback, orientation]
trigger: Hover after delay, focus immediately.
behavior: Fade with 2-4px offset from trigger.
duration: motion-fast (100-150ms); show delay 300-500ms on hover
easing: ease-out
spring: none
entrance: From the trigger side.
exit: Immediate or fast fade.
interruption: Moving between tooltips skips the delay.
responsive: Tap-to-show or visible labels on touch.
reduced_motion: Instant.
performance:
  cost: low
  notes: Opacity and transform.
technology:
  preferred: [tech.css]
  alternatives: [tech.native-js]
intensity: low
contexts: [application]
avoid_when: Essential information that should be visible text.
examples: Icon-only toolbar button label.
```

```yaml
id: motion.m1-loading
name: Loading indicator
kind: motion
category: micro
tier: M1
purpose: Show that work is in progress when duration is unknown.
serves: [feedback, state-change]
trigger: Request starts and exceeds ~300ms.
behavior: Spinner, pulsing dots, or indeterminate bar; for AI, a thinking indicator.
duration: Loop of 0.8-1.2s
easing: linear for rotation
spring: none
entrance: Appears only after a short delay to avoid flicker.
exit: Replaced by content or result.
interruption: Cancelled requests remove it immediately.
responsive: Same.
reduced_motion: Slow or static indicator with text such as Loading.
performance:
  cost: low
  notes: Transform rotation; stop when hidden.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
intensity: low
contexts: [application, commerce]
avoid_when: Known-duration work (use progress); content-shaped loading (use skeleton).
examples: Button spinner while submitting; AI thinking dots.
```

```yaml
id: motion.m1-success
name: Success confirmation
kind: motion
category: micro
tier: M1
purpose: Confirm that an action completed.
serves: [feedback, delight]
trigger: Action resolves successfully.
behavior: Check icon draws, color settles; celebration only for milestones.
duration: motion-fast to motion-normal (200-400ms)
easing: ease-out; gentle spring in playful styles
spring: gentle
entrance: At the control or area that triggered the action.
exit: Returns to rest after 1.5-2s or persists as status.
interruption: New action cancels it.
responsive: Same.
reduced_motion: Static success state and text.
performance:
  cost: low
  notes: Confetti or particles are high cost and only for real milestones.
technology:
  preferred: [tech.css, tech.svg]
  alternatives: [tech.lottie, tech.rive]
intensity: low
contexts: [application, commerce]
avoid_when: Routine saves every few seconds.
examples: Copy-to-clipboard check; payment confirmed.
```

```yaml
id: motion.m1-error
name: Error feedback
kind: motion
category: micro
tier: M1
purpose: Draw attention to a problem at its location.
serves: [feedback, attention]
trigger: Validation failure or failed action.
behavior: Message appears near the field; optional single small horizontal shake.
duration: motion-fast (150-250ms); shake max 300ms once
easing: ease-out
spring: none
entrance: Near the cause.
exit: When resolved.
interruption: Re-validation replaces it.
responsive: Same.
reduced_motion: No shake; color, icon and text.
performance:
  cost: low
  notes: Transform only.
technology:
  preferred: [tech.css]
  alternatives: [tech.waapi]
intensity: low
contexts: [application, commerce]
avoid_when: Repeated shaking; errors announced only by motion.
examples: Password field shakes once and shows the rule.
```

```yaml
id: motion.m1-skeleton
name: Skeleton shimmer
kind: motion
category: micro
tier: M1
purpose: Preserve layout and indicate loading of content with a known shape.
serves: [feedback, state-change]
trigger: Content loading beyond ~300ms.
behavior: Placeholder blocks with a slow, low-contrast shimmer or pulse.
duration: 1.2-2s loop
easing: linear or ease-in-out
spring: none
entrance: Immediately or after a short delay.
exit: Crossfade to content without layout shift.
interruption: Content arrival replaces it.
responsive: Same.
reduced_motion: Static placeholder.
performance:
  cost: low
  notes: Animate a gradient via transform on a pseudo-element.
technology:
  preferred: [tech.css]
  alternatives: []
intensity: low
contexts: [application, commerce, content]
avoid_when: Very fast loads (flash) or unknown layouts.
examples: Dashboard cards loading.
```

```yaml
id: motion.m1-progress
name: Progress
kind: motion
category: micro
tier: M1
purpose: Communicate completion of known-duration work.
serves: [feedback, state-change]
trigger: Upload, processing, multi-step flow.
behavior: Bar or ring fills proportionally; value text updates.
duration: Follows real progress; smoothing 150-250ms per update
easing: linear or ease-out per update
spring: none
entrance: Appears with the task.
exit: Completes to 100 then settles into success.
interruption: Cancel stops and resets.
responsive: Same.
reduced_motion: Discrete updates without smoothing.
performance:
  cost: low
  notes: transform scaleX, not width.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
intensity: low
contexts: [application, commerce]
avoid_when: Fake progress not tied to real work.
examples: File upload bar with percentage.
```

```yaml
id: motion.m1-button-feedback
name: Button async feedback
kind: motion
category: micro
tier: M1
purpose: Show a button's action is running and then its result, without layout jump.
serves: [feedback, state-change]
trigger: Async action starts from a button.
behavior: Label crossfades to spinner, then to success/error; width reserved.
duration: motion-fast crossfades (150-200ms)
easing: ease-out
spring: none
entrance: Crossfade within the button.
exit: Return to label after result.
interruption: Disabled while pending; cancel returns to label.
responsive: Same.
reduced_motion: Instant swaps with text.
performance:
  cost: low
  notes: Never animate width; reserve min-width.
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
intensity: low
contexts: [application, commerce, marketing]
avoid_when: Actions that complete instantly.
examples: Save button showing a spinner then Saved.
```
