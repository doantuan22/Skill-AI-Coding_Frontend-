---
id: E73
name: Layout sophistication
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate layout sophistication of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E45 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Layouts are chosen from content and adapt meaningfully across viewports rather than stacking a template.

## Input

Captures at desktop/tablet/mobile; CAPABILITY-PLAN layouts; source layout signals.

## Evidence

grid_layouts, grid_template_areas, container_queries, fluid_type, media_queries.

## Heuristics

Reviewer checks hierarchy, rhythm (open/dense alternation by narrative job) and responsive transformation versus the selected layout entries.

## Pass / fail criteria

PASS: layout matches selected patterns with responsive transformation. WARN: no responsive mechanisms. FAIL: generic template composition.

## Limitations

Sophistication is a judgment; signals only show capability, not quality.

## False positives

Simple single-column products can be sophisticated; judge fit, not complexity.

Fixtures: judged on benchmark implementations; the analyzer provides supporting signals only.
