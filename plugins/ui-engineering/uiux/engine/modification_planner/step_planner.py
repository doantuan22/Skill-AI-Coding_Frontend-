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
    knowledge_plan: dict[str, Any] | None = None,
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

    selected_knowledge = knowledge_plan.get("selected_knowledge", []) if knowledge_plan else []
    routed_ids = [k["id"] for k in selected_knowledge if isinstance(k, dict) and "id" in k]
    guidance_refs = [k["id"] for k in selected_knowledge if k.get("priority") in ("critical", "high", "medium")]

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
        "guidance_references": guidance_refs,
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
        or any("responsive" in rid for rid in routed_ids)
        or any(w in goal_lower for w in ("responsive", "mobile", "tablet", "viewport"))
    ):
        affected_viewports = ["desktop_1440", "tablet_768", "mobile_375"]
        required_checks.append("responsive_viewport_matrix")

    if (
        task_intent == "form_ux"
        or any("form" in rid for rid in routed_ids)
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

    if any(k in routed_ids for k in ("component.dialogs-drawers", "interaction.focus-management")) or any(w in goal_lower for w in ("modal", "drawer", "dialog")):
        interactions.extend(["modal_open_close", "drawer_slide_toggle", "focus_trap_verification"])
        required_checks.append("modal_focus_trap_test")

    if any(k in routed_ids for k in ("component.command-search", "component.tables-lists")) or any(w in goal_lower for w in ("table", "search", "filter", "chip")):
        interactions.extend(["search_filtering", "status_chip_toggle", "row_selection"])
        required_checks.append("table_filtering_test")

    if any(k in routed_ids for k in ("screen.loading-state", "screen.empty-state", "screen.error-state")) or any(w in goal_lower for w in ("loading", "skeleton", "empty", "error")):
        interactions.extend(["loading_skeleton_display", "empty_state_recovery", "error_retry_interaction"])
        required_checks.append("ui_state_transition_test")

    if any(k in routed_ids for k in ("tech.motion", "tech.css", "motion.fade-up")):
        required_checks.extend(["motion_duration_check", "reduced_motion_verification"])

    if workflow == "existing-ui":
        preservation_checks.extend([
            "locked_palette_intact",
            "brand_identity_preserved",
            "global_navigation_untouched",
        ])
        required_checks.append("preservation_invariants_verification")

    # Generate executable scenario specifications (P1.5)
    scenarios: list[dict[str, Any]] = [
        {
            "id": "scenario_smoke_test",
            "type": "smoke_render",
            "checks": ["no_console_errors", "no_unhandled_rejections", "root_rendered"],
        },
        {
            "id": "scenario_responsive_viewport",
            "type": "viewport_matrix",
            "viewports": [
                {"name": "desktop", "width": 1440, "height": 900},
                {"name": "tablet", "width": 768, "height": 1024},
                {"name": "mobile", "width": 375, "height": 667},
            ],
            "checks": ["no_horizontal_overflow", "responsive_grid_adaptation"],
        },
        {
            "id": "scenario_accessibility_audit",
            "type": "accessibility_audit",
            "standard": "WCAG_AA",
            "rules": ["color-contrast", "button-name", "image-alt", "label"],
        },
    ]

    if (
        task_intent == "form_ux"
        or any("form" in rid for rid in routed_ids)
        or any(w in goal_lower for w in ("form", "input", "submit", "login", "checkout"))
    ):
        scenarios.append({
            "id": "scenario_form_interaction",
            "type": "interaction_sequence",
            "target": primary_file,
            "actions": [
                {"action": "focus", "selector": "input"},
                {"action": "fill", "selector": "input", "value": "test-input"},
                {"action": "submit", "selector": "form"},
            ],
            "expected_states": ["validating", "submitted"],
        })

    if any(k in routed_ids for k in ("component.dialogs-drawers", "interaction.focus-management")) or any(w in goal_lower for w in ("modal", "drawer", "dialog")):
        scenarios.append({
            "id": "scenario_modal_drawer_interaction",
            "type": "interaction_sequence",
            "actions": [
                {"action": "click", "selector": "[data-action='open'], .menu-toggle, #open-new-deployment-btn", "expected_state": "open"},
                {"action": "press", "key": "Escape", "expected_state": "closed"},
            ],
        })

    if any(k in routed_ids for k in ("component.command-search", "component.tables-lists")) or any(w in goal_lower for w in ("table", "search", "filter", "chip")):
        scenarios.append({
            "id": "scenario_table_filter_interaction",
            "type": "interaction_sequence",
            "actions": [
                {"action": "fill", "selector": "input[type='search'], #search-input", "value": "auth"},
                {"action": "click", "selector": ".chip[data-filter], [data-filter='all']"},
            ],
            "expected_states": ["filtered_data"],
        })

    if any("state" in rid for rid in routed_ids) or any(w in goal_lower for w in ("loading", "skeleton", "empty", "error", "state")):
        scenarios.append({
            "id": "scenario_ui_states_validation",
            "type": "state_matrix",
            "states": ["data", "loading", "empty", "error"],
            "recovery_action": "reset_filters",
        })

    validation = {
        "required_checks": required_checks,
        "affected_viewports": affected_viewports,
        "interactions": interactions,
        "accessibility": accessibility_checks,
        "preservation": preservation_checks,
        "scenarios": scenarios,
        "requires_runtime": True,
        "knowledge_guidance": guidance_refs,
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
