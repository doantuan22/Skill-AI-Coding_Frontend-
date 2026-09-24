# Hero patterns

The hero answers "what is this, for whom, and what next?" within one viewport. Not every page needs a large hero; apps and dense commerce often need none.

## minimal-typographic
- **When:** Developer tools, minimal products, technical platforms, editorial; message is strong and short; no hero media.
- **Content:** Headline (≤ ~12 words), 1–2 sentence support, primary action, optional secondary (docs/install command).
- **Hierarchy:** Headline → support → action; whitespace does the framing.
- **Responsive:** Stack; display clamps down; install command block scrolls horizontally inside itself.
- **Motion:** minimal/snappy; optional line reveal (low).
- **Failure:** Giant heading with vague copy; empty feeling because content is weak; decorative gradient added to "fill" space.

## product-stage
- **When:** A tangible product/app screen is the proof; premium-product, consumer-tech, modern-saas.
- **Content:** High-quality product image/render or real UI; headline; action.
- **Hierarchy:** Product object dominates; headline above or beside; action close to headline.
- **Responsive:** Product scales with container; text above product on mobile; image `aspect-ratio` reserved.
- **Motion:** soft/expressive-controlled; product scale/fade on load (medium).
- **Failure:** Low-quality or generic mockups; product too small to read; device frames around blurry screenshots.

## cinematic-product
- **When:** Flagship launch, premium hardware/software, luxury; content supports a scroll story.
- **Content:** Exceptional product media (image sequence, video, or layered renders), very short headline.
- **Hierarchy:** Media first, one line of type, action deferred or quiet.
- **Responsive:** Simplified media on mobile; poster image fallback; no pinned sequences on small screens by default.
- **Motion:** cinematic HIGH — consumes the page's high budget.
- **Failure:** Heavy video delaying LCP; no reduced-motion fallback; used without premium media; story hides price/action.

## editorial-split
- **When:** Editorial, luxury, portfolio, premium services; typography carries voice.
- **Content:** Characterful headline, standfirst, one strong image.
- **Hierarchy:** Asymmetric: headline column + media column with deliberate imbalance.
- **Responsive:** Headline first, then media; keep asymmetry through crop rather than side-by-side.
- **Motion:** minimal/soft; optional mask reveal on image.
- **Failure:** 50/50 symmetric split with stock photo (generic split hero).

## immersive-fullscreen
- **When:** Portfolio, hospitality, travel inspiration, luxury — imagery sells the experience.
- **Content:** Art-directed full-bleed image/video with safe text area.
- **Hierarchy:** Image → short statement → single action.
- **Responsive:** Art-direction crops per breakpoint (`<picture>`); text contrast guaranteed with scrim, not hope.
- **Motion:** soft/cinematic; slow image scale (medium); video autoplay muted with pause control.
- **Failure:** Unreadable text over busy image; 100vh on mobile hiding the action (use `svh`/`dvh`); autoplay without control.

## media-led
- **When:** Marketplace/travel home, content platforms; media plus a task entry (search).
- **Content:** Background or side media, task object (search form/category picker).
- **Hierarchy:** Task object is the visual anchor, media supports.
- **Responsive:** Task object full-width on mobile, placed immediately after a short headline.
- **Motion:** minimal; feedback on the task object.
- **Failure:** Media dominates and the search/task is secondary; carousel hero hiding value.

## feature-preview
- **When:** SaaS, developer tools, technical platforms; the product UI is the proof.
- **Content:** Real UI screenshot/interactive preview or code sample; headline; actions.
- **Hierarchy:** Headline + action first, preview immediately below/beside with meaningful crop.
- **Responsive:** Preview cropped to its most meaningful region on mobile; not shrunk to illegibility.
- **Motion:** soft/snappy; preview state transitions (medium).
- **Failure:** Fake/generic dashboard art; unreadable tiny UI; floating decorative cards around the screenshot.

## interactive-product
- **When:** The product is best understood by trying it (configurator, playground, editor).
- **Content:** A working, lightweight interactive element with sensible default state.
- **Hierarchy:** Short instruction → interactive area → action to go further.
- **Responsive:** Touch-first controls; simplified mode on mobile.
- **Motion:** snappy feedback; state transitions.
- **Failure:** Heavy JS delaying first paint; unclear affordance; keyboard inaccessible; interaction required to see the value proposition.
