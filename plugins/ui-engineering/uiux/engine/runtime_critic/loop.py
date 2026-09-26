"""Critic-Repair Loop – Phase 7.

Orchestrates the iterative OBSERVE → COMPARE → CRITIQUE → REPAIR cycle.

Stop conditions (any one is sufficient):
  1. PASS – overall_status = "pass"
  2. max_iterations reached
  3. needs_permission – repair blocked due to L3 scope
  4. scope_expansion_required – repair would exceed blast radius
  5. runtime_unavailable – no browser to re-critique with
  6. repair would touch protected property
  7. oscillation detected – same issue fails repeatedly

Oscillation detection: if the same issue_id appears as a new_regression in
two consecutive iterations, the loop is halted immediately.
"""
from __future__ import annotations

import uuid
from typing import Any

from uiux.engine.runtime_critic.session import RuntimeValidationSession
from uiux.engine.runtime_critic.critic import CriticEngine, NEW_REGRESSION, WORSENED
from uiux.engine.runtime_critic.repair import RepairEngine
from uiux.engine.runtime_critic.recapture import build_recapture_plan

DEFAULT_MAX_ITERATIONS = 3


class CriticRepairLoop:
    """Bounded repair loop with oscillation detection and partial-failure preservation."""

    def __init__(
        self,
        critic_engine: CriticEngine | None = None,
        repair_engine: RepairEngine | None = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ) -> None:
        self.critic_engine = critic_engine or CriticEngine()
        self.repair_engine = repair_engine or RepairEngine()
        self.max_iterations = max(1, max_iterations)

    def run(
        self,
        session: RuntimeValidationSession,
        initial_report: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run the critic-repair loop until a stop condition is met.

        Returns the final critic_report enriched with repair_history and loop metadata.
        """
        repair_history: list[dict[str, Any]] = []
        current_report = initial_report or self.critic_engine.critique(session)
        seen_issue_signatures: list[set[str]] = []  # For oscillation detection

        for iteration in range(1, self.max_iterations + 1):
            overall = current_report.get("overall_status", "fail")

            # Stop condition 1: PASS
            if overall == "pass":
                break

            # Stop condition 5: no runtime for re-critique
            if overall == "blocked" and not session.has_runtime():
                current_report["loop_stop_reason"] = "runtime_unavailable"
                break

            # Build repair plan
            repair_plan = self.repair_engine.build_repair_plan(
                current_report, session.modification_plan
            )
            repair_status = repair_plan.get("repair_status")

            # Stop condition 2/3/4: blocked or needs permission or scope expansion
            if repair_status in ("blocked", "needs_permission", "scope_expansion_required", "nothing_to_repair"):
                current_report["loop_stop_reason"] = f"repair_{repair_status}"
                _record_history(repair_history, iteration, repair_plan, current_report, "stopped")
                break

            # Oscillation detection: check if we've seen the same failing issue signatures before
            current_new_issue_ids = {
                i["issue_id"] for i in current_report.get("issues", [])
                if i.get("status") in (NEW_REGRESSION, WORSENED)
            }
            if seen_issue_signatures and current_new_issue_ids == seen_issue_signatures[-1]:
                current_report["loop_stop_reason"] = "oscillation_detected"
                _record_history(repair_history, iteration, repair_plan, current_report, "oscillation")
                break
            seen_issue_signatures.append(current_new_issue_ids)

            # Execute repair
            repair_result = self.repair_engine.execute_repair(
                repair_plan, session.modification_plan
            )

            _record_history(repair_history, iteration, repair_plan, current_report, repair_result.get("status", "unknown"))

            # If execution was blocked/violated, stop
            if repair_result.get("status") in ("blocked", "scope_violation"):
                current_report["loop_stop_reason"] = f"repair_{repair_result['status']}"
                break

            # Build recapture plan for targeted evidence refresh
            recapture_plan = build_recapture_plan(repair_result, session.modification_plan, session.before_evidence)
            repair_result["recapture_plan"] = recapture_plan

            # In real execution: agent would recapture evidence and re-critique.
            # In test/unit mode: simulate re-critique with updated manifest only.
            # The loop records history and lets the caller decide next steps.
            # For now, check if any introduced issues were found:
            introduced = repair_result.get("introduced_issues", [])
            if introduced:
                # Critic detects repair introduced new issues – re-run critique
                pass  # In real scenario, new evidence would feed a new session

            # After iteration, if we're at max, mark final
            if iteration == self.max_iterations:
                current_report["loop_stop_reason"] = "max_iterations_reached"
                break

        # Enrich final report with loop metadata
        current_report["repair_history"] = repair_history
        current_report["loop_iterations"] = len(repair_history)
        current_report["max_repair_iterations"] = self.max_iterations
        if "loop_stop_reason" not in current_report:
            current_report["loop_stop_reason"] = "pass" if current_report.get("overall_status") == "pass" else "completed"

        return current_report


def _record_history(
    history: list[dict[str, Any]],
    iteration: int,
    repair_plan: dict[str, Any],
    critic_report: dict[str, Any],
    result: str,
) -> None:
    """Record a repair iteration in the history log."""
    new_issues = [
        i["issue_id"] for i in critic_report.get("issues", [])
        if i.get("status") in (NEW_REGRESSION, WORSENED)
    ]
    history.append({
        "iteration": iteration,
        "repair_id": repair_plan.get("repair_id"),
        "issue_ids_addressed": [a["issue_id"] for a in repair_plan.get("repair_actions", [])],
        "result": result,
        "remaining_new_issues": new_issues,
        "introduced_issues": [],  # Populated after re-critique in real scenario
    })
