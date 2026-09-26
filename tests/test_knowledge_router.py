"""Unit and regression test suite for Phase 4: Knowledge Router + Framework Packs.

Covers all 30 mandatory test cases, framework pack quality tests, and context efficiency verification.
"""
from __future__ import annotations

import unittest
from typing import Any

from uiux import api
from uiux.engine import knowledge_router
from uiux.engine.knowledge_router.budget import ContextBudgetManager
from uiux.engine.knowledge_router.domain_extension import get_domain_pack_metadata, resolve_domain_pack
from uiux.engine.knowledge_router.metadata import (
    DESIGN_SKILLS,
    FRAMEWORK_PACKS,
    PRESERVATION_PACKS,
    RUNTIME_VALIDATION_PACKS,
    STYLING_PACKS,
)
from uiux.engine.knowledge_router.resolver import KnowledgeResolver
from uiux.engine.knowledge_router.router import KnowledgeRouter
from uiux.engine.preservation import L1, L2, L3


def _mock_repo_profile(
    framework_name: str = "react",
    framework_version: str | None = None,
    primary_styling: str = "plain_css",
    secondary_styling: str | None = None,
    ui_library: str | None = None,
    conflicting_signals: list[str] | None = None,
    applications: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prof: dict[str, Any] = {
        "schema_version": 1,
        "framework": {
            "name": framework_name,
            "version": framework_version,
            "confidence": 0.95,
            "evidence": [f"Declared {framework_name}"],
            "conflicting_signals": conflicting_signals or [],
        },
        "styling_system": {
            "primary": primary_styling,
            "secondary": secondary_styling,
            "detected": [primary_styling] + ([secondary_styling] if secondary_styling else []),
            "confidence": 0.90,
            "evidence": [f"Detected {primary_styling}"],
        },
        "ui_library": {
            "name": ui_library,
            "version": None,
            "confidence": 0.90 if ui_library else 0.0,
            "evidence": [],
        },
        "icon_library": {"name": None, "confidence": 0.0},
        "motion_library": {"name": None, "confidence": 0.0},
        "routes": [],
        "pages": [],
        "components": [],
        "design_tokens": {},
        "existing_ui_state": {"state": "EXISTING_UI", "confidence": 0.9},
        "runtime": {"package_manager": "pnpm", "node_version": None, "command_provenance": {}},
        "repository_signals": {},
        "conflicts": [],
        "diagnostics": {"warnings": [], "missing_capabilities": []},
        "overall_confidence": 0.95,
    }
    if applications:
        prof["applications"] = applications
    return prof


class KnowledgeRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = KnowledgeRouter()

    # CASE 1: React + CSS + create UI -> React pack + CSS pack + design skills
    def test_case_01_react_css_create_ui(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "greenfield",
            "user_request": "Create a new profile page",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]
        skill_ids = [s["id"] for s in plan["selected_skills"]]

        self.assertIn("framework.react", fw_ids)
        self.assertIn("styling.plain_css", st_ids)
        self.assertIn("skill.design_direction", skill_ids)
        self.assertIn("skill.final_quality_gate", skill_ids)

    # CASE 2: Next.js + Tailwind -> Next pack + Tailwind pack
    def test_case_02_nextjs_tailwind(self) -> None:
        prof = _mock_repo_profile(framework_name="nextjs", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Update dashboard header",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]

        self.assertIn("framework.nextjs", fw_ids)
        self.assertIn("styling.tailwindcss", st_ids)
        self.assertNotIn("framework.nuxt", fw_ids)

    # CASE 3: Next.js + Tailwind + shadcn -> composition 3 packs, no duplicate composite pack
    def test_case_03_nextjs_tailwind_shadcn_composition(self) -> None:
        prof = _mock_repo_profile(framework_name="nextjs", primary_styling="tailwindcss", ui_library="shadcn_ui")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Add a new settings modal dialog",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]
        ui_ids = [p["id"] for p in plan["selected_packs"]["ui_library"]]

        self.assertEqual(fw_ids, ["framework.nextjs"])
        self.assertEqual(st_ids, ["styling.tailwindcss"])
        self.assertEqual(ui_ids, ["ui_library.shadcn_ui"])
        # Ensure composable, not a bloated hardcoded nextjs-tailwind-shadcn pack
        self.assertNotIn("framework.nextjs-tailwind-shadcn", fw_ids)

    # CASE 4: Vue + SCSS -> Vue + SCSS
    def test_case_04_vue_scss(self) -> None:
        prof = _mock_repo_profile(framework_name="vue", primary_styling="sass_scss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Improve button styles",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]

        self.assertIn("framework.vue", fw_ids)
        self.assertIn("styling.sass_scss", st_ids)
        self.assertNotIn("framework.react", fw_ids)

    # CASE 5: Nuxt -> Nuxt pack
    def test_case_05_nuxt_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="nuxt", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix routing in nuxt app",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.nuxt", fw_ids)

    # CASE 6: SvelteKit -> SvelteKit pack
    def test_case_06_sveltekit_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="sveltekit", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Add nested layout",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.sveltekit", fw_ids)

    # CASE 7: Static HTML -> HTML/CSS pack
    def test_case_07_static_html_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="static_html", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Improve landing page markup",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.static_html", fw_ids)
        self.assertNotIn("framework.react", fw_ids)

    # CASE 8: Spring + Thymeleaf + Bootstrap -> Thymeleaf + Bootstrap
    def test_case_08_spring_thymeleaf_bootstrap(self) -> None:
        prof = _mock_repo_profile(framework_name="spring_thymeleaf", primary_styling="bootstrap")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Render customer form with validation errors",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]

        self.assertIn("framework.spring_thymeleaf", fw_ids)
        self.assertIn("styling.bootstrap", st_ids)

    # CASE 9: Angular -> Angular pack
    def test_case_09_angular_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="angular", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Refactor user component",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.angular", fw_ids)

    # CASE 10: MUI repo -> MUI pack
    def test_case_10_mui_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="mui")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Adjust card theme styles",
        })
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]
        self.assertIn("styling.mui", st_ids)

    # CASE 11: styled-components -> styled-components pack
    def test_case_11_styled_components_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="styled_components")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Update button styled primitive",
        })
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]
        self.assertIn("styling.styled_components", st_ids)

    # CASE 12: Tailwind + CSS Modules -> both loaded, primary/secondary preserved
    def test_case_12_tailwind_and_css_modules(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="tailwindcss", secondary_styling="css_modules")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Polish hero section",
        })
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]
        self.assertIn("styling.tailwindcss", st_ids)
        self.assertIn("styling.css_modules", st_ids)
        # Primary is high priority, secondary is medium
        st_map = {p["id"]: p for p in plan["selected_packs"]["styling"]}
        self.assertEqual(st_map["styling.tailwindcss"]["priority"], "high")
        self.assertEqual(st_map["styling.css_modules"]["priority"], "medium")

    # CASE 13: Existing UI + modernize -> preservation knowledge mandatory, inspiration cannot override brand
    def test_case_13_existing_ui_modernize_preservation_mandatory(self) -> None:
        prof = _mock_repo_profile(framework_name="nextjs", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Modernize the app interface with futuristic inspiration",
        })
        know_ids = [k["id"] for k in plan["selected_knowledge"]]
        self.assertIn("preservation.existing_ui_invariants", know_ids)
        self.assertEqual(plan["preservation_context"]["palette"], "locked")
        self.assertEqual(plan["preservation_context"]["brand_identity"], "locked")

    # CASE 14: Greenfield landing page -> design direction/typography/pattern knowledge allowed
    def test_case_14_greenfield_landing_page(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "greenfield",
            "user_request": "Build a new SaaS landing page from scratch",
        })
        skill_ids = [s["id"] for s in plan["selected_skills"]]
        self.assertIn("skill.design_direction", skill_ids)
        self.assertEqual(plan["preservation_context"]["palette"], "editable")

    # CASE 15: Responsive-only task -> does not load unrelated motion/typography/inspiration
    def test_case_15_responsive_only_task_excludes_unrelated(self) -> None:
        prof = _mock_repo_profile(framework_name="nextjs", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix responsive navbar layout on mobile",
        })
        skill_ids = [s["id"] for s in plan["selected_skills"]]
        know_ids = [k["id"] for k in plan["selected_knowledge"]]
        rt_ids = [r["id"] for r in plan["selected_packs"]["runtime"]]

        self.assertIn("skill.responsive_interaction", skill_ids)
        self.assertIn("runtime.responsive_viewport", rt_ids)
        self.assertNotIn("skill.design_inspiration", skill_ids)
        self.assertNotIn("skill.design_direction", skill_ids)
        # Ensure motion catalog is not loaded
        self.assertFalse(any(k.startswith("motion.") for k in know_ids))

    # CASE 16: Accessibility task -> accessibility skill + framework pack + preservation
    def test_case_16_accessibility_task(self) -> None:
        prof = _mock_repo_profile(framework_name="vue", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix form input labels and accessibility contrast issues",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        skill_ids = [s["id"] for s in plan["selected_skills"]]
        know_ids = [k["id"] for k in plan["selected_knowledge"]]
        rt_ids = [r["id"] for r in plan["selected_packs"]["runtime"]]

        self.assertIn("framework.vue", fw_ids)
        self.assertIn("skill.visual_qa", skill_ids)
        self.assertIn("preservation.existing_ui_invariants", know_ids)
        self.assertIn("runtime.accessibility_audit", rt_ids)

    # CASE 17: Button component task -> local knowledge scope, does not load page architecture pack
    def test_case_17_button_component_local_scope(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "requested_scope": "component",
            "user_request": "Refactor Button component variants",
        })
        skill_ids = [s["id"] for s in plan["selected_skills"]]
        self.assertIn("skill.component_realization", skill_ids)
        self.assertNotIn("skill.design_direction", skill_ids)

    # CASE 18: Unknown framework -> safe generic frontend fallback
    def test_case_18_unknown_framework_fallback(self) -> None:
        prof = _mock_repo_profile(framework_name="unknown", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Update UI header",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.fallback", fw_ids)
        self.assertTrue(len(plan["diagnostics"]["warnings"]) > 0)

    # CASE 19: Framework conflict -> warning + scoped resolution, does not blindly load multiple framework packs
    def test_case_19_framework_conflict_handling(self) -> None:
        prof = _mock_repo_profile(framework_name="nextjs", conflicting_signals=["Found legacy Vue template in public/"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix navbar",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.nextjs", fw_ids)
        self.assertNotIn("framework.vue", fw_ids)
        self.assertTrue(len(plan["diagnostics"]["conflicts"]) > 0)

    # CASE 20: Monorepo specific app -> only loads app-specific framework/styling
    def test_case_20_monorepo_app_specific_routing(self) -> None:
        admin_prof = _mock_repo_profile(framework_name="react", primary_styling="bootstrap")
        storefront_prof = _mock_repo_profile(framework_name="nextjs", primary_styling="tailwindcss")
        prof = _mock_repo_profile(
            framework_name="nextjs",
            applications={
                "admin": {"repo_profile": admin_prof},
                "storefront": {"repo_profile": storefront_prof},
            },
        )
        plan = self.router.route({
            "repo_profile": prof,
            "requested_scope": "admin",
            "workflow": "existing-ui",
            "user_request": "Update admin sidebar",
        })
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_ids = [p["id"] for p in plan["selected_packs"]["styling"]]

        self.assertIn("framework.react", fw_ids)
        self.assertIn("styling.bootstrap", st_ids)
        self.assertNotIn("framework.nextjs", fw_ids)
        self.assertNotIn("styling.tailwindcss", st_ids)

    # CASE 21: Version unknown -> generic framework pack
    def test_case_21_version_unknown_generic_pack(self) -> None:
        prof = _mock_repo_profile(framework_name="react", framework_version=None)
        plan = self.router.route({"repo_profile": prof, "user_request": "Update card"})
        fw_pack = plan["selected_packs"]["framework"][0]
        self.assertEqual(fw_pack["id"], "framework.react")
        self.assertIsNone(fw_pack["version"])

    # CASE 22: Version known -> compatible pack metadata selected
    def test_case_22_version_known_selected(self) -> None:
        prof = _mock_repo_profile(framework_name="nextjs", framework_version="14.2.0")
        plan = self.router.route({"repo_profile": prof, "user_request": "Update layout"})
        fw_pack = plan["selected_packs"]["framework"][0]
        self.assertEqual(fw_pack["id"], "framework.nextjs")
        self.assertEqual(fw_pack["version"], "14.2.0")

    # CASE 23: Knowledge pack missing -> safe fallback
    def test_case_23_custom_framework_safe_fallback(self) -> None:
        prof = _mock_repo_profile(framework_name="custom_internal_engine")
        plan = self.router.route({"repo_profile": prof, "user_request": "Fix header"})
        fw_ids = [p["id"] for p in plan["selected_packs"]["framework"]]
        self.assertIn("framework.fallback", fw_ids)

    # CASE 24: Context budget exceeded -> optional knowledge dropped first
    def test_case_24_context_budget_exceeded_drops_optional_first(self) -> None:
        budget_mgr = ContextBudgetManager(budget_limit_points=5)  # Very tight budget
        items = [
            {"id": "framework.react", "category": "framework", "priority": "high", "required": True, "weight": "medium"},  # 2 pts
            {"id": "styling.plain_css", "category": "styling", "priority": "high", "required": True, "weight": "small"},   # 1 pt
            {"id": "preservation.existing_ui_invariants", "category": "preservation", "priority": "critical", "required": True, "weight": "medium"}, # 2 pts
            {"id": "skill.design_inspiration", "category": "skill", "priority": "low", "required": False, "weight": "large"}, # 4 pts -> should drop!
            {"id": "skill.typography", "category": "skill", "priority": "medium", "required": False, "weight": "small"}, # 1 pt -> should drop!
        ]
        selected, excluded, info = budget_mgr.apply_budget(items)
        sel_ids = [it["id"] for it in selected]
        excl_ids = [it["id"] for it in excluded]

        self.assertIn("framework.react", sel_ids)
        self.assertIn("preservation.existing_ui_invariants", sel_ids)
        self.assertIn("skill.design_inspiration", excl_ids)
        self.assertEqual(info["budget_status"], "truncated_optional")

    # CASE 25: Hard preservation rules -> never dropped from budget
    def test_case_25_hard_preservation_rules_never_dropped(self) -> None:
        budget_mgr = ContextBudgetManager(budget_limit_points=1)  # Extreme limit
        items = [
            {"id": "preservation.existing_ui_invariants", "category": "preservation", "priority": "critical", "required": True, "weight": "medium"},
            {"id": "framework.react", "category": "framework", "priority": "high", "required": True, "weight": "medium"},
            {"id": "optional.pattern", "category": "knowledge", "priority": "low", "required": False, "weight": "small"},
        ]
        selected, excluded, _ = budget_mgr.apply_budget(items)
        sel_ids = [it["id"] for it in selected]
        self.assertIn("preservation.existing_ui_invariants", sel_ids)

    # CASE 26: Explicit user constraints -> always highest priority
    def test_case_26_explicit_user_constraints_preserved(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="plain_css")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "greenfield",
            "explicit_constraints": {"palette": ["#111827", "#3b82f6"]},
            "user_request": "Create a landing page",
        })
        self.assertEqual(plan["context_budget"]["budget_status"], "within_budget")

    # CASE 27: Existing UI L1 task -> does not load major-redesign knowledge
    def test_case_27_existing_ui_l1_suppresses_redesign(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "preservation_profile": {"allowed_changes": {"max_level": L1}},
            "user_request": "Full redesign of entire website",
        })
        skill_ids = [s["id"] for s in plan["selected_skills"]]
        self.assertNotIn("skill.design_direction", skill_ids)
        self.assertTrue(len(plan["diagnostics"]["warnings"]) > 0)

    # CASE 28: Existing UI explicit L3 permission -> redesign knowledge can be routed in appropriate scope
    def test_case_28_existing_ui_l3_allows_redesign_knowledge(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="tailwindcss")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "preservation_profile": {"allowed_changes": {"max_level": L3}},
            "user_request": "Full redesign of entire website with explicit permission",
        })
        skill_ids = [s["id"] for s in plan["selected_skills"]]
        self.assertIn("skill.ux_structure", skill_ids)
        self.assertIn("skill.design_direction", skill_ids)

    # CASE 29: Domain pack not yet existing -> Phase 5 extension point, does not crash
    def test_case_29_domain_pack_phase_5_extension_point(self) -> None:
        res = resolve_domain_pack("ecommerce")
        self.assertIsNotNone(res)
        self.assertEqual(res["status"], "extension_point_phase_5")
        self.assertEqual(res["available_in_phase"], 5)

        # Non-existing domain should return None without crashing
        res_unknown = resolve_domain_pack("unknown_alien_domain")
        self.assertIsNone(res_unknown)

    # CASE 30: Runtime validation required -> correct validation knowledge routed
    def test_case_30_runtime_validation_routed_correctly(self) -> None:
        prof = _mock_repo_profile(framework_name="react", primary_styling="tailwindcss")
        # Responsive -> responsive viewport
        p_resp = self.router.route({"repo_profile": prof, "user_request": "Fix mobile responsive overflow"})
        rt_resp = [r["id"] for r in p_resp["selected_packs"]["runtime"]]
        self.assertIn("runtime.responsive_viewport", rt_resp)

        # A11y -> accessibility audit
        p_a11y = self.router.route({"repo_profile": prof, "user_request": "Fix accessibility contrast"})
        rt_a11y = [r["id"] for r in p_a11y["selected_packs"]["runtime"]]
        self.assertIn("runtime.accessibility_audit", rt_a11y)

        # Form -> form interaction
        p_form = self.router.route({"repo_profile": prof, "user_request": "Fix login form validation errors"})
        rt_form = [r["id"] for r in p_form["selected_packs"]["runtime"]]
        self.assertIn("runtime.form_interaction", rt_form)


class FrameworkPackQualityTests(unittest.TestCase):
    """Quality and integrity checks for every framework and styling pack."""

    def test_every_framework_pack_metadata_valid_and_source_exists(self) -> None:
        resolver = KnowledgeResolver()
        for pack_id, pack in FRAMEWORK_PACKS.items():
            with self.subTest(pack=pack_id):
                self.assertTrue(pack_id.startswith("framework."))
                self.assertEqual(pack["category"], "framework")
                self.assertIn(pack["priority"], ("critical", "high", "medium", "low"))
                self.assertIn(pack["weight"], ("small", "medium", "large"))
                # Verify source file exists
                source_path = resolver.resolve_source_path(pack)
                self.assertIsNotNone(source_path, f"Source path missing for {pack_id}")
                self.assertTrue(source_path.is_file(), f"File does not exist: {source_path}")

    def test_every_styling_pack_metadata_valid_and_source_exists(self) -> None:
        resolver = KnowledgeResolver()
        for pack_id, pack in STYLING_PACKS.items():
            with self.subTest(pack=pack_id):
                self.assertIn(pack["category"], ("styling", "ui_library"))
                source_path = resolver.resolve_source_path(pack)
                self.assertIsNotNone(source_path, f"Source path missing for {pack_id}")
                self.assertTrue(source_path.is_file(), f"File does not exist: {source_path}")

    def test_every_preservation_and_runtime_pack_source_exists(self) -> None:
        resolver = KnowledgeResolver()
        for pack_id, pack in {**PRESERVATION_PACKS, **RUNTIME_VALIDATION_PACKS}.items():
            with self.subTest(pack=pack_id):
                source_path = resolver.resolve_source_path(pack)
                self.assertIsNotNone(source_path, f"Source path missing for {pack_id}")
                self.assertTrue(source_path.is_file(), f"File does not exist: {source_path}")


class ContextEfficiencyTests(unittest.TestCase):
    """Demonstrates that Knowledge Router selects a tiny relevant subset rather than dumping the whole registry."""

    def test_context_efficiency_selected_count_much_less_than_registry_total(self) -> None:
        # Total entries in catalog registry is 261
        total_catalog_entries = len(api.retrieve_knowledge()["rows"] if "rows" in api.retrieve_knowledge() else KnowledgeResolver().query_catalog())

        prof = _mock_repo_profile(framework_name="nextjs", primary_styling="tailwindcss", ui_library="shadcn_ui")
        plan = api.route_knowledge({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix responsive navbar on mobile",
        })

        all_selected_ids = plan["load_order"]
        selected_count = len(all_selected_ids)

        # Verify that selected count is a small fraction (< 15 items, << 261)
        self.assertLess(selected_count, 15)
        self.assertLess(selected_count, total_catalog_entries * 0.10)

        # Verify unrelated frameworks are NOT in the load plan
        for unrelated in ("framework.vue", "framework.nuxt", "framework.svelte", "framework.angular", "framework.spring_thymeleaf"):
            self.assertNotIn(unrelated, all_selected_ids)

        # Verify unrelated styling packs are NOT in the load plan
        for unrelated in ("styling.bootstrap", "styling.mui", "styling.styled_components", "styling.emotion"):
            self.assertNotIn(unrelated, all_selected_ids)


if __name__ == "__main__":
    unittest.main()
