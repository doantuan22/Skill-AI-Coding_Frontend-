---
id: E80
name: Composition quality
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate composition quality of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E52 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Style, layout, type, color, motion, interaction and effects form one design language with a clear signature and no default template.

## Input

Captures, CAPABILITY-PLAN, DESIGN-INSPIRATION pattern selection.

## Evidence

three_equal_columns, sections; plan guards (default tells, homogenized); reviewer judgment with the premium quality model.

## Heuristics

Check intensity alignment across layers, one signature, narrative rhythm, anti-homogenization guard.

## Pass / fail criteria

PASS: coherent, content-driven, one signature. WARN: repeated equal-card rows without reasons. FAIL: GENERIC_TEMPLATE_COMPOSITION or HOMOGENIZED_DESIGN.

## Limitations

Composition is judgment-heavy; use at least two reviewers or the adversarial review for benchmark scoring.

## False positives

Three equal cards are correct when content has exactly three equal items; record the reason.

Fixtures: judged on benchmark implementations; the analyzer provides supporting signals only.
