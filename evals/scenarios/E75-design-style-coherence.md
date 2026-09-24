---
id: E75
name: Design style coherence
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate design style coherence of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E47 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

The rendered result expresses the selected primary style and recipe consistently, at a matching intensity across layers.

## Input

Captures, CAPABILITY-PLAN (style, secondary scope, recipe anchor, signature).

## Evidence

font_families count; reviewer comparison of type, color, surface, motion and effect with the style entry.

## Heuristics

Every layer maps to the style entry fields; the secondary style stays in its declared scope; one signature moment.

## Pass / fail criteria

PASS: coherent. WARN: > 3 font families or minor drift. FAIL: layers express conflicting styles (`STYLE_INCOHERENCE`) or the default tech look without reasons (`HOMOGENIZED_DESIGN`).

## Limitations

Requires the plan; without it, only drift signals are available.

## False positives

Brand-mandated fonts may exceed the family count; record as justified.

Fixtures: judged on benchmark implementations; the analyzer provides supporting signals only.
