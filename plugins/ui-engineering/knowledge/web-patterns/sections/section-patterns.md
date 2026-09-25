# Section patterns

Each pattern: **when** · **content required** · **hierarchy** · **responsive** · **motion** · **common failure**.

| Pattern | When | Content required | Hierarchy | Responsive | Motion | Common failure |
|---|---|---|---|---|---|---|
| **feature-alternating** | 3–5 substantial features, each with a visual | Per feature: heading, 1–3 sentences, real visual | Text/visual alternate sides to pace reading | Stack text above visual; don't alternate on mobile | low–medium reveal per row | Alternating with icons instead of visuals; > 5 rows becomes monotonous |
| **feature-grid** | Many small, parallel capabilities (6–12) | Short title + one line each; optional small icon with meaning | Grouped by category; not equal-weight if importance differs | 1–2 columns mobile | low (none or single group reveal) | Three equal cards with generic icons and vague copy as the default block |
| **editorial-sections** | Argument or narrative in prose | Real paragraphs, pull quotes, images with captions | Typography carries hierarchy; no boxes | Single column with media breakouts | minimal | Card-ifying prose; losing measure |
| **sticky-storytelling** (layout mechanics: `layout.story-sticky`) | 3–6 steps changing one visual | Step texts + a visual per state | Sticky visual beside steps | Stack steps with inline visuals on mobile | medium (sticky reveal); HIGH only with scrubbed pinning (`layout.story-pinned-demo`) | Too few steps; sticky text column; no reduced fallback |
| **product-showcase** | Several views of one product | Multiple quality images/UI states | One large view + switcher/gallery | Swipeable or stacked | medium | Carousel hiding key views; tiny thumbnails only |
| **comparison** (layout mechanics: `layout.story-comparison`) | Buyer compares tiers/options/competitors honestly | Real attributes and values | Table with sticky header/first column; highlight recommended | Horizontal scroll inside table or per-option cards | low | Fabricated competitor claims; check-mark walls without meaning |
| **metric-story** | 1–4 real metrics prove a claim | Numbers with source/context | Claim → metrics → explanation | Stack; keep numbers large | low–medium counter | Vanity/unsourced numbers; 4+ metrics in a strip as decoration |
| **testimonial** | Real quotes from identifiable people/orgs | Quote, name, role/company, optional photo | One strong quote > many weak ones | Single column | low | Anonymous quotes; carousels of generic praise |
| **social-proof** | Recognizable customers/numbers exist | Logos (with permission)/counts | Quiet, below the main value proposition | Wrap or scroll | none/low; avoid infinite marquee without pause | Fake logos; marquee that never stops |
| **technical-detail** | Expert audience needs specs/architecture | Specs, diagrams, code | Dense but structured; mono/tabular where relevant | Tables scroll inside; diagrams simplified | low (layered reveal optional) | Marketing tone over missing specs |
| **CTA** | Decision point after value is shown | Clear action + short reassurance | Single primary action | Full-width button on mobile | low | Repeated identical CTA banner after every section; gradient box by default |
| **FAQ** | Real recurring objections/questions | Questions users actually ask, concise answers | Accordion or two-column Q&A | Accordion on mobile | low (expand/collapse) | Filler FAQ to lengthen page; hiding critical info (price, terms) in accordions |

Rhythm guidance: alternate **open** sections (low density, large type/media) with **dense** ones (grids, specs, comparisons) according to narrative job; do not alternate background colors mechanically to fake rhythm.

Where a row names a `layout.*` id, the structured entry in [story-layouts.md](../storytelling/story-layouts.md) is the source of truth for its mechanics; this table only summarizes section-level fit.
