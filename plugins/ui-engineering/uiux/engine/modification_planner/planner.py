"""Modification Planner: Generates context-bounded, permission-verified modification plans.

Enforces:
- PLAN FIRST -> VALIDATE SCOPE -> EDIT WITHIN BUDGET -> VERIFY -> STOP
- L1, L2, L3 Change Classification & Permission Gates
- Hard Preservation Rules (Palette, Brand, Layout, Navigation)
- Framework & UI Library Lock (No unsolicited migrations)
- Business Logic Boundary (No backend, database, medical, or payment logic refactors)
- Blast Radius Boundaries (Allowed vs Protected surfaces)
- Validation Handoff Contract
"""
from __future__ import annotations

import re
import uuid
from typing import Any

from uiux.engine.modification_planner.blast_radius import calculate_blast_radius
from uiux.engine.modification_planner.change_classifier import classify_changes
from uiux.engine.modification_planner.scope_resolver import resolve_scope
from uiux.engine.modification_planner.step_planner import plan_implementation_steps
from uiux.engine.preservation import (
    L1,
    L2,
    L3,
    extract_explicit_permissions,
)


class ModificationPlanner:
    """Core deterministic planning engine for UI modifications."""

    def plan(
        self,
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
        """Produce a complete, machine-readable Modification Plan."""
        user_goal = (user_request or "").strip()
        active_repo = repo_profile or {}
        active_ui = existing_ui_profile or {}
        
        # Enforce preservation profile for existing-ui workflow
        if workflow == "existing-ui" and not preservation_profile:
            preservation_profile = {
                "required": True,
                "allowed_changes": {"max_level": L1},
                "granular_permissions": {
                    "palette": "locked",
                    "brand": "locked",
                    "layout": "protected",
                    "navigation": "protected",
                },
                "protected_invariants": {
                    "palette_locked": True,
                    "brand_locked": True,
                    "navigation_protected": True,
                },
            }

        active_pres = preservation_profile or {
            "required": False,
            "allowed_changes": {"max_level": L3 if workflow == "greenfield" else L1},
            "granular_permissions": {
                "palette": "editable" if workflow == "greenfield" else "locked",
                "brand": "editable" if workflow == "greenfield" else "locked",
                "layout": "editable" if workflow == "greenfield" else "protected",
                "navigation": "editable" if workflow == "greenfield" else "protected",
            },
        }

        # Determine effective task intent
        effective_intent = task_intent or (knowledge_plan.get("task_intent") if knowledge_plan else "general_ui")

        status_reasons: list[str] = []
        violations: list[str] = []

        # 1. Scope Resolution
        scope_info = resolve_scope(
            user_goal=user_goal,
            requested_scope=requested_scope,
            task_intent=effective_intent,
            repo_profile=active_repo,
        )
        status_reasons.extend(scope_info.get("reasons", []))

        # Check for insufficient context in monorepos
        if scope_info.get("is_insufficient_context"):
            return self._build_empty_plan(
                user_goal=user_goal,
                effective_intent=effective_intent,
                scope_info=scope_info,
                workflow=workflow,
                active_repo=active_repo,
                active_pres=active_pres,
                knowledge_plan=knowledge_plan,
                status="insufficient_context",
                status_reasons=status_reasons + ["Ambiguous target application in monorepo."],
            )

        # 2. Surface Resolution
        from uiux.engine.modification_planner.surface_resolver import resolve_surface
        surface = resolve_surface(
            user_goal=user_goal,
            scope_info=scope_info,
            repo_profile=active_repo,
            existing_ui_profile=active_ui,
            preservation_profile=active_pres,
        )

        # 3. Change Classification & Permission Gates
        change_info = classify_changes(
            user_goal=user_goal,
            surface=surface,
            workflow=workflow,
            preservation_profile=active_pres,
            explicit_constraints=explicit_constraints,
        )
        violations.extend(change_info.get("violations", []))

        # 4. Blast Radius Calculation
        blast_radius = calculate_blast_radius(
            surface=surface,
            scope_info=scope_info,
            change_info=change_info,
            user_goal=user_goal,
            repo_profile=active_repo,
        )

        # 5. Implementation Step Planning, Rollback & Validation
        step_info = plan_implementation_steps(
            surface=surface,
            blast_radius=blast_radius,
            change_info=change_info,
            task_intent=effective_intent,
            workflow=workflow,
            preservation_profile=active_pres,
            user_goal=user_goal,
            knowledge_plan=knowledge_plan,
        )

        # 6. Policy Invariant Checks
        goal_lower = user_goal.lower()

        # Check A: Framework Migration (No unsolicited migration)
        fw_migration_match = re.search(r'\b(migrate|switch|convert|chuyển)\s+(?:from\s+\w+\s+)?to\s+(react|vue|angular|svelte|next|nuxt)\b', goal_lower)
        if fw_migration_match and not any(w in goal_lower for w in ("explicitly migrate", "cho phép chuyển", "authorized migration")):
            violations.append(f"Framework migration to '{fw_migration_match.group(2)}' rejected; unsolicited stack migration is strictly prohibited.")

        # Check B: UI Library Replacement (No unsolicited library replacement)
        ui_lib_replacement_match = re.search(r'\b(replace|swap|switch)\s+(?:styling\s+with|css\s+with|tailwind\s+with|bootstrap\s+with)\s+(tailwind|bootstrap|mui|shadcn)\b', goal_lower)
        if ui_lib_replacement_match and not any(w in goal_lower for w in ("explicitly replace", "cho phép đổi thư viện")):
            violations.append(f"UI Library replacement to '{ui_lib_replacement_match.group(2)}' rejected; unsolicited library replacement is prohibited.")

        # Check C: Business Logic Boundary (No backend / DB / medical / trading refactors)
        business_logic_keywords = (
            "backend logic", "database schema", "sql query", "payment processing logic",
            "trading execution", "clinical diagnostic logic", "auth token generation",
            "refactor database", "sửa database", "xử lý thanh toán backend",
        )
        if any(b in goal_lower for b in business_logic_keywords):
            violations.append("Business/backend/service logic modification is strictly outside the boundary of UI tasks.")

        # Check D: Route Renaming outside scope
        if any(w in goal_lower for w in ("rename route", "delete route", "xóa route", "đổi tên route")) and not any(w in goal_lower for w in ("explicitly rename route", "được phép đổi route")):
            violations.append("Renaming or removing routes is protected and cannot be performed without explicit permission.")

        # Check E: New Dependency Policy
        dep_match = re.search(r'\b(install|add\s+dependency|npm\s+i|yarn\s+add)\s+([a-z0-9\-@\/]+)\b', goal_lower)
        unnecessary_deps = ("lodash", "jquery", "moment", "styled-components", "framer-motion", "axios")
        if dep_match and dep_match.group(2) in unnecessary_deps:
            violations.append(f"New dependency '{dep_match.group(2)}' rejected: prefer existing framework/styling primitives.")

        # 7. Status Resolution
        if effective_intent == "audit_only":
            status = "read_only"
            status_reasons.append("Task intent is 'audit_only': plan is read-only, no editing permitted.")
        elif violations:
            if change_info.get("has_palette_violation") or change_info.get("has_unjustified_l2"):
                status = "blocked"
                status_reasons.extend(violations)
            elif change_info.get("has_unauthorized_l3"):
                status = "needs_permission"
                status_reasons.extend(violations)
            else:
                status = "blocked"
                status_reasons.extend(violations)
        else:
            status = "ready"
            status_reasons.append("Modification plan validated and authorized within scope boundaries.")

        if plan_only and status == "ready":
            status_reasons.append("Plan-only mode requested: ready for review, editing suppressed.")

        # 8. Assemble Repository Context
        framework_data = active_repo.get("framework") or {}
        styling_data = active_repo.get("styling_system") or {}
        repo_context = {
            "application_root": scope_info.get("application_target") or ".",
            "framework": framework_data.get("name", "generic_frontend"),
            "styling_system": styling_data.get("primary", "plain_css"),
            "ui_library": active_repo.get("ui_library"),
        }

        # 9. Assemble Constraints
        constraints = {
            "explicit_user_constraints": explicit_constraints or {},
            "repository_constraints": [
                f"Framework: {repo_context['framework']}",
                f"Styling: {repo_context['styling_system']}",
            ],
            "framework_constraints": active_repo.get("framework", {}).get("conflicting_signals", []),
        }

        # 10. Assemble Knowledge Context
        knowledge_context = {
            "selected_packs": knowledge_plan.get("selected_packs", {}) if knowledge_plan else {},
            "selected_skills": [s.get("id") if isinstance(s, dict) else str(s) for s in (knowledge_plan.get("selected_skills", []) if knowledge_plan else [])],
            "selected_knowledge": knowledge_plan.get("selected_knowledge", []) if knowledge_plan else [],
            "routed_catalog_ids": [k["id"] for k in (knowledge_plan.get("selected_knowledge", []) if knowledge_plan else []) if isinstance(k, dict) and "id" in k],
        }

        # 11. Preservation Block
        preservation_block = {
            "required": active_pres.get("required", True),
            "protected_properties": [
                k for k, v in active_pres.get("granular_permissions", {}).items() if v in ("locked", "protected")
            ],
            "permission_level": active_pres.get("allowed_changes", {}).get("max_level", L1),
            "granular_permissions": {
                "palette": active_pres.get("granular_permissions", {}).get("palette", "locked"),
                "brand": active_pres.get("granular_permissions", {}).get("brand", "locked"),
                "layout": active_pres.get("granular_permissions", {}).get("layout", "protected"),
                "navigation": active_pres.get("granular_permissions", {}).get("navigation", "protected"),
            },
        }

        plan_id = f"plan_{uuid.uuid4().hex[:12]}"

        return {
            "schema_version": 1,
            "plan_id": plan_id,
            "request": {
                "user_goal": user_goal,
                "task_intent": effective_intent,
                "requested_scope": scope_info.get("scope", "component"),
            },
            "workflow": workflow,
            "repository": repo_context,
            "constraints": constraints,
            "preservation": preservation_block,
            "knowledge": knowledge_context,
            "affected_surface": {
                "files": surface.get("files", []),
                "pages": surface.get("pages", []),
                "components": surface.get("components", []),
                "tokens": surface.get("tokens", []),
                "routes": surface.get("routes", []),
            },
            "change_classification": {
                "overall_level": change_info.get("overall_level", L1),
                "changes": change_info.get("changes", []),
            },
            "implementation_steps": step_info.get("implementation_steps", []),
            "validation": step_info.get("validation", {}),
            "blast_radius": blast_radius,
            "rollback": step_info.get("rollback", {}),
            "risks": step_info.get("risks", {}),
            "status": status,
            "status_reasons": status_reasons,
        }

    def _build_empty_plan(
        self,
        user_goal: str,
        effective_intent: str,
        scope_info: dict[str, Any],
        workflow: str,
        active_repo: dict[str, Any],
        active_pres: dict[str, Any],
        knowledge_plan: dict[str, Any] | None,
        status: str,
        status_reasons: list[str],
    ) -> dict[str, Any]:
        """Build an early blocked/insufficient_context plan."""
        return {
            "schema_version": 1,
            "plan_id": f"plan_{uuid.uuid4().hex[:12]}",
            "request": {
                "user_goal": user_goal,
                "task_intent": effective_intent,
                "requested_scope": scope_info.get("scope", "global"),
            },
            "workflow": workflow,
            "repository": {
                "application_root": ".",
                "framework": active_repo.get("framework", {}).get("name", "unknown"),
                "styling_system": active_repo.get("styling_system", {}).get("primary", "unknown"),
                "ui_library": active_repo.get("ui_library"),
            },
            "constraints": {
                "explicit_user_constraints": {},
                "repository_constraints": [],
                "framework_constraints": [],
            },
            "preservation": {
                "required": active_pres.get("required", True),
                "protected_properties": ["palette", "brand", "navigation"],
                "permission_level": L1,
                "granular_permissions": {
                    "palette": "locked", "brand": "locked", "layout": "protected", "navigation": "protected",
                },
            },
            "knowledge": {
                "selected_packs": knowledge_plan.get("selected_packs", {}) if knowledge_plan else {},
                "selected_skills": [],
            },
            "affected_surface": {"files": [], "pages": [], "components": [], "tokens": [], "routes": []},
            "change_classification": {"overall_level": L1, "changes": []},
            "implementation_steps": [],
            "validation": {
                "required_checks": [], "affected_viewports": [], "interactions": [], "accessibility": [], "preservation": [],
            },
            "blast_radius": {
                "allowed_files": [], "allowed_components": [], "protected_files": [], "protected_routes": [], "protected_tokens": [],
                "max_scope": "none", "estimated_risk": "high", "cross_app_impact": False, "affected_applications": [],
            },
            "rollback": {"strategy": "none", "checkpoints": []},
            "risks": {"regression": "high", "architecture": "high", "preservation": "high", "runtime": "high"},
            "status": status,
            "status_reasons": status_reasons,
        }
