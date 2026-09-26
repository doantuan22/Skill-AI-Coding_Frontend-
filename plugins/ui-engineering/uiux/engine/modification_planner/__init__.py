"""Modification Planner & Controlled Editing package.

Provides deterministic planning, blast-radius control, permission gates,
and plan-drift verification for UI modifications.
"""
from __future__ import annotations

from typing import Any

from uiux.engine.modification_planner.controlled_editor import ControlledEditingEngine
from uiux.engine.modification_planner.planner import ModificationPlanner

_PLANNER_INSTANCE: ModificationPlanner | None = None
_EDITOR_INSTANCE: ControlledEditingEngine | None = None


def _get_planner() -> ModificationPlanner:
    global _PLANNER_INSTANCE
    if _PLANNER_INSTANCE is None:
        _PLANNER_INSTANCE = ModificationPlanner()
    return _PLANNER_INSTANCE


def _get_editor() -> ControlledEditingEngine:
    global _EDITOR_INSTANCE
    if _EDITOR_INSTANCE is None:
        _EDITOR_INSTANCE = ControlledEditingEngine()
    return _EDITOR_INSTANCE


def plan_modification(
    user_request: str = "",
    workflow: str = "existing-ui",
    repo_profile: dict[str, Any] | None = None,
    existing_ui_profile: dict[str, Any] | None = None,
    preservation_profile: dict[str, Any] | None = None,
    knowledge_plan: dict[str, Any] | None = None,
    explicit_constraints: dict[str, Any] | None = None,
    requested_scope: str = "global",
    task_intent: str | None = None,
    plan_only: bool = False,
) -> dict[str, Any]:
    """Generate a machine-readable Modification Plan."""
    return _get_planner().plan(
        user_request=user_request,
        workflow=workflow,
        repo_profile=repo_profile,
        existing_ui_profile=existing_ui_profile,
        preservation_profile=preservation_profile,
        knowledge_plan=knowledge_plan,
        explicit_constraints=explicit_constraints,
        requested_scope=requested_scope,
        task_intent=task_intent,
        plan_only=plan_only,
    )


def validate_modification_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate a Modification Plan for structural integrity and policy compliance."""
    errors: list[str] = []
    required_keys = (
        "schema_version", "plan_id", "request", "workflow", "repository",
        "constraints", "preservation", "knowledge", "affected_surface",
        "change_classification", "implementation_steps", "validation",
        "blast_radius", "rollback", "risks", "status", "status_reasons",
    )
    for k in required_keys:
        if k not in plan:
            errors.append(f"Missing required key '{k}' in modification plan.")

    status = plan.get("status")
    valid_statuses = ("ready", "blocked", "needs_permission", "insufficient_context", "read_only")
    if status not in valid_statuses:
        errors.append(f"Invalid plan status '{status}'. Must be one of {valid_statuses}.")

    return {
        "valid": len(errors) == 0,
        "status": status,
        "errors": errors,
    }


def evaluate_plan_permissions(plan: dict[str, Any]) -> dict[str, Any]:
    """Evaluate whether the plan violates any preservation rules or lacks necessary permissions."""
    violations: list[str] = []
    status = plan.get("status", "ready")
    status_reasons = plan.get("status_reasons", [])

    if status in ("blocked", "needs_permission"):
        violations.extend(status_reasons)

    return {
        "authorized": status in ("ready", "read_only"),
        "status": status,
        "violations": violations,
    }


def build_validation_handoff(plan: dict[str, Any]) -> dict[str, Any]:
    """Extract the validation handoff contract from an approved Modification Plan."""
    return dict(plan.get("validation", {}))


def compare_plan_to_changes(
    plan: dict[str, Any],
    actual_changes: list[dict[str, Any]] | dict[str, Any],
) -> dict[str, Any]:
    """Compare the approved modification plan against actual implementation changes."""
    return _get_editor().compare_plan_to_changes(plan, actual_changes)


__all__ = [
    "plan_modification",
    "validate_modification_plan",
    "evaluate_plan_permissions",
    "build_validation_handoff",
    "compare_plan_to_changes",
    "ModificationPlanner",
    "ControlledEditingEngine",
]
