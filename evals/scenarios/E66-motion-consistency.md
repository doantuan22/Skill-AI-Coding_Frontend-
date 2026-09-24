---
id: E66
name: Motion consistency
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate motion consistency of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E38 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Equivalent interactions share duration and easing tokens; no global `transition: all`.

## Input

Source CSS/JS and MOTION-SYSTEM tokens.

## Evidence

distinct_durations_ms, distinct_easings, transition_all; runtime animation timing list.

## Heuristics

Count distinct durations/easings across all motion declarations and compare them with the token set.

## Pass / fail criteria

PASS: ≤ 6 durations, ≤ 4 easings, no `transition: all`. WARN: in between. FAIL: > 9 durations or > 6 easings.

## Limitations

Library presets defined in JS objects may be missed; values in CSS variables are counted where declared.

## False positives

Large design systems with several documented motion tokens may exceed thresholds legitimately; compare against the token table.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
