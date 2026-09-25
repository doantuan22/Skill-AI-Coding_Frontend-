---
id: E79
name: Interaction discoverability
category: design-quality
project_state: rendered implementation with CAPABILITY-PLAN and optional runtime evidence
user_request: Evaluate interaction discoverability of the implemented interface.
expected_route: Phase 2 → implementation → runtime capture (runner, optional motion_probe/reduced_motion) → analyze_design_quality → heuristic review → DESIGN-QUALITY-REPORT
required_artifacts: [CAPABILITY-PLAN, DESIGN-QUALITY-REPORT]
forbidden_behavior: [install-browser-or-tools, claim-visual-pass-without-evidence, score-taste-without-criteria]
expected_context: [evals/quality/README, knowledge/composition/premium-quality-model, analyze_design_quality]
success_conditions: [evidence-recorded, heuristic-status-assigned, limitations-stated, false-positives-considered]
failure_conditions: [fake-visual-pass, missing-evidence, unexplained-score]
---

Requested as E51 in the milestone brief; renumbered because E37–E64 were already in use.

## Purpose

Hidden interactions (hover-only, gestures, shortcuts, custom cursors) have visible cues and alternatives.

## Input

Source, captures, manual keyboard/touch pass.

## Evidence

hover_rules vs focus rules, custom_cursor_none, keyboard_handlers; plan interaction list.

## Heuristics

Each planned gesture/shortcut has a visible control or hint; hover affordances have focus/touch equivalents.

## Pass / fail criteria

PASS: all interactions discoverable. WARN: native cursor hidden. FAIL: hover-only affordances or gesture-only actions.

## Limitations

Gesture discoverability needs manual review on touch.

## False positives

Decorative hover effects without meaning do not need focus equivalents.

Fixtures: [`fixtures/quality/overanimated`](../fixtures/quality/overanimated/index.html) (expected non-PASS) and [`fixtures/quality/restrained`](../fixtures/quality/restrained/index.html) (expected PASS or review).
