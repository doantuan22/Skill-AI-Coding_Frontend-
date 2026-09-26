"""Plan Consistency Validator: Pre-execution semantic & structural validation of Modification Plans.

Enforces:
1. Requirement Coverage: Every user requirement mapped to IMPLEMENT/ALREADY_SATISFIED/BLOCKED/DEFERRED/OUT_OF_SCOPE.
2. Requirement Trace: requirement -> affected surface -> file/component -> step -> change level -> validation.
3. Blast Radius Consistency: step targets ⊆ allowed_files/allowed_components (blocks PLAN_INTERNAL_CONTRADICTION).
4. File Existence Contract: Every file is EXISTING_FILE or PLANNED_CREATE (blocks ungrounded_target_file).
5. Framework & Styling Consistency: No tailwind.config.js or React files on static HTML / plain CSS repos.
6. Change Level Consistency: L1 cannot alter palette; L2 requires justification; L3 requires explicit permission.
7. Validation Coverage: Responsive -> viewports; Modal/Interactions -> interaction tests; Motion -> reduced-motion.
"""
from __future__ import annotations

import re
from typing import Any

COMMON_REQUIREMENT_PATTERNS = [
    ("sidebar", r"\b(sidebar|menu\s+drawer|collapsible\s+nav)\b"),
    ("navigation", r"\b(navbar|navigation|header\s+nav|tabs)\b"),
    ("table", r"\b(table|data\s+table|grid\s+table|list\s+view)\b"),
    ("search", r"\b(search|search\s+input|command\s+palette)\b"),
    ("filter", r"\b(filter|filtering|chips?|sort)\b"),
    ("modal", r"\b(modal|dialog|popup|slide-over|drawer)\b"),
    ("drawer", r"\b(drawer|slide-over)\b"),
    ("loading", r"\b(loading|skeleton|spinner)\b"),
    ("empty", r"\b(empty\s+state|no\s+data|placeholder)\b"),
    ("error", r"\b(error\s+state|validation\s+error|alert)\b"),
    ("responsive", r"\b(responsive|mobile|tablet|viewport)\b"),
    ("motion", r"\b(animate|animated|animation|transition|transitions|motion|stagger)\b"),
]


def extract_explicit_requirements(user_goal: str) -> list[str]:
    """Extract discrete UI feature requirements from prompt."""
    reqs: list[str] = []
    goal_lower = user_goal.lower()
    for req_name, pattern in COMMON_REQUIREMENT_PATTERNS:
        if re.search(pattern, goal_lower) and req_name not in reqs:
            reqs.append(req_name)
    return reqs


def validate_plan_consistency(
    plan: dict[str, Any],
    repo_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run comprehensive plan consistency validation before controlled editing."""
    issues: list[str] = []
    active_repo = repo_profile or plan.get("repository", {})
    user_goal = plan.get("request", {}).get("user_goal", "")
    workflow = plan.get("workflow", "existing-ui")
    
    surface = plan.get("affected_surface", {})
    allowed_files = set(surface.get("allowed_files", []) or plan.get("blast_radius", {}).get("allowed_files", []))
    allowed_components = set(surface.get("allowed_components", []) or plan.get("blast_radius", {}).get("allowed_components", []))
    protected_files = set(surface.get("protected_files", []) or plan.get("blast_radius", {}).get("protected_files", []))
    
    planned_files_meta = surface.get("planned_files", [])
    planned_file_paths = {pf["path"] for pf in planned_files_meta if isinstance(pf, dict) and pf.get("planned_create")}

    steps = plan.get("implementation_steps", [])
    validation = plan.get("validation", {})
    change_class = plan.get("change_classification", {})
    overall_level = change_class.get("overall_level", "L1")

    # 1. Requirement Coverage & Traceability
    explicit_reqs = extract_explicit_requirements(user_goal)
    req_coverage: list[dict[str, Any]] = []
    
    step_descriptions = " ".join(
        f"{s.get('id', '')} {s.get('title', '')} {s.get('description', '')} {s.get('target', '')} {s.get('expected_result', '')}"
        for s in steps
    ).lower()
    allowed_comps_lower = {c.lower() for c in allowed_components}
    allowed_files_lower = {f.lower() for f in allowed_files}

    req_pat_map = dict(COMMON_REQUIREMENT_PATTERNS)

    for req in explicit_reqs:
        pat = req_pat_map.get(req, req)
        # Check if covered in allowed surface or steps
        is_in_surface = any(re.search(pat, c) for c in allowed_comps_lower) or any(re.search(pat, f) for f in allowed_files_lower)
        is_in_steps = bool(re.search(pat, step_descriptions))
        is_in_validation = bool(
            req in ("responsive", "motion")
            and (validation.get("affected_viewports") or "responsive" in step_descriptions or "motion" in step_descriptions)
        )
        
        # Check if mention is purely a prepositional container/location (e.g. 'button on navbar', 'icon in sidebar')
        is_container_context = bool(re.search(r"\b(?:on|in|inside|within|at|trên|trong|tại)\s+(?:the\s+)?(?:" + pat + r")\b", user_goal.lower()))

        if is_in_surface or is_in_steps or is_in_validation:
            status = "IMPLEMENT"
        elif is_container_context:
            # Mentioned only as a parent location / container for the scoped component
            status = "OUT_OF_SCOPE"
        elif active_repo.get("components") and any(re.search(pat, (c.get("name", "") if isinstance(c, dict) else str(c)).lower()) for c in active_repo.get("components", [])):
            # Present in repo inventory already
            status = "ALREADY_SATISFIED"
        else:
            # Dropped requirement without explicit deferral
            status = "BLOCKED"
            issues.append(f"unaddressed_requirement: Requirement '{req}' was requested by user but omitted from allowed surface and implementation steps.")
        
        req_coverage.append({
            "requirement": req,
            "status": status,
            "mapped_component": next((c for c in allowed_components if re.search(pat, c.lower())), None),
            "mapped_file": next((f for f in allowed_files if re.search(pat, f.lower())), None),
            "step_count": sum(1 for s in steps if re.search(pat, str(s).lower())),
        })

    # 2. Blast Radius & Step Target Consistency
    blast_radius_issues: list[str] = []
    for step in steps:
        target = step.get("target", "")
        if not target:
            continue
        # Step target must be in allowed_files or planned_files
        if target not in allowed_files and target not in planned_file_paths:
            msg = f"Step '{step.get('id')}' targets '{target}' which is outside allowed_files {list(allowed_files)}."
            blast_radius_issues.append(msg)
            issues.append(f"PLAN_INTERNAL_CONTRADICTION: {msg}")

    # 3. File Existence & Grounding Contract
    from uiux.engine.modification_planner.surface_resolver import _collect_repo_files
    known_repo_files = set(_collect_repo_files(active_repo))
    has_explicit_files = "files" in active_repo or "ui_files" in active_repo
    file_grounding_issues: list[str] = []

    if has_explicit_files and known_repo_files:
        all_plan_files = allowed_files | protected_files | {s.get("target") for s in steps if s.get("target")}
        for f in all_plan_files:
            if f not in known_repo_files and f not in planned_file_paths:
                msg = f"ungrounded_target_file: File '{f}' does not exist in repository and is not marked planned_create."
                file_grounding_issues.append(msg)
                issues.append(msg)

    # 4. Framework & Styling Consistency
    framework_name = active_repo.get("framework", {}).get("name", "") if isinstance(active_repo.get("framework"), dict) else ""
    styling_primary = active_repo.get("styling_system", {}).get("primary", "") if isinstance(active_repo.get("styling_system"), dict) else ""
    
    if styling_primary == "plain_css":
        for f in (allowed_files | protected_files):
            if "tailwind" in f.lower():
                issues.append(f"Framework inconsistency: Plain CSS repository contains Tailwind config target '{f}'.")
    
    if framework_name == "static_html":
        for f in allowed_files:
            if f.endswith((".tsx", ".jsx")) and f not in known_repo_files and f not in planned_file_paths:
                issues.append(f"Framework inconsistency: Static HTML repository contains hallucinated React target '{f}'.")

    # 5. Permission & Change Level Consistency
    permission_issues: list[str] = []
    
    # Check L2 justification
    if overall_level == "L2" or any(c.get("change_level") == "L2" or c.get("level") == "L2" for c in change_class.get("changes", [])):
        has_justification = False
        for c in change_class.get("changes", []):
            if (c.get("change_level") == "L2" or c.get("level") == "L2") and str(c.get("justification", "")).strip():
                has_justification = True
                break
        if not has_justification:
            msg = "missing architectural justification: L2 change level requested without justification."
            permission_issues.append(msg)
            issues.append(msg)

    # Check L3 authorization
    if overall_level == "L3" or any(c.get("change_level") == "L3" or c.get("level") == "L3" for c in change_class.get("changes", [])):
        perm_level = plan.get("preservation", {}).get("permission_level")
        if perm_level != "L3" or change_class.get("has_unauthorized_l3"):
            msg = "exceeds authorized preservation level: L3 change level requested but lacks explicit authorization."
            permission_issues.append(msg)
            issues.append(msg)

    if change_class.get("has_palette_violation"):
        msg = "Palette change attempted while palette is locked."
        permission_issues.append(msg)
        issues.append(msg)

    # 6. Validation Coverage
    validation_coverage: dict[str, Any] = {
        "has_viewport_validation": len(validation.get("affected_viewports", [])) > 1 or any("viewport" in c for c in validation.get("checks", [])),
        "has_interaction_validation": len(validation.get("required_interactions", [])) > 0 or any("interaction" in c for c in validation.get("checks", [])),
        "has_accessibility_validation": len(validation.get("accessibility_checks", [])) > 0 or any("accessibility" in c for c in validation.get("checks", [])),
        "has_reduced_motion_validation": "prefers-reduced-motion" in str(validation) or "reduced_motion" in str(validation),
    }

    # Check required validation types for specific changes
    all_step_texts = " ".join(str(s.get("description", "")) + " " + str(s.get("expected_result", "")) for s in steps).lower()
    user_goal_lower = user_goal.lower()

    # Motion validation requirement
    if any(k in all_step_texts or k in user_goal_lower for k in ("animation", "motion", "stagger", "transition")):
        if not validation_coverage["has_reduced_motion_validation"]:
            issues.append("reduced_motion validation missing: motion steps require prefers-reduced-motion validation.")

    # Modal/dialog interaction validation requirement
    if any(k in all_step_texts or k in user_goal_lower for k in ("modal", "dialog", "drawer", "popup")):
        if not validation_coverage["has_interaction_validation"]:
            issues.append("interaction validation missing: modal/dialog changes require interaction and focus validation.")

    is_valid = len(issues) == 0

    return {
        "valid": is_valid,
        "issues": issues,
        "requirement_coverage": req_coverage,
        "file_grounding": {
            "valid": len(file_grounding_issues) == 0,
            "issues": file_grounding_issues,
        },
        "blast_radius_consistency": {
            "valid": len(blast_radius_issues) == 0,
            "issues": blast_radius_issues,
        },
        "permission_consistency": {
            "valid": len(permission_issues) == 0,
            "issues": permission_issues,
        },
        "validation_coverage": validation_coverage,
    }
