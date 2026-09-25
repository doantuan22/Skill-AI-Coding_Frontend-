# Composition recipes

Recipes are **worked examples of coherent design languages**: style + layout + typography + color + surface + effects + motion + interaction + technology. They give vocabulary and a starting composition; they are not templates. The Capability Resolver ranks recipes by domain and style overlap and uses the best match as an **anchor**, then keeps only the items that pass the project's own filters (content, intensity, budget, dependencies).

Every recipe states `avoid` (what would break its coherence) and `why` (the reasoning an agent should be able to repeat).

```yaml
id: recipe.premium-ai-saas
name: Premium AI SaaS
kind: recipe
category: saas
domains: [ai, saas]
conveys: [premium, futuristic, calm, technical, impressive]
styles: [style.calm-futurism, style.ai-native]
layouts: [layout.hero-dashboard, layout.story-pinned-demo, layout.story-feature-explorer, layout.grid-bento]
typography: Large neo-grotesk display with tight tracking; neutral body; mono only for model/tool output.
surface: Dark or graphite layered surfaces separated by tone and faint edge highlights.
color: Low-saturation neutrals with one desaturated accent reserved for AI presence and primary action.
effects: [effect.radial-lighting, effect.noise, effect.glow, effect.depth]
motion: [motion.fade-up, motion.m3-shared-element, motion.m4-parallax, motion.m4-product-walkthrough, motion.ambient-drift]
interactions: [interaction.press-feedback, interaction.command-palette, interaction.progressive-disclosure, interaction.hover-intent]
technology: [tech.css, tech.native-js, tech.view-transitions, tech.rive]
avoid: Rainbow gradients everywhere, constant floating cards, glow on every element, large motion on every section, sparkle icons as the only AI signal, purple-by-default.
why: The product's value is intelligence shown through real UI; calm lighting and restrained motion signal confidence, while one walkthrough proves capability instead of claiming it.
```

```yaml
id: recipe.premium-saas
name: Premium SaaS (non-AI)
kind: recipe
category: saas
domains: [saas, productivity]
conveys: [clean, trustworthy, efficient, premium]
styles: [style.modern-saas, style.minimal]
layouts: [layout.hero-dashboard, layout.story-alternating, layout.story-feature-explorer, layout.story-comparison]
typography: Neutral sans with medium display contrast; excellent body readability.
surface: Light neutral base; framed UI previews with hairlines.
color: One brand accent for action; neutral everywhere else.
effects: [effect.shadow, effect.gradient]
motion: [motion.fade-up, motion.m2-tabs, motion.m4-scroll-reveal]
interactions: [interaction.press-feedback, interaction.progressive-disclosure, interaction.keyboard-navigation]
technology: [tech.css, tech.native-js]
avoid: Three equal icon cards, fake dashboards, gradient CTAs, testimonial carousels of anonymous quotes.
why: Buyers evaluate credibility and fit; real UI with alternating explanation and honest comparison persuades more than decoration.
```

```yaml
id: recipe.developer-tool
name: Developer tool
kind: recipe
category: developer
domains: [developer, data-platform]
conveys: [precise, technical, efficient, trustworthy]
styles: [style.developer-tool, style.monochrome]
layouts: [layout.hero-centered, layout.story-feature-explorer, layout.story-comparison, layout.app-sidebar-workspace]
typography: Neutral grotesk plus monospace for commands, code and identifiers; modest display scale.
surface: Flat panels, code blocks, hairline grid.
color: Monochrome or dark neutral with functional accents (links, status, syntax).
effects: [effect.noise, effect.edge-highlight]
motion: [motion.m1-button-feedback, motion.m2-tabs, motion.m2-command-palette]
interactions: [interaction.keyboard-navigation, interaction.command-palette, interaction.shortcut-discovery, interaction.press-feedback]
technology: [tech.css, tech.native-js]
avoid: Cinematic heroes, parallax, glassmorphism, luxury serif, marketing fluff without code.
why: Developers trust evidence and speed; code, commands and docs near every claim with snappy minimal motion match how they evaluate tools.
```

```yaml
id: recipe.enterprise-dashboard
name: Enterprise dashboard
kind: recipe
category: application
domains: [enterprise, analytics, saas]
conveys: [trustworthy, efficient, serious, dense]
styles: [style.enterprise-saas, style.data-dense]
layouts: [layout.app-dashboard-shell, layout.grid-dashboard, layout.grid-dense-data, layout.app-master-detail]
typography: Neutral sans with tabular numerals; compact scale.
surface: Panels and dividers; overlays are the only elevated layer.
color: Neutral UI; color reserved for data encoding and status.
effects: [effect.shadow]
motion: [motion.m1-skeleton, motion.m2-filter-transition, motion.m2-drawer]
interactions: [interaction.keyboard-navigation, interaction.multi-select, interaction.progressive-disclosure, interaction.undo]
technology: [tech.css, tech.native-js]
avoid: Cinematic or WebGL effects, gradients, glass, entrance animations, decorative charts.
why: Operators return daily for decisions; density, predictability and keyboard efficiency matter more than first impressions.
```

```yaml
id: recipe.luxury-commerce
name: Luxury commerce
kind: recipe
category: commerce
domains: [luxury, fashion, ecommerce]
conveys: [luxurious, exclusive, crafted, timeless]
styles: [style.luxury, style.ecommerce-premium]
layouts: [layout.hero-full-bleed, layout.grid-editorial, layout.grid-asymmetric, layout.story-scroll]
typography: Refined high-contrast serif display with spaced small-caps labels; legible sans for commerce UI.
surface: No containers; imagery and whitespace carry structure.
color: Deep neutrals or ivory with one material accent.
effects: [effect.grain, effect.mask, effect.contact-shadow]
motion: [motion.fade, motion.m4-image-mask-reveal, motion.m3-thumbnail-to-fullscreen]
interactions: [interaction.hover-preview, interaction.press-feedback, interaction.keyboard-navigation]
technology: [tech.css, tech.view-transitions]
avoid: Urgency badges, dense grids, bright semantic colors, bouncy motion, glow.
why: Rarity is expressed through restraint and craft; slow, few, precise moments make each product feel considered.
```

```yaml
id: recipe.creative-agency
name: Creative agency
kind: recipe
category: portfolio
domains: [agency, creative, portfolio]
conveys: [crafted, confident, bold, innovative]
styles: [style.creative-agency, style.swiss]
layouts: [layout.hero-asymmetric, layout.grid-asymmetric, layout.grid-masonry, layout.story-scroll]
typography: Oversized expressive display (condensed or serif) with quiet body.
surface: Media edges define structure; monochrome base.
color: Monochrome; the work provides color.
effects: [effect.mask, effect.clipping, effect.grain]
motion: [motion.m3-cross-page-continuity, motion.m4-image-mask-reveal, motion.text-line-reveal]
interactions: [interaction.hover-preview, interaction.cursor-follow, interaction.magnetic]
technology: [tech.css, tech.view-transitions, tech.native-js]
avoid: Template-like feature grids, stock imagery, effects that compete with the work.
why: The site is itself a portfolio piece; confident type and seamless transitions demonstrate taste while the work stays the hero.
```

```yaml
id: recipe.fintech-app
name: Fintech app
kind: recipe
category: application
domains: [fintech, consumer]
conveys: [trustworthy, precise, calm, clean]
styles: [style.fintech, style.data-dense]
layouts: [layout.app-dashboard-shell, layout.grid-dashboard, layout.app-master-detail]
typography: Neutral sans with excellent tabular numerals; large balances.
surface: Clean account cards, restrained elevation.
color: Calm neutral with a trustworthy accent; gains and losses semantic but not garish.
effects: [effect.shadow]
motion: [motion.text-counter, motion.m1-success, motion.m1-progress, motion.m2-modal]
interactions: [interaction.focus-management, interaction.progressive-disclosure, interaction.keyboard-navigation]
technology: [tech.css, tech.native-js]
avoid: Playful bounce on money, chromatic or glitch effects, red/green only status, fake urgency.
why: Money requires confidence; precise numbers, explicit confirmations and calm motion reduce anxiety.
```

```yaml
id: recipe.ecommerce-premium
name: Premium e-commerce
kind: recipe
category: commerce
domains: [ecommerce, consumer, fashion]
conveys: [premium, confident, clean, crafted]
styles: [style.ecommerce-premium, style.minimal]
layouts: [layout.grid-card-matrix, layout.grid-editorial, layout.story-before-after, layout.hero-full-bleed]
typography: Refined sans with clear price typography.
surface: Minimal; product photography as surface.
color: Neutral canvas; one action color.
effects: [effect.contact-shadow, effect.mask]
motion: [motion.m3-thumbnail-to-fullscreen, motion.m2-drawer, motion.m1-success, motion.m2-filter-transition]
interactions: [interaction.hover-preview, interaction.press-feedback, interaction.keyboard-navigation]
technology: [tech.css, tech.view-transitions]
avoid: Badge overload, carousels hiding products, heavy motion on listing pages.
why: Desire comes from product imagery and frictionless buying; motion is limited to gallery continuity and cart feedback.
```

```yaml
id: recipe.productivity-app
name: Productivity app
kind: recipe
category: application
domains: [productivity, saas]
conveys: [efficient, calm, clean, precise]
styles: [style.productivity, style.minimal]
layouts: [layout.app-sidebar-workspace, layout.app-command-driven, layout.app-inbox, layout.app-master-detail]
typography: Neutral compact sans; mono for shortcuts.
surface: Flat panes with dividers.
color: Neutral with one focus accent.
effects: [effect.shadow]
motion: [motion.m2-command-palette, motion.m3-animated-reorder, motion.m1-checkbox, motion.m3-list-to-detail]
interactions: [interaction.command-palette, interaction.keyboard-navigation, interaction.optimistic-update, interaction.undo, interaction.reorder]
technology: [tech.css, tech.native-js, tech.waapi]
avoid: Decorative gradients, slow transitions, confirmation dialogs where undo suffices.
why: Perceived speed is the brand; optimistic updates and keyboard paths matter more than visual flourish.
```

```yaml
id: recipe.experimental-portfolio
name: Experimental portfolio
kind: recipe
category: portfolio
domains: [portfolio, creative, music]
conveys: [experimental, innovative, bold, immersive]
styles: [style.experimental, style.brutalist]
layouts: [layout.hero-asymmetric, layout.grid-broken, layout.story-scroll]
typography: Variable fonts pushed to extremes for display; plain readable body.
surface: Canvas-like full-bleed pages.
color: Monochrome base with authored bursts.
effects: [effect.shader, effect.distortion, effect.noise]
motion: [motion.m5-cursor-reactive-scene, motion.m5-interactive-shader, motion.text-character-reveal, motion.m4-horizontal-scroll]
interactions: [interaction.cursor-follow, interaction.drag, interaction.hover-preview]
technology: [tech.webgl, tech.native-js, tech.css]
avoid: Inaccessible-only navigation, no content index, effects without a static path.
why: The experience is the work; experimentation is justified because the audience came to be surprised, and a plain index keeps it accessible.
```

```yaml
id: recipe.data-platform
name: Data platform
kind: recipe
category: developer
domains: [data-platform, developer, enterprise]
conveys: [technical, precise, trustworthy, serious]
styles: [style.monochrome, style.developer-tool]
layouts: [layout.hero-dashboard, layout.story-layered, layout.story-comparison, layout.grid-dense-data]
typography: Grotesk with mono for specs and queries; strong heading hierarchy.
surface: Diagrams, spec panels, bordered tables.
color: Monochrome with a limited functional diagram palette.
effects: [effect.noise, effect.edge-highlight]
motion: [motion.m4-layered-depth, motion.fade-up, motion.m2-tabs]
interactions: [interaction.progressive-disclosure, interaction.keyboard-navigation]
technology: [tech.css, tech.native-js, tech.svg]
avoid: Particles as data metaphors without data, playful motion, vague architecture claims.
why: Evaluators need architecture, specs and proof; layered diagrams explain depth without spectacle.
```

```yaml
id: recipe.consumer-app
name: Consumer app
kind: recipe
category: consumer
domains: [consumer, education, productivity]
conveys: [friendly, playful, approachable, warm]
styles: [style.playful, style.tactile]
layouts: [layout.hero-product, layout.story-alternating, layout.grid-bento]
typography: Rounded or geometric sans with bold headings and short copy.
surface: Rounded tonal containers.
color: Bright controlled palette with one primary action color.
effects: [effect.shadow, effect.gradient]
motion: [motion.m1-press, motion.m1-toggle, motion.m1-success, motion.m2-card-expansion]
interactions: [interaction.press-feedback, interaction.swipe-action, interaction.long-press]
technology: [tech.css, tech.rive]
avoid: Celebrations on every tap, childish tone for adult audiences, gesture-only actions.
why: Everyday delight builds habit; tactile feedback and one well-crafted interactive illustration create personality.
```

```yaml
id: recipe.hardware-launch
name: Hardware launch
kind: recipe
category: marketing
domains: [hardware, consumer]
conveys: [cinematic, premium, impressive, immersive]
styles: [style.cinematic, style.spatial]
layouts: [layout.hero-cinematic, layout.story-pinned-demo, layout.story-layered, layout.story-comparison]
typography: Large display with tight tracking and short lines; restrained body; tabular specs.
surface: Scenes, not cards; full-width tonal bands.
color: Dark or pure light stages; color comes from product and lighting.
effects: [effect.radial-lighting, effect.spotlight, effect.contact-shadow, effect.depth]
motion: [motion.m5-cinematic-hero, motion.m5-3d-sequence, motion.m4-pinned-section, motion.m4-zoom-through]
interactions: [interaction.press-feedback, interaction.keyboard-navigation]
technology: [tech.css, tech.gsap, tech.threejs, tech.canvas]
avoid: More than one pinned sequence in a row, hiding price and specs, heavy media without posters.
why: A physical product sells through form and detail; one cinematic sequence reveals it while specs remain accessible.
```

```yaml
id: recipe.editorial-publication
name: Editorial publication
kind: recipe
category: content
domains: [editorial, media, education]
conveys: [editorial, crafted, calm, human]
styles: [style.editorial, style.swiss]
layouts: [layout.hero-editorial, layout.grid-editorial, layout.grid-magazine, layout.story-scroll]
typography: Serif display with a highly readable text face; 55-75ch measure.
surface: Almost no containers; rules and whitespace.
color: Paper and ink neutrals; rare accent.
effects: [effect.grain, effect.mask]
motion: [motion.text-line-reveal, motion.m4-scroll-progress, motion.m4-image-mask-reveal]
interactions: [interaction.progressive-disclosure, interaction.hover-preview, interaction.keyboard-navigation]
technology: [tech.css, tech.native-js]
avoid: Card-ified articles, cinematic scroll effects in reading, pop-ups interrupting reading.
why: Reading is the product; typography does the hierarchy work and motion stays out of the reader's way.
```

```yaml
id: recipe.travel-booking
name: Travel booking
kind: recipe
category: commerce
domains: [travel, marketplace]
conveys: [warm, trustworthy, approachable]
styles: [style.organic, style.ecommerce-premium]
layouts: [layout.hero-media-led, layout.grid-card-matrix, layout.story-comparison]
typography: Friendly sans with strong price typography.
surface: Search panel as hero object; result cards.
color: Warm neutrals; destination imagery provides color.
effects: [effect.shadow, effect.mask]
motion: [motion.m3-thumbnail-to-fullscreen, motion.m2-filter-transition, motion.m2-drawer]
interactions: [interaction.keyboard-navigation, interaction.hover-preview, interaction.press-feedback]
technology: [tech.css, tech.view-transitions]
avoid: Cinematic storytelling before search, fake scarcity, hiding cancellation policy.
why: Inspire first, then transact with confidence; the search object anchors the page and reassurance sits next to price.
```

```yaml
id: recipe.gaming-campaign
name: Gaming campaign
kind: recipe
category: marketing
domains: [gaming, music, media]
conveys: [bold, energetic, futuristic, immersive]
styles: [style.cyberpunk, style.retro-futurism]
layouts: [layout.hero-cinematic, layout.grid-broken, layout.story-layered]
typography: Condensed or techno display, mono data readouts.
surface: Angular clipped panels on near-black.
color: Near-black with one or two neon hues.
effects: [effect.glow, effect.chromatic, effect.clipping, effect.noise]
motion: [motion.m5-webgl-transition, motion.text-character-reveal, motion.m4-parallax]
interactions: [interaction.press-feedback, interaction.hover-intent]
technology: [tech.css, tech.webgl]
avoid: Endless glitch loops, flashing above safe thresholds, unreadable neon small text.
why: The audience expects spectacle; intensity is concentrated in a few scenes and kept readable and safe.
```
