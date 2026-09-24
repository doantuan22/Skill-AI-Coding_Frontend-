# Inspiration, typography and motion dry-run

- Run type: documentation/routing dry-run. No application or browser was run, and none is claimed.
- Date: 2026-09-24
- Scope: seven required dry-run cases plus two control cases, mapped to E53–E64.
- Method: tag each case with task triggers; match them against `workflow/reference-index.md` (triggers/excludes) using a throwaway script; read the router's inspiration/typography/motion table for the module files beyond each index entry; confirm every loaded file exists; check expected artifacts and forbidden behavior against the scenario metadata.

## Reference loading

| Case | Index entries loaded | Router module files added | Not loaded (by design) | Result |
|---|---|---|---|---|
| Premium technology landing (E53, E61) | design_inspiration, pattern_selection, web_patterns, typography_intelligence, motion_engine, scroll_motion, system, visual_language, button_grammar | archetypes, hero/sections/storytelling/conversion/motion-composition, typography archetypes/selection/display, motion principles/character/reduced-motion/performance-safety | dashboard/tables/forms, reference profiles (no name given) | PASS |
| Developer SaaS/product (E54) | design_inspiration, pattern_selection, web_patterns, typography_intelligence, system, visual_language, button_grammar | technical-type, font-pairing, motion character + microinteractions | scroll_motion (no scroll trigger), cinematic profiles | PASS |
| Editorial product (E55) | design_inspiration, web_patterns, typography_intelligence, craft_review, system, visual_language | body-type, typographic-composition, content patterns, font-selection (Vietnamese) | hero/storytelling, scroll motion | PASS |
| Marketplace/travel | design_inspiration, web_patterns, typography_intelligence, forms, tables, icon_grammar, system, visual_language | content (listing/detail), interaction-patterns, conversion | cinematic hero, sticky storytelling, luxury patterns | PASS after fix |
| Animation-heavy bad UI (E58, E59) | motion_engine, scroll_motion, craft_review, visual_language | motion-review, performance-safety, reduced-motion | design inspiration, web patterns (task is motion-only) | PASS after fix |
| Reference-inspired redesign (E52, E63) | reference_extraction, anti_copying, design_inspiration, full_visual_redesign, typography_intelligence, system, visual_language | matching reference profile entry only | full profile list, fetching the site | PASS |
| Already-good design (E64) | craft_review, visual_language | typography-review, motion-review for the audited dimensions | inspiration engine, patterns, new fonts or libraries | PASS |
| Control: dashboard | dashboard, motion_engine, visual_language | microinteractions, spatial, reduced-motion | hero, storytelling, scroll motion, web patterns | PASS |
| Control: small form | forms, accessibility, motion_engine | microinteractions, reduced-motion | inspiration, web patterns, scroll motion | PASS |

## Issues the dry-run found and fixed

1. `phase_2_pattern_selection` did not trigger on plain `landing-page`/`marketing`. Those triggers were added.
2. `phase_2_design_inspiration` did not trigger for marketplace or editorial work. `marketplace-home` and `editorial` were added.
3. `phase_2_scroll_motion` missed a generic `scroll-effect` trigger. It was added; dashboards and forms are still excluded.

## Behavior checks

| Scenario | Key expectation | Where the contract lives |
|---|---|---|
| E53 | Archetype chosen without a supplied style, with rejected alternatives recorded | design-inspiration/workflow.md, DESIGN-INSPIRATION template |
| E54 | No cinematic or luxury language; mono limited to technical content | archetypes compatibility, font-pairing, motion-character |
| E55 | No card-ified prose; reading measure; Vietnamese verified | content-patterns, body-type, font-selection |
| E56–E57 | Coverage and licence recorded; family limits; display misuse detected | font-selection, font-pairing, typography-review |
| E58–E59 | Budget applied; IntersectionObserver instead of scroll handler; per-pattern reduced equivalents; content visible without JS | motion-principles, performance-safety, reduced-motion, motion-review |
| E60 | `GENERIC_TEMPLATE_COMPOSITION` flagged; blocks mapped to narrative jobs | pattern-selection, storytelling-patterns |
| E61 | One `HIGH` region; static reduced-motion steps; no scroll hijacking | scroll-motion, motion-composition |
| E62 | Existing library reused; `UNNECESSARY_DEPENDENCY` otherwise | motion/README dependencies |
| E63 | Profile gives transferable traits; never-transfer list; distance test | reference-profiles, anti-copying |
| E64 | `KEEP` recorded; no rewrite | typography-review, motion-review, craft-review |

## Result

All cases route to local, selectively loaded modules and keep the Structure Lock boundary. Pattern selection sends content or section changes back to Phase 1. No module needs an external website, a font file or a media asset at runtime. This is a contract dry-run only. A real task with an executable app must still produce browser and accessibility evidence through the existing execution gates.
