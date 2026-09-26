# Phase 7 – Runtime Critic & Repair Loop

## 1. Overview & Core Principles

Phase 7 introduces the **Runtime Critic & Targeted Repair Loop** to the UI Engineering Plugin.

While Phases 1–6 established deep repo/domain understanding, preservation policy enforcement, and bounded implementation planning with controlled editing, Phase 7 answers the ultimate verification question:

> **"Did the actual implementation meet the quality standard, preserve visual identity, avoid regressions, and stay within the approved plan?"**

### Core Principles

1. **Critic Before Completion**: No task is declared complete without evaluating runtime evidence against baselines and invariants.
2. **Pre-Existing vs. New Classification**: Differentiate regressions introduced by the current edit from pre-existing issues in the codebase to prevent false blame and runaway fixes.
3. **Strict Loop Bounding**: The repair loop is strictly bounded (default maximum of 3 iterations). Infinite loops and oscillation between fixes are detected and aborted.
4. **Bounded Targeted Repair**: Repairs must strictly remain within the original Phase 6 modification plan's blast radius and permissions.
5. **No Blind or Silent Fixes**: `PRESERVATION_VIOLATION` and `PLAN_DRIFT` issues are never silently auto-repaired; they require explicit human or orchestrator intervention.
6. **Minimal Targeted Recapture**: Evidence re-capture after a fix targets only the affected pages and viewports, avoiding costly and noisy full-site scans.

---

## 2. Pipeline & Workflow Integration

```text
Modification Plan + Change Manifest (Phase 6)
          │
          ├── Before Evidence (Baseline)
          └── After Evidence (Current Execution)
                    │
                    ▼
          ┌────────────────────────────────────────────────────────┐
          │                  Runtime Critic Engine                 │
          │  uiux.engine.runtime_critic.critic                     │
          │                                                        │
          │  1. Visual Regression Analysis                         │
          │  2. Preservation Invariants Check                      │
          │  3. Responsive & Breakpoint Verification               │
          │  4. Interactive & State Coverage                       │
          │  5. Accessibility Regression Detection                 │
          │  6. Runtime Error & Console Log Inspection             │
          │  7. Plan-Drift & Scope Verification                    │
          │  8. Pre-existing vs New Issue Attribution              │
          └────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                             Critic Report
                     (critic-report.schema.json)
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
          Status: PASS / WARN                 Status: FAIL / BLOCKED
                  │                                   │
                  ▼                                   ▼
          Validation Complete                 Repair Loop Controller
          (Authorized to finalize)            (uiux.engine.runtime_critic.loop)
                                                      │
                                                      ▼
                                              Targeted Repair Plan
                                            (repair-plan.schema.json)
                                                      │
                                       ┌──────────────┴──────────────┐
                                       ▼                             ▼
                                Repairable Issues            Blocked Violations
                                (Scoped CSS/DOM/Tokens)     (Preservation, Drift, L3)
                                       │                             │
                                       ▼                             ▼
                                Targeted Patch               Halt & Escalate
                                       │
                                       ▼
                               Minimal Evidence Recapture
                            (uiux.engine.runtime_critic.recapture)
                                       │
                                       ▼
                             (Loop back to Critic,
                              max iterations: 3)
```

---

## 3. Seven Inspection Dimensions

The `RuntimeCritic` inspects runtime evidence across seven distinct dimensions:

| Dimension | Focus & Detection | Severity |
|---|---|---|
| **Visual Regression** | Unintended shifts in layout, spacing, typography, colors, or structural element appearance compared to baseline. | CRITICAL / WARNING |
| **Preservation Violation** | Breaches of protected tokens, locked layouts, brand assets, or invariant components defined in Phase 3. | CRITICAL (Never auto-repaired) |
| **Responsive Failure** | Horizontal overflow, text clipping, broken flex/grid wrapping, or overlapping interactive targets across desktop/tablet/mobile viewports. | CRITICAL / WARNING |
| **Interaction & State** | Missing or broken loading, empty, error, active, focus, or hover states required by domain packs (Phase 5). | WARNING / INFO |
| **Accessibility Regression**| Contrast ratio drops below WCAG 2.1 AA (4.5:1 / 3:1), missing ARIA labels on new interactive elements, broken keyboard tab order. | CRITICAL / WARNING |
| **Runtime Errors** | Unhandled JS exceptions, console errors, failed network requests, or unhandled promise rejections during execution. | CRITICAL |
| **Plan Drift** | Modifications made outside `allowed_files` or `allowed_components`, or change levels exceeding permitted L1/L2/L3 permissions. | CRITICAL (Never auto-repaired) |

---

## 4. Pre-Existing vs. New Issue Attribution

A critical capability of the Critic is **provenance attribution**:
- If an issue (e.g. an accessibility contrast warning or an existing console log) existed in `before_evidence`, it is classified as `is_preexisting: True` and assigned `origin: "pre_existing"`.
- If an issue is newly introduced by the edit session, it is classified as `is_preexisting: False` and assigned `origin: "new_regression"`.
- Pre-existing issues do not block the current modification from completion unless they directly violate a newly specified hard requirement.

---

## 5. Targeted Repair & Scope Guardrails

The `RepairPlanner` converts detected issues into bounded, executable repair actions:

1. **Blast Radius Check**: Every repair action must target a file within the original plan's `allowed_files` or components in `allowed_components`.
2. **Blocked Categories**:
   - `PRESERVATION_VIOLATION`: Auto-repair could further degrade design identity; flagged for developer review.
   - `PLAN_DRIFT`: Indicates unauthorized editing; requires plan update or rollback, not auto-patching.
   - `L3 Permission Required`: Actions requiring high-risk changes (e.g., modifying global design tokens) cannot be executed without explicit authorization.
3. **Iteration Control**:
   - Loop tracks history with fingerprint hashing of issues.
   - If the same issues persist across consecutive iterations (oscillation/divergence), the loop halts immediately with `DIVERGENCE_DETECTED`.

---

## 6. Minimal Targeted Evidence Recapture

Following an applied repair, the `recapture_evidence` tool computes the exact minimal surface to re-verify:
- **Local Component Fixes**: Re-captures only the pages hosting the component and the affected viewports (e.g., mobile viewport for a responsive overflow fix).
- **Shared / Layout Fixes**: Re-captures a representative subset of dependent pages rather than the entire application.
- **Never Full-Site by Default**: Full-site recapture is disabled for targeted repairs unless all routes were modified.

---

## 7. Public API & Tool Registration

All capabilities are exposed via the stable `uiux.api` contract and registered in `tools.json`:

```python
from uiux import api

# Run complete critic + validation session
report = api.run_runtime_validation(
    modification_plan=plan,
    change_manifest=manifest,
    before_evidence=before_ev,
    after_evidence=after_ev,
    workflow="existing-ui",
    max_repair_iterations=3,
)

# Evaluate report for gating
result = api.evaluate_runtime_result(report)
if result["authorized_to_proceed"]:
    print("Implementation verified successfully.")
else:
    # Build targeted repair plan
    repair_plan = api.build_repair_plan(report, plan)
    
    # Execute repair through scope gate
    repair_result = api.run_targeted_repair(repair_plan, plan)
    
    # Compute minimal recapture
    recapture_plan = api.recapture_evidence(repair_result, plan, before_ev)
```

---

## 8. Test Verification

Phase 7 is backed by comprehensive automated test coverage:
- **`tests/test_runtime_critic.py`**: 58 test cases covering critic dimensions, evidence delta comparison, pre-existing issue filtering, repair plan creation, scope gating, loop termination, and divergence detection.
- **Full Phase 1–7 Regression Suite**: 246 tests passing across all engine subsystems.
- **Contract & Self-Test Suite**: 84 tests passing across registries, schemas, and public API boundaries.
