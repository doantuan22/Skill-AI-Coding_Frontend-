# Productivity interactions

Patterns that make tools fast for repeat users. Most are keyboard-first and rely on quick feedback rather than expressive motion.

```yaml
id: interaction.multi-select
name: Multi-select
kind: interaction
category: productivity
purpose: Act on many items at once.
flow:
  input: Checkbox, Shift+click range, Ctrl/Cmd+click, Shift+arrows.
  feedback: Selected rows highlighted; selection count appears.
  state: Selection set; bulk actions enabled.
  motion: motion.m1-checkbox; selection toolbar enters.
  result: Bulk action applied with summary.
input_methods:
  mouse: Checkbox and modifier-click.
  touch: Long press enters selection mode, then tap.
  keyboard: Space to toggle, Shift+arrows to extend, Ctrl/Cmd+A.
states: [none-selected, some-selected, all-selected, all-matching-selected]
feedback: Count plus clear-selection action.
motion: Toolbar fade/slide in 150ms.
error_behavior: Partial failures listed per item.
accessibility: aria-selected/aria-checked; count announced.
mobile: Selection mode with visible exit.
desktop: Modifier keys.
recommended_use: Tables, file browsers, inboxes.
avoid_when: Only single actions exist.
contexts: [application]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.inline-editing
name: Inline editing
kind: interaction
category: productivity
purpose: Edit a value where it is displayed.
flow:
  input: Click, Enter or F2 on an editable field.
  feedback: Field turns into an input with the current value selected.
  state: Editing; Enter saves, Escape cancels.
  motion: Instant swap with subtle focus transition.
  result: Value saved with confirmation or error in place.
input_methods:
  mouse: Click or edit icon.
  touch: Tap edit icon.
  keyboard: Enter or F2, then Enter or Escape.
states: [display, editing, saving, saved, error]
feedback: Visible edit affordance on hover and focus.
motion: motion.m1-focus and motion.m1-success.
error_behavior: Keep the edited value, show error inline, allow retry.
accessibility: Label persists; errors linked with aria-describedby.
mobile: Edit via sheet for long values.
desktop: In place.
recommended_use: Tables, titles, settings values.
avoid_when: Complex multi-field edits (use a form).
contexts: [application]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.optimistic-update
name: Optimistic update
kind: interaction
category: productivity
purpose: Make actions feel instant by showing the expected result before the server confirms.
flow:
  input: User action with a predictable outcome.
  feedback: Result shown immediately.
  state: Pending sync marker (subtle).
  motion: motion.m3-layout-reflow or motion.m1-checkbox.
  result: Confirmed silently, or reverted with a message.
input_methods:
  mouse: Any.
  touch: Any.
  keyboard: Any.
states: [applied-pending, confirmed, reverted]
feedback: Immediate result; pending indicator only if slow.
motion: Revert animates back so the change is noticed.
error_behavior: Revert with explanation and retry; never lose user input.
accessibility: Announce reverts.
mobile: Same; handle offline queues.
desktop: Same.
recommended_use: Likes, toggles, reordering, task completion, chat messages.
avoid_when: Payments, irreversible or server-validated actions.
contexts: [application]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.undo
name: Undo
kind: interaction
category: productivity
purpose: Replace confirmation dialogs for reversible actions and forgive mistakes.
flow:
  input: Action performed (delete, archive, move).
  feedback: Action applied and toast offers Undo.
  state: Grace period; action finalized after timeout.
  motion: motion.m2-notification.
  result: Action kept, or restored on Undo.
input_methods:
  mouse: Undo button in toast.
  touch: Undo button.
  keyboard: Ctrl/Cmd+Z and focusable toast button.
states: [applied, undo-available, undone, finalized]
feedback: Clear description of what happened.
motion: Restored item animates back into place.
error_behavior: If undo fails, explain and offer recovery.
accessibility: Toast announced; timeout long enough (5-10s) or pausable.
mobile: Toast above safe area.
desktop: Also Ctrl/Cmd+Z.
recommended_use: Deletions, archiving, bulk moves.
avoid_when: Truly irreversible actions (confirm instead).
contexts: [application]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.command-palette
name: Command palette
kind: interaction
category: productivity
purpose: Let users find and run anything by typing.
flow:
  input: Ctrl/Cmd+K or visible search button.
  feedback: Palette opens instantly with focus in input.
  state: Results filter per keystroke; arrow keys select.
  motion: motion.m2-command-palette.
  result: Command runs or navigation happens; palette closes.
input_methods:
  mouse: Click results.
  touch: Visible search entry point.
  keyboard: Primary; arrows, Enter, Escape.
states: [closed, open-empty, results, no-results, running]
feedback: Highlighted result and shortcut hints.
motion: Near-instant open; no animation per keystroke.
error_behavior: No results suggests alternatives; failed command explained.
accessibility: Combobox pattern with listbox; announce result count.
mobile: Full-screen search.
desktop: Centered overlay.
recommended_use: Productivity, developer tools, admin apps with many destinations.
avoid_when: Small sites with few actions.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.keyboard-navigation
name: Keyboard navigation
kind: interaction
category: productivity
purpose: Operate everything without a pointer, efficiently.
flow:
  input: Tab, arrows, Enter, Escape, shortcuts.
  feedback: Visible focus and selection.
  state: Focus moves predictably within composites (roving tabindex).
  motion: motion.m1-focus.
  result: Tasks completed by keyboard.
input_methods:
  mouse: Not applicable.
  touch: Not applicable (external keyboards supported).
  keyboard: Tab between regions, arrows within lists/grids, Escape to close.
states: [focused, selected, active]
feedback: Focus ring always visible.
motion: None or instant.
error_behavior: Focus never lost to body after actions.
accessibility: Follows WAI-ARIA composite patterns.
mobile: External keyboard support.
desktop: Essential.
recommended_use: Every application.
avoid_when: Never.
contexts: [application, marketing, content, commerce]
min_interaction_intensity: 1
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.selection-toolbar
name: Selection toolbar
kind: interaction
category: productivity
purpose: Offer actions for the current selection near it.
flow:
  input: Text or item selection.
  feedback: Floating toolbar near the selection.
  state: Toolbar actions apply to the selection.
  motion: motion.m2-popover.
  result: Selection formatted, commented, or acted on.
input_methods:
  mouse: Select then click.
  touch: Native selection handles plus toolbar.
  keyboard: Shortcut to focus toolbar.
states: [hidden, visible, action-running]
feedback: Toolbar anchored to selection.
motion: Fast fade and offset.
error_behavior: Failed action keeps selection.
accessibility: Toolbar reachable by keyboard; role toolbar.
mobile: Avoid covering native selection menu.
desktop: Floating near selection.
recommended_use: Editors, document tools, bulk selection in tables.
avoid_when: Selection is rare.
contexts: [application]
min_interaction_intensity: 3
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.shortcut-discovery
name: Shortcut discovery
kind: interaction
category: productivity
purpose: Teach keyboard shortcuts without burdening new users.
flow:
  input: Hover or focus on actions; ? key; palette use.
  feedback: Shortcut hints in tooltips, menus and palette results.
  state: Shortcut sheet available.
  motion: motion.m1-tooltip.
  result: Users progressively adopt shortcuts.
input_methods:
  mouse: Tooltips show shortcuts.
  touch: Not applicable.
  keyboard: The question-mark key opens the shortcut sheet.
states: [hint-hidden, hint-visible, sheet-open]
feedback: Consistent kbd styling.
motion: None beyond tooltips.
error_behavior: Conflicting shortcuts are prevented at design time.
accessibility: Shortcuts avoid assistive technology keys; can be remapped or disabled for single-key shortcuts.
mobile: Hidden.
desktop: Visible hints.
recommended_use: Productivity and developer tools.
avoid_when: Tools used rarely.
contexts: [application]
min_interaction_intensity: 2
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.focus-management
name: Focus management
kind: interaction
category: productivity
purpose: Keep keyboard and screen-reader users oriented after changes.
flow:
  input: Overlay opens, route changes, item deleted, content inserted.
  feedback: Focus moves to the logical next element.
  state: Focus trapped in modal contexts; restored on close.
  motion: Follows the transition.
  result: No lost focus.
input_methods:
  mouse: Not applicable.
  touch: Screen reader gestures.
  keyboard: Primary beneficiary.
states: [focused, trapped, restored]
feedback: Visible focus at new location.
motion: None needed.
error_behavior: On errors, focus moves to the error summary or first invalid field.
accessibility: Core requirement; inert on background content.
mobile: Screen reader focus follows.
desktop: Same.
recommended_use: Every overlay, route change, and dynamic insertion.
avoid_when: Never.
contexts: [application, marketing, content, commerce]
min_interaction_intensity: 1
technology:
  preferred: [tech.native-js]
  alternatives: []
```

```yaml
id: interaction.progressive-disclosure
name: Progressive disclosure
kind: interaction
category: productivity
purpose: Show essentials first, details on demand.
flow:
  input: Expand control, Show more, Advanced settings.
  feedback: Control indicates expanded state.
  state: Additional content revealed in place.
  motion: motion.m2-accordion.
  result: Complexity available without overwhelming.
input_methods:
  mouse: Click.
  touch: Tap.
  keyboard: Enter or Space on the disclosure button.
states: [collapsed, expanded]
feedback: aria-expanded and icon rotation.
motion: Expand/collapse 150-250ms.
error_behavior: Errors inside collapsed sections auto-expand the section.
accessibility: Disclosure button semantics; content in DOM order.
mobile: Same.
desktop: Same.
recommended_use: Settings, forms with advanced options, feature details, AI reasoning details.
avoid_when: Hiding information users always need.
contexts: [application, marketing, content, commerce]
min_interaction_intensity: 1
technology:
  preferred: [tech.css, tech.native-js]
  alternatives: []
```
