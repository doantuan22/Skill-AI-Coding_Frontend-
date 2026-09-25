---
id: E71
name: Visual effect quality
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate visual effect quality of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E43 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Effects serve their stated visual purpose with good contrast, no banding and proper fallbacks.

## Input

Captures (desktop/mobile), source, CAPABILITY-PLAN effect list.

## Evidence

backdrop_filters with/without @supports, reduced_transparency handling, blend_modes; screenshot inspection.

## Heuristics

Each effect maps to a planned effect id; text over effects meets contrast; translucency has fallbacks.

## Pass / fail criteria

PASS: planned, purposeful, contrast-safe, with fallbacks. WARN: missing fallbacks. FAIL: text contrast broken by an effect.

## Limitations

Banding and contrast over dynamic backgrounds need visual inspection of captures.

## False positives

Browser-default rendering differences may exaggerate banding in screenshots.

Fixtures: judged on benchmark implementations; the analyzer provides supporting signals only.
