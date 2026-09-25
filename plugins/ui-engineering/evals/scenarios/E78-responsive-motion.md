---
id: E78
name: Responsive motion
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate responsive motion of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E50 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Motion adapts per device: desktop full, mobile reduced, low-power minimal, reduced motion honored.

## Input

Runner captures at desktop and mobile with motion_probe; source media queries.

## Evidence

Runtime running animations desktop vs mobile; hover/pointer media queries; reduced-motion handlers.

## Heuristics

Mobile must not run more motion than desktop; heavy effects degrade on mobile.

## Pass / fail criteria

PASS: mobile ≤ desktop and heavy effects degraded. WARN: mobile runs more. NEEDS_RUNTIME without probes.

## Limitations

Low-power behavior cannot be emulated by the runner; review code paths.

## False positives

Mobile-specific UI (e.g., sheets) can legitimately add small spatial motions.

Fixtures: judged on benchmark implementations; the analyzer provides supporting signals only.
