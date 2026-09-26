"""Runtime Critic Engine – Phase 7.

Core concept:
  Modification Plan  →  Controlled Editing  →  Change Manifest
       ↓
  Runtime Execution  →  Before / After Evidence
       ↓
  Critic   (visual_regression | preservation | responsive | interaction |
             accessibility | runtime_error | plan_drift | missing_required_state)
       ↓
  Critic Report  →  Repair Decision  →  Targeted Repair  →  Targeted Recapture
       ↓
  Re-critique  →  Final Validation

Principles:
  OBSERVE → COMPARE → CRITIQUE → REPAIR ONLY VERIFIED FAILURES
  → RECAPTURE ONLY AFFECTED EVIDENCE → STOP WHEN PASS OR BUDGET EXHAUSTED

This package is the public entry for Phase 7. All external callers
use only the functions exposed here.
"""
from __future__ import annotations

from uiux.engine.runtime_critic.session import RuntimeValidationSession
from uiux.engine.runtime_critic.critic import CriticEngine
from uiux.engine.runtime_critic.repair import RepairEngine
from uiux.engine.runtime_critic.loop import CriticRepairLoop

__all__ = [
    "RuntimeValidationSession",
    "CriticEngine",
    "RepairEngine",
    "CriticRepairLoop",
    "run_runtime_validation",
    "build_critic_report",
    "evaluate_runtime_result",
    "build_repair_plan",
    "run_targeted_repair",
    "recapture_evidence",
]


def run_runtime_validation(
    modification_plan: dict,
    change_manifest: dict | None = None,
    before_evidence: dict | None = None,
    after_evidence: dict | None = None,
    workflow: str = "existing-ui",
    validate_only: bool = False,
    max_repair_iterations: int = 3,
) -> dict:
    """Top-level entry: run validation session and return a full critic report.

    Args:
        modification_plan: Phase 6 ModificationPlan.
        change_manifest: Phase 6 ChangeManifest (actual changes).
        before_evidence: Runtime evidence captured before editing.
        after_evidence: Runtime evidence captured after editing.
        workflow: "greenfield" or "existing-ui".
        validate_only: If True, no repairs are attempted.
        max_repair_iterations: Maximum repair loop iterations.

    Returns:
        critic_report dict.
    """
    session = RuntimeValidationSession(
        modification_plan=modification_plan,
        change_manifest=change_manifest,
        before_evidence=before_evidence,
        after_evidence=after_evidence,
        workflow=workflow,
    )
    engine = CriticEngine()
    report = engine.critique(session)

    if validate_only:
        report["validate_only"] = True
        return report

    loop = CriticRepairLoop(
        critic_engine=engine,
        repair_engine=RepairEngine(),
        max_iterations=max_repair_iterations,
    )
    return loop.run(session, report)


def build_critic_report(session_data: dict) -> dict:
    """Build a critic report from a pre-assembled session data dict."""
    from uiux.engine.runtime_critic.session import RuntimeValidationSession
    from uiux.engine.runtime_critic.critic import CriticEngine

    session = RuntimeValidationSession.from_dict(session_data)
    return CriticEngine().critique(session)


def evaluate_runtime_result(critic_report: dict) -> dict:
    """Evaluate an already-built critic report for overall pass/fail/blocked status."""
    overall = critic_report.get("overall_status", "fail")
    issues = critic_report.get("issues", [])
    critical_issues = [i for i in issues if i.get("severity") in ("HIGH", "CRITICAL") and i.get("status") != "pre_existing"]
    return {
        "authorized_to_proceed": overall in ("pass", "warn"),
        "overall_status": overall,
        "critical_issue_count": len(critical_issues),
        "repair_required": overall in ("warn", "fail") and any(i.get("repairable") for i in issues),
        "blocked": overall == "blocked",
    }


def build_repair_plan(critic_report: dict, modification_plan: dict) -> dict:
    """Build a targeted repair plan from a critic report and the original modification plan."""
    return RepairEngine().build_repair_plan(critic_report, modification_plan)


def run_targeted_repair(
    repair_plan: dict,
    modification_plan: dict,
) -> dict:
    """Execute a targeted repair plan through Phase 6 Controlled Editing gate."""
    return RepairEngine().execute_repair(repair_plan, modification_plan)


def recapture_evidence(
    repair_result: dict,
    modification_plan: dict,
    before_evidence: dict | None = None,
) -> dict:
    """Determine the minimal recapture surface after a repair and return a recapture plan."""
    from uiux.engine.runtime_critic.recapture import build_recapture_plan
    return build_recapture_plan(repair_result, modification_plan, before_evidence)
