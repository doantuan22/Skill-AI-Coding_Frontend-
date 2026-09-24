# Expressive styles

Expressive styles earn attention through deliberate rule-breaking. They need a brand that can carry them and still must pass readability, focus and contrast.

```yaml
id: style.neo-brutalism
name: Neo-brutalism
kind: style
category: expressive
family: expressive
character: Direct, energetic, honest; UI parts are visible and proud.
visual_language: Thick black outlines, flat saturated fills, hard offset shadows, chunky type, visible structure.
layout: Blocky grid, stacked cards with hard edges, clear sections.
typography: Heavy grotesk or geometric sans; big labels; mono accents.
color_behavior: Flat saturated palette (3-4 hues) on off-white; high contrast.
surface: Outlined blocks with solid fills.
borders: 2-3px solid dark borders on interactive and grouped elements.
shadows: Hard offset shadow with zero blur.
imagery: Flat illustration, stickers, cut-out photos.
iconography: Bold filled or thick-stroke icons.
motion: Snappy translate on press (shadow collapses), quick bounces kept short.
interaction: Press moves element into its shadow; strong hover color swaps.
recommended_effects: [effect.shadow, effect.clipping]
avoid_effects: [effect.glass, effect.backdrop-blur, effect.glow, effect.mesh-gradient, effect.specular-highlight]
recommended_motion: [motion.m1-press, motion.m1-hover, motion.m1-toggle, motion.m2-dropdown]
density: [medium]
accessibility_notes: Saturated fills behind text need contrast checks; ensure focus ring is distinct from the border style.
responsive_behavior: Borders and offsets scale down slightly; keep hit areas large.
good_for: Indie products, creator tools, startups with bold voice, education for young adults.
avoid_when: Finance, healthcare, enterprise buyers, luxury.
compatible_patterns: [layout.grid-bento, layout.grid-card-matrix, layout.hero-asymmetric]
compatible_styles: [style.playful, style.brutalist, style.y2k]
implementation_notes: Tokenize border width and shadow offset; press state translates by the shadow offset.
domains: [consumer, creative, education, productivity, music]
conveys: [bold, playful, energetic, raw, approachable]
perceived_risks: [loud, unserious, childish]
intensity: [3, 5]
contexts: [marketing, application]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.brutalist
name: Brutalist
kind: style
category: expressive
family: expressive
character: Raw, uncompromising, anti-polish; content and structure exposed.
visual_language: Default-looking elements used deliberately, system fonts, dense text, harsh contrast, visible HTML structure.
layout: Unbalanced grids, overlapping text, dense lists, unexpected scale.
typography: System or mono fonts, extreme sizes, underlines, uppercase blocks.
color_behavior: Pure black/white with one alarm color, or raw default blue links.
surface: None; raw page.
borders: Raw 1px borders, table-like structure.
shadows: None.
imagery: Unprocessed photos, screenshots, collage.
iconography: Text symbols instead of icons.
motion: Almost none; abrupt state changes are part of the voice.
interaction: Native controls, visible focus, plain links.
recommended_effects: [effect.clipping]
avoid_effects: [effect.glass, effect.glow, effect.shadow, effect.mesh-gradient, effect.particles, effect.backdrop-blur]
recommended_motion: [motion.m1-focus, motion.m1-hover]
density: [high]
accessibility_notes: Rawness is no excuse for broken semantics; native elements usually help accessibility.
responsive_behavior: Let content reflow; avoid fixed overlapping positions on mobile.
good_for: Art projects, manifestos, experimental portfolios, zines, music labels.
avoid_when: Commerce conversion, trust-sensitive or mainstream audiences.
compatible_patterns: [layout.grid-broken, layout.grid-dense-data, layout.hero-asymmetric]
compatible_styles: [style.experimental, style.neo-brutalism, style.monochrome]
implementation_notes: Keep CSS small; the style fails when half-polished.
domains: [creative, portfolio, music, agency, media]
conveys: [raw, rebellious, bold, experimental]
perceived_risks: [chaotic, unserious, intimidating]
intensity: [3, 5]
contexts: [marketing, content]
motion_ceiling: M2
default_tell: false
```

```yaml
id: style.y2k
name: Y2K
kind: style
category: expressive
family: expressive
character: Nostalgic, optimistic, glossy; early-2000s digital futurism.
visual_language: Chrome and iridescent surfaces, bubbly shapes, pixel or rounded type, star/sparkle motifs.
layout: Playful stacked panels, stickers, floating objects anchored by a clear content column.
typography: Rounded or wide display, pixel accents, bold weights.
color_behavior: Iridescent pastels, silver, electric blue and pink.
surface: Glossy panels with highlights.
borders: Rounded thick borders, bevels.
shadows: Soft colored shadows.
imagery: 3D chrome objects, retro devices, stickers.
iconography: Glossy or pixel icons, consistent family.
motion: Bouncy, sparkly, playful loops used sparingly.
interaction: Springy hovers, cursor trails only as opt-in toys.
recommended_effects: [effect.holographic, effect.specular-highlight, effect.reflection, effect.gradient]
avoid_effects: [effect.grain, effect.noise, effect.contact-shadow]
recommended_motion: [motion.m1-hover, motion.m1-press, motion.scale, motion.ambient-drift]
density: [low, medium]
accessibility_notes: Iridescent backgrounds make text unreadable; keep text on solid panels.
responsive_behavior: Drop floating decorations on mobile; keep the content column.
good_for: Music, fashion drops, youth brands, events, games-adjacent campaigns.
avoid_when: B2B software, finance, healthcare, long-term product UI.
compatible_patterns: [layout.hero-full-bleed, layout.grid-bento, layout.grid-broken]
compatible_styles: [style.retro-futurism, style.playful, style.neo-brutalism]
implementation_notes: Chrome looks best as pre-rendered assets; CSS gradients approximate but do not animate them constantly.
domains: [music, fashion, gaming, consumer, creative]
conveys: [nostalgic, playful, energetic, bold]
perceived_risks: [dated, gimmicky, loud]
intensity: [4, 5]
contexts: [marketing]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.playful
name: Playful
kind: style
category: expressive
family: expressive
character: Friendly, delightful, approachable; personality in details.
visual_language: Rounded shapes, bright but controlled palette, illustration, characterful microinteractions.
layout: Friendly grids, illustration-led sections, generous spacing.
typography: Rounded or geometric sans, bold headings, short copy.
color_behavior: Several bright hues assigned to roles, on light backgrounds; one primary action color.
surface: Rounded containers, tonal backgrounds.
borders: Soft or none.
shadows: Soft, low.
imagery: Illustration and mascots with one consistent style.
iconography: Rounded, friendly, filled or duotone.
motion: Springy but short; celebratory success moments.
interaction: Delightful feedback (confetti only on real milestones), tactile toggles.
recommended_effects: [effect.shadow, effect.gradient]
avoid_effects: [effect.chromatic, effect.distortion, effect.glass]
recommended_motion: [motion.m1-press, motion.m1-toggle, motion.m1-success, motion.m1-checkbox, motion.m2-card-expansion]
density: [low, medium]
accessibility_notes: Celebrations must respect reduced motion; avoid color-only role coding.
responsive_behavior: Illustrations scale or swap to smaller variants; keep touch targets large.
good_for: Consumer apps, education, habit trackers, family products.
avoid_when: Serious financial, legal, medical or enterprise contexts.
compatible_patterns: [layout.hero-product, layout.grid-bento, layout.story-alternating]
compatible_styles: [style.neo-brutalism, style.tactile, style.organic]
implementation_notes: Spring presets live in motion tokens; limit celebration animations to one per flow.
domains: [consumer, education, productivity, gaming]
conveys: [playful, friendly, approachable, energetic, warm]
perceived_risks: [childish, unserious]
intensity: [3, 4]
contexts: [marketing, application]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.experimental
name: Experimental
kind: style
category: expressive
family: expressive
character: Surprising, authored, boundary-pushing; the interface is part of the work.
visual_language: Unconventional navigation, oversized or distorted type, generative visuals, interaction as content.
layout: Non-standard grids, canvas-like pages, horizontal or spatial movement.
typography: Variable fonts pushed to extremes, kinetic type.
color_behavior: Author-defined; often monochrome base with bursts.
surface: Canvas or full-bleed media.
borders: Rare.
shadows: Rare.
imagery: Generative graphics, video, 3D.
iconography: Custom or none.
motion: Expressive and interactive; motion carries meaning.
interaction: Cursor, scroll and drag as primary expression; always with an accessible path.
recommended_effects: [effect.shader, effect.distortion, effect.particles, effect.noise]
avoid_effects: [effect.glass, effect.backdrop-blur]
recommended_motion: [motion.m5-cursor-reactive-scene, motion.m5-interactive-shader, motion.text-character-reveal, motion.m4-horizontal-scroll]
density: [low]
accessibility_notes: Provide a plain, navigable index of all content; pause controls; no seizure-risk flashes.
responsive_behavior: Mobile gets a simplified linear version with the same content.
good_for: Portfolios, art direction, festivals, creative technologists.
avoid_when: Task-based products, conversion funnels, anything needing speed.
compatible_patterns: [layout.hero-interactive, layout.grid-broken, layout.story-scroll]
compatible_styles: [style.brutalist, style.creative-agency, style.cyberpunk]
implementation_notes: Build the accessible content page first, then layer the experience on top.
domains: [portfolio, creative, agency, music, media]
conveys: [experimental, innovative, bold, immersive]
perceived_risks: [chaotic, gimmicky, heavy]
intensity: [4, 5]
contexts: [marketing, content]
motion_ceiling: M5
default_tell: false
```

```yaml
id: style.creative-agency
name: Creative agency
kind: style
category: expressive
family: expressive
character: Confident, crafted, memorable; case studies as proof of taste.
visual_language: Oversized type, full-bleed work, smooth transitions between projects, cursor-aware details.
layout: Case-study narratives, project index, asymmetric grids.
typography: Big expressive display (condensed or serif), quiet body.
color_behavior: Monochrome base; work provides color.
surface: Media edges define structure.
borders: Rare hairlines in indexes.
shadows: None.
imagery: Project imagery and video at large scale.
iconography: Minimal.
motion: Expressive-controlled; page transitions, image reveals, cursor labels.
interaction: Hover previews on project lists, drag galleries with visible controls.
recommended_effects: [effect.mask, effect.clipping, effect.grain]
avoid_effects: [effect.glass, effect.holographic, effect.glow]
recommended_motion: [motion.m3-cross-page-continuity, motion.m4-image-mask-reveal, motion.text-line-reveal, motion.m3-thumbnail-to-fullscreen]
density: [low, medium]
accessibility_notes: Hover previews need keyboard and touch equivalents; custom cursors must not hide the native one for precision tasks.
responsive_behavior: Hover previews become inline thumbnails; page transitions simplify to fades.
good_for: Agencies, studios, designers, production companies.
avoid_when: Products whose users need to do tasks quickly.
compatible_patterns: [layout.hero-full-bleed, layout.grid-asymmetric, layout.grid-masonry, layout.story-scroll]
compatible_styles: [style.editorial, style.experimental, style.cinematic, style.swiss]
implementation_notes: View Transitions for page continuity where supported; keep projects crawlable.
domains: [agency, creative, portfolio, media]
conveys: [crafted, confident, bold, innovative, premium]
perceived_risks: [heavy, flashy]
intensity: [3, 5]
contexts: [marketing, content]
motion_ceiling: M5
default_tell: false
```

```yaml
id: style.retro-futurism
name: Retro-futurism
kind: style
category: expressive
family: futuristic
character: Nostalgic optimism about the future; analog warmth meets sci-fi.
visual_language: Chrome, grids to the horizon, sunset gradients, space-age typography, CRT textures.
layout: Poster-like heroes, framed panels, console-like modules.
typography: Wide or rounded display, techno accents, mono readouts.
color_behavior: Warm sunset gradients, deep navy, orange and teal.
surface: Framed panels, bevels, scanline textures.
borders: Double or beveled frames.
shadows: Colored glows used as light sources, sparingly.
imagery: Retro product renders, space imagery, illustrations.
iconography: Pictograms with a technical feel.
motion: Scanline flickers only as rare accents; smooth parallax of horizon layers.
interaction: Console-like toggles and readouts.
recommended_effects: [effect.gradient, effect.grain, effect.glow, effect.specular-highlight]
avoid_effects: [effect.glass, effect.holographic]
recommended_motion: [motion.m4-parallax, motion.fade-up, motion.m1-toggle]
density: [low, medium]
accessibility_notes: Flicker effects must stay below 3 flashes per second and be disabled under reduced motion.
responsive_behavior: Parallax layers collapse to a static poster on mobile.
good_for: Games, music, events, space and automotive campaigns.
avoid_when: Enterprise, finance, healthcare.
compatible_patterns: [layout.hero-full-bleed, layout.hero-cinematic, layout.story-layered]
compatible_styles: [style.y2k, style.cyberpunk, style.cinematic]
implementation_notes: Textures as static images; glow reserved for one light source.
domains: [gaming, music, media, hardware]
conveys: [nostalgic, bold, futuristic, energetic]
perceived_risks: [dated, gimmicky]
intensity: [3, 5]
contexts: [marketing]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.cyberpunk
name: Cyberpunk
kind: style
category: expressive
family: futuristic
character: Dystopian, high-energy, dense; neon on darkness.
visual_language: Neon accents on near-black, glitch and scanline motifs, angular frames, HUD overlays.
layout: Dense HUD-like panels, angled cuts, overlapping data readouts.
typography: Condensed or techno display, mono data, uppercase labels.
color_behavior: Near-black base, one or two neon hues (magenta, cyan, acid yellow).
surface: Angular framed panels, clipped corners.
borders: Neon strokes, clipped corner frames.
shadows: Neon glow as light.
imagery: Night cityscapes, 3D renders, glitched photography.
iconography: Angular HUD glyphs.
motion: Glitch transitions as rare punctuation; fast HUD readouts.
interaction: Terminal-like typing, hover glitch micro effects.
recommended_effects: [effect.glow, effect.chromatic, effect.clipping, effect.noise, effect.distortion]
avoid_effects: [effect.grain, effect.contact-shadow]
recommended_motion: [motion.m1-hover, motion.text-character-reveal, motion.m5-webgl-transition]
density: [medium, high]
accessibility_notes: Glitch and flicker are seizure and vestibular risks; neon on black needs contrast checks for small text.
responsive_behavior: Remove overlays and glitch effects on mobile; keep readable panels.
good_for: Games, esports, music, security-themed campaigns.
avoid_when: Mainstream SaaS, finance, healthcare, anything needing calm trust.
compatible_patterns: [layout.hero-cinematic, layout.grid-dense-data, layout.hero-full-bleed]
compatible_styles: [style.futuristic, style.retro-futurism, style.experimental]
implementation_notes: Implement glitch with clip-path steps on a copy, time-boxed; never loop indefinitely.
domains: [gaming, music, media]
conveys: [bold, futuristic, rebellious, energetic, immersive]
perceived_risks: [flashy, noisy, chaotic, loud]
intensity: [4, 5]
contexts: [marketing]
motion_ceiling: M5
default_tell: false
```
