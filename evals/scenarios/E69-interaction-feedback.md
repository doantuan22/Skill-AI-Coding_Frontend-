---
id: E69
name: Interaction feedback
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate interaction feedback of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E41 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Every interactive element has hover (fine pointer), focus-visible, pressed, disabled and loading feedback as applicable.

## Input

Source plus manual keyboard pass or accessibility runtime.

## Evidence

hover_rules, focus_visible_rules, focus_rules, active_rules, outline_none, interactive_elements, aria_live.

## Heuristics

Focus styling must exist wherever interactive elements exist; outline removal needs a focus-visible replacement; pressed state exists.

## Pass / fail criteria

PASS: focus-visible and active present. WARN: no pressed state. FAIL: no focus styling or outline removed without replacement.

## Limitations

Component libraries that style focus internally may appear missing in project CSS.

## False positives

Projects relying on browser default focus rings may FAIL the heuristic while still accessible; verify with the accessibility gate.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
