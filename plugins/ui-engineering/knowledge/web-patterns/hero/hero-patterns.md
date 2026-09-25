# Hero patterns

The hero answers "what is this, for whom, and what next?" within one viewport. Not every page needs a large hero; apps and dense commerce often need none, and a giant heading is never the default. Earlier pattern names are kept as `aliases`.

```yaml
id: layout.hero-centered
name: Centered hero (minimal typographic)
aliases: [minimal-typographic]
kind: layout
category: hero
purpose: State a strong, short message with minimal distraction.
anatomy: Optional eyebrow, headline up to ~12 words, 1-2 sentence support, primary and optional secondary action, optional install command.
hierarchy: Headline, support, action; whitespace frames.
grid_behavior: Centered column of 8-10 of 12 columns; text max ~20ch per headline line.
responsive: Stack; display clamps down; commands scroll inside their block.
content_requirements: []
compatible_styles: [style.minimal, style.monochrome, style.developer-tool, style.swiss, style.calm-futurism]
compatible_motion: [motion.fade, motion.text-line-reveal, motion.ambient-drift]
interactions: [interaction.press-feedback]
accessibility: Single h1; actions are real links/buttons.
implementation: Pure CSS; the hero must render fully without JS.
anti_patterns: Giant heading with vague copy; decorative gradient blob to fill space; two equal CTAs.
good_for: Developer tools, minimal products, technical platforms, editorial statements.
avoid_when: The product needs to be seen to be understood.
contexts: [marketing, content]
density: [low]
motion_cost: low
default_tell: false
```

```yaml
id: layout.hero-split
name: Split hero
aliases: [split]
kind: layout
category: hero
purpose: Pair a message with a supporting visual of unequal weight.
anatomy: Text column (headline, support, actions) and visual column.
hierarchy: Text first in reading order; visual supports.
grid_behavior: 5/7 or 7/5 split rather than 6/6.
responsive: Text above visual on mobile; visual cropped to its meaningful region.
content_requirements: []
compatible_styles: [style.modern-saas, style.organic, style.gradient-heavy, style.fintech, style.playful]
compatible_motion: [motion.fade-up, motion.scale]
interactions: [interaction.press-feedback]
accessibility: Visual has alt text describing its message.
implementation: CSS grid with named areas.
anti_patterns: Symmetric 50/50 with stock imagery; visual unrelated to the claim.
good_for: SaaS, services, consumer apps with a clear visual.
avoid_when: The visual is decorative only.
contexts: [marketing, commerce]
density: [low, medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.hero-product
name: Product hero (product stage)
aliases: [product-stage]
kind: layout
category: hero
purpose: Make the tangible product the proof.
anatomy: Headline, action, dominant product render/photo or device frame.
hierarchy: Product object dominates; headline close to it; action near headline.
grid_behavior: Centered stage or offset product with text beside; product can break the container.
responsive: Product scales with container; text above product on mobile; aspect-ratio reserved.
content_requirements: [product-media]
compatible_styles: [style.calm-futurism, style.tactile, style.playful, style.liquid-glass, style.bento, style.futuristic]
compatible_motion: [motion.scale, motion.fade-up, motion.m5-cursor-reactive-scene]
interactions: [interaction.press-feedback, interaction.hover-intent]
accessibility: Product image alt text describes the product, not marketing claims.
implementation: Responsive images (srcset, AVIF/WebP) with explicit dimensions.
anti_patterns: Low-quality mockups; product too small to read; device frames around blurry screenshots.
good_for: Hardware, consumer tech, AI products with a tangible UI, premium launches.
avoid_when: No quality product media exists.
contexts: [marketing, commerce]
density: [low]
motion_cost: medium
default_tell: false
```

```yaml
id: layout.hero-dashboard
name: Dashboard / feature-preview hero
aliases: [feature-preview]
kind: layout
category: hero
purpose: Show the real product UI immediately as evidence.
anatomy: Headline and actions above or beside a large real UI screenshot or live preview.
hierarchy: Message then UI; UI cropped to a meaningful region.
grid_behavior: Full-width preview below a centered message, or split with preview bleeding off-edge.
responsive: Preview crops to its key region on mobile rather than shrinking.
content_requirements: [product-ui]
compatible_styles: [style.modern-saas, style.enterprise-saas, style.ai-native, style.developer-tool, style.calm-futurism]
compatible_motion: [motion.fade-up, motion.m4-parallax, motion.m2-tabs]
interactions: [interaction.press-feedback, interaction.progressive-disclosure]
accessibility: Screenshots need alt text naming the demonstrated capability.
implementation: Real UI images or a lightweight DOM replica; never a fake generic dashboard.
anti_patterns: Fake dashboards with random charts; floating decorative cards around the screenshot.
good_for: SaaS, analytics, developer tools, AI copilots.
avoid_when: UI is not ready or not self-explanatory.
contexts: [marketing]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.hero-editorial
name: Editorial hero
aliases: [editorial-split]
kind: layout
category: hero
purpose: Let typography and one strong image carry voice.
anatomy: Characterful headline, standfirst, byline or meta, one image.
hierarchy: Headline and image in dialogue; deliberate imbalance.
grid_behavior: Asymmetric columns (e.g., 2-7 headline, 8-12 image) with overlapping caption.
responsive: Headline first, image cropped with the same intent.
content_requirements: [brand-photography]
compatible_styles: [style.editorial, style.luxury, style.swiss, style.organic]
compatible_motion: [motion.text-line-reveal, motion.m4-image-mask-reveal]
interactions: [interaction.press-feedback]
accessibility: Headline hierarchy intact; image caption linked.
implementation: CSS grid with named lines; art-directed picture element.
anti_patterns: Symmetric split with stock photo; serif chosen only to look premium.
good_for: Publications, luxury, portfolios, premium services.
avoid_when: Task-first products.
contexts: [content, marketing]
density: [low]
motion_cost: low
default_tell: false
```

```yaml
id: layout.hero-full-bleed
name: Full-bleed hero (immersive)
aliases: [immersive-fullscreen]
kind: layout
category: hero
purpose: Let imagery or video sell the experience.
anatomy: Edge-to-edge media, safe text area with scrim, single action.
hierarchy: Image, short statement, action.
grid_behavior: Media spans viewport; text constrained to a column.
responsive: Art-direction crops per breakpoint; use svh/dvh units; action visible on mobile.
content_requirements: [brand-photography]
compatible_styles: [style.luxury, style.cinematic, style.creative-agency, style.glassmorphism, style.y2k]
compatible_motion: [motion.fade, motion.m4-parallax, motion.m4-image-mask-reveal]
interactions: [interaction.press-feedback]
accessibility: Text contrast guaranteed with a scrim; video has pause control and no autoplay sound.
implementation: picture element with art direction; video poster as LCP.
anti_patterns: Unreadable text over busy image; 100vh hiding the action; autoplay without control.
good_for: Hospitality, travel inspiration, luxury, portfolios.
avoid_when: Imagery is generic stock.
contexts: [marketing, commerce]
density: [low]
motion_cost: medium
default_tell: false
```

```yaml
id: layout.hero-asymmetric
name: Asymmetric hero
aliases: [asymmetric]
kind: layout
category: hero
purpose: Create tension and personality through deliberate imbalance.
anatomy: Oversized headline offset against media or whitespace; supporting text in a narrow column.
hierarchy: Scale contrast drives order.
grid_behavior: Offsets on a 12-column grid; elements may overlap by design.
responsive: Keep the offset idea via alignment and crop; avoid overlap on mobile.
content_requirements: []
compatible_styles: [style.swiss, style.neo-brutalism, style.brutalist, style.creative-agency, style.experimental]
compatible_motion: [motion.clip-reveal, motion.text-line-reveal, motion.slide]
interactions: [interaction.press-feedback]
accessibility: DOM order equals reading order regardless of visual placement.
implementation: CSS grid placement; no absolute positioning for text.
anti_patterns: Random offsets with no system; overlapping text and images that hurt contrast.
good_for: Agencies, portfolios, cultural brands, bold startups.
avoid_when: Conservative audiences.
contexts: [marketing, content]
density: [low]
motion_cost: low
default_tell: false
```

```yaml
id: layout.hero-interactive
name: Interactive hero
aliases: [interactive-product]
kind: layout
category: hero
purpose: Let users try the product immediately.
anatomy: Short instruction, working interactive element with a sensible default, action to go further.
hierarchy: Instruction, interactive area, next step.
grid_behavior: Interactive area as the dominant block.
responsive: Touch-first controls; simplified mode on mobile.
content_requirements: [product-ui]
compatible_styles: [style.developer-tool, style.playful, style.experimental, style.ai-native, style.modern-saas]
compatible_motion: [motion.m1-press, motion.m2-tabs, motion.m3-layout-reflow]
interactions: [interaction.press-feedback, interaction.keyboard-navigation, interaction.drag]
accessibility: Fully keyboard operable; the value proposition is readable without interacting.
implementation: Lazy-hydrate after first paint; static preview first.
anti_patterns: Heavy JS delaying first paint; unclear affordance; interaction required to see the message.
good_for: Developer playgrounds, editors, configurators, AI prompt demos.
avoid_when: Demo is slow or needs sign-up.
contexts: [marketing]
density: [medium]
motion_cost: low
default_tell: false
```

```yaml
id: layout.hero-cinematic
name: Cinematic hero
aliases: [cinematic-product]
kind: layout
category: hero
purpose: Open with a single memorable product scene that hands off to scroll storytelling.
anatomy: Exceptional media (sequence, video, 3D), one line of type, quiet action.
hierarchy: Media first, statement, deferred action.
grid_behavior: Full viewport scene; text layered in a safe area.
responsive: Poster image and fade on mobile; no pinning on small screens.
content_requirements: [product-media]
compatible_styles: [style.cinematic, style.futuristic, style.spatial, style.luxury, style.retro-futurism, style.cyberpunk]
compatible_motion: [motion.m5-cinematic-hero, motion.m4-zoom-through, motion.m5-3d-sequence]
interactions: [interaction.press-feedback]
accessibility: Skip link past the sequence; reduced-motion static poster.
implementation: Poster as LCP; media lazy-enhanced; consumes the page HIGH motion budget.
anti_patterns: Heavy video delaying LCP; story hides price or action; used without premium media.
good_for: Flagship launches, premium hardware, games, film.
avoid_when: Apps, documentation, weak media, low-bandwidth audiences.
contexts: [marketing]
density: [low]
motion_cost: high
default_tell: false
```

```yaml
id: layout.hero-media-led
name: Media-led hero with task entry
aliases: [media-led]
kind: layout
category: hero
purpose: Combine inspiration imagery with an immediate task (search, booking).
anatomy: Background or side media, short headline, task object (search form, category picker).
hierarchy: Task object is the anchor; media supports.
grid_behavior: Task object centered or overlapping media edge.
responsive: Task object full-width directly after a short headline.
content_requirements: [brand-photography]
compatible_styles: [style.ecommerce-premium, style.organic, style.modern-saas, style.playful]
compatible_motion: [motion.fade, motion.m2-dropdown]
interactions: [interaction.press-feedback, interaction.keyboard-navigation]
accessibility: Form fields labelled; search submit reachable.
implementation: Form is real and server-backed; media lazy after the form.
anti_patterns: Media dominates and search is secondary; carousel hero.
good_for: Travel, marketplaces, real estate, content platforms.
avoid_when: No task exists at page entry.
contexts: [commerce, marketing]
density: [medium]
motion_cost: low
default_tell: false
```
