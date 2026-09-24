# Design quality evals (E65–E80)

These evals judge the **rendered design outcome**. They complement the behavioral evals E01–E64, which judge agent routing, artifacts and gates. The milestone brief numbered them E37–E52, but those IDs were already taken (accessibility E37–E44, Visual Language E45–E52, inspiration E53–E64), so they continue from E65.

| ID | Brief ID | Quality | Mostly deterministic? |
|---|---|---|---|
| [E65](../scenarios/E65-motion-presence.md) | E37 | Motion presence | Partly (static + plan) |
| [E66](../scenarios/E66-motion-consistency.md) | E38 | Motion consistency | Yes (static counts) |
| [E67](../scenarios/E67-motion-performance.md) | E39 | Motion performance | Partly (static risk + runtime CLS) |
| [E68](../scenarios/E68-reduced-motion-support.md) | E40 | Reduced motion support | Yes with a runtime reduce capture |
| [E69](../scenarios/E69-interaction-feedback.md) | E41 | Interaction feedback | Partly |
| [E70](../scenarios/E70-transition-continuity.md) | E42 | Transition continuity | No (review) |
| [E71](../scenarios/E71-visual-effect-quality.md) | E43 | Visual effect quality | No (review + fallbacks) |
| [E72](../scenarios/E72-effect-overuse.md) | E44 | Effect overuse | Yes (budget estimate) |
| [E73](../scenarios/E73-layout-sophistication.md) | E45 | Layout sophistication | No (review) |
| [E74](../scenarios/E74-pattern-consistency.md) | E46 | Pattern consistency | Yes (value drift) |
| [E75](../scenarios/E75-design-style-coherence.md) | E47 | Design style coherence | No (review against plan) |
| [E76](../scenarios/E76-premium-detail-density.md) | E48 | Premium detail density | Partly (detail signals) |
| [E77](../scenarios/E77-scroll-experience.md) | E49 | Scroll experience | Partly (hijack signals) |
| [E78](../scenarios/E78-responsive-motion.md) | E50 | Responsive motion | Yes with desktop and mobile probes |
| [E79](../scenarios/E79-interaction-discoverability.md) | E51 | Interaction discoverability | Partly |
| [E80](../scenarios/E80-composition-quality.md) | E52 | Composition quality | No (review) |

## Pipeline

```text
Implementation
  → runtime capture (scripts/run_browser_execution.py; desktop + mobile; options.motion_probe: true;
                     a second capture with options.reduced_motion: "reduce")
  → static + probe evidence (scripts/analyze_design_quality.py <project> --manifest <session>/manifest.json --visual-intensity N)
  → heuristic review of NEEDS_REVIEW items against CAPABILITY-PLAN and the premium quality model
  → DESIGN-QUALITY-REPORT.md (templates/DESIGN-QUALITY-REPORT.md)
```

Statuses: `PASS`, `WARN`, `FAIL`, `NEEDS_REVIEW` (judgment required) and `NEEDS_RUNTIME` (browser evidence required). They also use `NOT_APPLICABLE` from the framework. A `NEEDS_RUNTIME` status is never converted to `PASS` without a capture. When no browser runtime exists, the report says so and the status stays `NEEDS_RUNTIME` (runner status `BLOCKED`). Nothing is installed to obtain evidence.

## Evidence sources

| Source | Provides |
|---|---|
| `analyze_design_quality.py` signals | Durations/easings, transition-all, layout-property animation, scroll listeners, reduced-motion handlers, effect counts, focus/hover/active rules, value drift, detail signals |
| Runner `motion_probe` (per capture) | Running animations (count, infinite, durations, easings), backdrop/blur/will-change element counts, transition-all elements, cumulative layout shift, whether reduced motion was active |
| Runner `reduced_motion` captures | Screenshot and probe under `prefers-reduced-motion: reduce` |
| CAPABILITY-PLAN / MOTION-SYSTEM | The intended styles, patterns, motion purposes, budget and signature to judge against |

## Validation

`scripts/test_quality_analyzer.py` checks that the analyzer marks the `overanimated` fixture as non-passing on E66, E67, E68, E69, E72, E77 and E79, and gives the `restrained` fixture passing or review statuses.
