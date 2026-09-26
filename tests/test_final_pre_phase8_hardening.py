"""Final Pre-Phase 8 Hardening Test Suite.

Covers all 38 mandatory cases specified in Final Pre-Phase-8 Hardening:
- Cases 1-8: Planner Grounding
- Cases 9-16: Semantic Negation & Permission Parser
- Cases 17-24: Plan Consistency Validator
- Cases 25-30: Domain -> Knowledge Catalog Bridge
- Cases 31-38: Public Evidence & Runtime Defensive Contract
"""
from __future__ import annotations

import sys
from pathlib import Path

_PLUGIN_DIR = Path(__file__).resolve().parent.parent / "plugins" / "ui-engineering"
if str(_PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_DIR))

import unittest
from unittest.mock import patch

from uiux.api import (
    build_knowledge_plan,
    plan_modification,
    retrieve_knowledge,
    run_runtime_validation,
    recapture_evidence,
    evaluate_runtime_result,
    build_repair_plan,
    run_targeted_repair,
)
from uiux.engine.modification_planner.semantic_parser import parse_semantic_constraints
from uiux.engine.modification_planner.consistency_validator import validate_plan_consistency
from uiux.engine.runtime_critic.validation import (
    validate_evidence,
    validate_repair_result,
)


class TestPlannerGrounding(unittest.TestCase):
    """Cases 1 - 8: Planner Grounding without hallucinated targets."""

    def test_case_1_vanilla_repo_sidebar(self):
        """Case 1: Vanilla repo (index.html, styles.css, app.js). Task: mobile sidebar.
        Expected: Real files only. No Sidebar.tsx.
        """
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "vanilla", "confidence": 1.0},
            "styling": {"framework": "plain_css", "primary": "plain_css"},
            "files": {"ui_files": ["index.html", "styles.css", "app.js"]},
            "pages": [{"name": "Home", "file": "index.html", "route": "/"}],
            "components": [],
        }
        plan = plan_modification(
            user_request="Improve mobile sidebar navigation drawer",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        affected = plan.get("affected_surface", {}).get("files", [])
        allowed = plan.get("blast_radius", {}).get("allowed_files", [])

        # Absolutely no Sidebar.tsx invented
        self.assertFalse(any("Sidebar.tsx" in f for f in affected))
        self.assertFalse(any("Sidebar.tsx" in f for f in allowed))
        # Affected files should be drawn from existing repo files
        for f in affected:
            self.assertIn(f, ["index.html", "styles.css", "app.js"])

    def test_case_2_react_repo_with_sidebar_component(self):
        """Case 2: React repo with src/components/Sidebar.tsx.
        Planner may target Sidebar.tsx because it exists in repo profile.
        """
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "react", "confidence": 1.0},
            "styling": {"framework": "tailwind", "primary": "tailwind"},
            "files": {"ui_files": ["src/components/Sidebar.tsx", "src/App.tsx"]},
            "pages": [{"name": "App", "file": "src/App.tsx", "route": "/"}],
            "components": [{"name": "Sidebar", "file": "src/components/Sidebar.tsx"}],
        }
        plan = plan_modification(
            user_request="Refactor Sidebar component props",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        allowed = plan.get("blast_radius", {}).get("allowed_files", [])
        self.assertTrue(any("Sidebar.tsx" in f for f in allowed))

    def test_case_3_repo_without_theme_ts(self):
        """Case 3: Repo without theme.ts. protected_files must not invent theme.ts."""
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "react", "confidence": 1.0},
            "styling": {"framework": "plain_css", "primary": "plain_css"},
            "files": {"ui_files": ["src/App.tsx", "src/styles.css"]},
            "pages": [{"name": "App", "file": "src/App.tsx", "route": "/"}],
            "components": [{"name": "App", "file": "src/App.tsx"}],
        }
        plan = plan_modification(
            user_request="Refactor button styling",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        prot_files = plan.get("affected_surface", {}).get("protected_files", [])
        self.assertFalse(any("theme.ts" in f for f in prot_files))

    def test_case_4_plain_css_repo_no_tailwind_config(self):
        """Case 4: Plain CSS repo must not invent tailwind.config.js."""
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "vanilla", "confidence": 1.0},
            "styling": {"framework": "plain_css", "primary": "plain_css"},
            "files": {"ui_files": ["index.html", "styles.css"]},
            "pages": [{"name": "Home", "file": "index.html", "route": "/"}],
            "components": [],
        }
        plan = plan_modification(
            user_request="Update color scheme",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        prot_files = plan.get("affected_surface", {}).get("protected_files", [])
        allowed_files = plan.get("blast_radius", {}).get("allowed_files", [])
        self.assertFalse(any("tailwind.config.js" in f for f in prot_files))
        self.assertFalse(any("tailwind.config.js" in f for f in allowed_files))

    def test_case_5_new_component_explicit_planned_create(self):
        """Case 5: Truly new component required must mark planned_create=True."""
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "react", "confidence": 1.0},
            "styling": {"framework": "tailwind", "primary": "tailwind"},
            "files": {"ui_files": ["src/App.tsx"]},
            "pages": [{"name": "App", "file": "src/App.tsx", "route": "/"}],
            "components": [{"name": "App", "file": "src/App.tsx"}],
        }
        plan = plan_modification(
            user_request="Create new NotificationBadge component",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        planned = plan.get("affected_surface", {}).get("planned_files", [])
        # If new file is planned, planned_create must be True
        for pf in planned:
            self.assertTrue(pf.get("planned_create", False))

    def test_case_6_component_semantic_name_in_html_treated_as_dom_surface(self):
        """Case 6: Component semantic name exists only in monolithic HTML -> treated as DOM surface, not React component."""
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "vanilla", "confidence": 1.0},
            "styling": {"framework": "plain_css", "primary": "plain_css"},
            "files": {"ui_files": ["index.html", "style.css"]},
            "pages": [{"name": "Home", "file": "index.html", "route": "/"}],
            "components": [],
        }
        plan = plan_modification(
            user_request="Fix responsive layout of header navbar in index.html",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        allowed = plan.get("blast_radius", {}).get("allowed_files", [])
        self.assertFalse(any(f.endswith(".tsx") or f.endswith(".jsx") for f in allowed))
        self.assertIn("index.html", allowed)

    def test_case_7_monorepo_app_scope_targeting(self):
        """Case 7: Monorepo app scope targets correct application only."""
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "react", "confidence": 1.0},
            "styling": {"framework": "tailwind", "primary": "tailwind"},
            "files": {
                "ui_files": [
                    "apps/web/src/App.tsx",
                    "apps/web/src/index.css",
                    "apps/admin/src/AdminApp.tsx",
                    "apps/admin/src/admin.css",
                ]
            },
            "pages": [
                {"name": "Web", "file": "apps/web/src/App.tsx", "route": "/"},
                {"name": "Admin", "file": "apps/admin/src/AdminApp.tsx", "route": "/admin"},
            ],
            "components": [
                {"name": "WebApp", "file": "apps/web/src/App.tsx"},
                {"name": "AdminApp", "file": "apps/admin/src/AdminApp.tsx"},
            ],
            "repository_signals": {
                "is_monorepo": True,
                "apps": [
                    {"name": "web", "root": "apps/web"},
                    {"name": "admin", "root": "apps/admin"},
                ],
            },
        }
        plan = plan_modification(
            user_request="Update admin dashboard in apps/admin",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        allowed = plan.get("blast_radius", {}).get("allowed_files", [])
        # Should not target apps/web files when targeting apps/admin
        web_files = [f for f in allowed if f.startswith("apps/web")]
        self.assertEqual(len(web_files), 0)

    def test_case_8_unknown_repo_structure_insufficient_context(self):
        """Case 8: Unknown repo structure without ui files results in insufficient_context, not hallucinated paths."""
        repo_profile = {
            "application_root": ".",
            "framework": {"primary": "unknown", "confidence": 0.0},
            "styling": {"framework": "unknown", "primary": "unknown"},
            "files": {"ui_files": []},
            "pages": [],
            "components": [],
        }
        plan = plan_modification(
            user_request="Improve dashboard navigation",
            repo_profile=repo_profile,
            workflow="existing-ui",
        )
        self.assertEqual(plan.get("status"), "insufficient_context")
        self.assertEqual(plan.get("affected_surface", {}).get("files", []), [])


class TestSemanticNegation(unittest.TestCase):
    """Cases 9 - 16: Semantic Negation and Permission Parser."""

    def test_case_9_redesign_dashboard_requested(self):
        """Case 9: 'Redesign dashboard' -> full_redesign requested."""
        res = parse_semantic_constraints("Redesign dashboard")
        self.assertTrue(res["actions"]["full_redesign"]["requested"])
        self.assertFalse(res["actions"]["full_redesign"]["prohibited"])

    def test_case_10_do_not_redesign_dashboard_prohibited(self):
        """Case 10: 'Do not redesign dashboard' -> full_redesign prohibited."""
        res = parse_semantic_constraints("Do not redesign dashboard")
        self.assertTrue(res["actions"]["full_redesign"]["prohibited"])
        self.assertFalse(res["actions"]["full_redesign"]["requested"])

    def test_case_11_vietnamese_khong_redesign_toan_bo_prohibited(self):
        """Case 11: 'KHÔNG redesign toàn bộ' -> prohibited."""
        res = parse_semantic_constraints("KHÔNG redesign toàn bộ")
        self.assertTrue(res["actions"]["full_redesign"]["prohibited"])
        self.assertFalse(res["actions"]["full_redesign"]["requested"])

    def test_case_12_modernize_but_keep_current_colors(self):
        """Case 12: 'Modernize but keep current colors' -> refinement allowed, palette locked."""
        res = parse_semantic_constraints("Modernize but keep current colors")
        self.assertTrue(res["actions"]["palette_change"]["prohibited"])
        self.assertTrue(res["actions"]["visual_refinement"]["requested"])

    def test_case_13_redesign_layout_but_dont_change_brand(self):
        """Case 13: 'Redesign layout but don't change brand' -> layout permission, brand locked."""
        res = parse_semantic_constraints("Redesign layout but don't change brand")
        self.assertTrue(res["actions"]["brand_change"]["prohibited"])
        self.assertTrue(res["actions"]["layout_redesign"]["requested"])

    def test_case_14_improve_nav_without_changing_global_nav_model(self):
        """Case 14: 'Improve navigation without changing global nav model' -> local nav refinement, global nav protected."""
        res = parse_semantic_constraints("Improve navigation without changing global nav model")
        self.assertTrue(res["actions"]["navigation_change"]["prohibited"])
        self.assertTrue(res["actions"]["visual_refinement"]["requested"])

    def test_case_15_never_replace_framework(self):
        """Case 15: 'Never replace framework' -> migration prohibited."""
        res = parse_semantic_constraints("Never replace framework")
        self.assertTrue(res["actions"]["framework_migration"]["prohibited"])

    def test_case_16_keep_current_ui_structure(self):
        """Case 16: 'Keep current UI structure' -> structural redesign prohibited."""
        res = parse_semantic_constraints("Keep current UI structure")
        self.assertTrue(res["actions"]["structural_redesign"]["prohibited"])


class TestPlanConsistency(unittest.TestCase):
    """Cases 17 - 24: Plan Consistency Validator."""

    def test_case_17_missing_requirements_blocked(self):
        """Case 17: Requirement table + filter + modal but allowed file only Sidebar -> blocked."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Add data table, filter bar, and confirmation modal"},
            "blast_radius": {"allowed_files": ["src/components/Sidebar.tsx"], "allowed_components": ["Sidebar"]},
            "affected_surface": {"allowed_files": ["src/components/Sidebar.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Update Sidebar", "target": "src/components/Sidebar.tsx", "file": "src/components/Sidebar.tsx"}
            ],
            "change_classification": {"overall_level": "L1", "changes": [{"change_level": "L1", "justification": "minor"}]},
            "validation": {"checks": ["basic_render"]},
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/components/Sidebar.tsx"]}})
        self.assertFalse(res["valid"])
        self.assertTrue(any("unaddressed_requirement" in iss for iss in res["issues"]))

    def test_case_18_all_requirements_mapped_valid(self):
        """Case 18: All requirements mapped to files/steps -> valid."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Update Sidebar"},
            "blast_radius": {"allowed_files": ["src/components/Sidebar.tsx"], "allowed_components": ["Sidebar"]},
            "affected_surface": {"allowed_files": ["src/components/Sidebar.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Update Sidebar", "target": "src/components/Sidebar.tsx", "file": "src/components/Sidebar.tsx"}
            ],
            "change_classification": {"overall_level": "L1", "changes": [{"change_level": "L1", "justification": "minor"}]},
            "validation": {"checks": ["basic_render"]},
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/components/Sidebar.tsx"]}})
        self.assertTrue(res["valid"])

    def test_case_19_step_references_file_outside_allowed_blocked(self):
        """Case 19: Step references file outside allowed_files -> blocked (PLAN_INTERNAL_CONTRADICTION)."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Update table"},
            "blast_radius": {"allowed_files": ["src/components/Sidebar.tsx"], "allowed_components": ["Sidebar"]},
            "affected_surface": {"allowed_files": ["src/components/Sidebar.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Update DataTable", "target": "src/components/DataTable.tsx", "file": "src/components/DataTable.tsx"}
            ],
            "change_classification": {"overall_level": "L1", "changes": [{"change_level": "L1", "justification": "minor"}]},
            "validation": {"checks": ["basic_render"]},
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/components/Sidebar.tsx", "src/components/DataTable.tsx"]}})
        self.assertFalse(res["valid"])
        self.assertTrue(any("PLAN_INTERNAL_CONTRADICTION" in iss for iss in res["issues"]))

    def test_case_20_non_existent_file_not_planned_create_blocked(self):
        """Case 20: Non-existent file not marked planned_create -> blocked (ungrounded_target_file)."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Update header"},
            "blast_radius": {"allowed_files": ["src/components/GhostHeader.tsx"], "allowed_components": ["GhostHeader"]},
            "affected_surface": {"allowed_files": ["src/components/GhostHeader.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Update GhostHeader", "target": "src/components/GhostHeader.tsx", "file": "src/components/GhostHeader.tsx"}
            ],
            "change_classification": {"overall_level": "L1", "changes": [{"change_level": "L1", "justification": "minor"}]},
            "validation": {"checks": ["basic_render"]},
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/App.tsx"]}})
        self.assertFalse(res["valid"])
        self.assertTrue(any("ungrounded_target_file" in iss for iss in res["issues"]))

    def test_case_21_l2_without_justification_blocked(self):
        """Case 21: L2 change level without justification -> blocked."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Refactor component layout"},
            "blast_radius": {"allowed_files": ["src/App.tsx"], "allowed_components": ["App"]},
            "affected_surface": {"allowed_files": ["src/App.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Refactor layout", "target": "src/App.tsx", "file": "src/App.tsx"}
            ],
            "change_classification": {
                "overall_level": "L2",
                "changes": [{"change_level": "L2", "justification": ""}],  # Missing justification!
            },
            "validation": {"checks": ["basic_render"]},
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/App.tsx"]}})
        self.assertFalse(res["valid"])
        self.assertTrue(any("missing architectural justification" in iss for iss in res["issues"]))

    def test_case_22_l3_without_permission_blocked(self):
        """Case 22: L3 without permission -> blocked."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Redesign entire application"},
            "blast_radius": {"allowed_files": ["src/App.tsx"], "allowed_components": ["App"]},
            "affected_surface": {"allowed_files": ["src/App.tsx"]},
            "preservation": {"permission_level": "L1"},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Full redesign", "target": "src/App.tsx", "file": "src/App.tsx"}
            ],
            "change_classification": {
                "overall_level": "L3",
                "changes": [{"change_level": "L3", "justification": "User asked"}],
            },
            "validation": {"checks": ["basic_render"]},
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/App.tsx"]}})
        self.assertFalse(res["valid"])
        self.assertTrue(any("exceeds authorized preservation level" in iss for iss in res["issues"]))

    def test_case_23_motion_step_requires_reduced_motion_validation(self):
        """Case 23: Motion step without reduced-motion validation produces warning/block per policy."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Add complex animations"},
            "blast_radius": {"allowed_files": ["src/App.tsx"], "allowed_components": ["App"]},
            "affected_surface": {"allowed_files": ["src/App.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Add stagger animation", "target": "src/App.tsx", "file": "src/App.tsx"}
            ],
            "change_classification": {"overall_level": "L1", "changes": [{"change_level": "L1", "justification": "animation"}]},
            "validation": {"checks": ["basic_render"]},  # Missing reduced_motion
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/App.tsx"]}})
        self.assertTrue(any("reduced_motion" in iss for iss in res["issues"]))

    def test_case_24_modal_change_requires_interaction_validation(self):
        """Case 24: Modal change without interaction validation produces warning/block per policy."""
        plan = {
            "status": "ready",
            "request": {"user_goal": "Add modal dialog"},
            "blast_radius": {"allowed_files": ["src/App.tsx"], "allowed_components": ["App"]},
            "affected_surface": {"allowed_files": ["src/App.tsx"]},
            "implementation_steps": [
                {"step_id": "step_1", "description": "Add modal popup", "target": "src/App.tsx", "file": "src/App.tsx"}
            ],
            "change_classification": {"overall_level": "L1", "changes": [{"change_level": "L1", "justification": "modal"}]},
            "validation": {"checks": ["basic_render"]},  # Missing interaction
        }
        res = validate_plan_consistency(plan, repo_profile={"files": {"ui_files": ["src/App.tsx"]}})
        self.assertTrue(any("interaction" in iss for iss in res["issues"]))


class TestDomainBridge(unittest.TestCase):
    """Cases 25 - 30: Domain -> Knowledge Catalog Bridge."""

    def test_case_25_hospitality_booking_recipe_retrievable(self):
        """Case 25: Hospitality booking -> domain.hospitality_travel -> recipe.travel-booking retrievable."""
        plan = build_knowledge_plan(
            user_request="Hotel booking flow with date range, guests, rooms, booking summary, cancellation and pricing clarity.",
            workflow="greenfield",
        )
        domain_primary = plan.get("domain_context", {}).get("primary", {})
        self.assertEqual(domain_primary.get("id"), "domain.hospitality_travel")

        knowledge_ids = [k["id"] for k in plan.get("selected_knowledge", [])]
        self.assertIn("recipe.travel-booking", knowledge_ids)

        # Assert retrieve_knowledge succeeds on recipe.travel-booking
        res = retrieve_knowledge(ids=["recipe.travel-booking"])
        self.assertEqual(res["count"], 1)
        self.assertEqual(res["entries"][0]["id"], "recipe.travel-booking")

    def test_case_26_every_selected_knowledge_id_succeeds(self):
        """Case 26: Every selected_knowledge ID in knowledge plan resolves successfully via retrieve_knowledge."""
        plan = build_knowledge_plan(
            user_request="Hotel booking flow with date range, guests, rooms, booking summary, cancellation and pricing clarity.",
            workflow="greenfield",
        )
        knowledge_ids = [k["id"] for k in plan.get("selected_knowledge", [])]
        self.assertGreater(len(knowledge_ids), 0)
        res = retrieve_knowledge(ids=knowledge_ids)
        self.assertEqual(res["count"], len(knowledge_ids))

    def test_case_27_domain_pack_id_not_in_selected_knowledge(self):
        """Case 27: Domain pack ID is not incorrectly included in selected_knowledge."""
        plan = build_knowledge_plan(
            user_request="Hotel booking flow with room selection",
            workflow="greenfield",
        )
        knowledge_ids = [k["id"] for k in plan.get("selected_knowledge", [])]
        # domain.hospitality_travel must NOT be inside selected_knowledge
        self.assertNotIn("domain.hospitality_travel", knowledge_ids)
        # It must be inside selected_packs["domain"]
        domain_packs = [d["id"] for d in plan.get("selected_packs", {}).get("domain", [])]
        self.assertIn("domain.hospitality_travel", domain_packs)

    def test_case_28_ecommerce_checkout_routes_ecommerce_patterns(self):
        """Case 28: Ecommerce checkout routes ecommerce relevant recipe and patterns."""
        plan = build_knowledge_plan(
            user_request="Shopping cart drawer and multi-step checkout with payment",
            workflow="greenfield",
        )
        knowledge_ids = [k["id"] for k in plan.get("selected_knowledge", [])]
        self.assertTrue("recipe.consumer-app" in knowledge_ids or "screen.checkout" in knowledge_ids)

    def test_case_29_saas_dashboard_no_travel_knowledge(self):
        """Case 29: SaaS dashboard contains no travel knowledge."""
        plan = build_knowledge_plan(
            user_request="Enterprise Kubernetes cluster metrics and workload telemetry dashboard",
            workflow="greenfield",
        )
        knowledge_ids = [k["id"] for k in plan.get("selected_knowledge", [])]
        self.assertNotIn("recipe.travel-booking", knowledge_ids)
        self.assertIn("screen.dashboard", knowledge_ids)

    def test_case_30_unknown_domain_safe_generic_fallback(self):
        """Case 30: Unknown domain produces safe generic fallback without crashing."""
        plan = build_knowledge_plan(
            user_request="Simple personal bio and contact links page",
            workflow="greenfield",
        )
        self.assertIsNotNone(plan)
        self.assertIn("selected_knowledge", plan)


class TestEvidenceContract(unittest.TestCase):
    """Cases 31 - 38: Public Evidence & Runtime Defensive Contract."""

    def test_case_31_valid_evidence_accepted(self):
        """Case 31: Valid evidence is accepted and critiqued."""
        valid_evidence = {
            "session_id": "session_test_31",
            "status": "COMPLETED",
            "captures": [
                {
                    "id": "cap_1",
                    "page": "/",
                    "viewport": "desktop_1440",
                    "status": "CAPTURED",
                }
            ],
        }
        res = run_runtime_validation(
            modification_plan={"plan_id": "plan_31", "validation": {"requires_runtime": True}},
            after_evidence=valid_evidence,
            validate_only=True,
        )
        self.assertNotEqual(res.get("status"), "INVALID_CALL")
        self.assertIn("overall_status", res)

    def test_case_32_null_when_runtime_required_blocks_insufficient_evidence(self):
        """Case 32: null after_evidence when runtime required -> BLOCKED insufficient_evidence."""
        res = run_runtime_validation(
            modification_plan={"plan_id": "plan_32", "validation": {"requires_runtime": True}},
            after_evidence=None,
            validate_only=True,
        )
        self.assertEqual(res.get("overall_status"), "blocked")
        issues = res.get("issues", [])
        self.assertTrue(any(i.get("category") == "insufficient_evidence" for i in issues))

    def test_case_33_wrong_type_returns_structured_invalid_argument(self):
        """Case 33: Wrong type for after_evidence -> INVALID_ARGUMENT (no raw AttributeError)."""
        res = run_runtime_validation(
            modification_plan={},
            after_evidence="this_is_a_string_not_a_dict",
        )
        self.assertEqual(res.get("status"), "INVALID_CALL")
        self.assertEqual(res.get("error_code"), "INVALID_ARGUMENT")
        self.assertEqual(res.get("overall_status"), "blocked")
        self.assertIn("Invalid after_evidence payload", res.get("error", ""))

    def test_case_34_missing_required_nested_fields_returns_invalid_argument(self):
        """Case 34: Malformed nested capture in after_evidence -> INVALID_ARGUMENT."""
        malformed_evidence = {
            "captures": [
                "not_a_dict_capture"
            ]
        }
        res = run_runtime_validation(
            modification_plan={},
            after_evidence=malformed_evidence,
        )
        self.assertEqual(res.get("status"), "INVALID_CALL")
        self.assertEqual(res.get("error_code"), "INVALID_ARGUMENT")

    def test_case_35_malformed_actions_executed_returns_invalid_argument(self):
        """Case 35: Malformed actions_executed (array of strings instead of objects) -> INVALID_ARGUMENT."""
        malformed_repair_result = {
            "status": "repaired",
            "actions_executed": ["just a string instead of object"],
        }
        res = recapture_evidence(
            repair_result=malformed_repair_result,
            modification_plan={},
        )
        self.assertEqual(res.get("status"), "INVALID_CALL")
        self.assertEqual(res.get("error_code"), "INVALID_ARGUMENT")
        self.assertEqual(res.get("recapture_plan", {}).get("status"), "blocked")

    def test_case_36_valid_repair_result_recapture_works(self):
        """Case 36: Valid repair_result -> recapture produces targeted plan."""
        valid_repair = {
            "status": "repaired",
            "repair_id": "repair_36",
            "actions_executed": [
                {
                    "action_id": "act_1",
                    "target": "styles.css",
                    "files": ["styles.css"],
                    "validation_required": ["responsive_viewport"],
                }
            ],
        }
        mod_plan = {
            "affected_surface": {"routes": ["/"]},
            "blast_radius": {"allowed_files": ["styles.css"]},
            "validation": {"affected_viewports": ["mobile_375", "desktop_1440"]},
        }
        res = recapture_evidence(
            repair_result=valid_repair,
            modification_plan=mod_plan,
        )
        self.assertIn("recapture_pages", res)
        self.assertIn("recapture_viewports", res)
        self.assertFalse(res.get("is_full_site", True))

    def test_case_37_invalid_repair_result_structured_error_no_crash(self):
        """Case 37: Invalid repair_result (e.g. non-dict) -> structured error, no crash."""
        res = recapture_evidence(
            repair_result="not_a_dict",
            modification_plan={},
        )
        self.assertEqual(res.get("status"), "INVALID_CALL")
        self.assertEqual(res.get("error_code"), "INVALID_ARGUMENT")

    def test_case_38_no_raw_traceback_consumer_facing(self):
        """Case 38: Consumer-facing responses never contain raw Python tracebacks."""
        # Test malformed plan
        res1 = run_runtime_validation(modification_plan="bad_plan")
        self.assertNotIn("Traceback (most recent call last):", str(res1))

        # Test malformed repair plan
        res2 = run_targeted_repair(repair_plan=123, modification_plan={})
        self.assertNotIn("Traceback (most recent call last):", str(res2))

        # Test malformed critic report evaluation
        res3 = evaluate_runtime_result(critic_report="bad_report")
        self.assertFalse(res3["authorized_to_proceed"])


if __name__ == "__main__":
    unittest.main()
