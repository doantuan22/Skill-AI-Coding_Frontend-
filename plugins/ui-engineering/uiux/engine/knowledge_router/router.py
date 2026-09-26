"""Knowledge Router: Deterministic, context-efficient, framework-aware knowledge routing.

Maps:
Repo Profile + Existing UI Profile + Task Intent + Permissions
    -> Knowledge Load Plan
"""
from __future__ import annotations

from typing import Any

from uiux.engine.knowledge_router.budget import ContextBudgetManager
from uiux.engine.knowledge_router.domain_extension import resolve_domain_pack
from uiux.engine.knowledge_router.intent import (
    ACCESSIBILITY_FIX,
    AUDIT_ONLY,
    COMPONENT_REFACTOR,
    CONSISTENCY_FIX,
    CREATE_UI,
    DESIGN_SYSTEM_WORK,
    FORM_UX,
    FULL_REDESIGN,
    GENERAL_UI,
    IMPROVE_UI,
    MOTION,
    NAVIGATION_UX,
    PAGE_REDESIGN,
    RESPONSIVE_FIX,
    RUNTIME_VALIDATION,
    VISUAL_POLISH,
    classify_task_intent,
)
from uiux.engine.knowledge_router.metadata import (
    DESIGN_SKILLS,
    FRAMEWORK_PACKS,
    PRESERVATION_PACKS,
    RUNTIME_VALIDATION_PACKS,
    STYLING_PACKS,
)
from uiux.engine.knowledge_router.resolver import KnowledgeResolver
from uiux.engine.preservation import L1, L2, L3


class KnowledgeRouter:
    """Deterministic routing engine that produces machine-readable knowledge load plans."""

    def __init__(self, resolver: KnowledgeResolver | None = None, budget_limit_points: int = 25):
        self.resolver = resolver or KnowledgeResolver()
        self.budget_manager = ContextBudgetManager(budget_limit_points=budget_limit_points)

    def route(self, request: dict[str, Any]) -> dict[str, Any]:
        """Produce a complete, validated Knowledge Load Plan from a Knowledge Request."""
        user_request = (request.get("user_request") or "").strip()
        raw_intent = request.get("task_intent")
        workflow = request.get("workflow", "existing-ui")
        requested_scope = request.get("requested_scope", "global")
        repo_profile = request.get("repo_profile") or {}
        existing_ui_profile = request.get("existing_ui_profile") or {}
        preservation_profile = request.get("preservation_profile") or {}
        explicit_constraints = request.get("explicit_constraints") or {}

        diagnostics: dict[str, list[str]] = {
            "warnings": [],
            "conflicts": [],
            "unsupported": [],
        }
        rationale: list[str] = []

        # 1. Normalize Monorepo Scope
        active_repo_profile = repo_profile
        if "applications" in repo_profile and requested_scope in repo_profile["applications"]:
            active_repo_profile = repo_profile["applications"][requested_scope].get("repo_profile", repo_profile)
            rationale.append(f"Monorepo scope applied: resolved configuration for sub-app '{requested_scope}'.")
        elif "applications" in repo_profile:
            # Check if user prompt targets a specific app
            for app_name, app_data in repo_profile["applications"].items():
                if app_name.lower() in user_request.lower():
                    active_repo_profile = app_data.get("repo_profile", repo_profile)
                    rationale.append(f"Monorepo scope resolved from request context: '{app_name}'.")
                    break

        # 2. Classify Task Intent
        task_intent = classify_task_intent(user_request, raw_intent)
        rationale.append(f"Task intent classified as '{task_intent}'.")

        # 3. Resolve Framework Pack
        fw_data = active_repo_profile.get("framework") or {}
        fw_name = fw_data.get("name", "unknown")
        fw_version = fw_data.get("version")
        fw_conflicts = fw_data.get("conflicting_signals") or []

        if fw_conflicts:
            diagnostics["conflicts"].extend(fw_conflicts)
            diagnostics["warnings"].append(f"Conflicting framework signals detected for '{fw_name}'. Resolved using highest confidence evidence.")

        selected_framework_packs: list[dict[str, Any]] = []
        framework_pack_id = f"framework.{fw_name}"

        if framework_pack_id in FRAMEWORK_PACKS:
            pack_entry = dict(FRAMEWORK_PACKS[framework_pack_id])
            if fw_version:
                pack_entry["version"] = str(fw_version)
                pack_entry["reason"] = f"Detected {pack_entry['name']} (version {fw_version}) in repository profile."
            else:
                pack_entry["version"] = None
                pack_entry["reason"] = f"Detected {pack_entry['name']} (unspecified version) in repository profile."
            selected_framework_packs.append(pack_entry)
            rationale.append(f"Selected framework pack '{framework_pack_id}'.")
        else:
            fallback_pack = dict(FRAMEWORK_PACKS["framework.fallback"])
            fallback_pack["reason"] = f"Framework '{fw_name}' has no specific pack; loaded safe universal frontend fallback."
            selected_framework_packs.append(fallback_pack)
            diagnostics["warnings"].append(f"No specific framework pack for '{fw_name}'; fallback applied.")
            rationale.append("Applied generic frontend fallback pack.")

        # 4. Resolve Styling & UI Library Packs
        styling_data = active_repo_profile.get("styling_system") or {}
        primary_styling = styling_data.get("primary")
        secondary_styling = styling_data.get("secondary")
        detected_stylings = styling_data.get("detected") or []

        selected_styling_packs: list[dict[str, Any]] = []
        selected_ui_library_packs: list[dict[str, Any]] = []

        # Map styling names to pack IDs
        styling_name_map = {
            "tailwindcss": "styling.tailwindcss",
            "bootstrap": "styling.bootstrap",
            "plain_css": "styling.plain_css",
            "css_modules": "styling.css_modules",
            "sass_scss": "styling.sass_scss",
            "styled_components": "styling.styled_components",
            "emotion": "styling.emotion",
            "mui": "styling.mui",
            "shadcn_ui": "ui_library.shadcn_ui",
        }

        # Check primary styling
        if primary_styling and primary_styling in styling_name_map:
            pack_id = styling_name_map[primary_styling]
            if pack_id in STYLING_PACKS:
                entry = dict(STYLING_PACKS[pack_id])
                entry["reason"] = f"Primary styling system '{primary_styling}' active in repository."
                selected_styling_packs.append(entry)
                rationale.append(f"Selected primary styling pack '{pack_id}'.")

        # Check secondary styling (supports multi-styling composition, e.g. Tailwind + CSS Modules)
        if secondary_styling and secondary_styling in styling_name_map and secondary_styling != primary_styling:
            pack_id = styling_name_map[secondary_styling]
            if pack_id in STYLING_PACKS:
                entry = dict(STYLING_PACKS[pack_id])
                entry["priority"] = "medium"
                entry["reason"] = f"Secondary styling system '{secondary_styling}' detected in repository."
                selected_styling_packs.append(entry)
                rationale.append(f"Selected secondary styling pack '{pack_id}'.")

        # Check UI Library (e.g. shadcn/ui or mui)
        ui_lib_data = active_repo_profile.get("ui_library") or {}
        ui_lib_name = ui_lib_data.get("name")
        if ui_lib_name == "shadcn_ui" or "shadcn_ui" in detected_stylings:
            shadcn_pack = dict(STYLING_PACKS["ui_library.shadcn_ui"])
            shadcn_pack["reason"] = "shadcn/ui component library active in repository."
            selected_ui_library_packs.append(shadcn_pack)
            rationale.append("Selected UI library pack 'ui_library.shadcn_ui'.")
        elif ui_lib_name and f"styling.{ui_lib_name}" in STYLING_PACKS:
            lib_pack = dict(STYLING_PACKS[f"styling.{ui_lib_name}"])
            lib_pack["reason"] = f"UI library '{ui_lib_name}' active in repository."
            selected_ui_library_packs.append(lib_pack)

        # 5. Preservation Context & Invariants
        preservation_context: dict[str, Any] = {
            "preservation_required": workflow == "existing-ui",
            "palette": "locked" if workflow == "existing-ui" else "editable",
            "brand_identity": "locked" if workflow == "existing-ui" else "editable",
            "layout_identity": "protected" if workflow == "existing-ui" else "editable",
            "navigation": "protected" if workflow == "existing-ui" else "editable",
            "allowed_change_level": "L1",
            "scope": requested_scope,
            "precedence_rules": [
                "1. Explicit user instruction",
                "2. Existing brand identity",
                "3. Existing design system",
                "4. Existing UX / information architecture",
                "5. Repository / framework constraints",
                "6. Domain best practices",
                "7. Design inspiration",
                "8. AI preference",
            ],
        }

        # Override preservation context if explicit preservation_profile exists
        if preservation_profile:
            prot_design = preservation_profile.get("protected_design", {})
            if "color_palette" in prot_design:
                preservation_context["palette"] = "locked" if prot_design["color_palette"].get("policy") == "locked" else "editable"
            if "brand_identity" in prot_design:
                preservation_context["brand_identity"] = "locked" if prot_design["brand_identity"].get("policy") == "locked" else "editable"
            if "overall_layout_identity" in prot_design:
                preservation_context["layout_identity"] = "protected" if prot_design["overall_layout_identity"].get("policy") == "protected" else "editable"
            if "navigation_model" in prot_design:
                preservation_context["navigation"] = "protected" if prot_design["navigation_model"].get("policy") == "protected" else "editable"

            allowed_changes = preservation_profile.get("allowed_changes", {})
            max_level = allowed_changes.get("max_level", "L1")
            preservation_context["allowed_change_level"] = max_level

        # Selected Skills & Knowledge Candidates
        candidate_skills: list[dict[str, Any]] = []
        candidate_knowledge: list[dict[str, Any]] = []

        # Hard preservation knowledge for Existing UI
        if workflow == "existing-ui":
            pres_inv = dict(PRESERVATION_PACKS["preservation.existing_ui_invariants"])
            pres_inv["reason"] = "Existing UI workflow requires strict adherence to preservation invariants and change budgets."
            candidate_knowledge.append(pres_inv)

        # 6. Task Intent-Driven Routing
        # Check change level restrictions on Existing UI:
        is_existing_l1 = workflow == "existing-ui" and preservation_context.get("allowed_change_level") == L1

        # Skill selection based on intent and scope
        if task_intent == RESPONSIVE_FIX:
            resp_skill = dict(DESIGN_SKILLS["skill.responsive_interaction"])
            resp_skill["reason"] = "Responsive layout refinement requested."
            candidate_skills.append(resp_skill)
            # Layout catalog knowledge for responsive
            layout_entries = self.resolver.query_catalog(collection="layouts", ids=["layout.sidebar-content", "layout.grid-dense"])
            for e in layout_entries[:1]:
                candidate_knowledge.append({
                    "id": e["id"],
                    "category": "layout",
                    "name": e["name"],
                    "reason": "Responsive layout reference.",
                    "priority": "medium",
                    "source": e["file"],
                    "required": False,
                    "weight": "small",
                })

        elif task_intent == ACCESSIBILITY_FIX:
            qa_skill = dict(DESIGN_SKILLS["skill.visual_qa"])
            qa_skill["reason"] = "Accessibility compliance and contrast verification task."
            candidate_skills.append(qa_skill)

        elif task_intent == COMPONENT_REFACTOR:
            comp_skill = dict(DESIGN_SKILLS["skill.component_realization"])
            comp_skill["reason"] = "Component realization and refactor task."
            candidate_skills.append(comp_skill)
            # Local component scope: do NOT load page-level architecture

        elif task_intent == NAVIGATION_UX:
            nav_skill = dict(DESIGN_SKILLS["skill.ux_structure"])
            nav_skill["reason"] = "Navigation structure and user flow task."
            candidate_skills.append(nav_skill)

        elif task_intent in (PAGE_REDESIGN, FULL_REDESIGN):
            if is_existing_l1:
                # Existing UI with L1 change level: cannot load major redesign skills!
                diagnostics["warnings"].append("Major redesign requested but allowed change level is L1; suppressed full redesign knowledge.")
                qa_skill = dict(DESIGN_SKILLS["skill.visual_qa"])
                qa_skill["reason"] = "L1 change budget limits task to safe visual refinement."
                candidate_skills.append(qa_skill)
            else:
                # Greenfield or Existing UI with authorized L3 permission
                ux_skill = dict(DESIGN_SKILLS["skill.ux_structure"])
                ux_skill["reason"] = "Page architecture redesign task."
                candidate_skills.append(ux_skill)
                if workflow == "greenfield" or preservation_context.get("allowed_change_level") == L3:
                    dir_skill = dict(DESIGN_SKILLS["skill.design_direction"])
                    dir_skill["reason"] = "Holistic design direction for page restructuring."
                    candidate_skills.append(dir_skill)

        elif task_intent == MOTION:
            motion_entries = self.resolver.query_catalog(collection="motion")
            for e in motion_entries[:2]:
                candidate_knowledge.append({
                    "id": e["id"],
                    "category": "motion",
                    "name": e["name"],
                    "reason": "Motion pattern reference.",
                    "priority": "medium",
                    "source": e["file"],
                    "required": False,
                    "weight": "small",
                })

        elif task_intent == DESIGN_SYSTEM_WORK:
            comp_skill = dict(DESIGN_SKILLS["skill.component_realization"])
            comp_skill["reason"] = "Design token and component conventions task."
            candidate_skills.append(comp_skill)

        else:
            # Default general UI or visual polish
            qa_skill = dict(DESIGN_SKILLS["skill.visual_qa"])
            qa_skill["reason"] = "General visual quality verification."
            candidate_skills.append(qa_skill)
            if workflow == "greenfield":
                dir_skill = dict(DESIGN_SKILLS["skill.design_direction"])
                dir_skill["reason"] = "Greenfield interface design direction."
                candidate_skills.append(dir_skill)

        # Final quality gate is always included for UI modifications
        gate_skill = dict(DESIGN_SKILLS["skill.final_quality_gate"])
        gate_skill["reason"] = "Pre-delivery quality gate and non-regression check."
        candidate_skills.append(gate_skill)

        # 7. Runtime Validation Routing
        selected_runtime_packs: list[dict[str, Any]] = []
        if task_intent == RESPONSIVE_FIX:
            rt_entry = dict(RUNTIME_VALIDATION_PACKS["runtime.responsive_viewport"])
            rt_entry["reason"] = "Validates layout against mobile/tablet/desktop viewports."
            selected_runtime_packs.append(rt_entry)
        elif task_intent == ACCESSIBILITY_FIX:
            rt_entry = dict(RUNTIME_VALIDATION_PACKS["runtime.accessibility_audit"])
            rt_entry["reason"] = "Validates WCAG AA contrast, label associations, and keyboard focus."
            selected_runtime_packs.append(rt_entry)
        elif task_intent == FORM_UX:
            rt_entry = dict(RUNTIME_VALIDATION_PACKS["runtime.form_interaction"])
            rt_entry["reason"] = "Validates form blur validation, error messages, and submit states."
            selected_runtime_packs.append(rt_entry)
        else:
            rt_entry = dict(RUNTIME_VALIDATION_PACKS["runtime.smoke_test"])
            rt_entry["reason"] = "Validates clean page render without console errors."
            selected_runtime_packs.append(rt_entry)

        # 8. Check Phase 5 Domain Extension Point (if domain requested)
        if "domain" in request:
            domain_res = resolve_domain_pack(request["domain"])
            if domain_res:
                diagnostics["warnings"].append(f"Domain pack '{request['domain']}': {domain_res['message']}")

        # 9. Assemble All Candidates for Context Budgeting
        all_candidates: list[dict[str, Any]] = []
        all_candidates.extend(selected_framework_packs)
        all_candidates.extend(selected_styling_packs)
        all_candidates.extend(selected_ui_library_packs)
        all_candidates.extend(candidate_knowledge)
        all_candidates.extend(candidate_skills)
        all_candidates.extend(selected_runtime_packs)

        # Deduplicate candidates by ID while preserving order
        unique_candidates: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for cand in all_candidates:
            if cand["id"] not in seen_ids:
                seen_ids.add(cand["id"])
                unique_candidates.append(cand)

        # Apply Context Budgeting & Deterministic Pruning
        budgeted_items, excluded_items, budget_info = self.budget_manager.apply_budget(unique_candidates)

        # Re-partition into category buckets
        final_fw: list[dict[str, Any]] = []
        final_styling: list[dict[str, Any]] = []
        final_ui_lib: list[dict[str, Any]] = []
        final_skills: list[dict[str, Any]] = []
        final_knowledge: list[dict[str, Any]] = []
        final_runtime: list[dict[str, Any]] = []

        for it in budgeted_items:
            cat = it.get("category")
            if cat == "framework":
                final_fw.append(it)
            elif cat == "styling":
                final_styling.append(it)
            elif cat == "ui_library":
                final_ui_lib.append(it)
            elif cat == "skill":
                final_skills.append(it)
            elif cat == "runtime":
                final_runtime.append(it)
            else:
                final_knowledge.append(it)

        # Build Deterministic Load Order
        # 1. Hard constraints / preservation
        # 2. Framework pack
        # 3. Styling / UI Library packs
        # 4. Skills
        # 5. Catalog Knowledge
        # 6. Runtime validation
        load_order: list[str] = []
        for it in final_knowledge:
            if it.get("category") == "preservation":
                load_order.append(it["id"])
        for it in final_fw:
            load_order.append(it["id"])
        for it in final_styling:
            load_order.append(it["id"])
        for it in final_ui_lib:
            load_order.append(it["id"])
        for it in final_skills:
            load_order.append(it["id"])
        for it in final_knowledge:
            if it.get("category") != "preservation" and it["id"] not in load_order:
                load_order.append(it["id"])
        for it in final_runtime:
            load_order.append(it["id"])

        return {
            "schema_version": 1,
            "workflow": workflow,
            "requested_scope": requested_scope,
            "task_intent": task_intent,
            "selected_packs": {
                "framework": final_fw,
                "styling": final_styling,
                "ui_library": final_ui_lib,
                "runtime": final_runtime,
            },
            "selected_skills": final_skills,
            "selected_knowledge": final_knowledge,
            "preservation_context": preservation_context,
            "excluded_knowledge": excluded_items,
            "load_order": load_order,
            "context_budget": budget_info,
            "rationale": rationale,
            "diagnostics": diagnostics,
        }
