# Product storytelling patterns

Narratives that organize sections so layout serves meaning. Pick one primary narrative per page; a secondary may govern a sub-section. The narrative must use locked content; missing content is a Phase 1/content request, not invention.

| Narrative | Structure | Best for | Layout realization | Failure |
|---|---|---|---|---|
| **problem → solution** | Name a recognizable pain → show the product resolving it → proof | New categories, tools replacing manual work | Problem in text-led section (low density) → product UI/visual → metric/testimonial | Exaggerated or invented pain; solution never shown concretely |
| **capability → evidence** | Claim a capability → immediately prove it (UI, code, metric, quote) | SaaS, developer, technical platforms | Claim headline + adjacent proof block per capability; feature-alternating or technical-detail | Claims with no evidence; evidence far from claim |
| **feature → benefit** | What it does → why it matters to this audience | Consumer tech, SaaS | Feature name small, benefit as headline | Feature lists without outcomes |
| **visual demonstration** | Show usage steps or result visually | Visual products, design tools, hardware | Media-dominant sections, short captions | Decorative visuals that don't demonstrate |
| **progressive product reveal** | Reveal the product layer by layer (exterior → interior → detail → specs) | Premium hardware, flagship launches | cinematic-product → sticky-storytelling → technical-detail | Using it without enough media; hiding specs entirely |
| **technical deep-dive** | Overview → architecture → components → performance → docs | Infrastructure, APIs, developer platforms | Section navigation, diagrams, code, comparison | Marketing fluff; no path to docs |
| **before/after** | Show state without and with product | Editing tools, optimization, renovation, cleanup | Comparison slider or side-by-side pairs | Fake or unequal comparisons |
| **comparison** | Place options side-by-side to support choice | Pricing tiers, product lines, alternatives | Comparison table/cards with recommended option | Dishonest competitor claims |

## Selection

1. What does the audience doubt most? (capability → evidence for skeptics; problem → solution for unaware; comparison for evaluators.)
2. What evidence exists? (media → visual demonstration/progressive reveal; UI/code → capability → evidence; data → metric-story.)
3. What is the page goal? (convert → end at decision with reassurance; inform → end at next resource.)

Flag `VISUAL_STORYTELLING_WEAK` when sections are interchangeable claims with no progression or claims lack nearby evidence.
