# Design Knowledge System dry-run

- Date: 2026-09-24
- Scope: Capability Resolver on 11 scenario profiles (the 8 required plus hardware launch, AI copilot and editorial publication), the quality analyzer on two fixtures, and the runtime runner with the new options.
- Method: `scripts/resolve_capabilities.py` on `evals/resolver-scenarios/*.json`; `scripts/analyze_design_quality.py` on `evals/fixtures/quality/*`; runner executed against a locally served copy of the `restrained` fixture in a scratch directory.
- Honesty note: no browser capture was produced. Playwright is declared by the fixture's `package.json` but is not installed anywhere on this machine, and nothing was installed.

## Resolver results

| Scenario | Style (primary + scoped secondary) | Layouts | Motion tiers / HIGH | Effects (signature) | Technology | Recipe anchor | Top runner-up (score) |
|---|---|---|---|---|---|---|---|
| premium-ai-saas | calm-futurism + ai-native | hero-dashboard, story-feature-explorer, story-sticky | primitive/M1–M4; none | radial-lighting, noise, depth, edge-highlight (depth) | css, native-js, view-transitions; no new deps | premium-ai-saas | developer-tool (10 vs 18) |
| enterprise-analytics-dashboard | data-dense + enterprise-saas | app-dashboard-shell, app-master-detail, grid-dashboard | M1/M2; none | shadow | css, native-js, view-transitions | enterprise-dashboard | fintech (9 vs 16) |
| creative-agency | creative-agency + experimental | hero-full-bleed, grid-asymmetric, grid-broken | primitive/M1/M3/M4/M5; m5-interactive-shader | mask, clipping, grain, noise (mask) | css, native-js, view-transitions, webgl | creative-agency | y2k (7 vs 19) |
| luxury-ecommerce | luxury + ecommerce-premium | hero-editorial, grid-asymmetric, grid-card-matrix | primitive/M1/M2/M4; none | grain, mask, reflection (grain) | css, native-js, view-transitions | luxury-commerce | tactile (6 vs 21) |
| developer-tool | developer-tool + calm-futurism | hero-centered, story-feature-explorer, story-comparison | primitive/M1–M3; none | noise, edge-highlight, radial-lighting (noise) | css, native-js, view-transitions | developer-tool | minimal (9 vs 13) |
| fintech-dashboard | fintech + data-dense | app-dashboard-shell, app-master-detail, grid-dashboard | M1–M3; none | shadow, gradient (shadow) | css, native-js, view-transitions, waapi | fintech-app | developer-tool (8 vs 13) |
| consumer-productivity | playful + tactile | hero-split, story-alternating, grid-bento, app-canvas, app-sidebar-workspace | primitive/M1/M2/M4; none | shadow, gradient, inner-shadow, contact-shadow, noise (shadow) | css, native-js, view-transitions | consumer-app | modern-saas (9 vs 10) |
| experimental-portfolio | experimental + creative-agency | hero-asymmetric, grid-broken | primitive/M1/M3/M4/M5; m5-interactive-shader | shader, noise, mask, clipping, grain (shader) | css, native-js, view-transitions, webgl | experimental-portfolio | y2k (7 vs 16) |
| hardware-launch | cinematic + spatial | hero-cinematic, story-comparison, story-layered | M1–M5; m5-cinematic-hero | radial-lighting, spotlight, grain, depth, layered-transparency, contact-shadow (depth) | css, native-js, view-transitions | hardware-launch | futuristic (7 vs 13) |
| ai-copilot-app | productivity + ai-native | app-command-driven, app-sidebar-workspace | M1–M3; none | shadow, gradient, noise (shadow) | css, **reuses existing Motion**, native-js | productivity-app | modern-saas (10 vs 12) |
| editorial-publication | editorial + organic | hero-editorial, grid-editorial, grid-magazine, story-timeline | primitive/M1/M4; none | grain, mask (grain) | css, native-js | editorial-publication | swiss (7 vs 16) |

### What the dry-run checked

- **Diversity:** 11 scenarios produced 10 distinct primary styles, no repeated style + layout + signature combination, and a mean pairwise Jaccard similarity below 0.2 (`test_mean_similarity_is_low`). The "bento + gradient + glass" default look appears in no scenario.
- **The user's example** ("futuristic AI, premium, technical, impressive, not flashy") resolved to calm futurism with a scoped AI-native secondary, a product-UI hero, a feature explorer and a sticky demo, radial lighting, noise and depth, fade-rise, shared-element, parallax and a walkthrough, all on CSS/native JS. Cyberpunk, gradient-heavy and glassmorphism were ranked down by the `flashy` avoidance and default-tell penalties.
- **Retrieval gating:** the enterprise dashboard plan loads no cinematic, scroll or graphics files.
- **Technology:** no scenario adds a dependency. The copilot reuses its existing `framer-motion`. A synthetic test confirms an authorized preferred library (GSAP for pinned sections) is chosen only when `allow_new_dependencies` is true, and CSS is used otherwise.

### Issues found during the run and fixed

1. The resolver ignored attribute *conflicts*, so neo-brutalism became the secondary style for a "calm" brand. Added the `CONFLICTS` penalty.
2. A secondary style could introduce the page's high-cost signature effect, and its `avoid_effects` could veto the primary's recommendations. The secondary is now scoped to low/medium supporting effects.
3. Motion lists were uncapped (18 items), with baseline feedback last. Baseline now comes first and the list is capped at 12.
4. The technology order made authorized libraries unreachable, because a native *alternative* always won first. The order is now installed → native preferred → authorized preferred library → native alternative → degrade.
5. The analyzer counted `@supports (backdrop-filter: …)` conditions as usages, which caused E71/E72 false positives. Feature-query conditions are now excluded.
6. Windows consoles could not print UTF-8 output. Both CLIs now reconfigure stdout.

## Analyzer results

| Fixture | Non-passing (as expected) | Passing / review |
|---|---|---|
| `overanimated` | E66, E67, E68, E69, E72, E76, E77, E79 FAIL; E65, E71, E73, E75 WARN | E70, E80 NEEDS_REVIEW; E78 NEEDS_RUNTIME |
| `restrained` | none | E65, E66, E67, E69, E72, E74, E76 PASS; E68, E78 NEEDS_RUNTIME; rest NEEDS_REVIEW |

## Runtime runner

- Dry run with `options.motion_probe: true, reduced_motion: "reduce"`: `DRY_RUN`, strategy `playwright` (package declared).
- Real run against a locally served page: `FAILED` with `BROWSER_LAUNCH_FAILURE / PLAYWRIGHT_IMPORT_FAILURE`, 0 captures. `validate_runtime_evidence.py` reports the session `VALID` (honest failure). No install or download occurred, and the temporary server started for the run was stopped.
- The probe and reduced-motion paths are covered by unit tests (option validation, `node --check` of the generated helper) and by analyzer tests over synthetic probe manifests. **Live execution of the probe remains unverified** until a project with local Playwright is available.
