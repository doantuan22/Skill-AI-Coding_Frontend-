---
id: E65
name: Motion presence
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate motion presence of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E37 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Motion exists where it serves a purpose (feedback, state change, orientation), and not where it does not.

## Input

Rendered implementation plus CAPABILITY-PLAN/MOTION-SYSTEM.

## Evidence

Analyzer signals transition_declarations, keyframes, entrance_attributes; runtime probe animations.total; motion plan purposes.

## Heuristics

Interactive controls have transitioned states. Entrance motion is limited to section-level reveals. Every motion in the plan lists a `serves` purpose.

## Pass / fail criteria

PASS: feedback motion present and entrance markers ≤ 12 with purposes recorded. WARN: no motion at all on an interactive product, or many entrance markers. FAIL: motion present without any purpose in the plan (reviewer).

## Limitations

Static scan cannot see motion created by runtime libraries unless imported in source; purposes need the plan.

## False positives

Intentionally static products (e.g., brutalist or documentation sites) WARN and should be marked justified in the report.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
