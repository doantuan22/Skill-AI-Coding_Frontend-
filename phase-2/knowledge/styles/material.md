# Material and depth styles

These styles use simulated materials and depth. They are the most overused family in generated interfaces; every use needs a content or brand reason and a performance budget.

```yaml
id: style.glassmorphism
name: Glassmorphism
kind: style
category: material
family: material
character: Layered, airy, contemporary; content floats over a colorful or photographic backdrop.
visual_language: Frosted translucent panels, subtle light borders, vivid background behind the glass.
layout: Few floating panels over a meaningful background; not everything glass.
typography: Clean neo-grotesk; medium weights for legibility over blur.
color_behavior: Colorful background carries hue; panels are neutral translucency.
surface: Translucent panels with backdrop blur, max two glass levels.
borders: One-pixel light edge on glass panels.
shadows: Soft, low-opacity.
imagery: Photography or gradient fields that justify the glass.
iconography: Line or duotone icons on glass.
motion: Soft fades and scale for panels; background mostly static.
interaction: Panels brighten on hover; focus ring visible over blur.
recommended_effects: [effect.glass, effect.backdrop-blur, effect.edge-highlight]
avoid_effects: [effect.particles, effect.chromatic, effect.holographic]
recommended_motion: [motion.fade, motion.m2-modal, motion.m2-popover]
density: [low, medium]
accessibility_notes: Text over blur needs a solid enough tint (verify contrast on the busiest background region); support prefers-reduced-transparency.
responsive_behavior: Reduce blur radius or replace with solid tint on mobile and low-power devices.
good_for: Media players, OS-like overlays, visual consumer apps with a real backdrop.
avoid_when: Dense data, long text, plain white backgrounds where glass has nothing to show.
compatible_patterns: [layout.hero-full-bleed, layout.hero-product, layout.app-split-inspector]
compatible_styles: [style.spatial, style.liquid-glass, style.calm-futurism]
implementation_notes: backdrop-filter is expensive; limit glass layers per viewport to 2-3 and never animate blur.
domains: [consumer, media, music, travel]
conveys: [immersive, clean, futuristic, calm]
perceived_risks: [generic, fragile]
intensity: [2, 4]
contexts: [marketing, application]
motion_ceiling: M3
default_tell: true
```

```yaml
id: style.liquid-glass
name: Liquid glass
kind: style
category: material
family: material
character: Fluid, refractive, premium; surfaces behave like physical glass that bends light.
visual_language: Refraction at edges, specular highlights, adaptive tint, controls that morph between states.
layout: Content-first layouts with floating control layers.
typography: Clean sans with adaptive color over varying backgrounds.
color_behavior: Neutral with tint borrowed from content underneath.
surface: Refractive layers with specular edges; morphing containers.
borders: Implied by light, not strokes.
shadows: Very soft, adaptive.
imagery: Rich content under controls (photos, video, maps).
iconography: SF-like monoline icons with optical weight.
motion: Morphing, fluid, spring-based state changes.
interaction: Controls morph (button to menu), respond to press with fluid deformation.
recommended_effects: [effect.liquid, effect.specular-highlight, effect.backdrop-blur, effect.edge-highlight]
avoid_effects: [effect.grain, effect.noise, effect.particles]
recommended_motion: [motion.m3-navigation-morph, motion.m2-popover, motion.m1-press]
density: [low, medium]
accessibility_notes: Adaptive tint must keep contrast; honor reduced transparency and reduced motion by falling back to solid materials.
responsive_behavior: Refraction and morphs are touch-first; desktop keeps them subtle.
good_for: Media, maps, camera or photo apps, premium consumer interfaces.
avoid_when: Web contexts without the performance headroom, dense productivity data.
compatible_patterns: [layout.hero-product, layout.app-canvas, layout.hero-full-bleed]
compatible_styles: [style.glassmorphism, style.spatial, style.calm-futurism]
implementation_notes: True refraction needs WebGL or SVG displacement; a CSS approximation with blur and highlights is usually enough.
domains: [consumer, media, hardware, travel]
conveys: [premium, futuristic, immersive, tactile]
perceived_risks: [gimmicky, heavy]
intensity: [3, 4]
contexts: [marketing, application]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.bento
name: Bento
kind: style
category: material
family: material
character: Modular, scannable, product-showcase; many small proofs in one view.
visual_language: Grid of differently sized rounded tiles, each with one feature and a visual.
layout: Asymmetric tile grid where tile size encodes importance.
typography: Short tile titles, compact supporting text, neutral sans.
color_behavior: Neutral tiles with one or two accent tiles.
surface: Rounded tiles with subtle fill or border.
borders: Hairline or none.
shadows: Very soft or none.
imagery: Small product UI crops, icons with meaning, micro demos.
iconography: Consistent line family.
motion: Tile-level micro demos on hover or in view, low intensity.
interaction: Tiles may expand to detail.
recommended_effects: [effect.shadow, effect.gradient]
avoid_effects: [effect.glow, effect.particles, effect.holographic]
recommended_motion: [motion.m4-scroll-reveal, motion.m1-hover, motion.m2-card-expansion]
density: [medium]
accessibility_notes: Tile order in DOM must match reading order; interactive tiles need a single focus target.
responsive_behavior: Collapses to one or two columns; keep the importance order.
good_for: Summarizing many modular features with real visuals, product overviews, personal dashboards.
avoid_when: Features are not modular, lack visuals, or need sequence and explanation.
compatible_patterns: [layout.grid-bento, layout.hero-product, layout.grid-card-matrix]
compatible_styles: [style.modern-saas, style.playful, style.productivity]
implementation_notes: CSS grid with span-based areas; each tile needs one message.
domains: [saas, consumer, hardware, ai, productivity]
conveys: [clean, efficient, innovative]
perceived_risks: [generic]
intensity: [2, 4]
contexts: [marketing]
motion_ceiling: M3
default_tell: true
```

```yaml
id: style.tactile
name: Tactile
kind: style
category: material
family: material
character: Physical, satisfying, crafted; controls feel pressable.
visual_language: Soft depth, inner shadows, pressed states, material-like knobs and switches, subtle texture.
layout: Control-rich panels with clear grouping.
typography: Friendly geometric or humanist sans.
color_behavior: Soft neutrals with a single saturated control color.
surface: Raised and inset surfaces with consistent light direction.
borders: Implied by light and shadow.
shadows: Paired outer and inner shadows from one light source.
imagery: Product photography, device renders.
iconography: Filled icons with slight depth.
motion: Springy press and release, knob rotation, toggle travel.
interaction: Strong press feedback, haptic-like snaps, drag with resistance.
recommended_effects: [effect.inner-shadow, effect.shadow, effect.contact-shadow, effect.noise]
avoid_effects: [effect.glow, effect.chromatic, effect.holographic]
recommended_motion: [motion.m1-press, motion.m1-toggle, motion.m1-checkbox]
density: [low, medium]
accessibility_notes: Neumorphic low-contrast edges fail control boundary contrast; keep a 3:1 boundary.
responsive_behavior: Reduce shadow complexity on mobile; keep press feedback.
good_for: Audio tools, hardware companions, calculators, consumer controls.
avoid_when: Data-dense apps, content reading, enterprise tools.
compatible_patterns: [layout.hero-product, layout.app-split-inspector]
compatible_styles: [style.playful, style.organic, style.minimal]
implementation_notes: Tokenize light direction; press state inverts outer shadow into inner shadow.
domains: [hardware, music, consumer, productivity]
conveys: [tactile, crafted, friendly, premium]
perceived_risks: [dated]
intensity: [2, 3]
contexts: [application, marketing]
motion_ceiling: M3
default_tell: false
```

```yaml
id: style.spatial
name: Spatial
kind: style
category: material
family: material
character: Immersive, dimensional, calm; interface elements live in depth.
visual_language: Layered planes with parallax depth, soft light, glass-like panels, depth-based focus.
layout: Center-focused scenes with layered panels; depth encodes hierarchy.
typography: Large clean sans with optical sizing.
color_behavior: Environmental colors from imagery; neutral panels.
surface: Floating translucent planes at distinct depths.
borders: Light edges.
shadows: Soft depth shadows consistent with one light.
imagery: 3D renders, environments, video.
iconography: Monoline, optically sized.
motion: Camera-like depth movement, gentle parallax, focus shifts.
interaction: Hover lifts toward the viewer; focus brings a plane forward.
recommended_effects: [effect.depth, effect.layered-transparency, effect.backdrop-blur, effect.contact-shadow]
avoid_effects: [effect.chromatic, effect.grain, effect.holographic]
recommended_motion: [motion.m4-layered-depth, motion.m5-camera-motion, motion.m5-spatial-navigation, motion.m3-shared-element]
density: [low]
accessibility_notes: Depth motion is a vestibular trigger; reduced motion flattens to crossfades.
responsive_behavior: Flatten depth on mobile; keep layers as stacked sections.
good_for: XR products, hardware launches, immersive storytelling.
avoid_when: Task-heavy apps, text-heavy content, low-power audiences.
compatible_patterns: [layout.hero-cinematic, layout.story-layered, layout.story-pinned-demo]
compatible_styles: [style.cinematic, style.liquid-glass, style.glassmorphism, style.calm-futurism]
implementation_notes: Fake depth with transforms first; use Three.js only with real 3D assets.
domains: [hardware, gaming, media, ai]
conveys: [immersive, futuristic, premium, calm]
perceived_risks: [heavy, gimmicky]
intensity: [3, 5]
contexts: [marketing]
motion_ceiling: M5
default_tell: false
```

```yaml
id: style.gradient-heavy
name: Gradient-heavy
kind: style
category: material
family: material
character: Vibrant, energetic, modern; color fields are the brand signature.
visual_language: Large mesh or linear gradients as backgrounds and shapes; soft color transitions.
layout: Simple layouts that let color fields breathe.
typography: Bold sans, often white over color.
color_behavior: Multi-hue gradients as signature; UI elements neutral.
surface: Gradient bands and cards over neutral base.
borders: Rare.
shadows: Soft colored shadows sparingly.
imagery: Abstract gradient shapes, product UI on gradients.
iconography: White line icons on color.
motion: Slow gradient drift in one signature area only.
interaction: Standard feedback; no gradient on every hover.
recommended_effects: [effect.mesh-gradient, effect.gradient, effect.noise]
avoid_effects: [effect.glass, effect.particles, effect.chromatic]
recommended_motion: [motion.ambient-drift, motion.fade-up, motion.m1-hover]
density: [low, medium]
accessibility_notes: Text over gradients needs contrast at the lightest point of the gradient.
responsive_behavior: Static gradient on mobile; reduce size of animated fields.
good_for: Brand campaigns, consumer fintech launches, events, music.
avoid_when: Enterprise data, long reading, brands that already rely on photography.
compatible_patterns: [layout.hero-centered, layout.hero-split, layout.story-alternating]
compatible_styles: [style.modern-saas, style.playful, style.calm-futurism]
implementation_notes: Add subtle noise to prevent banding; animate background-position or a transformed layer, never repaint large filters.
domains: [consumer, fintech, music, media, saas]
conveys: [energetic, bold, innovative, friendly]
perceived_risks: [generic, flashy]
intensity: [3, 5]
contexts: [marketing]
motion_ceiling: M4
default_tell: true
```

```yaml
id: style.cinematic
name: Cinematic
kind: style
category: material
family: material
character: Dramatic, immersive, story-driven; the page behaves like a film sequence.
visual_language: Full-screen scenes, dramatic lighting, large type over media, deliberate pacing.
layout: Scene-by-scene sections, pinned sequences, full-bleed media.
typography: Large display with tight tracking, short lines.
color_behavior: Dark or high-contrast base; color comes from lighting and media.
surface: Scenes, not cards.
borders: None.
shadows: Lighting within media, not UI shadows.
imagery: Video, image sequences, 3D renders with lighting.
iconography: Minimal.
motion: One cinematic sequence per page, scroll-linked and scrubbable.
interaction: Scroll as the main input; clear skip and navigation.
recommended_effects: [effect.radial-lighting, effect.spotlight, effect.grain, effect.depth]
avoid_effects: [effect.glass, effect.holographic, effect.chromatic]
recommended_motion: [motion.m5-cinematic-hero, motion.m4-pinned-section, motion.m4-zoom-through, motion.m5-3d-sequence]
density: [low]
accessibility_notes: Provide static content equivalents and skip links past sequences; no autoplay audio.
responsive_behavior: Mobile gets poster frames and simple fades instead of pinned scrubbing.
good_for: Hardware launches, film and game marketing, premium brand stories.
avoid_when: Apps, documentation, commerce listings, low-bandwidth audiences.
compatible_patterns: [layout.hero-cinematic, layout.story-pinned-demo, layout.story-scroll, layout.hero-full-bleed]
compatible_styles: [style.luxury, style.spatial, style.calm-futurism, style.creative-agency]
implementation_notes: Pre-render sequences; lazy-load media; one HIGH motion region per page.
domains: [hardware, gaming, media, luxury, music]
conveys: [cinematic, immersive, premium, impressive]
perceived_risks: [heavy, flashy]
intensity: [3, 5]
contexts: [marketing]
motion_ceiling: M5
default_tell: false
```
