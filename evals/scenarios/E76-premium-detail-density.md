---
id: E76
name: Premium detail density
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate premium detail density of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E48 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Detail quality per the premium quality model: states, focus, numerals, aspect ratios, wrapping, fallbacks.

## Input

Source and captures.

## Evidence

detail_signals: focus_visible, tabular_numerals, text_wrap_balance, aspect_ratio, disabled_styles, busy_or_loading_states, reduced_motion, feature_fallbacks.

## Heuristics

Count present detail signals and review the premium detail checklist.

## Pass / fail criteria

PASS: ≥ 6/8. WARN: 4–5. FAIL: < 4.

## Limitations

Presence of a rule does not prove correct application everywhere.

## False positives

Products without numeric data legitimately lack tabular numerals; mark NOT_APPLICABLE for that signal.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
