# Futuristic and AI styles

The dark + purple gradient + glass + glow combination is the most common generated "tech" look. These entries separate three distinct futures so the resolver can choose one on purpose.

```yaml
id: style.futuristic
name: Futuristic
kind: style
category: futuristic
family: futuristic
character: Bold, high-tech, forward-looking; engineered spectacle.
visual_language: Dark stages, precise light, geometric structure, 3D or data-driven visuals, technical readouts.
layout: Hero scene plus technical capability sections; grid overlays.
typography: Wide or geometric display, mono readouts, uppercase micro labels.
color_behavior: Dark base, one electric accent, light used as color.
surface: Layered dark panels with edge light.
borders: Thin luminous strokes.
shadows: Light-based glow in one accent only.
imagery: 3D renders, technical visualizations, product in dramatic light.
iconography: Geometric line icons.
motion: Expressive hero, technical build-up of diagrams, scroll-linked reveals.
interaction: Cursor-aware lighting, precise hover states.
recommended_effects: [effect.radial-lighting, effect.edge-highlight, effect.glow, effect.shader, effect.depth]
avoid_effects: [effect.holographic, effect.grain, effect.chromatic]
recommended_motion: [motion.m5-cinematic-hero, motion.m4-layered-depth, motion.m4-scroll-storytelling, motion.m5-interactive-shader]
density: [low, medium]
accessibility_notes: Luminous thin strokes and small mono labels on dark need contrast verification.
responsive_behavior: Replace shaders and 3D with posters on mobile.
good_for: Hardware, robotics, space, automotive tech, deep-tech launches.
avoid_when: Calm productivity tools, trust-first finance, most B2B apps.
compatible_patterns: [layout.hero-cinematic, layout.story-layered, layout.story-pinned-demo, layout.hero-product]
compatible_styles: [style.cinematic, style.spatial, style.cyberpunk, style.calm-futurism]
implementation_notes: Keep one light source and one accent; shaders need a static fallback.
domains: [hardware, gaming, ai, media]
conveys: [futuristic, bold, impressive, innovative, technical]
perceived_risks: [flashy, cold, heavy]
intensity: [4, 5]
contexts: [marketing]
motion_ceiling: M5
default_tell: false
```

```yaml
id: style.calm-futurism
name: Calm futurism
kind: style
category: futuristic
family: futuristic
character: Quietly advanced, premium, precise; the future feels inevitable, not loud.
visual_language: Soft dark or warm-light stages, subtle radial light, fine noise, restrained depth, precise type.
layout: Product-first hero, a few deep sections, product demonstrations with sticky context.
typography: Neo-grotesk or geometric display with tight tracking; neutral body; mono only for technical details.
color_behavior: Low-saturation neutrals (graphite, warm grey) with one desaturated accent; no rainbow.
surface: Layered surfaces separated by tone and faint edge light.
borders: Hairlines at low contrast; edge highlights on key surfaces only.
shadows: Soft, large, low-opacity depth.
imagery: Real product UI and restrained renders in soft light.
iconography: Monoline, precise.
motion: Slow ambient light, fade-rise reveals, shared layout transitions; nothing constant or bouncy.
interaction: Precise hover light, keyboard-first command interactions.
recommended_effects: [effect.radial-lighting, effect.noise, effect.depth, effect.edge-highlight, effect.glow]
avoid_effects: [effect.holographic, effect.chromatic, effect.particles, effect.mesh-gradient]
recommended_motion: [motion.fade-up, motion.ambient-drift, motion.m3-shared-element, motion.m4-parallax, motion.m4-product-walkthrough]
density: [low, medium]
accessibility_notes: Low-contrast graphite palettes need verified text contrast; ambient motion pauses under reduced motion.
responsive_behavior: Ambient light static on mobile; walkthrough becomes stacked steps.
good_for: Premium AI products, advanced SaaS, developer platforms with brand ambition, premium hardware software.
avoid_when: Playful consumer products, dense operations tools, budget commerce.
compatible_patterns: [layout.hero-product, layout.story-pinned-demo, layout.grid-bento, layout.story-feature-explorer]
compatible_styles: [style.developer-tool, style.modern-saas, style.ai-native, style.minimal, style.spatial]
implementation_notes: Radial lighting and noise as static CSS layers; glow limited to one focal element.
domains: [ai, saas, developer, hardware, data-platform]
conveys: [premium, futuristic, calm, precise, technical, innovative, impressive]
perceived_risks: [cold]
intensity: [2, 4]
contexts: [marketing, application]
motion_ceiling: M4
default_tell: false
```

```yaml
id: style.ai-native
name: AI-native
kind: style
category: futuristic
family: futuristic
character: Conversational, adaptive, alive; the interface shows thinking and generation.
visual_language: Prompt-centric layouts, streaming text, subtle generative accents, clear distinction between human and model content.
layout: Conversation or copilot panels beside the work; command surfaces.
typography: Neutral readable sans for long answers; mono for code and tool output.
color_behavior: Neutral UI; one accent reserved for AI presence (thinking, generated state).
surface: Minimal chrome; message groups by spacing, not heavy bubbles.
borders: Subtle dividers; accent edge on active AI regions.
shadows: Low.
imagery: Product UI, generated examples labelled as such.
iconography: Clear model/tool/source icons; avoid sparkle overuse.
motion: Streaming, thinking indicators, smooth insertion of generated content, optimistic updates.
interaction: Prompt input with attachments, stop/regenerate, inline accept/reject, command palette.
recommended_effects: [effect.gradient, effect.glow, effect.noise]
avoid_effects: [effect.particles, effect.holographic, effect.chromatic, effect.glass]
recommended_motion: [motion.m1-loading, motion.m1-skeleton, motion.m2-command-palette, motion.m3-layout-reflow]
density: [medium]
accessibility_notes: Streaming content must not spam screen readers; announce completion politely; stop control always reachable.
responsive_behavior: Copilot panel becomes a sheet on mobile; input stays pinned above keyboard.
good_for: AI assistants, copilots, agent consoles, generative tools.
avoid_when: Marketing pages that only claim AI without an AI interaction to show.
compatible_patterns: [layout.app-three-panel, layout.app-command-driven, layout.app-split-inspector, layout.hero-dashboard]
compatible_styles: [style.calm-futurism, style.productivity, style.developer-tool, style.minimal]
implementation_notes: Reserve the AI accent for AI states only; sparkle icons and purple gradients are not a substitute for showing capability.
domains: [ai, productivity, developer, saas]
conveys: [innovative, calm, efficient, futuristic, human]
perceived_risks: [generic, gimmicky]
intensity: [2, 4]
contexts: [application, marketing]
motion_ceiling: M4
default_tell: true
```
