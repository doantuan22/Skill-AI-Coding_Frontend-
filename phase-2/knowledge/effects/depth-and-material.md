# Depth and material effects

```yaml
id: effect.shadow
name: Elevation shadow
kind: effect
category: depth-and-material
visual_purpose: Indicate layering (menus, dialogs, lifted cards) and interactivity.
construction: Two-layer shadow (tight ambient plus soft key) tied to elevation tokens.
parameters: 3-4 elevation levels; neutral or slightly tinted color; opacity under 20 percent.
compatible_styles: [style.minimal, style.modern-saas, style.enterprise-saas, style.productivity, style.tactile, style.playful, style.fintech]
recommended_contexts: [marketing, application, commerce]
performance:
  cost: low
  notes: Large blur radii on many elements cost paint; animate opacity of a shadow layer instead of box-shadow.
accessibility: Elevation should not be the only boundary cue for interactive controls.
responsive: Unchanged; reduce blur on low-power.
implementation: Elevation tokens mapped to box-shadow; hover lift animates a pseudo-element opacity.
anti_patterns: Colored glow shadows on CTAs; heavy shadows on every card; inconsistent light direction.
technology:
  preferred: [tech.css]
  alternatives: []
default_tell: false
```

```yaml
id: effect.contact-shadow
name: Contact shadow
kind: effect
category: depth-and-material
visual_purpose: Ground a product cut-out or object on a surface.
construction: Flattened elliptical soft shadow directly under the object.
parameters: Tight core, soft falloff; matches object width.
compatible_styles: [style.ecommerce-premium, style.tactile, style.spatial, style.cinematic]
recommended_contexts: [commerce, marketing]
performance:
  cost: low
  notes: Static radial gradient or baked into imagery.
accessibility: Decorative.
responsive: Scales with the image.
implementation: Radial-gradient pseudo-element or pre-rendered with the product image.
anti_patterns: Contact shadows under UI cards; mismatched perspective.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
default_tell: false
```

```yaml
id: effect.inner-shadow
name: Inner shadow
kind: effect
category: depth-and-material
visual_purpose: Show inset or pressed states and wells (inputs, toggles, sliders).
construction: Inset box-shadow consistent with the global light.
parameters: Small offset and blur; low opacity.
compatible_styles: [style.tactile, style.retro-futurism]
recommended_contexts: [application]
performance:
  cost: low
  notes: Negligible.
accessibility: Boundary of inputs still needs a visible 3 to 1 edge.
responsive: Unchanged.
implementation: box-shadow inset; toggles between outer and inner on press.
anti_patterns: Neumorphism where everything is inset and low-contrast.
technology:
  preferred: [tech.css]
  alternatives: []
default_tell: false
```

```yaml
id: effect.depth
name: Depth layering
kind: effect
category: depth-and-material
visual_purpose: Express hierarchy through distance (foreground focus, background context).
construction: Layered planes with scale, blur, shadow and parallax consistent with a virtual camera.
parameters: 2-4 depth planes; distant planes lower contrast.
compatible_styles: [style.spatial, style.cinematic, style.calm-futurism, style.futuristic]
recommended_contexts: [marketing]
performance:
  cost: medium
  notes: Many layered transforms and blurs; keep planes few and composited.
accessibility: Depth motion is a vestibular trigger; static depth is safe.
responsive: Flatten to 1-2 planes on mobile.
implementation: Transforms with translateZ/scale on composited layers; blur only on static background planes.
anti_patterns: Floating cards at random depths; depth without a focal plane.
technology:
  preferred: [tech.css]
  alternatives: [tech.threejs]
default_tell: false
```

```yaml
id: effect.blur
name: Blur (element or background)
kind: effect
category: depth-and-material
visual_purpose: De-emphasize background content or create atmospheric soft light shapes.
construction: filter blur on a decorative layer or pre-blurred image.
parameters: Static; radius proportional to layer size.
compatible_styles: [style.spatial, style.calm-futurism, style.gradient-heavy]
recommended_contexts: [marketing]
performance:
  cost: medium
  notes: Blurring large layers is expensive; animating blur radius is very expensive.
accessibility: Never blur readable content.
responsive: Use pre-blurred images on mobile.
implementation: Pre-render blurred assets or apply static filter to small layers; animate opacity between states.
anti_patterns: Animated blur transitions on page load; blurring content to force attention to a modal.
technology:
  preferred: [tech.css]
  alternatives: [tech.canvas]
default_tell: false
```

```yaml
id: effect.backdrop-blur
name: Backdrop blur
kind: effect
category: depth-and-material
visual_purpose: Keep context visible behind overlays and sticky bars while preserving legibility.
construction: backdrop-filter blur with a semi-opaque tint on a fixed or overlay surface.
parameters: Blur 8-24px; tint opacity high enough for AA text; 1-2 per viewport.
compatible_styles: [style.glassmorphism, style.liquid-glass, style.spatial]
recommended_contexts: [application, marketing]
performance:
  cost: high
  notes: Recomputed as content scrolls beneath; costly on large or many surfaces and on mobile GPUs.
accessibility: Respect prefers-reduced-transparency with an opaque fallback; verify contrast over busy content.
responsive: Replace with solid tint on mobile or low-power devices.
implementation: backdrop-filter with @supports fallback to an opaque background color token.
anti_patterns: Backdrop blur on every card; animating blur radius; blur over plain white.
technology:
  preferred: [tech.css]
  alternatives: []
default_tell: true
```

```yaml
id: effect.glass
name: Glass material
kind: effect
category: depth-and-material
visual_purpose: Communicate a translucent layer above meaningful content.
construction: Backdrop blur plus tint plus edge highlight plus soft shadow.
parameters: Max two glass levels; tint strength tuned for text contrast.
compatible_styles: [style.glassmorphism, style.liquid-glass, style.spatial]
recommended_contexts: [marketing, application]
performance:
  cost: high
  notes: Inherits backdrop blur cost; multiplied by the number of panels.
accessibility: Same as backdrop blur; focus rings must stay visible on glass.
responsive: Opaque fallback on mobile; keep layout identical.
implementation: Composite token (surface-glass) combining backdrop-filter, background tint and border highlight.
anti_patterns: Glass cards on a plain background; stacked glass-on-glass; glass as a generic premium signal.
technology:
  preferred: [tech.css]
  alternatives: []
default_tell: true
```

```yaml
id: effect.layered-transparency
name: Layered transparency
kind: effect
category: depth-and-material
visual_purpose: Show relationships between overlapping planes (maps, media, inspectors).
construction: Semi-transparent surfaces with deliberate overlap and consistent opacity steps.
parameters: 2-3 opacity levels; text on the most opaque layer.
compatible_styles: [style.spatial, style.liquid-glass, style.glassmorphism]
recommended_contexts: [application, marketing]
performance:
  cost: low
  notes: Plain opacity is cheap; combined with blur it inherits blur cost.
accessibility: Honor prefers-reduced-transparency; ensure text contrast.
responsive: Increase opacity on small screens.
implementation: Opacity tokens on surfaces; no per-element ad-hoc alpha.
anti_patterns: Random alpha values; transparency hiding content boundaries.
technology:
  preferred: [tech.css]
  alternatives: []
default_tell: false
```

```yaml
id: effect.reflection
name: Reflection
kind: effect
category: depth-and-material
visual_purpose: Suggest a glossy floor or material to add luxury or product presence.
construction: Flipped, masked, faded copy of an object below it, or baked into imagery.
parameters: Short fade (20-40 percent of object height); low opacity.
compatible_styles: [style.luxury, style.ecommerce-premium, style.y2k]
recommended_contexts: [commerce, marketing]
performance:
  cost: low
  notes: Prefer baked assets; duplicated DOM images double decode cost.
accessibility: Duplicate images must be aria-hidden.
responsive: Remove on small screens if cramped.
implementation: Pre-rendered in the image, or a masked transform scaleY(-1) copy.
anti_patterns: Reflections under UI components; dated glossy-floor overuse.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
default_tell: false
```

```yaml
id: effect.liquid
name: Liquid / refraction
kind: effect
category: depth-and-material
visual_purpose: Make controls or surfaces feel fluid and physical, bending content beneath.
construction: Displacement of the backdrop at edges plus specular highlights; morphing shapes.
parameters: Subtle displacement; only on a few control surfaces.
compatible_styles: [style.liquid-glass]
recommended_contexts: [application, marketing]
performance:
  cost: high
  notes: True refraction needs SVG displacement filters or WebGL; both are expensive.
accessibility: Reduce to solid material under reduced transparency/motion.
responsive: Approximate with blur plus highlight on mobile.
implementation: SVG feDisplacementMap on small elements or a WebGL pass; CSS approximation first.
anti_patterns: Liquid effects on text or large backgrounds; effects without the matching motion language.
technology:
  preferred: [tech.svg]
  alternatives: [tech.webgl, tech.css]
default_tell: false
```
