---
id: E70
name: Transition continuity
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate transition continuity of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E42 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Objects keep their identity across state and page changes (list→detail, card→modal, navigation).

## Input

MOTION-SYSTEM M3 selections, source, runtime captures of before/after states.

## Evidence

view_transitions, layout_animation_apis counts; reviewer walk-through of the plan's M3 moments.

## Heuristics

For each M3 entry in the plan, verify the implementation preserves the element and moves focus correctly.

## Pass / fail criteria

PASS: all planned continuity moments implemented with reduced fallbacks. FAIL: planned continuity missing or causing lost focus. NEEDS_REVIEW by default.

## Limitations

Screenshots cannot show motion; judgment needs a live walk-through or recorded evidence.

## False positives

Products with no M3 in the plan are NOT_APPLICABLE, not FAIL.

Fixtures: judged on benchmark implementations; the analyzer provides supporting signals only.
