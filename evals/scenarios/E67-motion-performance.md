---
id: E67
name: Motion performance
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate motion performance of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E39 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Motion and effects do not cause jank or layout instability.

## Input

Source plus runtime probe (cumulative_layout_shift, running animations, blur/backdrop counts).

## Evidence

scroll_listeners (throttling), animated_layout_properties, animated_filters, infinite_animations, will_change; runtime CLS.

## Heuristics

Risk score: unthrottled scroll work +2, layout-property animation +2, animated filters +2, > 2 infinite loops +1, > 10 will-change +1, runtime CLS > 0.1 +3.

## Pass / fail criteria

PASS: risk 0. WARN: 1–2. FAIL: ≥ 3.

## Limitations

No frame-timing measurement (no Lighthouse/profiler is installed); CLS needs a runtime capture.

## False positives

Height animation via grid-rows or interpolate-size is safe but may resemble layout animation in source.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
