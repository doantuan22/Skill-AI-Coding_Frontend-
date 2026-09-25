---
id: E72
name: Effect overuse
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate effect overuse of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E44 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

The page stays within the effect budget for its visual intensity with one signature effect.

## Input

Source, runtime probe effect counts, CAPABILITY-PLAN visual intensity.

## Evidence

Estimated effect points (backdrop, blur, large shadows, gradients, blend, canvas/WebGL, loops) versus budget.

## Heuristics

Budget by visual intensity 1→2, 2→3, 3→5, 4→8, 5→12 points.

## Pass / fail criteria

PASS: within budget. WARN: ≤ 150% of budget. FAIL: above 150%.

## Limitations

Point estimate counts effect kinds, not rendered area; large single effects may be under-weighted.

## False positives

Gradients used as flat tints inflate counts slightly.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
