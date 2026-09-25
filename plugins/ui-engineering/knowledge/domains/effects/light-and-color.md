# Light and color effects

```yaml
id: effect.gradient
name: Linear/radial gradient
kind: effect
category: light-and-color
visual_purpose: Add subtle dimension or a brand color transition to a surface or type.
construction: Two or three close color stops on a surface, or a brand pair on one signature element.
parameters: Stops 2-3; hue shift under 40 degrees for subtlety; angle consistent across the page.
compatible_styles: [style.modern-saas, style.gradient-heavy, style.playful, style.fintech, style.ai-native, style.bento]
recommended_contexts: [marketing, application]
performance:
  cost: low
  notes: Static gradients are cheap; large animated gradients repaint.
accessibility: Check text contrast at the lightest and darkest stop; gradient text needs a solid fallback color.
responsive: Unchanged; keep angles relative to the element.
implementation: CSS linear-gradient/radial-gradient on a token; add noise to prevent banding on large areas.
anti_patterns: Gradient on every button and card; purple-to-blue by default; gradient text for body copy.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
default_tell: false
```

```yaml
id: effect.mesh-gradient
name: Mesh gradient
kind: effect
category: light-and-color
visual_purpose: Create a soft, organic multi-hue color field as a brand signature or atmosphere.
construction: Several blurred color blobs or stacked radial gradients forming one field.
parameters: 3-5 hues from the brand palette; low contrast between neighbors; one field per page.
compatible_styles: [style.gradient-heavy, style.playful, style.y2k]
recommended_contexts: [marketing]
performance:
  cost: medium
  notes: Large blurred layers are expensive to repaint; animate only transforms of a pre-rendered layer.
accessibility: Place text on solid or strongly tinted zones; verify contrast over the brightest area.
responsive: Static on mobile; scale field to viewport.
implementation: Stacked radial-gradients or a pre-rendered image; subtle drift via transform only.
anti_patterns: Rainbow meshes behind every section; meshes used to hide weak content; default purple-pink-blue.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg, tech.webgl]
default_tell: true
```

```yaml
id: effect.radial-lighting
name: Radial lighting
kind: effect
category: light-and-color
visual_purpose: Direct attention to a focal area and suggest a light source on dark or neutral stages.
construction: Soft elliptical radial gradient of a lighter tone behind the focal content.
parameters: One light per viewport; low opacity (4-12 percent lightness shift); large radius.
compatible_styles: [style.calm-futurism, style.futuristic, style.cinematic, style.modern-saas, style.developer-tool]
recommended_contexts: [marketing]
performance:
  cost: low
  notes: Static CSS gradient; cheap unless animated over full viewport.
accessibility: Does not carry information; ensure focal text contrast independently.
responsive: Reposition behind content on mobile; reduce radius.
implementation: CSS radial-gradient pseudo-element behind hero or section; static or slow position drift.
anti_patterns: Multiple competing light sources; colored rainbow lights; lighting that washes out text.
technology:
  preferred: [tech.css]
  alternatives: [tech.webgl]
default_tell: false
```

```yaml
id: effect.spotlight
name: Spotlight (pointer-follow light)
kind: effect
category: light-and-color
visual_purpose: Reveal texture or edges near the pointer to make surfaces feel responsive.
construction: Radial gradient positioned at pointer coordinates via CSS variables, masked to a card or border.
parameters: Radius 150-400px; low opacity; only on hoverable desktop devices.
compatible_styles: [style.calm-futurism, style.futuristic, style.developer-tool, style.creative-agency]
recommended_contexts: [marketing]
performance:
  cost: low
  notes: Update CSS variables in rAF from pointermove; avoid layout reads.
accessibility: Purely decorative; no information in the light; disabled for coarse pointers and reduced motion.
responsive: Off on touch; static subtle highlight instead.
implementation: Pointer events set --x/--y on the container; background uses radial-gradient at var(--x) var(--y).
anti_patterns: Spotlights on every card in a grid; spotlight replacing visible focus/hover states.
technology:
  preferred: [tech.css, tech.native-js]
  alternatives: []
default_tell: false
```

```yaml
id: effect.glow
name: Glow
kind: effect
category: light-and-color
visual_purpose: Signal an active or focal element as a light source.
construction: Soft colored shadow or blurred duplicate behind one element.
parameters: One glowing element per view; accent color only; blur 12-40px at low opacity.
compatible_styles: [style.futuristic, style.cyberpunk, style.calm-futurism, style.retro-futurism, style.ai-native]
recommended_contexts: [marketing, application]
performance:
  cost: medium
  notes: Large blurred shadows cost paint; animating glow repaints every frame.
accessibility: Never the only focus or state indicator; can reduce edge contrast of text.
responsive: Reduce spread on mobile.
implementation: box-shadow or filter drop-shadow on one element; animate opacity of a pseudo-element, not the shadow.
anti_patterns: Glowing buttons, borders and icons everywhere; neon glow as a generic tech signal; pulsing glow loops.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
default_tell: true
```

```yaml
id: effect.edge-highlight
name: Edge highlight
kind: effect
category: light-and-color
visual_purpose: Separate layered dark surfaces and suggest a top light without heavy shadows.
construction: One-pixel lighter top or border gradient on a surface edge.
parameters: Low contrast (white at 6-15 percent); consistent light direction.
compatible_styles: [style.calm-futurism, style.futuristic, style.glassmorphism, style.liquid-glass, style.monochrome, style.developer-tool]
recommended_contexts: [marketing, application]
performance:
  cost: low
  notes: Border or inset shadow; negligible.
accessibility: Decorative; control boundaries still need 3 to 1 contrast by other means.
responsive: Unchanged.
implementation: Inset box-shadow 0 1px 0 or a border-image/linear-gradient mask on the border.
anti_patterns: Edge highlights on every nested element; inconsistent light direction.
technology:
  preferred: [tech.css]
  alternatives: []
default_tell: false
```

```yaml
id: effect.specular-highlight
name: Specular highlight
kind: effect
category: light-and-color
visual_purpose: Simulate a glossy material catching light (glass, chrome, liquid).
construction: Small bright gradient streak near an edge, following the surface curvature.
parameters: One highlight per object; aligned with the global light direction.
compatible_styles: [style.liquid-glass, style.y2k, style.retro-futurism, style.tactile]
recommended_contexts: [marketing, application]
performance:
  cost: low
  notes: Static gradient; pointer-driven versions cost like spotlight.
accessibility: Decorative only.
responsive: Static on touch devices.
implementation: Pseudo-element with linear-gradient and mix-blend-mode screen, clipped to shape.
anti_patterns: Highlights on flat UI that has no material story.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg, tech.webgl]
default_tell: false
```

```yaml
id: effect.holographic
name: Holographic / iridescent
kind: effect
category: light-and-color
visual_purpose: Signal novelty, collectibility or a playful future through shifting hue.
construction: Conic or multi-stop gradient with blend modes, optionally shifting with pointer or tilt.
parameters: Small areas (badges, cards, product accents); never full backgrounds with text.
compatible_styles: [style.y2k, style.retro-futurism]
recommended_contexts: [marketing]
performance:
  cost: medium
  notes: Blend modes and pointer updates add paint; keep areas small.
accessibility: Text on iridescence is unreadable; high flicker risk if animated quickly.
responsive: Static on mobile.
implementation: Conic-gradient layer with mix-blend-mode, hue shift bound to pointer position.
anti_patterns: Holographic UI chrome; iridescent text; used in serious products.
technology:
  preferred: [tech.css]
  alternatives: [tech.webgl]
default_tell: false
```

```yaml
id: effect.chromatic
name: Chromatic aberration
kind: effect
category: light-and-color
visual_purpose: Create a glitch, lens or energy feeling for a momentary emphasis.
construction: Offset red/blue copies of an element or image.
parameters: Offset 1-3px; brief duration if animated.
compatible_styles: [style.cyberpunk, style.experimental]
recommended_contexts: [marketing]
performance:
  cost: medium
  notes: Duplicated layers and blend modes; shader versions are GPU heavy.
accessibility: Blurs text edges; animated glitches are a seizure/vestibular risk.
responsive: Disable on mobile.
implementation: Pseudo-element copies with offsets and mix-blend-mode, or a fragment shader.
anti_patterns: Applied to body text or UI; constant looping glitch.
technology:
  preferred: [tech.css]
  alternatives: [tech.webgl]
default_tell: false
```
