---
id: E74
name: Pattern consistency
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate pattern consistency of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E46 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Equivalent components and values (radii, shadows, type sizes) converge on tokens.

## Input

Source; component samples in captures.

## Evidence

distinct_radii, distinct_shadows, distinct_font_sizes, css_custom_properties.

## Heuristics

Thresholds: > 6 radii, > 5 shadows, > 12 font sizes indicate drift.

## Pass / fail criteria

PASS: none exceeded. WARN: one exceeded. FAIL: two or more exceeded.

## Limitations

Counts raw values; tokens referenced through variables reduce counts correctly only when values are declared once.

## False positives

Fluid clamp() font sizes count as distinct values.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
