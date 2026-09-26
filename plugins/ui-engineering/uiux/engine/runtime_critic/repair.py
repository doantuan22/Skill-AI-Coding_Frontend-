"""Repair Engine – Phase 7.

Builds targeted repair plans derived directly from critic issues.
Routes every repair through Phase 6 Controlled Editing permission/scope gate.

Key principles:
  - Repair blast radius MUST be <= original modification plan blast radius.
  - Never auto-repair PRESERVATION_VIOLATION or PLAN_DRIFT (requires user permission).
  - Each repair plan cites the exact issue_id it addresses.
  - Low confidence repairs are not auto-executed when risk is high.
  - Repair records issue + outcome in repair_history for oscillation detection.
"""
from __future__ import annotations

import uuid
from typing import Any

from uiux.engine.runtime_critic.critic import (
    PRESERVATION_VIOLATION, PLAN_DRIFT,
    NEW_REGRESSION, WORSENED, PRE_EXISTING,
    CRITICAL, HIGH, MEDIUM, LOW, INFO,
    SEVERITY_ORDER,
)

# Categories blocked from auto-repair (need user permission or plan amendment)
NOT_AUTO_REPAIRABLE_CATEGORIES = {PRESERVATION_VIOLATION, PLAN_DRIFT}

# Change level map
L1, L2, L3 = "L1", "L2", "L3"
LEVEL_ORDER = {L1: 1, L2: 2, L3: 3}


class RepairEngine:
    """Builds repair plans and validates them against Phase 6 scope gates."""

    def build_repair_plan(
        self,
        critic_report: dict[str, Any],
        modification_plan: dict[str, Any],
    ) -> dict[str, Any]:
        """Build a targeted repair plan from critic issues and the original modification plan.

        Returns a repair_plan dict with:
          - repair_id
          - original_plan_id
          - repairable_issues (list of issue_ids)
          - blocked_issues (need permission or scope expansion)
          - repair_batches (grouped by root cause)
          - blast_radius_check (stays within original allowed blast radius)
        """
        repair_id = f"repair_{uuid.uuid4().hex[:12]}"
        issues = critic_report.get("issues", [])

        # Filter to actionable new issues only
        actionable = [
            i for i in issues
            if i.get("status") in (NEW_REGRESSION, WORSENED)
            and i.get("repairable", False)
            and i.get("category") not in NOT_AUTO_REPAIRABLE_CATEGORIES
        ]
        blocked = [
            i for i in issues
            if i.get("status") in (NEW_REGRESSION, WORSENED)
            and (not i.get("repairable", False) or i.get("category") in NOT_AUTO_REPAIRABLE_CATEGORIES)
        ]

        original_blast = modification_plan.get("blast_radius", {})
        original_allowed_files = set(original_blast.get("allowed_files", []))
        original_plan_level = modification_plan.get("change_classification", {}).get("overall_level", L1)

        # Build per-issue repair actions
        repair_actions: list[dict[str, Any]] = []
        scope_violations: list[str] = []

        for issue in actionable:
            action = self._build_repair_action(issue, original_allowed_files, original_plan_level)
            if action.get("scope_violation"):
                scope_violations.append(f"Issue {issue['issue_id']}: {action['scope_violation']}")
            else:
                repair_actions.append(action)

        # Group into repair batches by root cause / shared file
        batches = self._group_into_batches(repair_actions)

        # Overall repair status
        if not repair_actions and not blocked:
            repair_status = "nothing_to_repair"
        elif scope_violations:
            repair_status = "scope_expansion_required"
        elif blocked:
            needs_perm = any(i.get("permission_required") for i in blocked)
            repair_status = "needs_permission" if needs_perm else "blocked"
        else:
            repair_status = "ready"

        return {
            "schema_version": 1,
            "repair_id": repair_id,
            "original_plan_id": modification_plan.get("plan_id", ""),
            "repair_status": repair_status,
            "repairable_issue_count": len(repair_actions),
            "blocked_issue_count": len(blocked),
            "scope_violations": scope_violations,
            "repair_actions": repair_actions,
            "blocked_actions": [
                {
                    "issue_id": i["issue_id"],
                    "category": i["category"],
                    "reason": "not_auto_repairable" if i.get("category") in NOT_AUTO_REPAIRABLE_CATEGORIES else "requires_scope_expansion",
                    "permission_required": i.get("permission_required"),
                }
                for i in blocked
            ],
            "repair_batches": batches,
            "blast_radius_constraint": {
                "original_allowed_files": list(original_allowed_files),
                "max_change_level": original_plan_level,
                "constraint": "repair_blast_radius_must_be_subset_of_original",
            },
        }

    def execute_repair(
        self,
        repair_plan: dict[str, Any],
        modification_plan: dict[str, Any],
    ) -> dict[str, Any]:
        """Validate repair plan against Phase 6 scope gate and return execution result.

        In production, this hands off to ControlledEditingEngine.
        In this architecture layer, it validates the plan and returns a result dict
        (actual code modification is handled by the agent via the controlled editor).
        """
        from uiux.engine.modification_planner import evaluate_plan_permissions

        repair_status = repair_plan.get("repair_status")
        if repair_status not in ("ready", "nothing_to_repair"):
            return {
                "status": "blocked",
                "reason": repair_status,
                "repair_id": repair_plan.get("repair_id"),
                "actions_executed": [],
                "introduced_issues": [],
            }

        # Phase 6 scope gate: verify each repair action stays within blast radius
        original_blast = modification_plan.get("blast_radius", {})
        original_allowed = set(original_blast.get("allowed_files", []))
        violations: list[str] = []

        for action in repair_plan.get("repair_actions", []):
            for f in action.get("files", []):
                if original_allowed and f not in original_allowed:
                    violations.append(f"Repair action targets '{f}' outside original blast radius.")

        if violations:
            return {
                "status": "scope_violation",
                "reason": "repair_exceeds_blast_radius",
                "violations": violations,
                "repair_id": repair_plan.get("repair_id"),
                "actions_executed": [],
                "introduced_issues": [],
            }

        # Simulated execution (real code changes are performed by the agent)
        return {
            "status": "executed",
            "repair_id": repair_plan.get("repair_id"),
            "original_plan_id": repair_plan.get("original_plan_id"),
            "actions_executed": [
                {
                    "issue_id": action.get("issue_id"),
                    "target": action.get("target"),
                    "files": action.get("files"),
                    "change_level": action.get("change_level"),
                    "description": action.get("description"),
                }
                for action in repair_plan.get("repair_actions", [])
            ],
            "introduced_issues": [],  # Filled by re-critique after recapture
            "validation_required": repair_plan.get("validation_required", []),
        }

    # ── Private helpers ──────────────────────────────────────────────────────

    def _build_repair_action(
        self,
        issue: dict[str, Any],
        original_allowed_files: set[str],
        original_plan_level: str,
    ) -> dict[str, Any]:
        """Build a single repair action for an issue."""
        issue_id = issue["issue_id"]
        category = issue.get("category", "")
        repair_scope = issue.get("repair_scope", "affected file")
        affected_file = issue.get("affected_file")
        files = [affected_file] if affected_file else []

        # Determine change level for this repair (never exceed original plan level)
        change_level = L1  # Default: all targeted repairs are L1 (local CSS/attr fix)

        # Check if file is in original blast radius
        scope_violation = None
        for f in files:
            if original_allowed_files and f not in original_allowed_files:
                scope_violation = f"Repair target '{f}' outside original blast radius {list(original_allowed_files)[:3]}"

        # Compute confidence
        confidence = _compute_repair_confidence(issue, files, scope_violation)

        return {
            "issue_id": issue_id,
            "target": repair_scope or "affected component",
            "files": files,
            "components": [issue.get("affected_component")] if issue.get("affected_component") else [],
            "change_level": change_level,
            "reason": issue.get("description", ""),
            "evidence": issue.get("evidence", ""),
            "expected_fix": f"Resolve: {issue.get('actual', '')}",
            "validation_required": _repair_validation(issue),
            "confidence": confidence,
            "scope_violation": scope_violation,
        }

    def _group_into_batches(
        self, actions: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Group repair actions by shared root cause (same file = same batch)."""
        file_groups: dict[str, list[dict[str, Any]]] = {}
        no_file: list[dict[str, Any]] = []

        for action in actions:
            files = action.get("files", [])
            if files:
                key = files[0]  # Group by primary file
                file_groups.setdefault(key, []).append(action)
            else:
                no_file.append(action)

        batches: list[dict[str, Any]] = []
        for file, group_actions in file_groups.items():
            batches.append({
                "batch_id": f"repair_batch_{uuid.uuid4().hex[:6]}",
                "root_cause_file": file,
                "issue_count": len(group_actions),
                "action_ids": [a["issue_id"] for a in group_actions],
                "rationale": f"Grouped {len(group_actions)} issue(s) sharing root in '{file}'.",
            })

        if no_file:
            batches.append({
                "batch_id": f"repair_batch_{uuid.uuid4().hex[:6]}",
                "root_cause_file": None,
                "issue_count": len(no_file),
                "action_ids": [a["issue_id"] for a in no_file],
                "rationale": "Issues without a traceable file target.",
            })

        return batches


def _compute_repair_confidence(
    issue: dict[str, Any],
    files: list[str],
    scope_violation: str | None,
) -> str:
    if scope_violation:
        return "low"
    if not files:
        return "low"
    severity = issue.get("severity", INFO)
    if severity in (CRITICAL,):
        return "medium"  # Critical issues may have complex root causes
    if severity == HIGH:
        return "high"
    return "high"


def _repair_validation(issue: dict[str, Any]) -> list[str]:
    """Determine validation checks required after this repair."""
    from uiux.engine.runtime_critic.critic import (
        RESPONSIVE_FAILURE, INTERACTION_FAILURE,
        ACCESSIBILITY_REGRESSION, RUNTIME_ERROR,
    )
    category = issue.get("category", "")
    checks = ["smoke_render", "zero_console_errors"]
    if category == RESPONSIVE_FAILURE:
        checks.append("responsive_viewport_matrix")
    if category == INTERACTION_FAILURE:
        checks.append("interaction_scenario_rerun")
    if category == ACCESSIBILITY_REGRESSION:
        checks.append("accessibility_axe_audit")
    if category == RUNTIME_ERROR:
        checks.append("runtime_error_check")
    return checks
