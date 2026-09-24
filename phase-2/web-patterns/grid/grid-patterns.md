# Grid patterns

Grids organize many items or sections. Choose by content shape: equal parallel items, items of varying importance, items of varying aspect ratio, or dense data.

```yaml
id: layout.grid-bento
name: Bento grid
kind: layout
category: grid
purpose: Summarize several modular features of different importance in one view.
anatomy: 4-8 tiles of varying spans, each with one message and a real visual or micro demo.
hierarchy: Tile size encodes importance; one hero tile.
grid_behavior: 4-6 column grid with 1x1, 2x1, 2x2 spans.
responsive: Two columns on tablet, one on mobile, preserving importance order.
content_requirements: [product-ui]
compatible_styles: [style.bento, style.modern-saas, style.calm-futurism, style.playful, style.neo-brutalism]
compatible_motion: [motion.m4-scroll-reveal, motion.m1-hover, motion.m2-card-expansion]
interactions: [interaction.hover-preview, interaction.progressive-disclosure]
accessibility: DOM order equals importance order; each tile has one focus target at most.
implementation: CSS grid with grid-template-areas per breakpoint.
anti_patterns: Bento as default feature section; tiles with icons and vague copy; every tile animated.
good_for: Feature overviews with real visuals, personal dashboards.
avoid_when: Features need sequence or explanation; content is text-only.
contexts: [marketing]
density: [medium]
motion_cost: low
default_tell: true
```

```yaml
id: layout.grid-masonry
name: Masonry grid
kind: layout
category: grid
purpose: Display media of varying aspect ratios without cropping.
anatomy: Columns of items with natural heights.
hierarchy: Visual browsing; minimal text.
grid_behavior: 2-5 columns; items flow top to bottom per column.
responsive: Column count adapts; single column on small phones.
content_requirements: [brand-photography]
compatible_styles: [style.organic, style.creative-agency, style.ecommerce-premium, style.editorial]
compatible_motion: [motion.fade, motion.m3-thumbnail-to-fullscreen]
interactions: [interaction.hover-preview]
accessibility: Reading order across columns can confuse keyboard users; keep DOM order meaningful.
implementation: CSS columns or grid-template-rows masonry where supported; JS layout only if needed.
anti_patterns: Masonry for text cards; infinite scroll without footer access.
good_for: Portfolios, inspiration boards, photography.
avoid_when: Items must be compared in rows.
contexts: [content, marketing, commerce]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-editorial
name: Editorial grid
kind: layout
category: grid
purpose: Lay out stories with typographic hierarchy and varied scale.
anatomy: Lead story large, secondary stories smaller, text-only items as lists.
hierarchy: Editorial importance by size and position.
grid_behavior: 12-column grid with mixed spans and rules.
responsive: Lead first, then chronological list.
content_requirements: [long-form]
compatible_styles: [style.editorial, style.swiss, style.luxury, style.ecommerce-premium]
compatible_motion: [motion.fade, motion.m4-image-mask-reveal]
interactions: [interaction.hover-preview]
accessibility: Headlines as links with clear focus.
implementation: CSS grid; images with fixed aspect ratios.
anti_patterns: Equal cards with thumbnails for text-only content.
good_for: Publications, blogs, knowledge hubs, collection pages.
avoid_when: Items are equal and comparable (use card matrix).
contexts: [content, commerce]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-broken
name: Broken grid
kind: layout
category: grid
purpose: Create energy and authorship by breaking alignment deliberately.
anatomy: Overlapping media and text crossing column boundaries.
hierarchy: Scale and overlap direct attention.
grid_behavior: Underlying grid exists; elements break it in 2-3 repeated ways.
responsive: Overlaps removed on mobile; offsets preserved through crop.
content_requirements: []
compatible_styles: [style.swiss, style.brutalist, style.experimental, style.y2k, style.creative-agency]
compatible_motion: [motion.clip-reveal, motion.m4-parallax]
interactions: [interaction.hover-preview]
accessibility: Overlaps must not reduce text contrast; DOM order logical.
implementation: CSS grid with negative margins or overlapping grid areas; no absolute text.
anti_patterns: Chaos without a system; overlapping text on text.
good_for: Agencies, portfolios, fashion, culture.
avoid_when: Informational or task pages.
contexts: [marketing, content]
density: [low]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-magazine
name: Magazine layout
kind: layout
category: grid
purpose: Mix feature stories, pull quotes and images across a spread-like section.
anatomy: Multi-column text, pull quotes, image with captions, sidebars.
hierarchy: Feature, quotes, supporting items.
grid_behavior: Multi-column spreads on wide screens.
responsive: Single reading column with inline quotes on mobile.
content_requirements: [long-form, brand-photography]
compatible_styles: [style.editorial, style.luxury, style.swiss]
compatible_motion: [motion.fade, motion.text-line-reveal]
interactions: [interaction.progressive-disclosure]
accessibility: Multi-column text needs reasonable column heights to avoid excessive scrolling.
implementation: CSS grid and columns; avoid column spans for long text on small screens.
anti_patterns: Magazine layout without real editorial content.
good_for: Long reads, annual reports, brand journals.
avoid_when: Short marketing pages.
contexts: [content]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-dashboard
name: Dashboard grid
kind: layout
category: grid
purpose: Arrange KPIs, charts and lists by importance for monitoring.
anatomy: KPI row, primary chart, secondary charts and lists, activity.
hierarchy: Status and exceptions first; detail below.
grid_behavior: 12-column with widgets spanning 3, 4, 6 or 12.
responsive: KPIs stack; charts full width; secondary widgets collapse.
content_requirements: [data]
compatible_styles: [style.data-dense, style.enterprise-saas, style.fintech, style.productivity]
compatible_motion: [motion.m1-skeleton, motion.text-counter, motion.m2-filter-transition]
interactions: [interaction.keyboard-navigation, interaction.progressive-disclosure, interaction.hover-preview]
accessibility: Charts need text summaries or tables; widget headings for navigation.
implementation: CSS grid; container queries for widgets.
anti_patterns: Equal cards for unequal importance; decorative charts; everything tinted.
good_for: Operational dashboards, analytics overviews.
avoid_when: Users need a single workflow instead of monitoring.
contexts: [application]
density: [high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-card-matrix
name: Card matrix
kind: layout
category: grid
purpose: Present equal, comparable items for browsing.
anatomy: Uniform cards with media, title, key facts, action.
hierarchy: Consistent card anatomy; key fact emphasized.
grid_behavior: Auto-fill minmax columns.
responsive: Columns reduce; list view on mobile when facts matter more than images.
content_requirements: [listings]
compatible_styles: [style.ecommerce-premium, style.modern-saas, style.monochrome, style.neo-brutalism, style.playful]
compatible_motion: [motion.m1-hover, motion.m2-filter-transition, motion.m3-thumbnail-to-fullscreen]
interactions: [interaction.hover-preview, interaction.multi-select]
accessibility: Whole-card links use a single anchor with a stretched target.
implementation: CSS grid auto-fill; consistent aspect ratios.
anti_patterns: Three equal feature cards with generic icons as a default section.
good_for: Listings, catalogs, templates, integrations.
avoid_when: Items have different importance.
contexts: [commerce, application, marketing]
density: [medium, high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-asymmetric
name: Asymmetric grid
kind: layout
category: grid
purpose: Balance different-sized items for a curated, authored feel.
anatomy: Alternating large and small items with offsets.
hierarchy: Curated emphasis by size.
grid_behavior: Repeating asymmetric rhythm (e.g., 7/5 then 4/8).
responsive: Single column with alternating crops.
content_requirements: [brand-photography]
compatible_styles: [style.creative-agency, style.editorial, style.monochrome, style.luxury]
compatible_motion: [motion.m4-image-mask-reveal, motion.fade-up]
interactions: [interaction.hover-preview]
accessibility: Logical DOM order.
implementation: CSS grid with explicit placements.
anti_patterns: Asymmetry without rhythm.
good_for: Case study indexes, collections, portfolios.
avoid_when: Items must be scanned uniformly.
contexts: [marketing, content]
density: [low, medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.grid-dense-data
name: Dense data grid
kind: layout
category: grid
purpose: Show and operate on large tabular data efficiently.
anatomy: Toolbar (search, filters, views), sticky header, rows, pagination or virtualization, bulk actions.
hierarchy: Primary column and status first; secondary columns can hide.
grid_behavior: Table with sticky header and first column; column resize and hide.
responsive: Column priority; horizontal scroll inside the table; cards only if tasks require.
content_requirements: [data]
compatible_styles: [style.data-dense, style.enterprise-saas, style.fintech, style.brutalist, style.productivity]
compatible_motion: [motion.m1-skeleton, motion.m3-animated-reorder, motion.m2-filter-transition]
interactions: [interaction.multi-select, interaction.inline-editing, interaction.keyboard-navigation, interaction.resize]
accessibility: Real table semantics or ARIA grid; sort state announced.
implementation: Virtualize beyond a few hundred rows; tabular numerals.
anti_patterns: Card grids for data; zebra plus borders plus shadows; animating every row update.
good_for: Admin, CRM, analytics, logs.
avoid_when: Few items with rich media.
contexts: [application]
density: [high]
motion_cost: low
default_tell: false
```
