# Storytelling layouts

Layout mechanics for narratives. [storytelling-patterns.md](storytelling-patterns.md) chooses the *narrative* (problem → solution, capability → evidence...); these entries choose how it is *laid out and paced*. Use one high-intensity story layout per page at most.

```yaml
id: layout.story-sticky
name: Sticky story
kind: layout
category: storytelling
purpose: Keep one visual in place while 3-6 steps explain it.
anatomy: Sticky visual column plus scrolling step column.
hierarchy: Step text drives; visual reflects the active step.
grid_behavior: 5/7 split with the visual sticky.
responsive: Steps stacked with inline visuals on mobile.
content_requirements: [product-ui]
compatible_styles: [style.modern-saas, style.calm-futurism, style.developer-tool, style.ai-native]
compatible_motion: [motion.m4-sticky-reveal, motion.m2-tabs]
interactions: [interaction.keyboard-navigation]
accessibility: Each step readable as normal content; visual changes described in text.
implementation: position sticky plus IntersectionObserver on steps.
anti_patterns: One or two steps; long text inside the sticky column.
good_for: Workflows, how-it-works, feature sequences.
avoid_when: Steps do not change a shared visual.
contexts: [marketing, content]
density: [medium]
motion_cost: medium
default_tell: false
```

```yaml
id: layout.story-scroll
name: Scroll story (chapters)
kind: layout
category: storytelling
purpose: Tell a multi-chapter narrative with scroll as the timeline.
anatomy: Chapter openers, media scenes, text passages, transitions.
hierarchy: One idea per chapter.
grid_behavior: Full-width scenes alternating with reading columns.
responsive: Linear article with inline media on mobile.
content_requirements: [long-form, brand-photography]
compatible_styles: [style.editorial, style.cinematic, style.luxury, style.creative-agency, style.experimental]
compatible_motion: [motion.m4-scroll-storytelling, motion.m4-image-mask-reveal, motion.text-line-reveal]
interactions: [interaction.keyboard-navigation]
accessibility: Chapter navigation; skip links; reduced-motion linear article.
implementation: Native reveals first; scrubbed sequences only for one chapter.
anti_patterns: Story without real sequence; scroll hijacking.
good_for: Annual reports, brand stories, long-form features.
avoid_when: Users arrive with a task.
contexts: [marketing, content]
density: [low]
motion_cost: high
default_tell: false
```

```yaml
id: layout.story-pinned-demo
name: Pinned product demo
kind: layout
category: storytelling
purpose: Demonstrate the product while pinned, advancing with scroll or step controls.
anatomy: Pinned product frame, step captions, progress indicator, exit to action.
hierarchy: Product frame dominant; captions short.
grid_behavior: Full-width pinned stage.
responsive: Step list with static frames on mobile.
content_requirements: [product-ui]
compatible_styles: [style.calm-futurism, style.futuristic, style.spatial, style.cinematic, style.modern-saas]
compatible_motion: [motion.m4-product-walkthrough, motion.m4-pinned-section, motion.m3-shared-element]
interactions: [interaction.keyboard-navigation, interaction.press-feedback]
accessibility: Step controls as buttons; static alternative.
implementation: Prefer step controls plus IO; scroll pinning only if authorized tech allows.
anti_patterns: Long pinned distances; demo that hides key information.
good_for: AI products, SaaS walkthroughs, hardware software.
avoid_when: UI not ready.
contexts: [marketing]
density: [medium]
motion_cost: high
default_tell: false
```

```yaml
id: layout.story-alternating
name: Alternating feature
kind: layout
category: storytelling
purpose: Pace 3-5 substantial features with alternating text and visual.
anatomy: Rows of heading, short copy, real visual.
hierarchy: Each row one feature, one visual.
grid_behavior: 5/7 split alternating sides.
responsive: Text above visual, no alternation on mobile.
content_requirements: [product-ui]
compatible_styles: [style.modern-saas, style.organic, style.playful, style.minimal, style.gradient-heavy]
compatible_motion: [motion.fade-up, motion.m4-scroll-reveal]
interactions: [interaction.press-feedback]
accessibility: Headings per row.
implementation: CSS grid with order swap at breakpoints (visual order only; DOM text first).
anti_patterns: Icons instead of visuals; more than five rows.
good_for: SaaS and consumer feature explanations.
avoid_when: Features are small and many (use feature grid).
contexts: [marketing]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.story-layered
name: Layered feature
kind: layout
category: storytelling
purpose: Explain a system by revealing its layers.
anatomy: Layered diagram or product stack with callouts per layer.
hierarchy: Layer order equals conceptual order.
grid_behavior: Central diagram with side callouts.
responsive: Layers shown as a vertical list with small diagrams.
content_requirements: [illustrations]
compatible_styles: [style.futuristic, style.spatial, style.retro-futurism, style.calm-futurism]
compatible_motion: [motion.m4-layered-depth, motion.m5-3d-sequence]
interactions: [interaction.progressive-disclosure]
accessibility: Each layer described in text.
implementation: SVG layers with IO steps; 3D only with real assets.
anti_patterns: Layers without real structure.
good_for: Technical platforms, hardware internals, architecture.
avoid_when: Flat, simple products.
contexts: [marketing]
density: [medium]
motion_cost: medium
default_tell: false
```

```yaml
id: layout.story-feature-explorer
name: Interactive feature explorer
kind: layout
category: storytelling
purpose: Let users choose which capability to see in a shared visual area.
anatomy: Feature list or tabs plus a large visual area that switches.
hierarchy: Active feature highlighted; visual explains it.
grid_behavior: 4/8 split with list and visual.
responsive: Accordion with inline visuals on mobile.
content_requirements: [product-ui]
compatible_styles: [style.modern-saas, style.developer-tool, style.calm-futurism, style.ai-native]
compatible_motion: [motion.m2-tabs, motion.m3-shared-element]
interactions: [interaction.keyboard-navigation, interaction.progressive-disclosure]
accessibility: Tabs pattern or list of buttons with aria-controls.
implementation: Preload visuals; crossfade between states.
anti_patterns: Auto-rotation without pause; features unrelated to one visual.
good_for: SaaS, developer tools, AI products.
avoid_when: Features need sequential reading.
contexts: [marketing]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.story-timeline
name: Timeline
kind: layout
category: storytelling
purpose: Show progression over time (history, roadmap, process).
anatomy: Axis with dated entries, optional media.
hierarchy: Chronology; milestones emphasized.
grid_behavior: Vertical axis (or horizontal scroll with snap).
responsive: Vertical single-column on mobile.
content_requirements: []
compatible_styles: [style.swiss, style.editorial, style.enterprise-saas, style.minimal]
compatible_motion: [motion.m4-scroll-progress, motion.fade-up, motion.m4-horizontal-scroll]
interactions: [interaction.keyboard-navigation]
accessibility: Ordered list semantics.
implementation: Ordered list styled as timeline.
anti_patterns: Invented milestones; horizontal hijacked scroll.
good_for: Company history, changelogs, roadmaps, processes.
avoid_when: No real chronology.
contexts: [marketing, content]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.story-comparison
name: Comparison
kind: layout
category: storytelling
purpose: Support a choice between options honestly.
anatomy: Options side by side with real attributes; recommended option marked.
hierarchy: Differences emphasized over shared attributes.
grid_behavior: Table with sticky header or option columns.
responsive: Option cards or horizontally scrollable table.
content_requirements: []
compatible_styles: [style.developer-tool, style.enterprise-saas, style.modern-saas, style.fintech, style.cinematic]
compatible_motion: [motion.m2-accordion, motion.m2-tabs]
interactions: [interaction.progressive-disclosure, interaction.keyboard-navigation]
accessibility: Table semantics; check marks with text.
implementation: Real table; sticky header.
anti_patterns: Fabricated competitor claims; checkmark walls.
good_for: Pricing, alternatives, plan selection.
avoid_when: Only one option exists.
contexts: [marketing, commerce]
density: [medium, high]
motion_cost: low
default_tell: false
```

```yaml
id: layout.story-before-after
name: Before / after
kind: layout
category: storytelling
purpose: Prove impact by comparing the same subject without and with the product.
anatomy: Paired images or states with a slider or side-by-side view.
hierarchy: Outcome emphasized.
grid_behavior: Single frame with slider, or 6/6 pair.
responsive: Stacked pair or slider on touch.
content_requirements: [case-studies]
compatible_styles: [style.modern-saas, style.ecommerce-premium, style.fintech, style.organic]
compatible_motion: [motion.fade, motion.m1-hover]
interactions: [interaction.drag, interaction.keyboard-navigation]
accessibility: Slider keyboard operable with value text; results described in text.
implementation: Range input driving clip-path.
anti_patterns: Different framing between before and after; fake results.
good_for: Editing tools, optimization, renovation, performance improvements.
avoid_when: No honest pair exists.
contexts: [marketing, commerce]
density: [low]
motion_cost: low
default_tell: false
```
