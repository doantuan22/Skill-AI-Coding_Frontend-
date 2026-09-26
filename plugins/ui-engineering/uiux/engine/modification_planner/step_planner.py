"""Step Planner: Generates sequential implementation steps, batches, checkpoints, and validation handoff.

Enforces:
- Explicit dependency ordering between steps.
- Execution batches (Tokens -> Structure -> States -> Validation).
- Logical checkpoints for rollback.
- Risk modeling (regression, architecture, preservation, runtime).
- Validation handoff contract before editing commences.
"""
from __future__ import annotations

from typing import Any


def plan_implementation_steps(
    surface: dict[str, Any],
    blast_radius: dict[str, Any],
    change_info: dict[str, Any],
    task_intent: str,
    workflow: str = "existing-ui",
    preservation_profile: dict[str, Any] | None = None,
    user_goal: str = "",
) -> dict[str, Any]:
    """Generate sequential implementation steps, execution batches, checkpoints, and validation handoff.
    
    Returns:
    {
        "implementation_steps": list[dict],
        "validation": dict,
        "rollback": dict,
        "risks": dict,
    }
    """
    allowed_files = blast_radius.get("allowed_files", [])
    primary_file = allowed_files[0] if allowed_files else "src/components/Component.tsx"
    primary_comp = blast_radius.get("allowed_components", ["Component"])[0] if blast_radius.get("allowed_components") else "Component"

    overall_level = change_info.get("overall_level", "L1")
    estimated_risk = blast_radius.get("estimated_risk", "low")
    is_shared = blast_radius.get("is_shared_component_elevated", False)
    is_api_breaking = blast_radius.get("is_component_api_breaking", False)

    steps: list[dict[str, Any]] = []
    checkpoints: list[dict[str, Any]] = []

    # 1. Implementation Steps & Batches
    # Batch A: Shared primitives / Tokens / Component definition
    step_1_id = "step_1"
    steps.append({
        "id": step_1_id,
        "batch": "batch_a",
        "target": primary_file,
        "action": "modify",
        "dependencies": [],
        "risk": "medium" if is_shared else "low",
        "expected_result": f"Refine {primary_comp} structure/styles within authorized L1/L2 scope.",
    })

    cp_1_id = "cp_1"
    checkpoints.append({
        "id": cp_1_id,
        "after_steps": [step_1_id],
        "expected_state": f"{primary_comp} updated cleanly without syntax errors or prop regressions.",
        "validation_required": ["syntax_check", "prop_contract_check"],
    })

    # Batch B: Integration / Structure / Form flow
    if overall_level in ("L2", "L3") or len(allowed_files) > 1 or task_intent in ("page_redesign", "form_ux"):
        step_2_id = "step_2"
        target_file_2 = allowed_files[1] if len(allowed_files) > 1 else primary_file
        steps.append({
            "id": step_2_id,
            "batch": "batch_b",
            "target": target_file_2,
            "action": "modify",
            "dependencies": [step_1_id],
            "risk": "medium" if overall_level == "L2" else "high",
            "expected_result": f"Integrate structural layout changes in {target_file_2}.",
        })

        cp_2_id = "cp_2"
        checkpoints.append({
            "id": cp_2_id,
            "after_steps": [step_2_id],
            "expected_state": "Section hierarchy and layout flow render correctly.",
            "validation_required": ["layout_render_check"],
        })

    # Batch C: Interactive states & Edge cases
    step_3_id = f"step_{len(steps) + 1}"
    last_step_id = steps[-1]["id"]
    steps.append({
        "id": step_3_id,
        "batch": "batch_c",
        "target": primary_file,
        "action": "modify",
        "dependencies": [last_step_id],
        "risk": "low",
        "expected_result": "Implement required states (loading, empty, error, disabled, focus-visible).",
    })

    # If high-risk, add an extra intermediate checkpoint
    if estimated_risk == "high":
        checkpoints.append({
            "id": f"cp_{len(checkpoints) + 1}",
            "after_steps": [step_3_id],
            "expected_state": "All edge case states verified before final validation.",
            "validation_required": ["state_verification"],
        })

    # 2. Validation Handoff
    required_checks = ["smoke_render", "zero_console_errors"]
    affected_viewports = ["desktop_1440"]
    interactions: list[str] = ["keyboard_tab_focus", "button_click"]
    accessibility_checks: list[str] = ["wcag_contrast_minimum_4.5_to_1", "aria_labels_present"]
    preservation_checks: list[str] = []

    goal_lower = user_goal.lower()

    if (
        task_intent == "responsive_fix"
        or "responsive" in primary_file.lower()
        or any(w in goal_lower for w in ("responsive", "mobile", "tablet", "viewport"))
    ):
        affected_viewports = ["desktop_1440", "tablet_768", "mobile_375"]
        required_checks.append("responsive_viewport_matrix")

    if (
        task_intent == "form_ux"
        or any(w in goal_lower for w in ("form", "input", "checkout", "signup", "login"))
    ):
        interactions.extend(["form_input_typing", "field_blur_validation", "submit_handling"])
        required_checks.append("form_interaction_test")

    if (
        task_intent == "accessibility_fix"
        or any(w in goal_lower for w in ("accessibility", "a11y", "contrast", "wcag"))
    ):
        accessibility_checks.extend(["screen_reader_announcements", "colorblind_distinctiveness"])
        required_checks.append("accessibility_axe_audit")

    if workflow == "existing-ui":
        preservation_checks.extend([
            "locked_palette_intact",
            "brand_identity_preserved",
            "global_navigation_untouched",
        ])
        required_checks.append("preservation_invariants_verification")

    validation = {
        "required_checks": required_checks,
        "affected_viewports": affected_viewports,
        "interactions": interactions,
        "accessibility": accessibility_checks,
        "preservation": preservation_checks,
    }

    # 3. Rollback Strategy
    rollback = {
        "strategy": "file_restore_with_checkpoints",
        "checkpoints": checkpoints,
    }

    # 4. Risk Model
    regression_risk = "high" if is_api_breaking else ("medium" if is_shared else "low")
    architecture_risk = "high" if overall_level == "L3" else ("medium" if overall_level == "L2" else "low")
    preservation_risk = "high" if change_info.get("has_palette_violation") else ("medium" if overall_level == "L2" else "low")
    runtime_risk = "high" if estimated_risk == "high" else ("medium" if len(allowed_files) > 2 else "low")

    risks = {
        "regression": regression_risk,
        "architecture": architecture_risk,
        "preservation": preservation_risk,
        "runtime": runtime_risk,
    }

    return {
        "implementation_steps": steps,
        "validation": validation,
        "rollback": rollback,
        "risks": risks,
    }
