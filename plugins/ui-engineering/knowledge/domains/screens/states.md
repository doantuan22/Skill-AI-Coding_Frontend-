# State screens

State screens are designed parts of every screen, not afterthoughts. Their visual behavior also follows the [state grammar](../../visual-language/components/states.md) and [feedback grammar](../../visual-language/components/feedback.md).

```yaml
id: screen.empty-state
name: Empty state
kind: screen
category: state
phase_1_reference: phase-1/references/feedback-states.md
anatomy: Short explanation of what will appear, primary action to create or import, optional example or template.
hierarchy: Reason, then action.
primary_actions: Create first item or import.
secondary_actions: Learn more, use a template.
states: [first-use, no-results, cleared, permission-empty]
layout: Centered within the region it replaces.
interaction: Primary action; template preview.
motion: None or simple fade.
responsive: Same content, compact illustration or none.
accessibility: Text-first; illustration decorative.
common_mistakes: Generic illustration with no action; same message for no-results and first-use.
variants: First use, no search results, filtered to nothing, all done.
compatible_layouts: [layout.hero-centered]
key_interactions: [interaction.press-feedback]
key_motion: [motion.fade]
```

```yaml
id: screen.error-state
name: Error state
kind: screen
category: state
phase_1_reference: phase-1/references/feedback-states.md
anatomy: What happened, impact, what to do next, retry, support reference.
hierarchy: Recovery action prominent.
primary_actions: Retry or recover.
secondary_actions: Contact support, go back.
states: [network, server, not-found, permission, validation-summary]
layout: Replaces the failed region only when possible.
interaction: Retry with feedback, preserve user input.
motion: None beyond feedback.
responsive: Same.
accessibility: Focus moves to error heading for page-level errors; role alert for urgent inline errors.
common_mistakes: Blaming the user; losing input; stack traces.
variants: Inline, section, full page, offline banner.
compatible_layouts: [layout.hero-centered]
key_interactions: [interaction.focus-management, interaction.press-feedback]
key_motion: [motion.m1-error]
```

```yaml
id: screen.loading-state
name: Loading state
kind: screen
category: state
anatomy: Skeletons matching the expected layout, or progress for known work, or a short indicator with text.
hierarchy: Preserve layout; show what is loading.
primary_actions: Cancel where long-running.
secondary_actions: none
states: [initial, refreshing, background-sync, long-running]
layout: Same layout as loaded content.
interaction: Cancel; content remains interactive where possible.
motion: Skeleton shimmer, progress; delayed appearance to avoid flicker.
responsive: Same.
accessibility: aria-busy on the region; announce completion for long waits.
common_mistakes: Full-page spinners for partial loads; layout shift when content arrives.
variants: Skeleton, progress, optimistic placeholder.
compatible_layouts: [layout.app-dashboard-shell, layout.grid-dense-data]
key_interactions: [interaction.optimistic-update]
key_motion: [motion.m1-skeleton, motion.m1-progress, motion.m1-loading]
```
