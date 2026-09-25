# Restrained and editorial styles

```yaml
id: style.minimal
name: Minimal
kind: style
category: restrained
family: restrained
character: Calm, focused, honest; the interface disappears behind the task or message.
visual_language: Few elements per view, strong alignment, generous but purposeful whitespace, one accent.
layout: Single column or simple split; content-width containers; few sections.
typography: One family; hierarchy through size and weight only; excellent body readability.
color_behavior: Near-monochrome neutrals with one functional accent reserved for primary action and links.
surface: Whitespace and dividers instead of cards; one surface level plus overlays.
borders: Hairline dividers only where grouping needs them.
shadows: None except overlays.
imagery: Optional; small product UI or none.
iconography: Sparse line icons, labelled.
motion: Feedback-only micro motion; short fades.
interaction: Direct, predictable; no hidden gestures.
recommended_effects: [effect.shadow]
avoid_effects: [effect.glow, effect.mesh-gradient, effect.particles, effect.holographic, effect.chromatic]
recommended_motion: [motion.m1-hover, motion.m1-press, motion.fade]
density: [low, medium]
accessibility_notes: Low-contrast grey text is the main risk; keep secondary text at AA.
responsive_behavior: Collapses naturally; keep line length and spacing proportional on mobile.
good_for: Utilities, single-purpose tools, waitlists, documentation-light products.
avoid_when: The product needs breadth, emotional storytelling, or dense operational data.
compatible_patterns: [layout.hero-centered, layout.story-alternating, layout.app-sidebar-workspace]
compatible_styles: [style.swiss, style.monochrome, style.editorial, style.productivity]
implementation_notes: Most of the character comes from spacing and type tokens; resist adding decoration to fill space.
domains: [productivity, developer, saas, consumer, portfolio]
conveys: [minimal, calm, clean, precise, trustworthy]
perceived_risks: [sterile, generic]
intensity: [1, 2]
contexts: [marketing, application, content]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.swiss
name: Swiss / International
kind: style
category: restrained
family: restrained
character: Objective, rational, confident; grid and typography carry all meaning.
visual_language: Visible modular grid, flush-left ragged-right text, large grotesk headlines, asymmetric balance.
layout: Strict 12-column grid with deliberate asymmetric placement; strong horizontal rules.
typography: Neo-grotesk, large size contrast, tight tracking on display, numbered sections.
color_behavior: Black/white/paper plus one strong primary color used in blocks.
surface: Flat planes; color blocks as sections; no cards.
borders: Thick and thin rules as structure.
shadows: None.
imagery: Cropped photography or diagrams aligned to the grid.
iconography: Minimal, geometric, or replaced by numerals and arrows.
motion: Precise, linear-ish slides along the grid axis; no bounce.
interaction: Underline and color inversion on hover; clear focus rules.
recommended_effects: [effect.clipping, effect.mask]
avoid_effects: [effect.glass, effect.glow, effect.mesh-gradient, effect.shadow, effect.backdrop-blur]
recommended_motion: [motion.m1-hover, motion.slide, motion.clip-reveal, motion.m4-scroll-reveal]
density: [medium, high]
accessibility_notes: Color blocks must keep text contrast; rules must not be the only grouping cue for screen readers.
responsive_behavior: Grid collapses 12 to 6 to 4 columns while keeping the asymmetric offsets.
good_for: Design studios, cultural institutions, technical documentation brands, editorial products.
avoid_when: The brand must feel soft, playful, or warm.
compatible_patterns: [layout.grid-editorial, layout.grid-broken, layout.hero-asymmetric, layout.story-timeline]
compatible_styles: [style.minimal, style.editorial, style.monochrome, style.developer-tool]
implementation_notes: CSS grid with named lines; type scale ratio of 1.333 or more; avoid radius.
domains: [creative, agency, editorial, developer, portfolio, public-sector]
conveys: [precise, confident, serious, crafted, timeless]
perceived_risks: [cold, sterile]
intensity: [1, 3]
contexts: [marketing, content]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.editorial
name: Editorial
kind: style
category: restrained
family: editorial
character: Authored, thoughtful, intelligent; reads like a publication.
visual_language: Typography-led hierarchy, asymmetric columns, captions and pull quotes, image and text in dialogue.
layout: Reading column with media breakouts; magazine-like section openers.
typography: Serif or characterful display with a highly readable text face; italic has a job.
color_behavior: Paper or ink neutrals; accent rare (links, marks).
surface: Almost no containers; rules and whitespace define groups.
borders: Fine rules between sections and in tables of contents.
shadows: None.
imagery: Editorial photography or illustration with captions and credits.
iconography: Rare; text labels preferred.
motion: Minimal-soft; reading is protected; rare headline reveal.
interaction: Underlined links, footnote popovers, reading progress.
recommended_effects: [effect.grain, effect.mask]
avoid_effects: [effect.glow, effect.glass, effect.particles, effect.holographic, effect.mesh-gradient]
recommended_motion: [motion.fade, motion.text-line-reveal, motion.m4-image-mask-reveal, motion.m4-scroll-progress]
density: [medium]
accessibility_notes: Maintain 55-75ch measure, body at least 17px, real heading structure for long reads.
responsive_behavior: Asymmetry becomes crop and offset on mobile; captions stay attached to images.
good_for: Publishing, knowledge products, newsletters, journals, documentation brands.
avoid_when: Operational dashboards, dense commerce, products without substantive content.
compatible_patterns: [layout.hero-editorial, layout.grid-editorial, layout.grid-magazine, layout.story-scroll]
compatible_styles: [style.swiss, style.luxury, style.minimal, style.organic]
implementation_notes: Pair with Typography Intelligence editorial archetype; use text-wrap balance for headlines.
domains: [editorial, media, portfolio, education, luxury]
conveys: [editorial, crafted, calm, human, timeless]
perceived_risks: [dated]
intensity: [1, 3]
contexts: [content, marketing]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.monochrome
name: Monochrome
kind: style
category: restrained
family: restrained
character: Stark, disciplined, focused; contrast instead of color.
visual_language: Black/white or single-hue scale, hairline grids, inverse sections for emphasis.
layout: Centered or strict grid; visible hairline structure optional.
typography: Grotesk plus mono accents; very strong size contrast.
color_behavior: No brand hue or one functional status set; inversion marks emphasis.
surface: Flat panels separated by hairlines; inverse bands.
borders: One-pixel hairlines everywhere structure is needed.
shadows: None.
imagery: Grayscale or duotone; product UI in dark/light.
iconography: Monoline icons at one weight.
motion: Minimal-technical; crisp fades and slides.
interaction: Inversion on hover/active; keyboard hints.
recommended_effects: [effect.noise, effect.edge-highlight]
avoid_effects: [effect.mesh-gradient, effect.holographic, effect.chromatic, effect.gradient]
recommended_motion: [motion.m1-hover, motion.fade, motion.m2-tabs, motion.m4-scroll-reveal]
density: [medium, high]
accessibility_notes: Status cannot rely on color, which the style lacks; always pair text and shape.
responsive_behavior: Hairline grids simplify to stacked dividers.
good_for: Developer platforms, fashion, photography, architecture.
avoid_when: Products needing rich data color encoding or warmth.
compatible_patterns: [layout.hero-centered, layout.grid-card-matrix, layout.grid-asymmetric]
compatible_styles: [style.developer-tool, style.swiss, style.minimal, style.luxury]
implementation_notes: Tokenize a 10-step neutral scale; inverse sections swap tokens, not ad-hoc colors.
domains: [developer, fashion, portfolio, creative, hardware]
conveys: [precise, confident, minimal, bold, timeless]
perceived_risks: [cold, sterile]
intensity: [1, 3]
contexts: [marketing, application, content]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.luxury
name: Luxury
kind: style
category: restrained
family: editorial
character: Rare, refined, unhurried; restraint signals value.
visual_language: Very low density, long pauses of whitespace, art-directed imagery, refined serif display.
layout: Asymmetric editorial layouts, full-bleed imagery, centered brand mark navigation.
typography: High-contrast serif or refined sans; spaced small caps for labels; light weights checked for contrast.
color_behavior: Deep neutrals or ivory; one material-inspired accent; no bright semantics outside commerce feedback.
surface: None or near-none; hairlines.
borders: Hairline only.
shadows: None; depth from photography.
imagery: Art-directed photography showing material and texture.
iconography: Almost none.
motion: Slow, soft, cinematic transitions with long ease-out; very few moments.
interaction: Understated hover (underline, image shift); enquiry over urgency.
recommended_effects: [effect.grain, effect.mask, effect.reflection]
avoid_effects: [effect.glow, effect.particles, effect.holographic, effect.chromatic, effect.mesh-gradient]
recommended_motion: [motion.fade, motion.m4-image-mask-reveal, motion.m3-thumbnail-to-fullscreen, motion.m5-cinematic-hero]
density: [low]
accessibility_notes: Thin type and low-contrast ivory palettes often fail AA; verify every text size.
responsive_behavior: Keep whitespace ratio; art-direct crops per breakpoint.
good_for: Fashion, jewelry, hospitality, premium real estate, fine goods.
avoid_when: Speed, comparison, density or price-driven shopping.
compatible_patterns: [layout.hero-full-bleed, layout.hero-editorial, layout.grid-editorial, layout.story-scroll]
compatible_styles: [style.editorial, style.cinematic, style.monochrome, style.ecommerce-premium]
implementation_notes: Imagery quality decides the result; without it choose editorial or minimal instead.
domains: [luxury, fashion, travel, ecommerce]
conveys: [luxurious, exclusive, crafted, calm, timeless, premium]
perceived_risks: [cold, intimidating]
intensity: [1, 3]
contexts: [marketing, commerce, content]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.organic
name: Organic
kind: style
category: restrained
family: editorial
character: Warm, natural, human; soft forms and material honesty.
visual_language: Soft radii, natural palettes, textured backgrounds, hand-drawn or photographic nature cues.
layout: Relaxed grids with overlapping imagery; flowing section transitions.
typography: Humanist sans or soft serif; friendly weights.
color_behavior: Earth tones, muted greens, clay, cream; accent from nature.
surface: Tonal regions and soft-edged containers.
borders: Rare; soft tonal separation.
shadows: Soft and warm-tinted when used.
imagery: Natural photography, textures, illustration with visible hand.
iconography: Rounded, hand-drawn feel, consistent stroke.
motion: Soft easing, gentle drift, no mechanical snaps.
interaction: Gentle hover lifts and color warmth.
recommended_effects: [effect.grain, effect.noise, effect.shadow]
avoid_effects: [effect.chromatic, effect.holographic, effect.glow, effect.edge-highlight]
recommended_motion: [motion.fade-up, motion.m1-hover, motion.m4-scroll-reveal, motion.ambient-drift]
density: [low, medium]
accessibility_notes: Earth palettes easily lose contrast; test muted text on cream.
responsive_behavior: Overlaps flatten to stacked media on mobile.
good_for: Wellness, food, sustainability, education, healthcare consumer brands.
avoid_when: Technical infrastructure, trading, enterprise dashboards.
compatible_patterns: [layout.hero-split, layout.grid-masonry, layout.story-alternating]
compatible_styles: [style.editorial, style.tactile, style.playful]
implementation_notes: Grain via small tiled texture or SVG noise at low opacity; keep it static.
domains: [healthcare, consumer, education, travel, editorial]
conveys: [warm, organic, human, calm, approachable]
perceived_risks: [unserious]
intensity: [2, 3]
contexts: [marketing, content, commerce]
motion_ceiling: M4
default_tell: false
```
