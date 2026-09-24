# Application layouts

Layouts for product UIs. Navigation destinations and page responsibilities are locked in Phase 1; these entries choose the shell and pane composition that realizes them.

```yaml
id: layout.app-sidebar-workspace
name: Sidebar workspace
kind: layout
category: application
purpose: Persistent navigation plus a primary work area.
anatomy: Collapsible sidebar (workspace switcher, navigation, user), top bar (context, actions), main area.
hierarchy: Main content dominant; sidebar recedes.
grid_behavior: Fixed or resizable sidebar 220-280px; fluid main.
responsive: Sidebar becomes a drawer below tablet width.
content_requirements: []
compatible_styles: [style.productivity, style.minimal, style.developer-tool, style.enterprise-saas, style.ai-native]
compatible_motion: [motion.m2-navigation-state, motion.m2-drawer]
interactions: [interaction.keyboard-navigation, interaction.resize, interaction.command-palette]
accessibility: Landmarks (nav, main); skip link; collapsed state keeps accessible names.
implementation: CSS grid shell; sidebar state persisted.
anti_patterns: Pill-highlighted nav items; icons without labels in expanded state.
good_for: Most SaaS apps.
avoid_when: Single-page tools with one task.
contexts: [application]
density: [medium, high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-three-panel
name: Three-panel workspace
kind: layout
category: application
purpose: Navigate, work and inspect at the same time.
anatomy: Navigation or list panel, main work panel, context/inspector or AI panel.
hierarchy: Main panel dominant; side panels collapsible.
grid_behavior: Resizable panes with min widths.
responsive: Stack as navigation to list to detail on mobile; inspector becomes a sheet.
content_requirements: []
compatible_styles: [style.productivity, style.ai-native, style.developer-tool, style.data-dense]
compatible_motion: [motion.m3-layout-reflow, motion.m2-drawer]
interactions: [interaction.resize, interaction.keyboard-navigation, interaction.focus-management]
accessibility: Pane regions labelled; F6-style pane cycling helps keyboard users.
implementation: CSS grid with resizable splitters; persist widths.
anti_patterns: Three panels on small screens; panels competing for attention.
good_for: Email, IDEs, AI copilots, design tools.
avoid_when: Simple content consumption.
contexts: [application]
density: [high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-master-detail
name: Master-detail
kind: layout
category: application
purpose: Browse a list and see details of the selected item.
anatomy: List with search/filter, detail pane with actions.
hierarchy: Selection in list drives detail.
grid_behavior: 4/8 or resizable split.
responsive: List then detail as separate screens on mobile.
content_requirements: []
compatible_styles: [style.enterprise-saas, style.productivity, style.data-dense, style.fintech]
compatible_motion: [motion.m3-list-to-detail, motion.m1-skeleton]
interactions: [interaction.keyboard-navigation, interaction.multi-select]
accessibility: Selected item state announced; focus moves to detail heading on open.
implementation: URL reflects selection.
anti_patterns: Detail as modal over list for primary tasks.
good_for: CRM records, tickets, orders, files.
avoid_when: Items have no meaningful detail.
contexts: [application]
density: [medium, high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-canvas
name: Canvas workspace
kind: layout
category: application
purpose: Free-form spatial work (design, whiteboard, diagram).
anatomy: Infinite canvas, floating toolbars, layers or properties panel, zoom controls.
hierarchy: Canvas dominant; chrome minimal.
grid_behavior: Full viewport with overlay controls.
responsive: Touch gestures for pan/zoom; simplified toolbars.
content_requirements: []
compatible_styles: [style.productivity, style.liquid-glass, style.minimal, style.playful]
compatible_motion: [motion.m5-spatial-navigation, motion.m2-popover]
interactions: [interaction.drag, interaction.resize, interaction.multi-select, interaction.context-menu, interaction.selection-toolbar]
accessibility: Keyboard alternatives for object manipulation; object list for screen readers.
implementation: Canvas or SVG rendering with a DOM accessibility layer.
anti_patterns: No non-canvas representation; tiny touch targets.
good_for: Design tools, whiteboards, diagram editors.
avoid_when: Structured forms or lists.
contexts: [application]
density: [medium]
motion_cost: medium
default_tell: false
```

```yaml
id: layout.app-command-driven
name: Command-driven UI
kind: layout
category: application
purpose: Put a command input at the center of interaction.
anatomy: Command/prompt bar, results or conversation area, minimal navigation.
hierarchy: Input first; results follow.
grid_behavior: Centered column or bottom-anchored input.
responsive: Input pinned above the keyboard on mobile.
content_requirements: []
compatible_styles: [style.ai-native, style.developer-tool, style.minimal, style.productivity]
compatible_motion: [motion.m2-command-palette, motion.m3-layout-reflow, motion.m1-loading]
interactions: [interaction.command-palette, interaction.keyboard-navigation, interaction.shortcut-discovery]
accessibility: Combobox semantics; results announced.
implementation: Debounced search; streaming results appended without layout thrash.
anti_patterns: Command UI without discoverable examples.
good_for: AI assistants, launchers, developer consoles.
avoid_when: Users do not know what to ask; visual browsing tasks.
contexts: [application]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-dashboard-shell
name: Dashboard shell
kind: layout
category: application
purpose: Frame monitoring and analytics views with filters and navigation.
anatomy: Navigation, page header with date range and filters, widget grid.
hierarchy: Global filters, then KPIs, then detail.
grid_behavior: Shell plus dashboard grid.
responsive: Filters in a sheet; widgets stacked.
content_requirements: [data]
compatible_styles: [style.data-dense, style.enterprise-saas, style.fintech, style.productivity]
compatible_motion: [motion.m1-skeleton, motion.m2-filter-transition]
interactions: [interaction.keyboard-navigation, interaction.progressive-disclosure]
accessibility: Filter changes announce updated results.
implementation: Container queries for widgets; skeletons per widget.
anti_patterns: Decorative hero or gradients in the shell.
good_for: Analytics, monitoring, admin.
avoid_when: Task workflows.
contexts: [application]
density: [high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-editor-shell
name: Editor shell
kind: layout
category: application
purpose: Focus on authoring content with tools on demand.
anatomy: Document area, contextual toolbar, outline or file tree, optional inspector.
hierarchy: Document dominant.
grid_behavior: Centered measure-constrained document with side panes.
responsive: Toolbar collapses; panes become sheets.
content_requirements: []
compatible_styles: [style.minimal, style.productivity, style.editorial, style.ai-native]
compatible_motion: [motion.m2-popover, motion.m3-layout-reflow]
interactions: [interaction.selection-toolbar, interaction.keyboard-navigation, interaction.undo, interaction.shortcut-discovery]
accessibility: Editor semantics; toolbar roles; shortcuts documented.
implementation: Existing editor frameworks preferred over custom contenteditable.
anti_patterns: Always-visible heavy toolbars.
good_for: Docs, notes, code editors, CMS.
avoid_when: Read-only content.
contexts: [application]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-inbox
name: Inbox layout
kind: layout
category: application
purpose: Triage a stream of items quickly.
anatomy: Folder/filter nav, item list with preview lines, reading pane, bulk actions.
hierarchy: Unread and priority items stand out.
grid_behavior: Two or three panes.
responsive: List and reading screen on mobile with swipe actions.
content_requirements: []
compatible_styles: [style.productivity, style.minimal, style.enterprise-saas]
compatible_motion: [motion.m3-list-to-detail, motion.m3-animated-reorder, motion.m2-notification]
interactions: [interaction.swipe-action, interaction.multi-select, interaction.undo, interaction.keyboard-navigation]
accessibility: Item states announced; shortcuts optional.
implementation: Virtualized list; optimistic archive with undo.
anti_patterns: Card-styled messages; heavy per-item animation.
good_for: Email, notifications, support tickets, approvals.
avoid_when: Low-volume streams.
contexts: [application]
density: [high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.app-split-inspector
name: Split inspector
kind: layout
category: application
purpose: Edit properties of a selected object next to it.
anatomy: Main view with selection, inspector pane with grouped properties.
hierarchy: Selection context, then properties.
grid_behavior: Main plus 280-360px inspector.
responsive: Inspector becomes a bottom sheet.
content_requirements: []
compatible_styles: [style.productivity, style.tactile, style.glassmorphism, style.ai-native, style.developer-tool]
compatible_motion: [motion.m2-drawer, motion.m2-accordion]
interactions: [interaction.inline-editing, interaction.progressive-disclosure, interaction.resize]
accessibility: Inspector labelled by the selected object.
implementation: Inspector content keyed by selection.
anti_patterns: Inspector for trivial settings.
good_for: Design tools, CMS blocks, configuration UIs.
avoid_when: Few properties.
contexts: [application]
density: [medium, high]
motion_cost: low
default_tell: false
```
