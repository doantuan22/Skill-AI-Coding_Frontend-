# Search, command and AI screens

```yaml
id: screen.search
name: Search
kind: screen
category: discovery
phase_1_reference: phase-1/references/search-filter.md
anatomy: Query input, suggestions, filters/facets, result count, results, sort, no-results guidance.
hierarchy: Query and results; filters secondary.
primary_actions: Search; open result.
secondary_actions: Filter, sort, save search.
states: [empty-query, suggestions, results, no-results, loading, error]
layout: Filters sidebar plus results list/grid.
interaction: Instant suggestions, keyboard selection, facet toggles.
motion: Filter transitions; no animation per keystroke.
responsive: Filters in a sheet; sticky search bar.
accessibility: Combobox semantics; result count announced.
common_mistakes: No-results dead ends; filters that reset the query.
variants: Site search, catalog search, in-app search.
compatible_layouts: [layout.grid-card-matrix, layout.app-master-detail, layout.hero-media-led]
key_interactions: [interaction.keyboard-navigation, interaction.progressive-disclosure]
key_motion: [motion.m2-filter-transition, motion.m1-skeleton]
```

```yaml
id: screen.command-palette
name: Command palette
kind: screen
category: discovery
anatomy: Input, grouped results (navigation, actions, recent), shortcut hints, footer help.
hierarchy: Best match first.
primary_actions: Run command or navigate.
secondary_actions: Preview, nested commands.
states: [empty, results, no-results, running-command]
layout: Centered overlay or command-driven layout.
interaction: Keyboard-first with arrows, Enter, Escape, nested scopes.
motion: Near-instant open; no result animations.
responsive: Full-screen on mobile.
accessibility: Combobox with listbox; announcements.
common_mistakes: Slow opening; commands not discoverable elsewhere.
variants: Global palette, scoped palette.
compatible_layouts: [layout.app-command-driven]
key_interactions: [interaction.command-palette, interaction.shortcut-discovery]
key_motion: [motion.m2-command-palette]
```

```yaml
id: screen.chat
name: Chat
kind: screen
category: conversation
anatomy: Conversation list, message thread, composer with attachments, participant info.
hierarchy: Current thread and composer.
primary_actions: Send message.
secondary_actions: Attach, react, search, mute.
states: [sending, sent, failed, typing, offline, empty-thread]
layout: Inbox or three-panel.
interaction: Optimistic send, retry failed, reactions, keyboard send.
motion: Messages enter from composer side; typing indicator.
responsive: List then thread on mobile; composer above keyboard.
accessibility: Live region for new messages (polite); timestamps readable.
common_mistakes: Auto-scroll that steals position; lost drafts.
variants: Team chat, support chat, direct messages.
compatible_layouts: [layout.app-inbox, layout.app-three-panel]
key_interactions: [interaction.optimistic-update, interaction.keyboard-navigation]
key_motion: [motion.m3-layout-reflow, motion.m1-loading]
```

```yaml
id: screen.ai-chat
name: AI chat
kind: screen
category: conversation
anatomy: Conversation history, prompt input with attachments and model/tool options, streaming responses with sources, stop/regenerate, feedback.
hierarchy: Latest answer and prompt input.
primary_actions: Send prompt; stop generation.
secondary_actions: Regenerate, copy, rate, attach, open sources.
states: [idle, thinking, streaming, tool-running, complete, error, rate-limited, stopped]
layout: Command-driven centered column; history sidebar.
interaction: Streaming, stop, edit and resend, citations, copy code.
motion: Thinking indicator, streamed text without per-token layout animation, smooth reflow.
responsive: Input pinned above keyboard; history in a drawer.
accessibility: Announce completion politely, not every token; stop button always focusable.
common_mistakes: No stop control; sparkle-everywhere branding; answers without sources where sources matter.
variants: General assistant, support bot, domain assistant.
compatible_layouts: [layout.app-command-driven, layout.app-sidebar-workspace]
key_interactions: [interaction.keyboard-navigation, interaction.drop-zone, interaction.progressive-disclosure]
key_motion: [motion.m1-loading, motion.m3-layout-reflow]
```

```yaml
id: screen.ai-copilot
name: AI copilot panel
kind: screen
category: conversation
anatomy: Side panel attached to the main work, context indicator (what the AI sees), suggestions, prompt input, inline apply/reject of changes.
hierarchy: User's work remains primary; copilot supports.
primary_actions: Ask; apply suggestion.
secondary_actions: Reject, refine, view diff.
states: [closed, idle, thinking, suggestion-ready, applied, reverted, error]
layout: Three-panel or split inspector with the copilot as a pane.
interaction: Inline diff accept/reject, undo applied changes, selection-based prompts.
motion: Panel slide; suggestion insertion reflow; applied change highlight fading.
responsive: Bottom sheet on mobile.
accessibility: Changes described in text; focus stays in the work unless user moves it.
common_mistakes: Copilot covering the work; applying changes without undo.
variants: Code copilot, writing copilot, data copilot.
compatible_layouts: [layout.app-three-panel, layout.app-split-inspector]
key_interactions: [interaction.undo, interaction.selection-toolbar, interaction.progressive-disclosure]
key_motion: [motion.m2-drawer, motion.m3-layout-reflow]
```
