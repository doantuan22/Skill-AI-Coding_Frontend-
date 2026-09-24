"""Performance and motion budgets (single source for the resolver and the quality analyzer).

Values come from configuration (``performance_budget`` and ``motion_budget``); defaults reproduce the documented
budgets in phase-2/05-frontend-implementation/performance-budget.md.
"""
from __future__ import annotations

from uiux.core import config


def cost_points() -> dict[str, int]:
    """Cost label -> budget points (none, low, medium, high, very-high)."""
    return dict(config.get()["performance_budget"]["cost_points"])


def effect_budget() -> dict[int, int]:
    """Visual intensity (1..5) -> page effect points."""
    return {int(k): v for k, v in config.get()["performance_budget"]["effect_budget_by_visual_intensity"].items()}


def motion_budget() -> dict[str, int]:
    """max_high_regions, max_motion_patterns, max_interactions, max_section_layouts."""
    return dict(config.get()["motion_budget"])
