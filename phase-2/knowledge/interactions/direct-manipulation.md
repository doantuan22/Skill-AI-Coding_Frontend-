# Direct manipulation

Direct manipulation feels best when the object tracks input 1:1 and settles with a physical feel. Every gesture has a visible, keyboard-operable alternative.

```yaml
id: interaction.drag
name: Drag
kind: interaction
category: direct-manipulation
purpose: Move an object directly to a new place.
flow:
  input: Pointer down on handle and move beyond a 4-8px threshold.
  feedback: Object lifts (shadow, slight scale) and follows the pointer.
  state: Dragging; valid targets highlight.
  motion: 1-to-1 tracking, then motion.m3-animated-reorder or snap on drop.
  result: Object placed; change saved or undoable.
input_methods:
  mouse: Handle or whole item with threshold.
  touch: Long press to start, to avoid scroll conflict.
  keyboard: Grab with Space, move with arrows, drop with Space, cancel with Escape.
states: [idle, grabbed, dragging, over-valid-target, over-invalid-target, dropped, cancelled]
feedback: Lifted appearance; placeholder shows origin.
motion: Tracking without easing; settle 150-250ms.
error_behavior: Invalid drop animates back to origin with a message; failed save reverts with undo option.
accessibility: Live region announces grab, position and drop; keyboard alternative mandatory.
mobile: Long-press start, auto-scroll near edges.
desktop: Handles visible on hover and focus.
recommended_use: Kanban, file organization, canvas layout.
avoid_when: Ordering that could be a simple sort control.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: [tech.motion]
```

```yaml
id: interaction.drag-resistance
name: Drag resistance
kind: interaction
category: direct-manipulation
purpose: Signal limits (end of list, closed drawer) by resisting further drag.
flow:
  input: Drag beyond an allowed bound.
  feedback: Movement dampens progressively (rubber band).
  state: Over-drag.
  motion: Springs back on release.
  result: User understands the boundary.
input_methods:
  mouse: Drag.
  touch: Drag/swipe.
  keyboard: Not applicable; bounds are enforced silently.
states: [within-bounds, over-bound, releasing]
feedback: Damped displacement (e.g., displacement divided by 3).
motion: Critically-damped spring back.
error_behavior: n/a
accessibility: Purely enhancing; no information only in resistance.
mobile: Primary use.
desktop: Subtle.
recommended_use: Sheets, carousels, pull areas.
avoid_when: Keyboard-only contexts where it has no equivalent meaning.
contexts: [application, commerce]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: [tech.motion]
```

```yaml
id: interaction.spring-snap
name: Spring snap
kind: interaction
category: direct-manipulation
purpose: Settle dragged objects into valid positions with a physical feel.
flow:
  input: Release after drag or fling.
  feedback: Nearest snap point highlighted during drag.
  state: Snapping to target.
  motion: Spring to snap point based on velocity.
  result: Object aligned.
input_methods:
  mouse: Release.
  touch: Release with velocity.
  keyboard: Arrow keys move between snap points.
states: [dragging, snapping, settled]
feedback: Snap guides.
motion: Critically damped or gentle spring.
error_behavior: No valid point returns to origin.
accessibility: Keyboard steps equal snap points.
mobile: Fling velocity respected.
desktop: Guides visible.
recommended_use: Sheets with detents, carousels, canvas alignment.
avoid_when: Precise free positioning is required.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.motion]
  alternatives: [tech.native-js, tech.css]
```

```yaml
id: interaction.reorder
name: Reorder
kind: interaction
category: direct-manipulation
purpose: Change the order of items in a list.
flow:
  input: Drag handle, or move up/down controls.
  feedback: Item lifts; gap opens at target.
  state: Order changes.
  motion: motion.m3-animated-reorder.
  result: New order persisted.
input_methods:
  mouse: Drag handle.
  touch: Long press then drag.
  keyboard: Move up/down buttons or grab with arrows.
states: [idle, dragging, reordered, saving, error]
feedback: Placeholder gap and position announcement.
motion: Neighbors slide 150-250ms.
error_behavior: Revert order with message and undo.
accessibility: Announce new position ("item 3 of 7").
mobile: Handles large enough (44px).
desktop: Handles on hover and focus.
recommended_use: Playlists, priority lists, navigation editors.
avoid_when: Lists sorted by data (dates, names).
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js, tech.waapi]
  alternatives: [tech.motion]
```

```yaml
id: interaction.resize
name: Resize
kind: interaction
category: direct-manipulation
purpose: Adjust panel or object size to fit the task.
flow:
  input: Drag a resize handle or splitter.
  feedback: Cursor change and handle highlight.
  state: Size changes live.
  motion: Direct tracking; no easing.
  result: Size persisted per user.
input_methods:
  mouse: Drag handle.
  touch: Larger handle or preset sizes.
  keyboard: Focusable splitter with arrow keys.
states: [idle, hover, resizing, min-size, max-size]
feedback: Min/max limits resist.
motion: None while dragging; snap to presets optional.
error_behavior: Clamp to limits.
accessibility: role separator with aria-valuenow.
mobile: Preset sizes instead of free resize.
desktop: Split panes and inspectors.
recommended_use: Split views, sidebars, canvas objects.
avoid_when: Layouts that should adapt automatically.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.drop-zone
name: Drop zone
kind: interaction
category: direct-manipulation
purpose: Accept files or objects dropped onto an area.
flow:
  input: Drag files over the page or zone.
  feedback: Zone highlights and states what will happen.
  state: Dropped; upload/processing begins.
  motion: Fade highlight, then motion.m1-progress per file.
  result: Files attached or error per file.
input_methods:
  mouse: Drag and drop.
  touch: File picker button (drag rarely available).
  keyboard: Visible browse button.
states: [idle, drag-over, invalid-type, uploading, success, error]
feedback: Clear accept or reject before drop.
motion: Highlight transition 100-150ms.
error_behavior: Per-file error with reason and retry.
accessibility: Browse button always present; announce results.
mobile: Picker button primary.
desktop: Page-level drop overlay optional.
recommended_use: Upload areas, attachment fields, AI prompt inputs.
avoid_when: It is the only way to upload.
contexts: [application]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.swipe-action
name: Swipe action
kind: interaction
category: direct-manipulation
purpose: Quick actions on list items on touch devices.
flow:
  input: Horizontal swipe on a list row.
  feedback: Action revealed with icon and color under the row.
  state: Past threshold, action armed.
  motion: Row follows finger, snaps open or completes.
  result: Action executed with undo.
input_methods:
  mouse: Visible action buttons on hover.
  touch: Swipe.
  keyboard: Action buttons in row or context menu.
states: [idle, swiping, armed, executing, undone]
feedback: Armed state changes color and haptic if available.
motion: 1-to-1 tracking then spring snap.
error_behavior: Failed action restores row with message.
accessibility: Alternative controls required.
mobile: Primary.
desktop: Hidden; use visible actions.
recommended_use: Inbox, notifications, task lists.
avoid_when: Destructive actions without undo.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: [tech.motion]
```

```yaml
id: interaction.long-press
name: Long press
kind: interaction
category: direct-manipulation
purpose: Access secondary actions or start drag on touch.
flow:
  input: Touch held 400-600ms without movement.
  feedback: Progressive highlight during hold.
  state: Menu opens or drag begins.
  motion: Scale up slightly as confirmation.
  result: Secondary action available.
input_methods:
  mouse: Right click equivalent.
  touch: Hold.
  keyboard: Menu key or visible more button.
states: [idle, holding, triggered, cancelled]
feedback: Visible progress of hold.
motion: Subtle scale.
error_behavior: Moving cancels.
accessibility: Never the only path to an action.
mobile: Common for context menus.
desktop: Not used.
recommended_use: Context menus and drag start on touch.
avoid_when: Primary actions.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.pull-interaction
name: Pull to refresh / reveal
kind: interaction
category: direct-manipulation
purpose: Refresh or reveal content by pulling past the top.
flow:
  input: Pull down at scroll top.
  feedback: Indicator appears and fills with pull distance.
  state: Past threshold, release triggers refresh.
  motion: Resistance then spring back; motion.m1-loading while refreshing.
  result: Content refreshed.
input_methods:
  mouse: Refresh button.
  touch: Pull gesture.
  keyboard: Refresh button or shortcut.
states: [idle, pulling, armed, refreshing, done, error]
feedback: Indicator with progress.
motion: Rubber band resistance.
error_behavior: Error message inline with retry.
accessibility: Visible refresh control for non-touch users.
mobile: Common in feeds.
desktop: Button instead.
recommended_use: Feeds, inboxes on mobile.
avoid_when: Content that updates live anyway.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: [tech.motion]
```
