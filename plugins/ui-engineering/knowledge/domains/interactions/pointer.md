# Pointer interactions

```yaml
id: interaction.hover-intent
name: Hover intent
kind: interaction
category: pointer
purpose: Distinguish deliberate hover from pointer passing through, to avoid flicker of menus and previews.
flow:
  input: Pointer rests over a target for 100-300ms or slows down.
  feedback: Target highlights immediately; secondary content waits for intent.
  state: Preview or submenu opens.
  motion: motion.m2-dropdown or motion.m2-popover.
  result: Content available without accidental triggers.
input_methods:
  mouse: Delay plus movement threshold; safe triangle for submenus.
  touch: Not applicable; use tap.
  keyboard: Focus opens immediately (no delay).
states: [idle, highlighted, intent-detected, open, closing]
feedback: Highlight at once, open after intent delay.
motion: Short fade/scale; closing has a grace period of 150-300ms.
error_behavior: If content fails to load, show inline retry inside the opened panel.
accessibility: Must also open with focus/Enter; content reachable without pointer.
mobile: Tap to open, tap outside to close.
desktop: Delay-based intent and submenu safe areas.
recommended_use: Mega menus, nested menus, hover previews.
avoid_when: Primary actions; content that should be visible anyway.
contexts: [marketing, application, commerce]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: []
```

```yaml
id: interaction.press-feedback
name: Press feedback
kind: interaction
category: pointer
purpose: Confirm any activation instantly.
flow:
  input: Pointer down, touch start, Enter or Space.
  feedback: Pressed visual within one frame.
  state: Action starts; control shows pending if async.
  motion: motion.m1-press, then motion.m1-button-feedback if async.
  result: Success or error state.
input_methods:
  mouse: active state.
  touch: active state without delay (touch-action manipulation).
  keyboard: Same visual on Enter/Space.
states: [default, hover, focus-visible, pressed, loading, success, error, disabled]
feedback: Visual press plus pending state for async actions.
motion: Micro scale/darken 50-100ms.
error_behavior: Returns to default with an error message near the control.
accessibility: Disabled vs aria-disabled chosen deliberately; loading announced.
mobile: Essential because hover is absent.
desktop: Pairs with hover.
recommended_use: Every interactive control.
avoid_when: Never; tune intensity to style.
contexts: [marketing, application, content, commerce]
min_interaction_intensity: 1
technology:
  preferred: [tech.css]
  alternatives: [tech.motion]
```

```yaml
id: interaction.magnetic
name: Magnetic element
kind: interaction
category: pointer
purpose: Pull a key control slightly toward the pointer to signal importance and playfulness.
flow:
  input: Pointer within a radius of the element.
  feedback: Element translates a few pixels toward the pointer.
  state: Attracted, then released.
  motion: Damped follow with gentle spring back.
  result: A tactile, crafted feel on one focal control.
input_methods:
  mouse: Pointer position within radius.
  touch: Disabled.
  keyboard: Normal focus state only.
states: [idle, attracted, pressed]
feedback: Movement of at most 4-10px.
motion: Spring back when pointer leaves.
error_behavior: n/a
accessibility: Hit area must not move away from the pointer; disabled for reduced motion.
mobile: Off.
desktop: One or two focal elements only.
recommended_use: Creative agency and portfolio CTAs, playful brands.
avoid_when: Forms, dense UI, lists of buttons, serious products.
contexts: [marketing]
min_interaction_intensity: 4
technology:
  preferred: [tech.native-js, tech.css]
  alternatives: [tech.motion, tech.gsap]
```

```yaml
id: interaction.cursor-follow
name: Cursor follower
kind: interaction
category: pointer
purpose: Add a contextual cursor label (View, Drag) that clarifies what hovering an area does.
flow:
  input: Pointer moves over a region.
  feedback: A label or shape follows the pointer with damping.
  state: Label changes per target type.
  motion: Damped follow in rAF.
  result: Clearer affordance for media-heavy regions.
input_methods:
  mouse: Pointer position.
  touch: Disabled; use visible labels.
  keyboard: Focus shows the same label as visible text.
states: [hidden, following, contextual-label]
feedback: Label under 150ms lag.
motion: Damped interpolation; no trailing particles.
error_behavior: n/a
accessibility: Never hide the native cursor for text or form areas; label text also available to assistive tech.
mobile: Off.
desktop: Only in media galleries or case study lists.
recommended_use: Portfolios, galleries, drag carousels.
avoid_when: Productivity apps, forms, pages with text selection needs.
contexts: [marketing]
min_interaction_intensity: 4
technology:
  preferred: [tech.native-js]
  alternatives: [tech.motion, tech.gsap]
```

```yaml
id: interaction.hover-preview
name: Hover preview
kind: interaction
category: pointer
purpose: Preview linked content (project image, link card, file) before committing.
flow:
  input: Hover intent over a link or list item.
  feedback: Item highlights.
  state: Preview panel appears near the item or in a fixed preview area.
  motion: motion.fade or motion.m2-popover.
  result: Users choose with more confidence.
input_methods:
  mouse: Hover intent.
  touch: Tap opens the item; preview becomes an inline thumbnail.
  keyboard: Focus shows the preview.
states: [idle, intent, previewing]
feedback: Immediate highlight, delayed preview.
motion: Fast fade in, faster fade out.
error_behavior: Preview fails silently to a placeholder; navigation still works.
accessibility: Preview is supplementary; link text must stand alone.
mobile: Inline thumbnails replace hover previews.
desktop: Hover intent delay 150-300ms.
recommended_use: Project indexes, file lists, reference links.
avoid_when: Information needed to decide is only in the preview.
contexts: [marketing, application, content]
min_interaction_intensity: 3
technology:
  preferred: [tech.css, tech.native-js]
  alternatives: [tech.motion]
```

```yaml
id: interaction.smart-tooltip
name: Smart tooltip
kind: interaction
category: pointer
purpose: Label icon-only controls and explain terms without clutter.
flow:
  input: Hover intent or focus.
  feedback: Tooltip after delay (hover) or immediately (focus).
  state: Visible, positioned to avoid viewport edges.
  motion: motion.m1-tooltip.
  result: Control meaning is clear.
input_methods:
  mouse: Hover intent 300-500ms; moving between tooltips skips delay.
  touch: Long press or visible labels instead.
  keyboard: Focus shows; Escape hides.
states: [hidden, delayed, visible]
feedback: Positioned near trigger, collision-aware.
motion: Fast fade.
error_behavior: n/a
accessibility: aria-describedby or label; dismissible with Escape; hoverable content persists.
mobile: Prefer visible labels.
desktop: Standard for icon toolbars.
recommended_use: Icon-only buttons, abbreviations, truncated text.
avoid_when: Essential instructions or interactive content (use popover).
contexts: [application]
min_interaction_intensity: 1
technology:
  preferred: [tech.css, tech.native-js]
  alternatives: []
```

```yaml
id: interaction.context-menu
name: Context menu
kind: interaction
category: pointer
purpose: Offer object-specific actions where the object is.
flow:
  input: Right click, long press, menu button, or Shift+F10.
  feedback: Object highlighted as target.
  state: Menu open with actions for that object.
  motion: motion.m2-dropdown.
  result: Action executed on the object.
input_methods:
  mouse: Right click or visible more button.
  touch: Long press plus visible more button.
  keyboard: Menu key, Shift+F10, or focused more button.
states: [closed, open, submenu-open, action-pending]
feedback: Target outline plus menu.
motion: Fast scale from pointer location.
error_behavior: Failed action shows toast with retry; destructive actions confirm or undo.
accessibility: role menu with arrow key navigation; focus returns to object.
mobile: Long press plus bottom sheet.
desktop: Right click positioned at pointer.
recommended_use: File browsers, editors, canvases, lists with many actions.
avoid_when: It is the only way to access an action.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: []
```
