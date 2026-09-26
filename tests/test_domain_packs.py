"""Unit, quality, and regression test suite for Phase 5: Domain Design Packs.

Covers all 36 mandatory test cases, domain pack quality tests,
and context efficiency verification.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import Any
import sys
sys.path.insert(0, str(Path(__file__).parent))
import _paths  # noqa: F401

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PLUGIN_ROOT = _REPO_ROOT / "plugins" / "ui-engineering"

from uiux import api
from uiux.engine import knowledge_router
from uiux.engine.knowledge_router.budget import ContextBudgetManager
from uiux.engine.knowledge_router.domain_classifier import (
    DOMAINS,
    classify_domain,
)
from uiux.engine.knowledge_router.domain_extension import (
    get_domain_pack,
    list_domain_packs,
    query_domain_subtopics,
    resolve_domain_pack,
)
from uiux.engine.knowledge_router.domain_registry import DOMAIN_PACKS
from uiux.engine.knowledge_router.metadata import (
    FRAMEWORK_PACKS,
    RUNTIME_VALIDATION_PACKS,
    STYLING_PACKS,
)
from uiux.engine.knowledge_router.resolver import KnowledgeResolver
from uiux.engine.knowledge_router.router import KnowledgeRouter
from uiux.engine.preservation import L1, L2, L3


def _mock_repo_profile(
    framework_name: str = "react",
    primary_styling: str = "plain_css",
    routes: list[str] | None = None,
    components: list[Any] | None = None,
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
        "routes": routes or [],
        "pages": [],
        "components": components or [],
        "design_tokens": {"colors": {"primary": "#3b82f6"}},
        "runtime_capabilities": {"has_node": True, "has_playwright": False},
        "overall_confidence": 0.92,
    }
    if applications:
        prof["applications"] = applications
    return prof


class DomainClassificationTests(unittest.TestCase):
    """Tests covering domain classification across multi-signal evidence, precedence, and monorepos."""

    # CASE 1: Explicit ecommerce project -> domain.ecommerce
    def test_case_01_explicit_ecommerce_declaration(self) -> None:
        res = classify_domain(user_request="", explicit_domain="ecommerce")
        self.assertEqual(res["primary_domain"], "ecommerce")
        self.assertEqual(res["confidence"], 1.0)
        self.assertEqual(res["source"], "explicit")
        self.assertEqual(res["secondary_domains"], [])

        # Check alias
        res_alias = classify_domain(user_request="", explicit_domain="shop")
        self.assertEqual(res_alias["primary_domain"], "ecommerce")
        self.assertEqual(res_alias["source"], "explicit")

    # CASE 2: Routes product/cart/checkout -> ecommerce confidence cao
    def test_case_02_routes_ecommerce_evidence(self) -> None:
        prof = _mock_repo_profile(routes=["/products", "/cart", "/checkout"])
        res = classify_domain(user_request="view items", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "ecommerce")
        self.assertGreaterEqual(res["confidence"], 0.65)
        self.assertEqual(res["source"], "inferred")

    # CASE 3: Beauty ecommerce -> primary ecommerce, secondary beauty_fashion
    def test_case_03_beauty_ecommerce_multi_domain(self) -> None:
        prof = _mock_repo_profile(
            routes=["/products", "/cart", "/checkout", "/lookbook"],
            components=["ProductCard", "CartDrawer", "ShadeSwatch"],
        )
        res = classify_domain(
            user_request="Browse makeup collection, select shade swatch and checkout cart",
            repo_profile=prof,
        )
        self.assertEqual(res["primary_domain"], "ecommerce")
        self.assertIn("beauty_fashion", res["secondary_domains"])
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 4: SaaS dashboard -> domain.saas_ai
    def test_case_04_saas_dashboard_detection(self) -> None:
        prof = _mock_repo_profile(
            routes=["/dashboard", "/workspace", "/pricing", "/billing"],
            components=["MetricCard", "WorkspaceShell", "PricingTable"],
        )
        res = classify_domain(user_request="Manage subscription and team workspace", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "saas_ai")
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 5: Developer CLI/dashboard -> developer_tool
    def test_case_05_developer_tool_detection(self) -> None:
        prof = _mock_repo_profile(
            routes=["/terminal", "/logs", "/metrics", "/debug"],
            components=["CodeBlock", "LogViewer", "TerminalEmulator"],
        )
        res = classify_domain(user_request="View stack trace and terminal output in debugger", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "developer_tool")
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 6: Hotel booking -> hospitality_travel
    def test_case_06_hospitality_travel_detection(self) -> None:
        prof = _mock_repo_profile(
            routes=["/hotels", "/rooms", "/booking", "/destinations"],
            components=["DateRangePicker", "GuestCounter", "RoomCard"],
        )
        res = classify_domain(user_request="Reserve hotel room for guests and check availability", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "hospitality_travel")
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 7: Patient/practitioner UI -> healthcare
    def test_case_07_healthcare_detection(self) -> None:
        prof = _mock_repo_profile(
            routes=["/patients", "/appointments", "/records", "/prescriptions"],
            components=["PatientHeader", "VitalSignsCard", "MedicationList"],
        )
        res = classify_domain(user_request="Schedule appointment for patient vitals and clinic records", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "healthcare")
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 8: Transaction/payment dashboard -> finance_fintech
    def test_case_08_finance_fintech_detection(self) -> None:
        prof = _mock_repo_profile(
            routes=["/transfers", "/accounts", "/transactions", "/wallet"],
            components=["BalanceDisplay", "TransferModal", "TransactionList"],
        )
        res = classify_domain(user_request="Transfer funds and check account balance and transaction history", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "finance_fintech")
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 9: Portfolio/case studies -> portfolio_agency
    def test_case_09_portfolio_agency_detection(self) -> None:
        prof = _mock_repo_profile(
            routes=["/projects", "/case-studies", "/services", "/about"],
            components=["ProjectShowcase", "CaseStudyHero", "TestimonialSlider"],
        )
        res = classify_domain(user_request="Showcase agency case studies and creative client projects", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "portfolio_agency")
        self.assertGreaterEqual(res["confidence"], 0.70)

    # CASE 10: Weak evidence -> general/unknown
    def test_case_10_weak_evidence_falls_back_to_general(self) -> None:
        prof = _mock_repo_profile(routes=["/about", "/contact"])
        res = classify_domain(user_request="Update footer text", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "general")
        self.assertLessEqual(res["confidence"], 0.40)
        self.assertEqual(res["secondary_domains"], [])

    # CASE 11: User explicit domain overrides weak inference
    def test_case_11_explicit_domain_overrides_inference(self) -> None:
        prof = _mock_repo_profile(routes=["/pricing", "/about"])
        res = classify_domain(
            user_request="Add contact page",
            repo_profile=prof,
            explicit_domain="healthcare",
        )
        self.assertEqual(res["primary_domain"], "healthcare")
        self.assertEqual(res["source"], "explicit")
        self.assertEqual(res["confidence"], 1.0)

    # CASE 19: Multi-domain evidence weak -> don't load 2 packs
    def test_case_19_weak_multi_domain_does_not_load_secondary(self) -> None:
        prof = _mock_repo_profile(
            routes=["/products", "/cart", "/checkout"],
            components=["ProductCard"],
        )
        # Mentions "look" once, not enough to trigger beauty secondary
        res = classify_domain(user_request="Look at cart checkout page", repo_profile=prof)
        self.assertEqual(res["primary_domain"], "ecommerce")
        self.assertEqual(res["secondary_domains"], [])

    # CASE 20: Multi-domain evidence strong -> primary + one secondary
    def test_case_20_strong_multi_domain_loads_one_secondary_only(self) -> None:
        prof = _mock_repo_profile(
            routes=["/products", "/cart", "/checkout", "/collections", "/lookbook"],
            components=["ProductCard", "ShadeSwatch"],
        )
        res = classify_domain(
            user_request="Shop beauty cosmetics collection with shade swatches and cart checkout",
            repo_profile=prof,
        )
        self.assertEqual(res["primary_domain"], "ecommerce")
        self.assertEqual(len(res["secondary_domains"]), 1)
        self.assertEqual(res["secondary_domains"][0], "beauty_fashion")

    # CASE 23: Unknown domain -> safe fallback
    def test_case_23_unknown_domain_safe_fallback(self) -> None:
        res = classify_domain(user_request="Do some work", repo_profile=None)
        self.assertEqual(res["primary_domain"], "general")
        self.assertIn("general", res["evidence"][0].lower())

    # CASE 24: Unsupported explicit domain -> diagnostics warning, no crash
    def test_case_24_unsupported_explicit_domain_safe(self) -> None:
        router = KnowledgeRouter()
        plan = router.route({
            "domain": "education_platform",
            "user_request": "Build course player",
        })
        self.assertEqual(plan["domain_context"]["primary"], None)
        self.assertTrue(len(plan["diagnostics"]["warnings"]) > 0)
        self.assertTrue(any("education_platform" in w for w in plan["diagnostics"]["warnings"]))

    # CASE 25: Monorepo different domain per app -> correct app domain only
    def test_case_25_monorepo_different_domain_per_app(self) -> None:
        monorepo_profile = {
            "schema_version": 1,
            "framework": {"name": "nextjs", "version": "14.0.0", "confidence": 0.95, "evidence": []},
            "styling_system": {"primary": "tailwindcss", "detected": ["tailwindcss"], "confidence": 0.9},
            "applications": {
                "storefront": {
                    "repo_profile": _mock_repo_profile(
                        routes=["/products", "/cart", "/checkout"],
                        components=["ProductCard", "CartDrawer"],
                    ),
                },
                "admin": {
                    "repo_profile": _mock_repo_profile(
                        routes=["/dashboard", "/metrics", "/settings", "/billing"],
                        components=["MetricCard", "WorkspaceShell"],
                    ),
                },
                "docs": {
                    "repo_profile": _mock_repo_profile(
                        routes=["/docs", "/terminal", "/logs"],
                        components=["CodeBlock", "LogViewer"],
                    ),
                },
            },
        }

        # App 1: Storefront
        res_store = classify_domain(
            user_request="Improve page",
            repo_profile=monorepo_profile,
            requested_scope="storefront",
        )
        self.assertEqual(res_store["primary_domain"], "ecommerce")

        # App 2: Admin
        res_admin = classify_domain(
            user_request="Improve page",
            repo_profile=monorepo_profile,
            requested_scope="admin",
        )
        self.assertEqual(res_admin["primary_domain"], "saas_ai")

        # App 3: Docs
        res_docs = classify_domain(
            user_request="Improve page",
            repo_profile=monorepo_profile,
            requested_scope="docs",
        )
        self.assertEqual(res_docs["primary_domain"], "developer_tool")


class DomainRouterIntegrationTests(unittest.TestCase):
    """Tests covering domain pack routing, precedence, subtopics, and budget."""

    def setUp(self) -> None:
        self.router = KnowledgeRouter()

    # CASE 12: Existing UI ecommerce -> domain pack loaded, palette remains locked
    def test_case_12_existing_ui_ecommerce_locks_palette(self) -> None:
        prof = _mock_repo_profile(routes=["/cart", "/checkout", "/products"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "existing_ui_profile": {
                "color_system": {"primary": "#e11d48", "background": "#ffffff"},
                "typography_system": {"font_families": ["Inter"]},
            },
            "user_request": "Update product cart layout",
        })
        # Domain pack is loaded
        dom_ids = [d["id"] for d in plan["selected_packs"]["domain"]]
        self.assertIn("domain.ecommerce", dom_ids)

        # Palette remains strictly locked
        self.assertEqual(plan["preservation_context"]["palette"], "locked")
        self.assertEqual(plan["preservation_context"]["brand_identity"], "locked")

        # Rationale confirms Level 6 precedence
        rationale_str = " ".join(plan["rationale"])
        self.assertIn("Level 6", rationale_str)

    # CASE 13: Existing healthcare UI -> domain guidance cannot recolor brand
    def test_case_13_existing_healthcare_ui_cannot_recolor_brand(self) -> None:
        prof = _mock_repo_profile(routes=["/patients", "/appointments"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "existing_ui_profile": {
                "color_system": {"primary": "#7c3aed", "background": "#f8fafc"},  # Purple brand
            },
            "user_request": "Add patient vitals card",
        })
        dom_ids = [d["id"] for d in plan["selected_packs"]["domain"]]
        self.assertIn("domain.healthcare", dom_ids)
        self.assertEqual(plan["preservation_context"]["palette"], "locked")
        self.assertEqual(plan["preservation_context"]["brand_identity"], "locked")

    # CASE 14: Greenfield fintech -> domain can influence hierarchy but not violate explicit user palette
    def test_case_14_greenfield_fintech_respects_explicit_palette(self) -> None:
        plan = self.router.route({
            "workflow": "greenfield",
            "domain": "finance_fintech",
            "explicit_constraints": {"palette": ["#000000", "#ffffff"]},  # Monochrome request
            "user_request": "Build monochrome bank dashboard",
        })
        dom_ids = [d["id"] for d in plan["selected_packs"]["domain"]]
        self.assertIn("domain.finance_fintech", dom_ids)
        self.assertEqual(plan["preservation_context"]["palette"], "editable")
        # Explicit constraints are in plan
        self.assertIn("Greenfield domain intelligence applied", " ".join(plan["rationale"]))

    # CASE 15: Ecommerce button-only task -> no full ecommerce context load
    def test_case_15_ecommerce_button_only_task_minimal_context(self) -> None:
        prof = _mock_repo_profile(routes=["/cart", "/checkout", "/products"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix button alignment on card",
            "task_intent": "component_refactor",
        })
        dom_packs = plan["selected_packs"]["domain"]
        if dom_packs:
            # Domain entry should have small weight because no specific flows are queried
            self.assertEqual(dom_packs[0]["weight"], "small")
            # Subtopics should be empty for a local button task
            self.assertEqual(plan["domain_context"]["selected_subtopics"], [])

    # CASE 16: Ecommerce checkout task -> checkout subtopic loaded
    def test_case_16_ecommerce_checkout_subtopic_loaded(self) -> None:
        prof = _mock_repo_profile(routes=["/cart", "/checkout", "/products"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Redesign checkout payment flow and order summary",
        })
        subtopics = plan["domain_context"]["selected_subtopics"]
        self.assertIn("checkout", subtopics)
        self.assertIn("cart", subtopics)

    # CASE 17: Hospitality room-selection task -> room-selection/booking subtopic
    def test_case_17_hospitality_room_selection_subtopic_loaded(self) -> None:
        prof = _mock_repo_profile(routes=["/hotels", "/rooms", "/booking"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Select hotel room and bed rate breakdown",
        })
        subtopics = plan["domain_context"]["selected_subtopics"]
        self.assertIn("room_selection", subtopics)

    # CASE 18: SaaS AI interaction task -> AI interaction guidance
    def test_case_18_saas_ai_interaction_subtopic_loaded(self) -> None:
        prof = _mock_repo_profile(routes=["/dashboard", "/workspace"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Add AI prompt input with streaming response and retry mechanism",
        })
        subtopics = plan["domain_context"]["selected_subtopics"]
        self.assertIn("ai_interaction", subtopics)

    # CASE 21: Context budget exceeded -> secondary/optional domain knowledge pruned first
    def test_case_21_budget_exceeded_prunes_optional_domain_knowledge(self) -> None:
        # Tight budget limit (6 pts: protected items take 4 pts, ecommerce takes 2 pts = 6 pts; beauty_fashion needs 1 pt -> pruned)
        budget_mgr = ContextBudgetManager(budget_limit_points=6)
        items = [
            {"id": "preservation.existing_ui_invariants", "category": "preservation", "priority": "critical", "required": True, "weight": "medium"},
            {"id": "framework.nextjs", "category": "framework", "priority": "high", "required": True, "weight": "medium"},
            {"id": "domain.ecommerce", "category": "domain", "priority": "high", "required": False, "weight": "medium"},
            {"id": "domain.beauty_fashion", "category": "domain", "priority": "medium", "required": False, "weight": "small"},
        ]
        selected, excluded, info = budget_mgr.apply_budget(items)
        sel_ids = [it["id"] for it in selected]
        excl_ids = [it["id"] for it in excluded]

        # Critical preservation and required framework MUST stay
        self.assertIn("preservation.existing_ui_invariants", sel_ids)
        self.assertIn("framework.nextjs", sel_ids)
        # Secondary domain must be pruned first
        self.assertIn("domain.beauty_fashion", excl_ids)

    # CASE 22: Preservation invariants never pruned for domain knowledge
    def test_case_22_preservation_never_pruned_for_domain(self) -> None:
        budget_mgr = ContextBudgetManager(budget_limit_points=2)  # Tiny budget
        items = [
            {"id": "preservation.existing_ui_invariants", "category": "preservation", "priority": "critical", "required": True, "weight": "medium"},
            {"id": "domain.ecommerce", "category": "domain", "priority": "high", "required": False, "weight": "medium"},
        ]
        selected, excluded, _ = budget_mgr.apply_budget(items)
        sel_ids = [it["id"] for it in selected]
        excl_ids = [it["id"] for it in excluded]

        self.assertIn("preservation.existing_ui_invariants", sel_ids)
        self.assertIn("domain.ecommerce", excl_ids)

    # CASE 26: Domain + Next.js + Tailwind -> composable routing
    def test_case_26_composable_domain_framework_styling_routing(self) -> None:
        prof = _mock_repo_profile(
            framework_name="nextjs",
            primary_styling="tailwindcss",
            routes=["/cart", "/checkout", "/products"],
        )
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "greenfield",
            "user_request": "Build ecommerce checkout with Next.js and Tailwind",
        })
        fw_ids = [f["id"] for f in plan["selected_packs"]["framework"]]
        st_ids = [s["id"] for s in plan["selected_packs"]["styling"]]
        dom_ids = [d["id"] for d in plan["selected_packs"]["domain"]]

        self.assertIn("framework.nextjs", fw_ids)
        self.assertIn("styling.tailwindcss", st_ids)
        self.assertIn("domain.ecommerce", dom_ids)

        # Verify load_order hierarchy: framework -> styling -> domain -> skills
        order = plan["load_order"]
        idx_fw = order.index("framework.nextjs")
        idx_st = order.index("styling.tailwindcss")
        idx_dom = order.index("domain.ecommerce")
        self.assertLess(idx_fw, idx_st)
        self.assertLess(idx_st, idx_dom)

    # CASE 27: Domain pack does not duplicate framework/styling rules
    def test_case_27_domain_packs_do_not_duplicate_framework_or_styling(self) -> None:
        for pack_id, pack in DOMAIN_PACKS.items():
            source_file = _PLUGIN_ROOT / pack["source"]
            content = source_file.read_text(encoding="utf-8")
            # Verify no framework-specific hooks or Tailwind utilities are mandated
            self.assertNotIn("useState(", content)
            self.assertNotIn("useEffect(", content)
            self.assertNotIn("className=\"flex items-center", content)

    # CASE 33: Runtime validation recommendations map to existing validation packs
    def test_case_33_runtime_validation_mapping(self) -> None:
        for pack_id, pack in DOMAIN_PACKS.items():
            rec_runtime = pack.get("recommended_runtime_validation", [])
            for rt_id in rec_runtime:
                self.assertIn(rt_id, RUNTIME_VALIDATION_PACKS, f"{pack_id} references unknown runtime {rt_id}")

    # CASE 34: Existing UI inspiration does not override domain/brand precedence
    def test_case_34_existing_ui_inspiration_precedence(self) -> None:
        prof = _mock_repo_profile(routes=["/cart", "/products"])
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Make it look like a cool modern ecommerce site with crazy animations",
        })
        # Inspiration skill cannot override locked palette
        self.assertEqual(plan["preservation_context"]["palette"], "locked")
        self.assertEqual(plan["preservation_context"]["brand_identity"], "locked")

    # CASE 36: Phase 4 context efficiency still holds
    def test_case_36_context_efficiency_still_holds(self) -> None:
        prof = _mock_repo_profile(framework_name="vue", primary_styling="sass")
        plan = self.router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "user_request": "Fix button border color",
            "task_intent": "visual_polish",
        })
        # Only Vue and Sass should be routed, no unrelated frameworks or bloated domains
        fw_ids = [f["id"] for f in plan["selected_packs"]["framework"]]
        st_ids = [s["id"] for s in plan["selected_packs"]["styling"]]
        self.assertEqual(fw_ids, ["framework.vue"])
        self.assertEqual(st_ids, ["styling.sass_scss"])
        self.assertLessEqual(plan["context_budget"]["used_points"], 15)


class DomainPackQualityTests(unittest.TestCase):
    """Quality, schema integrity, and anti-cloning verification for all 8 Domain Packs."""

    # CASE 28: Domain pack metadata valid
    def test_case_28_domain_pack_metadata_valid(self) -> None:
        expected_domains = [
            "domain.ecommerce",
            "domain.beauty_fashion",
            "domain.saas_ai",
            "domain.developer_tool",
            "domain.hospitality_travel",
            "domain.healthcare",
            "domain.finance_fintech",
            "domain.portfolio_agency",
        ]
        self.assertEqual(len(DOMAIN_PACKS), 8)
        for dom_id in expected_domains:
            self.assertIn(dom_id, DOMAIN_PACKS)
            pack = DOMAIN_PACKS[dom_id]
            self.assertEqual(pack["id"], dom_id)
            self.assertEqual(pack["status"], "stable")
            self.assertEqual(pack["version"], "1.0.0")
            self.assertIsInstance(pack["subtopics"], dict)
            self.assertGreaterEqual(len(pack["subtopics"]), 3)
            self.assertGreaterEqual(len(pack["critical_flows"]), 2)
            self.assertGreaterEqual(len(pack["required_states"]), 4)
            self.assertGreaterEqual(len(pack["anti_patterns"]), 2)

    # CASE 29: Every domain resource exists
    def test_case_29_every_domain_resource_file_exists(self) -> None:
        for dom_id, pack in DOMAIN_PACKS.items():
            rel_path = pack["source"]
            full_path = _PLUGIN_ROOT / rel_path
            self.assertTrue(full_path.is_file(), f"Missing markdown file: {full_path}")

    # CASE 30: Every subtopic reference resolves
    def test_case_30_every_subtopic_reference_resolves(self) -> None:
        for dom_id, pack in DOMAIN_PACKS.items():
            domain_name = pack["domain"]
            for sub_key in pack["subtopics"].keys():
                # Querying with the subtopic key directly should find it
                matched = query_domain_subtopics(domain_name, f"Work on {sub_key} section")
                self.assertIn(sub_key, matched, f"Failed to query subtopic {sub_key} for {domain_name}")

    # CASE 31: Domain anti-pattern metadata available
    def test_case_31_domain_anti_patterns_available(self) -> None:
        for dom_id, pack in DOMAIN_PACKS.items():
            anti_patterns = pack.get("anti_patterns", [])
            self.assertGreaterEqual(len(anti_patterns), 2)
            for ap in anti_patterns:
                self.assertIsInstance(ap, str)
                self.assertGreater(len(ap), 10)

    # CASE 32: Required states metadata available
    def test_case_32_required_states_available(self) -> None:
        standard_states = {"loading", "empty", "error", "confirmation", "out_of_stock", "pending"}
        for dom_id, pack in DOMAIN_PACKS.items():
            req_states = pack.get("required_states", [])
            self.assertGreaterEqual(len(req_states), 3)
            # Ensure at least some standard states exist
            overlap = set(req_states) & standard_states
            self.assertTrue(len(overlap) > 0, f"{dom_id} has no recognizable states: {req_states}")

    # CASE 35: No exact product cloning instructions exist in packs
    def test_case_35_no_exact_product_cloning_instructions(self) -> None:
        forbidden_clone_phrases = [
            "clone shopee", "clone amazon", "clone airbnb", "clone stripe", "clone linear",
            "pixel-perfect copy of", "copy the exact layout of", "exact clone",
        ]
        for dom_id, pack in DOMAIN_PACKS.items():
            rel_path = pack["source"]
            full_path = _PLUGIN_ROOT / rel_path
            text = full_path.read_text(encoding="utf-8").lower()
            for phrase in forbidden_clone_phrases:
                self.assertNotIn(phrase, text, f"Found forbidden clone phrase '{phrase}' in {rel_path}")

    # CASE 37: Domain packs specify UI state representation only, no business/medical/financial decision logic
    def test_case_37_domain_packs_do_not_generate_business_logic(self) -> None:
        health_pack = DOMAIN_PACKS["domain.healthcare"]
        finance_pack = DOMAIN_PACKS["domain.finance_fintech"]

        # Healthcare: critical_alert / dosage_warning are UI representation states
        self.assertIn("critical_alert", health_pack["required_states"])
        self.assertIn("dosage_warning", health_pack["required_states"])

        # Finance: risk_blocked / insufficient_balance are UI representation states
        self.assertIn("risk_blocked", finance_pack["required_states"])
        self.assertIn("insufficient_balance", finance_pack["required_states"])

        # Markdown verification: must explicitly prohibit clinical diagnosis or automated trading
        health_text = (_PLUGIN_ROOT / health_pack["source"]).read_text(encoding="utf-8")
        self.assertIn("NEVER generate medical diagnoses", health_text)

        finance_text = (_PLUGIN_ROOT / finance_pack["source"]).read_text(encoding="utf-8")
        self.assertIn("NEVER generate algorithmic financial recommendations", finance_text)


class ContextEfficiencyVerification(unittest.TestCase):
    """Context efficiency proof for Next.js + Tailwind ecommerce checkout."""

    def test_ecommerce_checkout_context_efficiency(self) -> None:
        router = KnowledgeRouter()
        prof = _mock_repo_profile(
            framework_name="nextjs",
            primary_styling="tailwindcss",
            routes=["/products", "/cart", "/checkout"],
        )
        plan = router.route({
            "repo_profile": prof,
            "workflow": "existing-ui",
            "existing_ui_profile": {
                "color_system": {"primary": "#3b82f6", "background": "#ffffff"},
            },
            "user_request": "Redesign the checkout payment flow and review order steps",
            "task_intent": "page_redesign",
        })

        sel_fw = [f["id"] for f in plan["selected_packs"]["framework"]]
        sel_st = [s["id"] for s in plan["selected_packs"]["styling"]]
        sel_dom = [d["id"] for d in plan["selected_packs"]["domain"]]
        sel_rt = [r["id"] for r in plan["selected_packs"]["runtime"]]
        subtopics = plan["domain_context"]["selected_subtopics"]

        # MUST LOAD:
        self.assertIn("framework.nextjs", sel_fw)
        self.assertIn("styling.tailwindcss", sel_st)
        self.assertIn("domain.ecommerce", sel_dom)
        self.assertIn("checkout", subtopics)

        # MUST NOT LOAD:
        # Unrelated domains
        self.assertNotIn("domain.beauty_fashion", sel_dom)
        self.assertNotIn("domain.hospitality_travel", sel_dom)
        self.assertNotIn("domain.healthcare", sel_dom)
        self.assertNotIn("domain.finance_fintech", sel_dom)
        self.assertNotIn("domain.developer_tool", sel_dom)
        self.assertNotIn("domain.portfolio_agency", sel_dom)
        self.assertNotIn("domain.saas_ai", sel_dom)

        # Unrelated frameworks
        self.assertNotIn("framework.vue", sel_fw)
        self.assertNotIn("framework.angular", sel_fw)
        self.assertNotIn("framework.svelte", sel_fw)

        # Budget verification: strictly under DEFAULT_BUDGET_POINTS
        used_pts = plan["context_budget"]["used_points"]
        limit_pts = plan["context_budget"]["budget_limit_points"]
        self.assertLessEqual(used_pts, limit_pts)
        self.assertEqual(plan["context_budget"]["budget_status"], "within_budget")


if __name__ == "__main__":
    unittest.main()
