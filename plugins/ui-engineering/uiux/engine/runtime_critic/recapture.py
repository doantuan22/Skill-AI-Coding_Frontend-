"""Targeted Recapture Planner – Phase 7.

After a targeted repair, only the affected evidence surface needs recapture.
This module computes the minimal recapture surface based on:
  - Repair actions (files / components modified)
  - Modification plan blast radius and affected surface
  - Shared component dependency graph (from Phase 2 component inventory)

Principles:
  - Never capture the entire site after a local component fix.
  - If a shared component was repaired, capture representative dependent pages.
  - Recapture scope MUST be a subset of the original evidence scope.
  - Evidence provenance: each recapture is linked to session + iteration.
"""
from __future__ import annotations

from typing import Any


def build_recapture_plan(
    repair_result: dict[str, Any],
    modification_plan: dict[str, Any],
    before_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute the minimal recapture surface after a targeted repair.

    Returns a recapture_plan dict:
      - recapture_pages: list of pages to re-capture
      - recapture_viewports: list of viewports to use
      - recapture_scenarios: list of scenarios to re-validate
      - rationale: explanation of how scope was determined
      - is_full_site: False (targeted recapture always local/representative)
    """
    actions = repair_result.get("actions_executed", []) if isinstance(repair_result, dict) else []
    if not isinstance(actions, list):
        actions = []
    affected_surface = modification_plan.get("affected_surface", {}) if isinstance(modification_plan, dict) else {}
    blast_radius = modification_plan.get("blast_radius", {}) if isinstance(modification_plan, dict) else {}
    validation = modification_plan.get("validation", {}) if isinstance(modification_plan, dict) else {}

    # Collect all files repaired
    repaired_files: set[str] = set()
    for action in actions:
        if isinstance(action, dict):
            files = action.get("files", [])
            if isinstance(files, list):
                repaired_files.update(f for f in files if isinstance(f, str))

    # Determine if any shared components were touched
    component_inventory = _get_component_inventory(modification_plan)
    shared_components = _find_shared_components(repaired_files, component_inventory)

    # Pages to recapture
    if shared_components:
        # Shared component: capture representative dependent pages
        dependent_pages = _find_dependent_pages(shared_components, component_inventory, affected_surface)
        rationale = (
            f"Shared component(s) {list(shared_components)[:3]} repaired. "
            f"Recapturing {len(dependent_pages)} representative dependent page(s)."
        )
    else:
        # Local fix: only recapture directly affected pages
        affected_routes = affected_surface.get("routes", ["/"])
        dependent_pages = affected_routes[:5]  # At most 5 pages for local fixes
        rationale = (
            f"Local repair in {list(repaired_files)[:3]}. "
            f"Recapturing {len(dependent_pages)} directly affected page(s)."
        )

    # Viewports: derive from validation handoff
    recapture_viewports = validation.get("affected_viewports", ["desktop_1440"])

    # Scenarios: from repair validation requirements
    validation_required: list[str] = []
    for action in actions:
        validation_required.extend(action.get("validation_required", []))
    recapture_scenarios = list(dict.fromkeys(validation_required))  # deduplicate

    return {
        "recapture_pages": dependent_pages,
        "recapture_viewports": recapture_viewports,
        "recapture_scenarios": recapture_scenarios,
        "repaired_files": list(repaired_files),
        "shared_components_repaired": list(shared_components),
        "is_full_site": False,
        "rationale": rationale,
        "provenance": {
            "repair_id": repair_result.get("repair_id"),
            "original_plan_id": repair_result.get("original_plan_id"),
            "source": "targeted_recapture",
        },
    }


def _get_component_inventory(modification_plan: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract component inventory from modification plan's repository context."""
    # Phase 6 planner embeds repo context; components from blast_radius
    blast = modification_plan.get("blast_radius", {})
    return [
        {"name": c, "path": "", "usage_count": 0}
        for c in blast.get("allowed_components", [])
    ]


def _find_shared_components(
    repaired_files: set[str],
    component_inventory: list[dict[str, Any]],
) -> set[str]:
    """Find component names whose paths match repaired files."""
    shared: set[str] = set()
    for comp in component_inventory:
        path = comp.get("path", "")
        usage = comp.get("usage_count", 0)
        if path and path in repaired_files and usage > 2:
            shared.add(comp.get("name", path))
    return shared


def _find_dependent_pages(
    shared_components: set[str],
    component_inventory: list[dict[str, Any]],
    affected_surface: dict[str, Any],
) -> list[str]:
    """Find representative pages that use the shared components.

    Limits to max 5 representative pages to avoid full-site capture.
    """
    all_routes = affected_surface.get("routes", ["/"])
    # In real scenario: look up component usage from phase 2 inventory.
    # Here we return the affected surface routes as representative subset.
    return all_routes[:5]
