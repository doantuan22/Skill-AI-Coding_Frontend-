"""Unit, quality, and regression test suite for Phase 6: Modification Planning & Controlled Editing.

Covers all 45 mandatory test cases, quality tests, and schema verification.
"""
from __future__ import annotations

import unittest
from typing import Any
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import _paths  # noqa: F401

from uiux import api
from uiux.engine import modification_planner
from uiux.engine.modification_planner import (
    ControlledEditingEngine,
    ModificationPlanner,
    compare_plan_to_changes,
    evaluate_plan_permissions,
    plan_modification,
    validate_modification_plan,
)
from uiux.engine.preservation import L1, L2, L3


def _mock_repo_profile(
    framework_name: str = "react",
    primary_styling: str = "plain_css",
    components: list[Any] | None = None,
    routes: list[str] | None = None,
    applications: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prof: dict[str, Any] = {
        "schema_version": 1,
        "framework": {
            "name": framework_name,
            "version": "18.2.0",
            "confidence": 0.95,
            "evidence": [f"Declared {framework_name}"],
            "conflicting_signals": [],
        },
        "styling_system": {
            "primary": primary_styling,
            "secondary": None,
            "detected": [primary_styling],
            "confidence": 0.90,
            "evidence": [f"Detected {primary_styling}"],
        },
        "ui_library": None,
        "routes": routes or ["/"],
        "pages": [],
        "components": components or [
            {"name": "Button", "path": "src/components/Button.tsx", "usage_count": 1},
        ],
        "design_tokens": {"colors": {"primary": "#3b82f6"}},
        "runtime_capabilities": {"has_node": True, "has_playwright": False},
        "overall_confidence": 0.92,
    }
    if applications:
        prof["applications"] = applications
    return prof


class ModificationPlannerTests(unittest.TestCase):
    """Test suite covering the 45 mandatory test cases for Phase 6."""

    def setUp(self) -> None:
        self.planner = ModificationPlanner()
        self.editor = ControlledEditingEngine()

    # CASE 1: Existing UI + fix spacing button -> L1, component scope
    def test_case_01_existing_ui_spacing_button_l1_component_scope(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Fix button spacing on navbar",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["request"]["requested_scope"], "component")
        self.assertEqual(plan["change_classification"]["overall_level"], L1)
        self.assertIn("src/components/Button.tsx", plan["blast_radius"]["allowed_files"])

    # CASE 2: Existing UI + responsive navbar -> L1/L2, palette locked
    def test_case_02_existing_ui_responsive_navbar_palette_locked(self) -> None:
        prof = _mock_repo_profile(components=[{"name": "Navbar", "path": "src/components/Navbar.tsx", "usage_count": 1}])
        plan = self.planner.plan(
            user_request="Fix responsive overflow on navbar",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertIn(plan["change_classification"]["overall_level"], (L1, L2))
        self.assertEqual(plan["preservation"]["granular_permissions"]["palette"], "locked")
        self.assertIn("desktop_1440", plan["validation"]["affected_viewports"])
        self.assertIn("mobile_375", plan["validation"]["affected_viewports"])

    # CASE 3: Existing UI + reorganize form sections -> L2, justification required
    def test_case_03_existing_ui_reorganize_form_sections_l2_justification(self) -> None:
        prof = _mock_repo_profile(components=[{"name": "CheckoutForm", "path": "src/components/CheckoutForm.tsx"}])
        # User explains concrete layout issue causing friction
        plan = self.planner.plan(
            user_request="Reorganize checkout form sections because mobile field overflow causes friction",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["change_classification"]["overall_level"], L2)
        l2_change = [c for c in plan["change_classification"]["changes"] if c["level"] == L2][0]
        self.assertIsNotNone(l2_change["justification"])
        self.assertIn("friction", l2_change["justification"]["issue"].lower())

    # CASE 4: L2 without justification -> plan blocked
    def test_case_04_l2_without_justification_blocked(self) -> None:
        prof = _mock_repo_profile(components=[{"name": "CheckoutForm", "path": "src/components/CheckoutForm.tsx"}])
        plan = self.planner.plan(
            user_request="Reorganize checkout form sections",  # No issue/justification given
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("justification" in r.lower() for r in plan["status_reasons"]))

    # CASE 5: Full dashboard redesign explicit -> L3 allowed for page architecture
    def test_case_05_full_dashboard_redesign_explicit_l3_allowed(self) -> None:
        prof = _mock_repo_profile(routes=["/dashboard"])
        plan = self.planner.plan(
            user_request="Redesign toàn bộ dashboard from scratch",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["change_classification"]["overall_level"], L3)

    # CASE 6: Full dashboard redesign but "keep current colors" -> layout L3 allowed, palette locked
    def test_case_06_full_dashboard_redesign_keep_colors_layout_l3_palette_locked(self) -> None:
        prof = _mock_repo_profile(routes=["/dashboard"])
        plan = self.planner.plan(
            user_request="Redesign toàn bộ dashboard nhưng giữ nguyên bảng màu hiện tại",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["change_classification"]["overall_level"], L3)
        self.assertEqual(plan["preservation"]["granular_permissions"]["palette"], "locked")
        self.assertIn("src/theme.ts", plan["blast_radius"]["protected_files"])

    # CASE 7: Modernize UI vague request -> no L3 permission
    def test_case_07_modernize_ui_vague_request_no_l3_permission(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Modernize the UI and make it look clean",
            workflow="existing-ui",
            repo_profile=prof,
        )
        # Vague request does not grant L3
        self.assertNotEqual(plan["change_classification"]["overall_level"], L3)
        self.assertEqual(plan["change_classification"]["overall_level"], L1)
        self.assertEqual(plan["preservation"]["granular_permissions"]["palette"], "locked")

    # CASE 8: User allows recolor only -> palette editable, navigation protected
    def test_case_08_user_allows_recolor_only_palette_editable_nav_protected(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Change color palette to dark emerald theme",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["change_classification"]["overall_level"], L3)
        self.assertEqual(plan["preservation"]["granular_permissions"]["navigation"], "protected")
        self.assertIn("src/router.tsx", plan["blast_radius"]["protected_files"])

    # CASE 9: Button-only task -> allowed files limited
    def test_case_09_button_only_task_allowed_files_limited(self) -> None:
        prof = _mock_repo_profile(components=[
            {"name": "Button", "path": "src/components/Button.tsx", "usage_count": 1},
            {"name": "Header", "path": "src/components/Header.tsx", "usage_count": 1},
        ])
        plan = self.planner.plan(
            user_request="Fix button alignment",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["blast_radius"]["allowed_files"], ["src/components/Button.tsx"])
        self.assertNotIn("src/components/Header.tsx", plan["blast_radius"]["allowed_files"])

    # CASE 10: Actual change touches theme.ts unexpectedly -> plan drift detected
    def test_case_10_actual_change_touches_theme_drift_detected(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        # Simulated actual changes include unauthorized theme.ts
        actual = {
            "modified_files": ["src/components/Button.tsx", "src/theme.ts"],
            "actual_change_levels": [L1, L3],
        }
        manifest = self.editor.compare_plan_to_changes(plan, actual)
        self.assertTrue(manifest["drift_detected"])
        self.assertEqual(manifest["status"], "failed_permission")
        self.assertTrue(any("theme.ts" in r for r in manifest["drift_reasons"]))

    # CASE 11: Shared Button change affects multiple pages -> blast radius elevated
    def test_case_11_shared_button_affects_multiple_pages_blast_radius_elevated(self) -> None:
        prof = _mock_repo_profile(components=[
            {"name": "Button", "path": "src/components/Button.tsx", "usage_count": 12},
        ])
        plan = self.planner.plan(
            user_request="Update Button padding",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertTrue(plan["blast_radius"]["is_shared_component_elevated"])
        self.assertIn(plan["blast_radius"]["estimated_risk"], ("medium", "high"))

    # CASE 12: Shared API breaking prop rename -> regression risk high
    def test_case_12_shared_api_breaking_prop_rename_regression_risk_high(self) -> None:
        prof = _mock_repo_profile(components=[{"name": "Button", "path": "src/components/Button.tsx", "usage_count": 5}])
        plan = self.planner.plan(
            user_request="Rename prop 'variant' to 'buttonStyle' on Button",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertTrue(plan["blast_radius"]["is_component_api_breaking"])
        self.assertEqual(plan["risks"]["regression"], "high")

    # CASE 13: Fix repeated issue via shared component -> shared-first plan preferred
    def test_case_13_fix_repeated_issue_via_shared_component_preferred(self) -> None:
        prof = _mock_repo_profile(components=[{"name": "Button", "path": "src/components/Button.tsx", "usage_count": 8}])
        plan = self.planner.plan(
            user_request="Standardize button focus ring across all components",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertIn("src/components/Button.tsx", plan["blast_radius"]["allowed_files"])
        self.assertEqual(plan["request"]["requested_scope"], "component")

    # CASE 14: Single page custom case -> no unsafe global shared change
    def test_case_14_single_page_custom_case_no_unsafe_global_change(self) -> None:
        prof = _mock_repo_profile(
            routes=["/checkout", "/login"],
            components=[{"name": "Button", "path": "src/components/Button.tsx", "usage_count": 5}],
        )
        plan = self.planner.plan(
            user_request="Fix button alignment on checkout page",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["request"]["requested_scope"], "component")
        self.assertEqual(plan["blast_radius"]["max_scope"], "component")

    # CASE 15: Greenfield multi-page -> design system/primitives before expansion
    def test_case_15_greenfield_multi_page_primitives_before_expansion(self) -> None:
        plan = self.planner.plan(
            user_request="Build new multi-page store with home, cart, and checkout",
            workflow="greenfield",
        )
        self.assertEqual(plan["workflow"], "greenfield")
        # First batch must be batch_a (tokens/primitives) before subsequent expansion
        batches = [s["batch"] for s in plan["implementation_steps"]]
        self.assertEqual(batches[0], "batch_a")

    # CASE 16: Existing UI -> preservation profile mandatory
    def test_case_16_existing_ui_preservation_profile_mandatory(self) -> None:
        plan = self.planner.plan(
            user_request="Refine card layout",
            workflow="existing-ui",
            preservation_profile=None,  # Not provided
        )
        # Planner synthesizes mandatory preservation rules
        self.assertTrue(plan["preservation"]["required"])
        self.assertEqual(plan["preservation"]["granular_permissions"]["palette"], "locked")

    # CASE 17: Framework migration not requested -> blocked
    def test_case_17_framework_migration_not_requested_blocked(self) -> None:
        prof = _mock_repo_profile(framework_name="react")
        plan = self.planner.plan(
            user_request="Migrate to Vue because Vue is better",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("framework migration" in r.lower() for r in plan["status_reasons"]))

    # CASE 18: UI library replacement not requested -> blocked
    def test_case_18_ui_library_replacement_not_requested_blocked(self) -> None:
        prof = _mock_repo_profile(primary_styling="tailwindcss")
        plan = self.planner.plan(
            user_request="Replace tailwind with bootstrap components",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("ui library replacement" in r.lower() for r in plan["status_reasons"]))

    # CASE 19: Business logic refactor unrelated -> blocked
    def test_case_19_business_logic_refactor_unrelated_blocked(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Refactor database schema and payment processing logic",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("business/backend" in r.lower() for r in plan["status_reasons"]))

    # CASE 20: Route rename outside scope -> blocked
    def test_case_20_route_rename_outside_scope_blocked(self) -> None:
        prof = _mock_repo_profile(routes=["/cart", "/checkout"])
        plan = self.planner.plan(
            user_request="Rename route /cart to /shopping-bag",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("route" in r.lower() for r in plan["status_reasons"]))

    # CASE 21: Global primary color change without permission -> blocked
    def test_case_21_global_primary_color_change_without_permission_blocked(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Change primary color to bright orange",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("palette" in r.lower() for r in plan["status_reasons"]))

    # CASE 22: Existing token reuse -> L1 allowed
    def test_case_22_existing_token_reuse_l1_allowed(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Reuse existing --spacing-md on button margin",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["change_classification"]["overall_level"], L1)

    # CASE 23: Accessibility contrast minor adjustment -> allowed minimal change
    def test_case_23_accessibility_contrast_minor_adjustment_minimal_change(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Adjust button text contrast to meet WCAG AA 4.5:1",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["change_classification"]["overall_level"], L1)
        self.assertIn("accessibility_axe_audit", plan["validation"]["required_checks"])

    # CASE 24: Global breakpoint modification -> risk escalated
    def test_case_24_global_breakpoint_modification_risk_escalated(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Modify global media query breakpoint for tablet",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertTrue(plan["blast_radius"]["is_global_breakpoint_modified"])
        self.assertEqual(plan["blast_radius"]["estimated_risk"], "high")

    # CASE 25: Monorepo admin task -> storefront untouched
    def test_case_25_monorepo_admin_task_storefront_untouched(self) -> None:
        prof = _mock_repo_profile(
            applications={
                "admin": {"repo_profile": {"components": [{"name": "Sidebar", "path": "apps/admin/Sidebar.tsx"}]}},
                "storefront": {"repo_profile": {"components": [{"name": "Navbar", "path": "apps/storefront/Navbar.tsx"}]}},
            }
        )
        plan = self.planner.plan(
            user_request="Fix admin sidebar padding",
            workflow="existing-ui",
            repo_profile=prof,
            requested_scope="admin",
        )
        self.assertEqual(plan["status"], "ready")
        self.assertIn("apps/admin/Sidebar.tsx", plan["blast_radius"]["allowed_files"])
        for f in plan["blast_radius"]["allowed_files"]:
            self.assertNotIn("storefront", f)

    # CASE 26: Shared monorepo package modification -> cross-app blast radius reported
    def test_case_26_shared_monorepo_package_cross_app_blast_radius(self) -> None:
        prof = _mock_repo_profile(
            components=[{"name": "Button", "path": "packages/ui/Button.tsx", "usage_count": 5}],
            applications={"admin": {}, "storefront": {}},
        )
        plan = self.planner.plan(
            user_request="Update Button component in shared package",
            workflow="existing-ui",
            repo_profile=prof,
            requested_scope="admin",
        )
        self.assertTrue(plan["blast_radius"]["cross_app_impact"])
        self.assertGreaterEqual(len(plan["blast_radius"]["affected_applications"]), 2)

    # CASE 27: Audit-only -> no editing (status: read_only)
    def test_case_27_audit_only_no_editing(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Audit checkout page accessibility and report findings",
            workflow="existing-ui",
            repo_profile=prof,
            task_intent="audit_only",
        )
        self.assertEqual(plan["status"], "read_only")
        self.assertTrue(any("audit_only" in r for r in plan["status_reasons"]))

    # CASE 28: Plan-only -> ready for review, no execution
    def test_case_28_plan_only_no_editing(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Fix button alignment",
            workflow="existing-ui",
            repo_profile=prof,
            plan_only=True,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertTrue(any("plan-only" in r.lower() for r in plan["status_reasons"]))

    # CASE 29: Unknown target application in monorepo -> insufficient context
    def test_case_29_unknown_target_application_insufficient_context(self) -> None:
        prof = _mock_repo_profile(
            applications={"admin": {}, "storefront": {}, "docs": {}}
        )
        plan = self.planner.plan(
            user_request="Fix button spacing",
            workflow="existing-ui",
            repo_profile=prof,
            requested_scope="global",
        )
        self.assertEqual(plan["status"], "insufficient_context")

    # CASE 30: Unexpected file during execution -> editor stops / rejects
    def test_case_30_unexpected_file_during_execution_editor_stops(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        manifest = self.editor.compare_plan_to_changes(plan, {
            "modified_files": ["src/components/Button.tsx", "src/unauthorized.ts"],
        })
        self.assertTrue(manifest["drift_detected"])
        self.assertEqual(manifest["status"], "failed_drift")

    # CASE 31: Create file not in plan -> blocked
    def test_case_31_create_file_not_in_plan_blocked(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        manifest = self.editor.compare_plan_to_changes(plan, {
            "created_files": ["src/components/NewUnexpectedComponent.tsx"],
        })
        self.assertTrue(manifest["drift_detected"])
        self.assertEqual(manifest["status"], "failed_drift")

    # CASE 32: Delete file not explicit -> blocked
    def test_case_32_delete_file_not_explicit_blocked(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        manifest = self.editor.compare_plan_to_changes(plan, {
            "deleted_files": ["src/components/LegacyCard.tsx"],
        })
        self.assertTrue(manifest["drift_detected"])
        self.assertEqual(manifest["status"], "failed_permission")

    # CASE 33: New dependency unnecessary -> rejected
    def test_case_33_new_dependency_unnecessary_rejected(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Install lodash to center the button",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "blocked")
        self.assertTrue(any("lodash" in r for r in plan["status_reasons"]))

    # CASE 34: Required dependency justified -> recorded in plan, not auto-installed
    def test_case_34_required_dependency_justified_recorded(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Add Lucide icon to button",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["status"], "ready")

    # CASE 35: Responsive task -> viewport validation included
    def test_case_35_responsive_task_viewport_validation_included(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Fix mobile responsive navbar",
            workflow="existing-ui",
            repo_profile=prof,
            task_intent="responsive_fix",
        )
        self.assertIn("responsive_viewport_matrix", plan["validation"]["required_checks"])
        self.assertIn("mobile_375", plan["validation"]["affected_viewports"])

    # CASE 36: Form task -> form interaction validation included
    def test_case_36_form_task_form_interaction_validation_included(self) -> None:
        prof = _mock_repo_profile(components=[{"name": "LoginForm", "path": "src/components/LoginForm.tsx"}])
        plan = self.planner.plan(
            user_request="Improve login form validation states",
            workflow="existing-ui",
            repo_profile=prof,
            task_intent="form_ux",
        )
        self.assertIn("form_interaction_test", plan["validation"]["required_checks"])
        self.assertIn("form_input_typing", plan["validation"]["interactions"])

    # CASE 37: Accessibility task -> accessibility validation included
    def test_case_37_accessibility_task_accessibility_validation_included(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Fix keyboard focus on modal",
            workflow="existing-ui",
            repo_profile=prof,
            task_intent="accessibility_fix",
        )
        self.assertIn("accessibility_axe_audit", plan["validation"]["required_checks"])
        self.assertIn("wcag_contrast_minimum_4.5_to_1", plan["validation"]["accessibility"])

    # CASE 38: Existing UI task -> preservation validation included
    def test_case_38_existing_ui_task_preservation_validation_included(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Refine card padding",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertIn("preservation_invariants_verification", plan["validation"]["required_checks"])
        self.assertIn("locked_palette_intact", plan["validation"]["preservation"])

    # CASE 39: High-risk task -> smaller batches / checkpoints
    def test_case_39_high_risk_task_smaller_batches_checkpoints(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(
            user_request="Redesign toàn bộ dashboard from scratch",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertGreaterEqual(len(plan["rollback"]["checkpoints"]), 2)

    # CASE 40: Actual changes match plan exactly -> PASS
    def test_case_40_actual_changes_match_plan_exactly_pass(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        manifest = self.editor.compare_plan_to_changes(plan, {
            "modified_files": ["src/components/Button.tsx"],
            "actual_change_levels": [L1],
        })
        self.assertFalse(manifest["drift_detected"])
        self.assertEqual(manifest["status"], "passed")

    # CASE 41: Actual change level > planned level -> FAIL
    def test_case_41_actual_change_level_greater_than_planned_fail(self) -> None:
        prof = _mock_repo_profile()
        plan = self.planner.plan(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        # Plan was L1, actual is L3
        manifest = self.editor.compare_plan_to_changes(plan, {
            "modified_files": ["src/components/Button.tsx"],
            "actual_change_levels": [L3],
        })
        self.assertEqual(manifest["status"], "failed_permission")
        self.assertTrue(any("escalated" in r for r in manifest["drift_reasons"]))

    # CASE 42: Actual affected routes > planned routes -> FAIL
    def test_case_42_actual_affected_routes_greater_than_planned_fail(self) -> None:
        prof = _mock_repo_profile(routes=["/checkout"])
        plan = self.planner.plan(user_request="Improve checkout button", workflow="existing-ui", repo_profile=prof)
        manifest = self.editor.compare_plan_to_changes(plan, {
            "modified_files": ["src/components/Button.tsx"],
            "changed_routes": ["/checkout", "/unauthorized-admin-route"],
        })
        self.assertTrue(manifest["drift_detected"])
        self.assertEqual(manifest["status"], "failed_drift")

    # CASE 43: Domain guidance suggests extra UX improvement outside scope -> not automatically added
    def test_case_43_domain_guidance_extra_ux_outside_scope_not_added(self) -> None:
        prof = _mock_repo_profile(routes=["/cart", "/checkout"])
        # E-commerce task to fix button should NOT expand into cart or checkout redesign
        plan = self.planner.plan(
            user_request="Fix button alignment on product card",
            workflow="existing-ui",
            repo_profile=prof,
        )
        self.assertEqual(plan["request"]["requested_scope"], "component")
        self.assertEqual(plan["blast_radius"]["allowed_files"], ["src/components/Button.tsx"])

    # CASE 44: Knowledge Plan contains optional inspiration -> does not widen editing scope
    def test_case_44_knowledge_plan_optional_inspiration_does_not_widen_scope(self) -> None:
        prof = _mock_repo_profile()
        fake_knowledge_plan = {
            "task_intent": "visual_polish",
            "selected_skills": [{"id": "skill.design_inspiration", "weight": "small"}],
            "selected_packs": {"framework": [], "styling": []},
        }
        plan = self.planner.plan(
            user_request="Adjust button border color",
            workflow="existing-ui",
            repo_profile=prof,
            knowledge_plan=fake_knowledge_plan,
        )
        self.assertEqual(plan["change_classification"]["overall_level"], L1)
        self.assertEqual(plan["request"]["requested_scope"], "component")

    # CASE 45: Explicit user scope always wins over AI preference
    def test_case_45_explicit_user_scope_always_wins_over_ai_preference(self) -> None:
        prof = _mock_repo_profile(routes=["/dashboard"])
        plan = self.planner.plan(
            user_request="Fix card spacing in dashboard",
            workflow="existing-ui",
            repo_profile=prof,
            requested_scope="component",  # Explicitly restricted to component
        )
        self.assertEqual(plan["request"]["requested_scope"], "component")
        self.assertEqual(plan["blast_radius"]["max_scope"], "component")


class ModificationPlanQualityTests(unittest.TestCase):
    """Quality and schema integrity verification for Phase 6 Modification Plans and Manifests."""

    def test_plan_structure_and_schema_conformance(self) -> None:
        prof = _mock_repo_profile()
        plan = plan_modification(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        validation_res = validate_modification_plan(plan)
        self.assertTrue(validation_res["valid"], f"Plan validation failed: {validation_res['errors']}")
        self.assertEqual(validation_res["status"], "ready")

    def test_evaluate_plan_permissions_api(self) -> None:
        prof = _mock_repo_profile()
        plan_ready = plan_modification(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        perm_ready = evaluate_plan_permissions(plan_ready)
        self.assertTrue(perm_ready["authorized"])

        plan_blocked = plan_modification(user_request="Change primary color to purple", workflow="existing-ui", repo_profile=prof)
        perm_blocked = evaluate_plan_permissions(plan_blocked)
        self.assertFalse(perm_blocked["authorized"])
        self.assertEqual(perm_blocked["status"], "blocked")

    def test_change_manifest_structure(self) -> None:
        prof = _mock_repo_profile()
        plan = plan_modification(user_request="Fix button spacing", workflow="existing-ui", repo_profile=prof)
        manifest = compare_plan_to_changes(plan, {"modified_files": ["src/components/Button.tsx"]})
        self.assertEqual(manifest["schema_version"], 1)
        self.assertTrue(manifest["manifest_id"].startswith("manifest_"))
        self.assertEqual(manifest["status"], "passed")
        self.assertFalse(manifest["drift_detected"])


if __name__ == "__main__":
    unittest.main()
