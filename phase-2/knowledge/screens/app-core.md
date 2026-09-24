# Core application screens

```yaml
id: screen.dashboard
name: Dashboard
kind: screen
category: overview
phase_1_reference: phase-1/references/dashboard.md
anatomy: Page header with scope and date range, KPI summary, primary chart or status, exceptions/alerts, recent activity, shortcuts to frequent tasks.
hierarchy: Exceptions and status first, trends second, detail on demand.
primary_actions: Act on exceptions; drill into a metric.
secondary_actions: Change date range, customize widgets, export.
states: [loading, empty-first-use, partial-data, error-per-widget, stale-data, permission-limited]
layout: Dashboard shell with a widget grid; one dominant widget.
interaction: Drill-down, filter, hover tooltips on charts, keyboard access to widgets.
motion: Skeleton per widget, counters only on value change, filter transitions; no entrance animations.
responsive: KPIs stack; charts full width; secondary widgets collapse behind tabs.
accessibility: Chart text summaries; widget headings; status not by color alone.
common_mistakes: Equal-weight cards; vanity metrics; decorative charts; every widget tinted.
variants: Operational monitoring, executive summary, personal home.
compatible_layouts: [layout.app-dashboard-shell, layout.grid-dashboard]
key_interactions: [interaction.progressive-disclosure, interaction.keyboard-navigation, interaction.hover-preview]
key_motion: [motion.m1-skeleton, motion.text-counter, motion.m2-filter-transition]
```

```yaml
id: screen.analytics
name: Analytics
kind: screen
category: overview
anatomy: Query/filter bar, metric selector, primary chart, breakdown table, comparison controls, saved views.
hierarchy: Question (filters) then answer (chart) then evidence (table).
primary_actions: Change dimension/metric; compare periods.
secondary_actions: Save view, export, share.
states: [loading, no-data-for-range, query-error, partial, large-result-truncated]
layout: Dashboard shell with a chart plus dense data grid.
interaction: Brush and zoom on charts, keyboard-accessible table, synced hover between chart and table.
motion: Chart transitions between queries (short), skeletons; no decorative animation.
responsive: Filters in a sheet; table horizontal scroll; chart simplified.
accessibility: Data tables for every chart; announced query results.
common_mistakes: Chart junk; too many series colors; filters hidden.
variants: Product analytics, finance reporting, marketing attribution.
compatible_layouts: [layout.app-dashboard-shell, layout.grid-dense-data]
key_interactions: [interaction.keyboard-navigation, interaction.multi-select, interaction.progressive-disclosure]
key_motion: [motion.m2-filter-transition, motion.m1-skeleton]
```

```yaml
id: screen.workspace
name: Workspace
kind: screen
category: work
anatomy: Workspace navigation, current context header, main work area, optional inspector or AI panel.
hierarchy: The object being worked on dominates.
primary_actions: Create and edit work items.
secondary_actions: Share, switch workspace, settings.
states: [empty-workspace, loading, syncing, offline, conflict]
layout: Sidebar workspace or three-panel.
interaction: Command palette, keyboard navigation, drag organization, inline editing.
motion: Snappy panel transitions; optimistic updates; minimal otherwise.
responsive: Navigation drawer, single pane at a time on mobile.
accessibility: Landmarks, pane cycling, persistent focus.
common_mistakes: Chrome heavier than content; hidden core actions.
variants: Docs workspace, project workspace, design workspace.
compatible_layouts: [layout.app-sidebar-workspace, layout.app-three-panel]
key_interactions: [interaction.command-palette, interaction.keyboard-navigation, interaction.optimistic-update]
key_motion: [motion.m2-navigation-state, motion.m3-layout-reflow]
```

```yaml
id: screen.admin
name: Admin console
kind: screen
category: work
phase_1_reference: phase-1/references/tables.md
anatomy: Navigation by resource, resource list with filters, detail/edit view, audit info.
hierarchy: Resource lists and their status first.
primary_actions: Create, edit, disable resources.
secondary_actions: Bulk actions, export, view audit log.
states: [empty, loading, error, permission-limited, destructive-confirmation]
layout: Sidebar workspace plus master-detail or dense table.
interaction: Bulk selection, filters, confirmations/undo for destructive actions.
motion: Minimal.
responsive: Desktop-first; read and approve flows on mobile.
accessibility: Full keyboard; destructive actions clearly labelled.
common_mistakes: Destructive actions styled like primary; no audit trail visibility.
variants: User management, content moderation, system configuration.
compatible_layouts: [layout.app-sidebar-workspace, layout.grid-dense-data, layout.app-master-detail]
key_interactions: [interaction.multi-select, interaction.undo, interaction.keyboard-navigation]
key_motion: [motion.m2-modal, motion.m1-skeleton]
```

```yaml
id: screen.list
name: List screen
kind: screen
category: collection
anatomy: Title with count, search/filter/sort, list items with key attributes and actions, pagination or infinite load.
hierarchy: Item identity and status first.
primary_actions: Open item; create new.
secondary_actions: Sort, filter, bulk actions.
states: [empty, no-results, loading, error, end-of-list]
layout: Single list or card matrix depending on item shape.
interaction: Keyboard navigation, multi-select, hover preview.
motion: Filter transitions, skeleton rows.
responsive: Compact rows with the two most important attributes.
accessibility: List semantics; result counts announced.
common_mistakes: Cards for text-only items; no empty state guidance.
variants: Project list, contact list, order list.
compatible_layouts: [layout.app-master-detail, layout.grid-card-matrix]
key_interactions: [interaction.multi-select, interaction.keyboard-navigation, interaction.hover-preview]
key_motion: [motion.m2-filter-transition, motion.m1-skeleton]
```

```yaml
id: screen.detail
name: Detail screen
kind: screen
category: collection
anatomy: Identity header (title, status, key facts), primary action, tabs or sections for detail, related items, activity.
hierarchy: Identity and status, then primary action, then detail.
primary_actions: The main operation on the object.
secondary_actions: Edit, share, duplicate, delete.
states: [loading, not-found, permission-limited, archived, error]
layout: Master-detail pane or full page with sections.
interaction: Inline editing, tabs, progressive disclosure.
motion: List-to-detail continuity; tab transitions.
responsive: Sticky primary action on mobile.
accessibility: Heading structure; status text.
common_mistakes: Primary action lost among secondary buttons.
variants: Record detail, product detail, profile detail.
compatible_layouts: [layout.app-master-detail, layout.app-split-inspector]
key_interactions: [interaction.inline-editing, interaction.progressive-disclosure]
key_motion: [motion.m3-list-to-detail, motion.m2-tabs]
```

```yaml
id: screen.data-table
name: Data table
kind: screen
category: collection
phase_1_reference: phase-1/references/tables.md
anatomy: Toolbar (search, filters, views, columns), table with sticky header, row actions, bulk action bar, pagination.
hierarchy: Primary column and status; numeric columns aligned right.
primary_actions: Open or act on rows.
secondary_actions: Configure columns, export, save view.
states: [loading, empty, no-results, error, selection-active]
layout: Dense data grid.
interaction: Sort, filter, multi-select, inline edit, keyboard grid navigation, column resize.
motion: Skeleton rows; reorder on sort only for small sets.
responsive: Column priority and horizontal scroll inside the table.
accessibility: Table semantics or ARIA grid; sort state announced.
common_mistakes: Card views for tabular comparison; heavy zebra and borders.
variants: Admin table, financial ledger, log viewer.
compatible_layouts: [layout.grid-dense-data]
key_interactions: [interaction.multi-select, interaction.inline-editing, interaction.keyboard-navigation, interaction.resize]
key_motion: [motion.m1-skeleton, motion.m3-animated-reorder]
```

```yaml
id: screen.kanban
name: Kanban board
kind: screen
category: work
anatomy: Board header with filters, columns by status, cards with key info, add card, WIP limits.
hierarchy: Column status then card priority.
primary_actions: Move cards between columns; create card.
secondary_actions: Filter, group, edit card.
states: [empty-column, loading, move-error, wip-exceeded]
layout: Horizontal columns with independent vertical scroll.
interaction: Drag and drop with keyboard alternative (move to column menu), reorder, quick edit.
motion: Lift on drag, animated reorder, spring snap into columns.
responsive: One column at a time with column switcher on mobile.
accessibility: Move actions available without drag; announcements for moves.
common_mistakes: Drag as the only way to move; overcrowded cards.
variants: Sprint board, sales pipeline, content calendar.
compatible_layouts: [layout.app-sidebar-workspace]
key_interactions: [interaction.drag, interaction.reorder, interaction.spring-snap, interaction.keyboard-navigation]
key_motion: [motion.m3-animated-reorder]
```

```yaml
id: screen.calendar
name: Calendar
kind: screen
category: work
anatomy: Date navigation, view switcher (day/week/month), events grid, event detail, create event.
hierarchy: Today and current time; conflicts.
primary_actions: Create or open events.
secondary_actions: Change view, filter calendars.
states: [loading, empty-range, conflict, sync-error]
layout: Sidebar plus calendar grid.
interaction: Drag to create or move, resize duration, keyboard date navigation.
motion: Directional slide between ranges; event drag follows pointer.
responsive: Agenda list on mobile.
accessibility: Grid navigation with arrow keys; events announced with time.
common_mistakes: Tiny targets; color-only calendar identification.
variants: Scheduling, booking availability, content calendar.
compatible_layouts: [layout.app-sidebar-workspace, layout.app-split-inspector]
key_interactions: [interaction.drag, interaction.resize, interaction.keyboard-navigation]
key_motion: [motion.slide, motion.m2-popover]
```

```yaml
id: screen.file-browser
name: File browser
kind: screen
category: collection
anatomy: Location breadcrumb, toolbar, file list or grid, preview pane, upload area.
hierarchy: Current location and files.
primary_actions: Open, upload, create folder.
secondary_actions: Move, rename, share, delete.
states: [empty-folder, uploading, error, permission-limited, search-results]
layout: Master-detail or three-panel with preview.
interaction: Multi-select, context menu, drag to move, drop zone, rename inline.
motion: Upload progress, list-to-preview continuity.
responsive: List view with actions sheet on mobile.
accessibility: Tree and grid semantics; keyboard move alternatives.
common_mistakes: Context-menu-only actions; no upload progress.
variants: Cloud drive, asset library, repository browser.
compatible_layouts: [layout.app-three-panel, layout.app-master-detail]
key_interactions: [interaction.multi-select, interaction.context-menu, interaction.drop-zone, interaction.inline-editing]
key_motion: [motion.m1-progress, motion.m3-list-to-detail]
```

```yaml
id: screen.editor
name: Editor
kind: screen
category: work
anatomy: Document or canvas, toolbar, outline/layers, inspector, save/sync status, collaboration presence.
hierarchy: Content being authored dominates.
primary_actions: Author and format content.
secondary_actions: Share, history, export, comments.
states: [saving, saved, offline, conflict, read-only]
layout: Editor shell or canvas workspace.
interaction: Selection toolbar, shortcuts, undo/redo, drag blocks.
motion: Minimal; save status transitions; collaborator cursors smooth.
responsive: Reduced toolbar; read-first on mobile.
accessibility: Editor roles and shortcuts; announcements for collaboration events kept polite.
common_mistakes: Heavy chrome; hidden save state.
variants: Rich text, code, design canvas, form builder.
compatible_layouts: [layout.app-editor-shell, layout.app-canvas]
key_interactions: [interaction.selection-toolbar, interaction.undo, interaction.shortcut-discovery]
key_motion: [motion.m2-popover, motion.m1-success]
```
