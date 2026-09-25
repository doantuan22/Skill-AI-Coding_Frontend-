# Reference profiles

Abstract design DNA of widely known product languages, written from general public observation. They are **reasoning anchors**, not specifications: products change, and these profiles describe a recognizable *language*, never a page to rebuild. When the user supplies a concrete current reference, [reference-extraction.md](reference-extraction.md) takes precedence over the profile. No profile requires fetching the site.

Use a profile to translate a request such as "make it feel Apple-like" into transferable traits, then apply [anti-copying.md](anti-copying.md). Refer to the result by family (`premium-cinematic-product`), not by brand, in project artifacts.

Profile schema: `composition`, `density`, `typography`, `surfaces`, `color`, `buttons`, `navigation`, `imagery`, `motion`, `section_rhythm`, `hierarchy`, `transferable`, `never_transfer`.

---

## premium-cinematic-product (Apple-like)

```yaml
family: premium-product
composition: {whitespace: very-high, hero_scale: large, alignment: centered, section_rhythm: cinematic}
density: low
typography: {display_contrast: very-high, tracking: tight-on-display, body_restraint: high, weights: few}
surfaces: {card_usage: low, border_usage: very-low, elevation: restrained, bands: full-width tonal}
color: {base: pure light or deep dark alternating by section, accent: minimal, color_from: product imagery}
buttons: {character: calm, shape: soft/pill for primary, secondary: text link with chevron}
navigation: {global: thin and quiet, local: sticky product sub-nav with one buy action}
imagery: {product_first: true, scale: very-large, background: clean, crop: centered hero object}
motion: {hero: expressive, scroll: controlled storytelling, micro: subtle, budget: one high moment per page}
section_rhythm: one message per section; headline → short support → visual; long vertical pacing
hierarchy: headline states a single benefit; specs deferred to a dedicated area
transferable: [scale contrast, single-message sections, product-as-hero, restraint in chrome, scroll-linked reveal for one story]
never_transfer: [product photography, device silhouettes, exact headline phrasing, logo/marks, proprietary typeface, exact section order]
```

## precise-product-dark (Linear-like)

```yaml
family: modern-saas + developer-tool
composition: {whitespace: high, hero_scale: medium-large, alignment: left or centered, section_rhythm: tight-then-open}
density: medium
typography: {display_contrast: high, tracking: tight, body: neutral grotesk, weights: medium-heavy for headings}
surfaces: {card_usage: medium, border_usage: hairline, elevation: glow-free or very soft, theme: dark-first}
color: {base: near-black neutrals, accent: single desaturated hue, gradients: subtle and local if any}
buttons: {character: crisp, shape: small radius, keyboard-shortcut hints visible}
navigation: {global: compact product header, emphasis: changelog/method pages}
imagery: {product_ui: true, treatment: cropped high-fidelity UI with perspective or masks, decorative: rare}
motion: {character: snappy-precise, micro: fast, hero: medium, scroll: light reveals}
section_rhythm: product UI → principle statement → detailed capability rows
hierarchy: opinionated statements; product UI as proof
transferable: [precision, hairline surfaces, keyboard-centric affordances, product UI as proof, restrained dark palette]
never_transfer: [UI screenshots, brand color, exact copy tone, custom illustrations]
```

## gradient-technical-commerce (Stripe-like)

```yaml
family: technical-platform + modern-saas
composition: {whitespace: high, hero_scale: large, grid: visible strict columns with diagonal/angled color fields, section_rhythm: varied}
density: medium-high below the fold
typography: {display_contrast: high, body: neutral sans, mono: code samples, numerics: prominent}
surfaces: {card_usage: medium, border_usage: low, elevation: soft layered UI previews}
color: {base: light, accent: rich multi-hue field used as a single signature moment, ui: restrained}
buttons: {character: confident, secondary: arrow link}
navigation: {global: mega menu with product groups, docs as first-class}
imagery: {product_ui: layered, code: real samples, diagrams: flow illustrations}
motion: {signature: animated color field or flow diagram, micro: soft, scroll: section reveals}
section_rhythm: capability → code/evidence → customer proof → developer depth
hierarchy: business value headline, developer credibility immediately beneath
transferable: [one signature color moment, code as evidence, layered UI previews, dual audience (business + developer) hierarchy]
never_transfer: [signature gradient artwork, illustrations, customer logos, copy]
```

## monochrome-developer-platform (Vercel-like)

```yaml
family: developer-tool + minimal-product
composition: {whitespace: high, hero_scale: large, alignment: centered, grid: visible hairline grid}
density: medium
typography: {display_contrast: very-high, tracking: tight, sans + mono pairing, weights: bold display}
surfaces: {card_usage: medium, border_usage: hairline, elevation: none, theme: black/white}
color: {base: pure monochrome, accent: almost none, status colors functional only}
buttons: {character: stark, primary: inverse solid, secondary: outline}
navigation: {global: compact, docs/templates prominent}
imagery: {product: deployments/UI/code, decorative: geometric line work only}
motion: {character: minimal-technical, micro: fast, hero: restrained}
section_rhythm: statement → proof (metrics/logos/UI) → capability grid → templates
hierarchy: very short headlines; developer outcomes
transferable: [monochrome discipline, hairline grid, sans+mono system, stark contrast]
never_transfer: [triangle mark, templates, product screenshots, exact grid artwork]
```

## warm-document-product (Notion-like)

```yaml
family: editorial-product + consumer-tech
composition: {whitespace: high, hero_scale: medium, alignment: centered, section_rhythm: friendly-modular}
density: medium
typography: {display_contrast: medium-high, character: friendly and bookish, serif accents possible}
surfaces: {card_usage: medium, border_usage: low, elevation: low, background: warm off-white}
color: {base: warm neutrals, accent: minimal, illustration: monochrome line drawings}
buttons: {character: friendly, shape: small radius}
navigation: {global: product header with templates/use cases}
imagery: {product_ui: real documents, illustration: hand-drawn monochrome}
motion: {character: soft, micro: subtle, product demo: stepped}
section_rhythm: use-case tabs → real document examples → community/templates
hierarchy: "for you / for teams" framing; examples over claims
transferable: [warmth via neutrals and illustration, document-as-product proof, use-case switching]
never_transfer: [illustration characters, UI, copy]
```

## motion-forward-creative-tool (Framer-like)

```yaml
family: creative-portfolio + modern-saas
composition: {whitespace: high, hero_scale: very-large, alignment: centered, section_rhythm: showcase-heavy}
density: low-medium
typography: {display_contrast: very-high, tracking: tight, display: bold condensed-feel sans}
surfaces: {card_usage: medium, theme: dark, elevation: layered media}
color: {base: dark, accent: vivid and sparing, media provides color}
buttons: {character: pill/soft, confident}
navigation: {global: compact floating-style header (earned by showcase context)}
imagery: {showcase sites and UI in motion, video-first}
motion: {character: expressive-controlled, scroll: rich, micro: springy, budget: high but focused on product demos}
section_rhythm: demo → feature in motion → community showcase → templates
hierarchy: show capability in motion before explaining it
transferable: [motion as product proof, showcase-first narrative, very large display with brief copy]
never_transfer: [community showcase work, UI, brand assets]
```

## pragmatic-developer-platform (GitHub-like)

```yaml
family: developer-tool + data-heavy-product (app); technical-platform (marketing)
composition: {app: dense, functional; marketing: dark cinematic sections with illustrations}
density: app high; marketing medium
typography: {system-font-first app, mono for code/refs, strong numeric usage}
surfaces: {app: bordered boxes, dividers, low elevation; marketing: glowing illustrations}
color: {app: neutral + functional semantic system (status, diff), accent: restrained}
buttons: {character: utilitarian, many sizes, clear primary green-like semantic role}
navigation: {app: repo tabs, breadcrumbs, persistent header; marketing: mega menu}
imagery: {code, diffs, UI, product illustrations on marketing only}
motion: {app: minimal; marketing: medium scroll reveals}
section_rhythm: app is task-first; marketing is capability → customer evidence
hierarchy: object/context first (repo, issue) then actions
transferable: [functional semantic color system, system fonts for dense apps, mono for references, task-first app density]
never_transfer: [mascots/illustrations, octicons, brand colors, product UI]
```

## trust-led-marketplace (Airbnb-like)

```yaml
family: marketplace + travel-commerce + consumer-tech
composition: {search-first entry, photographic listing grid, generous but efficient}
density: medium-high
typography: {friendly rounded-geometric sans, strong titles, price typography clear}
surfaces: {listing cards with borderless photos, rounded corners, low elevation; sticky booking panel}
color: {base: white/neutral, accent: single warm brand hue for primary action only}
buttons: {character: friendly, primary: solid accent, secondary: underlined text}
navigation: {search bar as navigation hub, category chips with icons}
imagery: {host/user photography, consistent aspect, carousel per listing}
motion: {soft microinteractions, heart/favorite feedback, shared-element-like transitions}
section_rhythm: search → categories → results; detail: gallery → facts → booking
hierarchy: photo → place → price/rating → action
transferable: [photo-first listings, single accent for action, sticky booking summary, trust signals near price]
never_transfer: [logo, brand hue, illustrations/icons, listing content]
```

## deal-dense-booking (Agoda-like)

```yaml
family: marketplace + travel-commerce (high density)
composition: {search panel dominant, dense result lists, filters sidebar, many badges}
density: high
typography: {neutral legible sans, bold prices, strike-through original price, compact labels}
surfaces: {result rows/cards with borders, promo banners, sticky price summary}
color: {base: white, accent: brand blue-like for actions, semantic red/green for deals/availability}
buttons: {character: direct, high-contrast "select/book"}
navigation: {product tabs (hotels/flights/...), persistent search, account/cart}
imagery: {property photos, thumbnails, maps}
motion: {minimal; loading skeletons; filter feedback}
section_rhythm: task-driven, no storytelling
hierarchy: price and availability first; reviews next
transferable: [price clarity, dense comparable rows, filter-first layout, urgency only when truthful]
never_transfer: [badge overload, fake urgency, brand identity]
note: its density is right for comparison shopping; do not import it into premium or editorial products.
```

---

## Using a profile

1. Map the request to the profile, then to its **family** in [archetypes.md](archetypes.md).
2. Keep only traits listed as `transferable` that the project's content can support.
3. Re-express each trait in project terms (tokens, grammar rules, pattern names).
4. Record `never_transfer` items as anti-copy constraints in `DESIGN-INSPIRATION.md`.

Profiles are not added without a reason: add one only when it contributes DNA that no archetype/profile here covers. Keep this list under ~12.
