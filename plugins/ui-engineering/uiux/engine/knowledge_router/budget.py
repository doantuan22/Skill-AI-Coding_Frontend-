"""Context Budget Manager: Enforces context budgeting, prioritization, and deterministic pruning.

Ensures that the agent's context window is not saturated by irrelevant knowledge,
while strictly guaranteeing that hard constraints and framework packs are never pruned.
"""
from __future__ import annotations

from typing import Any

from uiux.engine.knowledge_router.metadata import WEIGHT_POINTS

DEFAULT_BUDGET_POINTS = 25

# Priority order (higher index = higher priority)
PRIORITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def calculate_points(item: dict[str, Any]) -> int:
    """Return numeric points for an item based on its weight."""
    weight = item.get("weight", "small")
    return WEIGHT_POINTS.get(weight, 1)


class ContextBudgetManager:
    """Manages context budgeting, prioritization, and pruning."""

    def __init__(self, budget_limit_points: int = DEFAULT_BUDGET_POINTS):
        self.budget_limit_points = budget_limit_points

    def apply_budget(
        self,
        items: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
        """Prune items exceeding budget, returning (selected, excluded, budget_info).
        
        Hard rules:
        - Critical priority items are NEVER pruned.
        - Required framework items are NEVER pruned.
        - Pruning starts from lowest priority ('low'), then optional 'medium'.
        """
        # Sort items primarily by priority descending, then by required descending
        def sort_key(it: dict[str, Any]) -> tuple[int, int]:
            prio = PRIORITY_ORDER.get(it.get("priority", "low"), 1)
            req = 1 if it.get("required", False) else 0
            return (prio, req)

        # Separate items into protected (cannot be pruned) and prunable
        protected: list[dict[str, Any]] = []
        candidates: list[dict[str, Any]] = []

        for item in items:
            is_critical = item.get("priority") == "critical"
            is_framework = item.get("category") == "framework" and item.get("required", False)
            is_preservation = item.get("category") == "preservation"
            is_explicit = item.get("category") == "explicit_constraint"

            if is_critical or is_framework or is_preservation or is_explicit:
                protected.append(item)
            else:
                candidates.append(item)

        # Calculate base points for protected items
        used_points = sum(calculate_points(it) for it in protected)
        selected: list[dict[str, Any]] = list(protected)
        excluded: list[dict[str, Any]] = []

        # Sort prunable candidates by priority descending
        candidates.sort(key=sort_key, reverse=True)

        for candidate in candidates:
            pts = calculate_points(candidate)
            if used_points + pts <= self.budget_limit_points:
                selected.append(candidate)
                used_points += pts
            else:
                # Excluded due to budget constraints
                excluded.append({
                    "id": candidate["id"],
                    "category": candidate.get("category", "knowledge"),
                    "reason": f"Context budget exceeded ({used_points}/{self.budget_limit_points} points used; item weight {pts} pts)",
                })

        # Organize by priority
        by_prio: dict[str, list[str]] = {"critical": [], "high": [], "medium": [], "low": []}
        for it in selected:
            prio = it.get("priority", "medium")
            if prio in by_prio:
                by_prio[prio].append(it["id"])

        budget_info = {
            "budget_limit_points": self.budget_limit_points,
            "used_points": used_points,
            "budget_status": "within_budget" if not excluded else "truncated_optional",
            "items_by_priority": by_prio,
        }

        return selected, excluded, budget_info
