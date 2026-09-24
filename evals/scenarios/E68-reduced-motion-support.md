---
id: E68
name: Reduced motion support
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate reduced motion support of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E40 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

All non-essential motion has a `prefers-reduced-motion` equivalent and content stays visible.

## Input

Source; runner capture with `options.reduced_motion: reduce` and motion probe.

## Evidence

reduced_motion_queries, library hooks; runtime infinite animations under reduce; screenshot of reduced capture.

## Heuristics

Motion present → a reduced-motion handler must exist; under reduce, no infinite decorative loops and no content stuck invisible.

## Pass / fail criteria

PASS: handlers exist and runtime reduce capture shows no decorative loops. NEEDS_RUNTIME: handlers exist, no reduce capture. FAIL: motion without handlers. WARN: loops still running under reduce.

## Limitations

Cannot prove each individual pattern has an equivalent; the reviewer checks MOTION-SYSTEM's reduced-motion table.

## False positives

Essential progress indicators legitimately keep animating under reduce.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
