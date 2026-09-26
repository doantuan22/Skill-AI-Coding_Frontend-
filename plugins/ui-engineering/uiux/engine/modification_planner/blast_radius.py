"""Blast Radius Calculator: Enforces strict blast radius boundaries.

Evaluates:
- Allowed files and components
- Protected files, routes, and tokens
- Shared component modification impact (usage across multiple pages)
- Component API safety (prop rename/removal/default changes)
- Cross-application impact in monorepos
"""
from __future__ import annotations

from typing import Any


def calculate_blast_radius(
    surface: dict[str, Any],
    scope_info: dict[str, Any],
    change_info: dict[str, Any],
    user_goal: str,
    repo_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Calculate the blast radius and associated risk factors.
    
    Returns:
    {
        "allowed_files": list[str],
        "allowed_components": list[str],
        "protected_files": list[str],
        "protected_routes": list[str],
        "protected_tokens": list[str],
        "max_scope": str,
        "estimated_risk": "low" | "medium" | "high",
        "cross_app_impact": bool,
        "affected_applications": list[str],
        "is_shared_component_elevated": bool,
        "is_component_api_breaking": bool,
        "is_global_breakpoint_modified": bool,
    }
    """
    active_repo = repo_profile or {}
    goal_lower = user_goal.lower()

    allowed_files = list(surface.get("allowed_files", []))
    allowed_components = list(surface.get("allowed_components", []))
    protected_files = list(surface.get("protected_files", []))
    protected_routes = list(surface.get("protected_routes", []))
    protected_tokens = list(surface.get("protected_tokens", []))
    max_scope = scope_info.get("scope", "component")

    # 1. Monorepo cross-app evaluation
    cross_app_impact = False
    affected_applications: list[str] = []
    app_target = scope_info.get("application_target")
    applications = active_repo.get("applications", {})

    if applications and isinstance(applications, dict):
        if app_target:
            affected_applications.append(app_target)
            # Check if allowed_files touch a shared package directory
            for f in allowed_files:
                if any(shared_dir in f.lower() for shared_dir in ("packages/ui", "packages/components", "packages/common", "shared/")):
                    cross_app_impact = True
                    affected_applications = list(applications.keys())
                    break
        else:
            affected_applications = list(applications.keys())
            cross_app_impact = len(affected_applications) > 1

    # 2. Shared component usage evaluation
    is_shared = surface.get("is_shared_component", False)
    usage_count = surface.get("shared_component_usage_count", 1)
    is_shared_elevated = is_shared and usage_count > 1

    # 3. Component API safety check
    is_component_api_breaking = False
    api_breaking_keywords = ("rename prop", "remove prop", "change default", "breaking change", "đổi tên prop", "xóa prop")
    if any(k in goal_lower for k in api_breaking_keywords):
        is_component_api_breaking = True

    # 4. Global breakpoint check
    is_global_breakpoint_modified = False
    if any(k in goal_lower for k in ("breakpoint", "media query breakpoint", "đổi breakpoint")):
        is_global_breakpoint_modified = True

    # 5. Estimate overall blast radius risk
    overall_level = change_info.get("overall_level", "L1")
    if is_component_api_breaking or cross_app_impact or is_global_breakpoint_modified or overall_level == "L3":
        estimated_risk = "high"
    elif is_shared_elevated or len(allowed_files) > 3 or overall_level == "L2":
        estimated_risk = "medium"
    else:
        estimated_risk = "low"

    return {
        "allowed_files": allowed_files,
        "allowed_components": allowed_components,
        "protected_files": protected_files,
        "protected_routes": protected_routes,
        "protected_tokens": protected_tokens,
        "max_scope": max_scope,
        "estimated_risk": estimated_risk,
        "cross_app_impact": cross_app_impact,
        "affected_applications": affected_applications,
        "is_shared_component_elevated": is_shared_elevated,
        "is_component_api_breaking": is_component_api_breaking,
        "is_global_breakpoint_modified": is_global_breakpoint_modified,
    }
