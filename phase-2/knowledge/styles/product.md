# Product and commerce styles

```yaml
id: style.developer-tool
name: Developer tool
kind: style
category: product
family: product
character: Precise, fast, honest, engineered; respects expert time.
visual_language: Code and terminal as proof, hairline structure, mono metadata, keyboard hints.
layout: Documentation-like rhythm; evidence near claims; docs sidebar in docs areas.
typography: Neutral grotesk plus monospace for code, commands and identifiers.
color_behavior: Dark or high-contrast neutral; accent is functional (links, status, syntax).
surface: Code blocks, bordered panels, terminal frames; flat.
borders: Hairlines over shadows.
shadows: Minimal.
imagery: Code, CLI output, diagrams, real UI.
iconography: Small monoline, consistent.
motion: Snappy and minimal; stepped code reveal only if it teaches.
interaction: Copy-to-clipboard, keyboard shortcuts, command palette, tabs for languages.
recommended_effects: [effect.noise, effect.edge-highlight]
avoid_effects: [effect.glass, effect.holographic, effect.particles, effect.mesh-gradient, effect.chromatic]
recommended_motion: [motion.m1-button-feedback, motion.m2-tabs, motion.m2-command-palette, motion.m1-success]
density: [medium, high]
accessibility_notes: Syntax highlighting colors need contrast; code blocks must be keyboard scrollable.
responsive_behavior: Code blocks scroll horizontally inside themselves; commands stay copyable on mobile.
good_for: CLIs, SDKs, APIs, frameworks, devops, open-source projects.
avoid_when: Consumer lifestyle, luxury, emotional brand storytelling.
compatible_patterns: [layout.hero-centered, layout.story-feature-explorer, layout.story-comparison, layout.app-sidebar-workspace]
compatible_styles: [style.monochrome, style.calm-futurism, style.swiss, style.minimal]
implementation_notes: Pair with Typography developer archetype; hairline grid optional.
domains: [developer, saas, data-platform, ai]
conveys: [precise, technical, efficient, trustworthy, clean]
perceived_risks: [cold, intimidating]
intensity: [1, 3]
contexts: [marketing, application, content]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.enterprise-saas
name: Enterprise SaaS
kind: style
category: product
family: product
character: Dependable, clear, governed; reduces risk for large organizations.
visual_language: Neutral structured UI, clear navigation, strong information hierarchy, compliance and trust signals.
layout: App shell with sidebar; marketing pages with capability to evidence structure.
typography: Neutral humanist or neo-grotesk; tabular numerals; compact scale.
color_behavior: Neutral with one brand blue-like accent; semantic status set.
surface: Panels, tables, cards only for grouping.
borders: Dividers and bordered panels.
shadows: Minimal; overlays only.
imagery: Real UI, diagrams, customer logos with permission.
iconography: Consistent system icon set.
motion: Minimal, fast state transitions.
interaction: Keyboard navigation, bulk actions, filters, predictable dialogs.
recommended_effects: [effect.shadow]
avoid_effects: [effect.glow, effect.glass, effect.particles, effect.mesh-gradient, effect.holographic, effect.shader]
recommended_motion: [motion.m1-hover, motion.m1-focus, motion.m2-drawer, motion.m2-dropdown, motion.m1-skeleton]
density: [medium, high]
accessibility_notes: Procurement often requires WCAG conformance; tables and forms need full keyboard support.
responsive_behavior: Desktop-first; tablet keeps core flows; mobile for approvals and read-only views.
good_for: B2B platforms, admin, compliance, ERP, HR, security tooling.
avoid_when: Consumer brands, launches needing emotion.
compatible_patterns: [layout.app-dashboard-shell, layout.app-master-detail, layout.grid-dense-data, layout.hero-dashboard]
compatible_styles: [style.data-dense, style.productivity, style.modern-saas]
implementation_notes: Design tokens and component library consistency matter more than any effect.
domains: [enterprise, saas, analytics, public-sector, healthcare]
conveys: [trustworthy, serious, efficient, clean]
perceived_risks: [generic, sterile]
intensity: [1, 2]
contexts: [application, marketing]
motion_ceiling: M2
default_tell: false
```

```yaml
id: style.modern-saas
name: Modern SaaS
kind: style
category: product
family: product
character: Capable, organized, current; product UI is the proof.
visual_language: Clean grid, product screenshots with meaningful crops, alternating feature rhythm, one accent.
layout: Feature-preview hero, alternating features, social proof, pricing.
typography: Neutral sans, medium display contrast.
color_behavior: Neutral base with one brand accent.
surface: Light cards or framed UI previews; hairline borders.
borders: Hairlines.
shadows: Low, soft.
imagery: Real product UI annotated; diagrams.
iconography: Consistent line family.
motion: Soft entrances, UI preview transitions, feature switchers.
interaction: Tabs and feature switchers, interactive demos when useful.
recommended_effects: [effect.shadow, effect.gradient, effect.radial-lighting]
avoid_effects: [effect.particles, effect.holographic, effect.chromatic]
recommended_motion: [motion.fade-up, motion.m2-tabs, motion.m4-scroll-reveal, motion.m3-layout-reflow]
density: [medium]
accessibility_notes: UI screenshots need alt text describing the demonstrated capability.
responsive_behavior: Crop screenshots to the meaningful region on mobile.
good_for: B2B and prosumer software marketing, onboarding surfaces.
avoid_when: Luxury, editorial, portfolios needing personality.
compatible_patterns: [layout.hero-dashboard, layout.story-alternating, layout.story-feature-explorer, layout.grid-bento]
compatible_styles: [style.enterprise-saas, style.productivity, style.calm-futurism, style.bento]
implementation_notes: The most generic style if applied without product evidence; demand real UI.
domains: [saas, productivity, analytics, ai]
conveys: [clean, efficient, trustworthy, approachable]
perceived_risks: [generic]
intensity: [2, 3]
contexts: [marketing, application]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.data-dense
name: Data-dense
kind: style
category: product
family: product
character: Efficient, reliable, in control; information first.
visual_language: Compact tables, small multiples, aligned numerals, minimal chrome.
layout: App shell, panels, tables and charts; alignment creates hierarchy.
typography: Neutral sans with tabular numerals; compact scale; mono for IDs.
color_behavior: Neutral UI; color reserved for data encoding and status.
surface: Panels and tables; dividers.
borders: Dividers and gridlines at low contrast.
shadows: Overlays only.
imagery: Charts only.
iconography: Small functional icons.
motion: Minimal, fast; state change, loading, expand/collapse only.
interaction: Sorting, filtering, keyboard navigation, multi-select, inline editing.
recommended_effects: []
avoid_effects: [effect.glow, effect.glass, effect.backdrop-blur, effect.particles, effect.mesh-gradient, effect.shader, effect.grain]
recommended_motion: [motion.m1-skeleton, motion.m1-progress, motion.m2-filter-transition, motion.m3-animated-reorder]
density: [high]
accessibility_notes: Charts need data tables or text equivalents; do not encode status by color alone.
responsive_behavior: Prioritize columns; horizontal scroll inside tables; summary cards on mobile.
good_for: Dashboards, analytics, monitoring, trading, operations.
avoid_when: Marketing storytelling, brand launches.
compatible_patterns: [layout.app-dashboard-shell, layout.grid-dense-data, layout.grid-dashboard, layout.app-master-detail]
compatible_styles: [style.enterprise-saas, style.fintech, style.productivity]
implementation_notes: Virtualize long tables; animate only state, never data on every tick.
domains: [analytics, enterprise, fintech, data-platform, developer]
conveys: [efficient, dense, precise, serious, trustworthy]
perceived_risks: [cluttered, intimidating]
intensity: [1, 2]
contexts: [application]
motion_ceiling: M2
default_tell: false
```

```yaml
id: style.fintech
name: Fintech
kind: style
category: product
family: product
character: Trustworthy, clear, modern; money feels safe and understandable.
visual_language: Clear numbers, calm color, strong confirmation states, security cues without fear.
layout: Balance or value first, clear actions, transaction lists, charts with plain-language summaries.
typography: Neutral sans with excellent tabular numerals; large amounts.
color_behavior: Calm neutral with a trustworthy accent; gains/losses semantic but not garish.
surface: Clean cards for accounts, restrained elevation.
borders: Subtle.
shadows: Soft, low.
imagery: Product UI, simple illustration, real people sparingly.
iconography: Clear financial glyphs, consistent.
motion: Precise number transitions, confirmation success, no playful bounce on money.
interaction: Confirmations for irreversible actions, undo where possible, clear pending states.
recommended_effects: [effect.shadow, effect.gradient]
avoid_effects: [effect.chromatic, effect.distortion, effect.particles, effect.holographic, effect.glow]
recommended_motion: [motion.text-counter, motion.m1-success, motion.m1-progress, motion.m2-modal]
density: [medium, high]
accessibility_notes: Amounts need screen-reader friendly formatting; never rely on red/green alone.
responsive_behavior: Mobile-first for consumer fintech; dense tables for pro trading on desktop.
good_for: Banking, payments, investing, accounting, crypto with a trust focus.
avoid_when: Entertainment or youth campaigns that need loudness.
compatible_patterns: [layout.app-dashboard-shell, layout.grid-dashboard, layout.hero-product, layout.app-master-detail]
compatible_styles: [style.data-dense, style.enterprise-saas, style.minimal, style.calm-futurism]
implementation_notes: Tabular numerals and locale formatting tokens; number transitions only when values change.
domains: [fintech, enterprise, consumer]
conveys: [trustworthy, precise, calm, clean, serious]
perceived_risks: [cold]
intensity: [1, 3]
contexts: [application, marketing]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.productivity
name: Productivity
kind: style
category: product
family: product
character: Focused, fast, frictionless; the tool gets out of the way.
visual_language: Quiet chrome, strong focus states, keyboard affordances, content-first canvases.
layout: Sidebar workspace, lists and detail, command palette.
typography: Neutral sans, compact but readable; mono for shortcuts.
color_behavior: Neutral with one focus accent; subtle selection colors.
surface: Flat panes with dividers; overlays for commands.
borders: Dividers.
shadows: Overlays only.
imagery: Product UI.
iconography: Small consistent line icons.
motion: Snappy, short, spatially consistent; optimistic updates.
interaction: Keyboard navigation, command palette, drag reorder, inline editing, undo.
recommended_effects: [effect.shadow]
avoid_effects: [effect.glow, effect.particles, effect.holographic, effect.mesh-gradient, effect.shader]
recommended_motion: [motion.m2-command-palette, motion.m3-animated-reorder, motion.m1-checkbox, motion.m3-list-to-detail]
density: [medium, high]
accessibility_notes: Shortcuts must not override assistive technology keys; all drag actions need keyboard alternatives.
responsive_behavior: Panes collapse into navigation stack on mobile.
good_for: Task managers, notes, email, calendars, knowledge tools.
avoid_when: Brand campaigns and immersive marketing.
compatible_patterns: [layout.app-sidebar-workspace, layout.app-command-driven, layout.app-inbox, layout.app-master-detail]
compatible_styles: [style.minimal, style.developer-tool, style.ai-native, style.data-dense]
implementation_notes: Speed perception comes from optimistic updates and short durations.
domains: [productivity, saas, developer, ai]
conveys: [efficient, calm, clean, precise]
perceived_risks: [sterile]
intensity: [1, 3]
contexts: [application, marketing]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.ecommerce-premium
name: Premium e-commerce
kind: style
category: product
family: commerce
character: Desirable, confident, easy to buy; product photography leads.
visual_language: Large product imagery, restrained UI, clear price and options, generous product pages.
layout: Editorial collection pages, product detail with gallery and sticky purchase panel.
typography: Refined sans or serif display, highly legible UI text, clear prices.
color_behavior: Neutral canvas so products carry color; one action color.
surface: Minimal; product imagery as surface.
borders: Hairlines in option selectors.
shadows: Contact shadows on product cut-outs only.
imagery: Consistent studio and lifestyle photography.
iconography: Minimal, functional.
motion: Gallery transitions, zoom, add-to-bag feedback; calm elsewhere.
interaction: Variant selection, zoom, quick view, cart drawer.
recommended_effects: [effect.contact-shadow, effect.mask, effect.reflection]
avoid_effects: [effect.glow, effect.particles, effect.chromatic, effect.holographic, effect.glass]
recommended_motion: [motion.m3-thumbnail-to-fullscreen, motion.m2-drawer, motion.m1-success, motion.m2-carousel]
density: [low, medium]
accessibility_notes: Variant swatches need text labels; zoom must be keyboard accessible.
responsive_behavior: Mobile-first gallery swipe; sticky add-to-bag bar on mobile.
good_for: Fashion, beauty, furniture, premium consumer goods.
avoid_when: Catalog-scale marketplaces needing density.
compatible_patterns: [layout.grid-editorial, layout.grid-masonry, layout.hero-full-bleed, layout.story-before-after]
compatible_styles: [style.luxury, style.editorial, style.minimal]
implementation_notes: Image performance (responsive srcset, AVIF/WebP, aspect-ratio) is the core engineering task.
domains: [ecommerce, fashion, luxury, consumer]
conveys: [premium, crafted, confident, clean]
perceived_risks: [cold]
intensity: [2, 3]
contexts: [commerce, marketing]
motion_ceiling: M4
default_tell: false
```
