---
id: E77
name: Scroll experience
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate scroll experience of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E49 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Scroll is never hijacked; scroll motion carries narrative with one HIGH region and mobile simplification.

## Input

Source, captures, MOTION-SYSTEM scroll entries.

## Evidence

wheel_prevent_default, full-page scroll libraries, parallax_signals, scroll_snap_mandatory, scroll_driven_css, intersection_observers.

## Heuristics

Hijack signals fail immediately; parallax and mandatory snapping require justification.

## Pass / fail criteria

PASS: no hijack, ≤ 1 HIGH scroll region, reviewer confirms pacing. WARN: parallax > 2 or mandatory snap. FAIL: scroll hijacking.

## Limitations

Pacing and narrative need a scroll-through by a reviewer.

## False positives

Horizontal carousels with proximity snapping are acceptable and are not counted as mandatory snap.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
