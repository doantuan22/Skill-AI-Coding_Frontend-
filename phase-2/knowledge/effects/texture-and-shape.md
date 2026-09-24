# Texture and shape effects

```yaml
id: effect.noise
name: Noise
kind: effect
category: texture-and-shape
visual_purpose: Remove digital flatness and gradient banding; add subtle material.
construction: Tiled monochrome noise texture at very low opacity over a surface.
parameters: Opacity 2-6 percent; small tile; static.
compatible_styles: [style.calm-futurism, style.monochrome, style.developer-tool, style.gradient-heavy, style.organic, style.experimental]
recommended_contexts: [marketing, application]
performance:
  cost: low
  notes: Static tiled image is cheap; animated noise repaints every frame.
accessibility: Keep below perceptibility on text areas.
responsive: Unchanged.
implementation: Small PNG/SVG feTurbulence tile as background-image; never regenerate per frame.
anti_patterns: Visible noise over text; animated TV-static loops.
technology:
  preferred: [tech.css, tech.svg]
  alternatives: [tech.canvas]
default_tell: false
```

```yaml
id: effect.grain
name: Film grain
kind: effect
category: texture-and-shape
visual_purpose: Add analog, editorial or cinematic warmth to imagery and large fields.
construction: Coarser noise with slight luminance variation over images or backgrounds.
parameters: Opacity 4-10 percent over images; lower over UI.
compatible_styles: [style.editorial, style.luxury, style.organic, style.cinematic, style.creative-agency, style.retro-futurism]
recommended_contexts: [marketing, content]
performance:
  cost: low
  notes: Static overlay cheap; animated grain costs paint on full viewport.
accessibility: Avoid over small text.
responsive: Same texture scaled; skip on low-power.
implementation: Overlay pseudo-element with blend mode; bake into imagery when possible.
anti_patterns: Grain on dashboards; flickering animated grain everywhere.
technology:
  preferred: [tech.css]
  alternatives: [tech.canvas]
default_tell: false
```

```yaml
id: effect.mask
name: Mask
kind: effect
category: texture-and-shape
visual_purpose: Shape or fade media edges to integrate images with layout and type.
construction: CSS mask-image with gradients or shapes on media.
parameters: Soft edges or intentional shapes consistent across the page.
compatible_styles: [style.editorial, style.luxury, style.swiss, style.creative-agency, style.ecommerce-premium]
recommended_contexts: [marketing, content, commerce]
performance:
  cost: low
  notes: Static masks cheap; animated masks similar to clip-path.
accessibility: Must not crop meaningful parts of images; alt text describes the whole image.
responsive: Adjust mask geometry per breakpoint.
implementation: mask-image linear-gradient for fades; SVG masks for shapes.
anti_patterns: Random blob masks; fading content that users need to read.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
default_tell: false
```

```yaml
id: effect.clipping
name: Clipping
kind: effect
category: texture-and-shape
visual_purpose: Create strong graphic geometry (angled cuts, frames) and reveal areas.
construction: clip-path polygons or insets on containers or media.
parameters: One geometry language per page (angle, notch, inset).
compatible_styles: [style.swiss, style.neo-brutalism, style.brutalist, style.cyberpunk, style.creative-agency]
recommended_contexts: [marketing, content]
performance:
  cost: low
  notes: Static clip-path cheap; animating complex polygons costs paint.
accessibility: Clipped focus rings get cut off; add outline-offset or clip the background only.
responsive: Simplify angles on small screens.
implementation: clip-path on a background pseudo-element to keep focus rings intact.
anti_patterns: Mixed clip geometries; clipped text.
technology:
  preferred: [tech.css]
  alternatives: [tech.svg]
default_tell: false
```

```yaml
id: effect.distortion
name: Distortion
kind: effect
category: texture-and-shape
visual_purpose: Signal energy, transition or interactivity through warping media.
construction: Displacement maps or shaders warping images on hover or transition.
parameters: Brief, subtle; tied to an interaction or transition.
compatible_styles: [style.experimental, style.cyberpunk, style.creative-agency]
recommended_contexts: [marketing]
performance:
  cost: high
  notes: SVG filter or WebGL per frame; heavy on mobile.
accessibility: Distorted text is unreadable; motion-sensitive users need a static version.
responsive: Disable on mobile.
implementation: WebGL plane with displacement texture, or SVG feDisplacementMap on small images.
anti_patterns: Distorting UI or text; constant wobble.
technology:
  preferred: [tech.webgl]
  alternatives: [tech.svg, tech.threejs]
default_tell: false
```

```yaml
id: effect.particles
name: Particles
kind: effect
category: texture-and-shape
visual_purpose: Visualize data, energy or atmosphere when particles represent something.
construction: Many small points drawn on canvas/WebGL, optionally reacting to input.
parameters: Count scaled to device (hundreds on mobile, low thousands on desktop); purposeful behavior.
compatible_styles: [style.experimental, style.futuristic]
recommended_contexts: [marketing]
performance:
  cost: high
  notes: Continuous rendering loop; must pause off-screen and degrade on low-power.
accessibility: Decorative particles aria-hidden; pause control for persistent motion.
responsive: Reduce count or replace with static image on mobile.
implementation: Canvas 2D for hundreds, WebGL for thousands; stop loop when hidden.
anti_patterns: Floating dots as generic AI/tech decoration; particles behind text.
technology:
  preferred: [tech.canvas]
  alternatives: [tech.webgl, tech.threejs]
default_tell: true
```

```yaml
id: effect.shader
name: Shader effect
kind: effect
category: texture-and-shape
visual_purpose: Produce custom procedural visuals (noise fields, liquid light, gradients in motion) impossible in CSS.
construction: Fragment shader on a full-bleed or bounded WebGL canvas.
parameters: Single pass; resolution scaled 0.5-0.75 of device pixels; bounded area.
compatible_styles: [style.experimental, style.futuristic]
recommended_contexts: [marketing]
performance:
  cost: very-high
  notes: GPU load competes with page scrolling; requires context-loss handling and pause when hidden.
accessibility: Decorative, aria-hidden, pausable; avoid rapid luminance changes.
responsive: Static poster on mobile, save-data and reduced motion.
implementation: Minimal WebGL wrapper; poster image rendered first; shader enhances after load.
anti_patterns: Shader hero as the only proof of innovation; shaders under body text.
technology:
  preferred: [tech.webgl]
  alternatives: [tech.threejs]
default_tell: false
```
