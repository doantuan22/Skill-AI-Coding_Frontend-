"""Tests for UI Orchestrator, Workflow Routing, UI State Detection, and Preservation Rules.

Covers all 12 mandatory cases from Phase 1 specification:
- Case 1: Repo has almost no UI -> Greenfield
- Case 2: Repo has complete UI -> Existing UI
- Case 3: Existing UI + "improve responsive" -> Existing UI, L1/L2, palette locked
- Case 4: Existing UI + "modernize the UI" -> Existing UI, no auto L3, palette/brand/layout protected
- Case 5: Existing UI + "redesign toàn bộ và đổi sang tông đen tím" -> Existing UI, explicit L3 granted
- Case 6: Existing UI + user requests fix button/form -> local scope, no global redesign
- Case 7: Greenfield + user specifies palette -> user palette prioritized
- Case 8: Greenfield + user has not specified palette -> design freedom allows AI choice
- Case 9: UI state not confident enough -> UNKNOWN / safe fallback
- Case 10: User permits layout change but not color change -> granular permission: layout != palette
- Case 11: User permits color change but not architecture change -> palette != full redesign
- Case 12: Existing UI + domain/inspiration suggests different style -> existing identity wins
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import _paths
from uiux import api
from uiux.core import schema
from uiux.engine import orchestrator, preservation, ui_state

ROOT = _paths.PACKAGE_ROOT


class UIOrchestratorCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        schema_path = ROOT / "schemas" / "orchestrator.schema.json"
        self.schema_doc = json.loads(schema_path.read_text(encoding="utf-8"))

    def test_case_1_repo_almost_no_ui_routes_to_greenfield(self) -> None:
        """CASE 1: Repo has no UI -> Greenfield."""
        request = {
            "user_request": "Build a landing page for our new cloud product",
            "repo_context": {
                "files": ["main.py", "README.md", "requirements.txt", "server.go"],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "greenfield")
        self.assertEqual(res["ui_state"], "GREENFIELD")
        self.assertFalse(res["preservation_required"])
        self.assertEqual(res["allowed_change_level"]["max_level"], "L3")
        self.assertEqual(res["next_action"]["target_workflow"], "workflows/greenfield-workflow.md")

    def test_case_2_repo_has_complete_ui_routes_to_existing_ui(self) -> None:
        """CASE 2: Repo has complete UI -> Existing UI."""
        request = {
            "user_request": "Review our dashboard views and adjust layout",
            "repo_context": {
                "files": [
                    "src/components/Header.tsx",
                    "src/components/Sidebar.tsx",
                    "src/components/Button.tsx",
                    "src/pages/Dashboard.tsx",
                    "src/styles/globals.css",
                    "tailwind.config.js",
                ],
                "package_json": {"dependencies": {"react": "^18.2.0", "tailwindcss": "^3.4.0"}},
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertEqual(res["ui_state"], "EXISTING_UI")
        self.assertTrue(res["preservation_required"])
        self.assertEqual(res["protected_properties"]["color_palette"], "locked")
        self.assertEqual(res["protected_properties"]["brand_identity"], "locked")

    def test_case_3_existing_ui_improve_responsive(self) -> None:
        """CASE 3: Existing UI + 'improve responsive' -> Existing UI, L1/L2, palette still locked."""
        request = {
            "user_request": "improve responsive for mobile and tablet devices",
            "repo_context": {
                "files": [
                    "src/components/Nav.jsx",
                    "src/components/Hero.jsx",
                    "src/components/Footer.jsx",
                    "src/styles/app.css",
                ],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertTrue(res["preservation_required"])
        # L1 or L2 allowed for responsive adjustments
        self.assertIn(res["allowed_change_level"]["max_level"], ("L1", "L2"))
        # Palette remains locked
        self.assertEqual(res["protected_properties"]["color_palette"], "locked")
        self.assertFalse(res["permissions_detail"]["palette_editable"])

    def test_case_4_existing_ui_modernize_does_not_grant_l3(self) -> None:
        """CASE 4: Existing UI + 'modernize the UI' -> Existing UI, no auto L3, palette/brand protected."""
        vague_prompts = [
            "modernize the UI",
            "làm đẹp giao diện giúp tôi",
            "nâng cấp UI/UX cho chuyên nghiệp",
            "make it more professional and clean",
        ]
        repo_ctx = {
            "files": [
                "components/Card.vue",
                "components/Table.vue",
                "views/Overview.vue",
                "styles/main.scss",
            ],
        }
        for prompt in vague_prompts:
            with self.subTest(prompt=prompt):
                request = {"user_request": prompt, "repo_context": repo_ctx}
                res = api.orchestrate_ui(request)
                self.assertEqual(res["workflow"], "existing-ui")
                # L3 must NOT be granted
                self.assertNotEqual(res["allowed_change_level"]["max_level"], "L3")
                self.assertEqual(res["allowed_change_level"]["major_redesign"], "explicit_user_permission_only")
                # Palette, brand, and layout remain protected
                self.assertEqual(res["protected_properties"]["color_palette"], "locked")
                self.assertEqual(res["protected_properties"]["brand_identity"], "locked")
                self.assertEqual(res["protected_properties"]["overall_layout_identity"], "protected")

    def test_case_5_existing_ui_explicit_redesign_and_palette_change(self) -> None:
        """CASE 5: Existing UI + explicit redesign & palette permission -> L3 granted."""
        request = {
            "user_request": "redesign toàn bộ và đổi sang tông đen tím",
            "repo_context": {
                "files": ["src/components/Nav.tsx", "src/components/Card.tsx", "src/pages/Home.tsx"],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertEqual(res["allowed_change_level"]["max_level"], "L3")
        self.assertEqual(res["allowed_change_level"]["major_redesign"], "granted")
        self.assertTrue(res["permissions_detail"]["palette_editable"])
        self.assertEqual(res["protected_properties"]["color_palette"], "unlocked")

    def test_case_6_existing_ui_local_component_scope(self) -> None:
        """CASE 6: Existing UI + fix button/form -> local scope, no global redesign."""
        request = {
            "user_request": "sửa lại nút submit và form đăng nhập",
            "requested_scope": "component",
            "repo_context": {
                "files": [
                    "src/components/Button.tsx",
                    "src/components/Header.tsx",
                    "src/components/Sidebar.tsx",
                    "src/pages/Home.tsx",
                    "src/pages/Login.tsx",
                    "src/styles/theme.css",
                ],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertIn(res["allowed_change_level"]["max_level"], ("L1", "L2"))
        # Major redesign must be denied for local scope
        self.assertEqual(res["allowed_change_level"]["major_redesign"], "denied")
        self.assertFalse(res["permissions_detail"]["rebuild_allowed"])

    def test_case_7_greenfield_user_specifies_palette(self) -> None:
        """CASE 7: Greenfield + user specifies palette -> user palette prioritized."""
        request = {
            "user_request": "Build a SaaS app with color palette: deep slate (#0f172a) and violet (#8b5cf6)",
            "explicit_constraints": {"palette": ["#0f172a", "#8b5cf6"]},
            "repo_context": {"files": []},
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "greenfield")
        # User constraint forces constrained design freedom for palette
        self.assertEqual(res["design_freedom"], "constrained")
        self.assertTrue(any("user constraints take precedence" in note for note in res["notes"]))

    def test_case_8_greenfield_user_no_palette_allows_ai_freedom(self) -> None:
        """CASE 8: Greenfield + no palette specified -> design freedom allows AI choice."""
        request = {
            "user_request": "Build an inventory management system for warehouse operations",
            "repo_context": {"files": []},
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "greenfield")
        self.assertEqual(res["design_freedom"], "high")
        self.assertTrue(any("AI granted design freedom" in note for note in res["notes"]))

    def test_case_9_ui_state_not_confident_routes_to_unknown(self) -> None:
        """CASE 9: UI state not confident enough -> UNKNOWN / safe fallback."""
        request = {
            "user_request": "update the application interface",
            "repo_context": None,  # Missing context completely
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "unknown")
        self.assertEqual(res["ui_state"], "UNKNOWN")
        self.assertLess(res["confidence"], 0.5)
        self.assertEqual(res["next_action"]["step"], "inspect_repository_context")
        # In UNKNOWN, conservative preservation is enforced
        self.assertTrue(res["preservation_required"])
        self.assertEqual(res["allowed_change_level"]["max_level"], "L1")

    def test_case_10_granular_layout_permission_does_not_unlock_palette(self) -> None:
        """CASE 10: User permits layout change but not color change -> layout editable, palette locked."""
        request = {
            "user_request": "được phép thay đổi layout trang chủ nhưng giữ nguyên màu sắc thương hiệu",
            "explicit_permissions": {
                "allow_layout_change": True,
                "allow_palette_change": False,
            },
            "repo_context": {
                "files": ["components/Header.jsx", "components/Hero.jsx", "styles/app.css"],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertTrue(res["permissions_detail"]["layout_editable"])
        self.assertFalse(res["permissions_detail"]["palette_editable"])
        self.assertEqual(res["protected_properties"]["color_palette"], "locked")
        self.assertEqual(res["protected_properties"]["overall_layout_identity"], "unprotected")

    def test_case_11_granular_palette_permission_does_not_unlock_architecture(self) -> None:
        """CASE 11: User permits color change but not architecture change -> palette unlocked, IA protected."""
        request = {
            "user_request": "đổi toàn bộ màu sang tông xanh dương",
            "explicit_permissions": {
                "allow_palette_change": True,
                "allow_architecture_change": False,
                "allow_rebuild": False,
            },
            "repo_context": {
                "files": ["src/components/Card.tsx", "src/components/Nav.tsx", "src/styles/theme.css"],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertTrue(res["permissions_detail"]["palette_editable"])
        self.assertFalse(res["permissions_detail"]["architecture_editable"])
        self.assertEqual(res["protected_properties"]["color_palette"], "unlocked")
        self.assertEqual(res["protected_properties"]["information_architecture"], "protected")
        self.assertEqual(res["protected_properties"]["navigation_model"], "protected")

    def test_case_12_existing_identity_beats_domain_inspiration(self) -> None:
        """CASE 12: Existing UI + domain/inspiration suggestion -> existing identity wins."""
        request = {
            "user_request": "tune the store UI for higher conversion",
            "repo_context": {
                "files": [
                    "components/ProductCard.tsx",
                    "components/Cart.tsx",
                    "styles/brand-orange.css",
                ],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        # Precedence order check
        order = res["precedence_order"]
        # Existing brand identity (2) and design system (3) come BEFORE design inspiration (7)
        brand_idx = next(i for i, v in enumerate(order) if "Existing brand identity" in v)
        system_idx = next(i for i, v in enumerate(order) if "Existing design system" in v)
        inspiration_idx = next(i for i, v in enumerate(order) if "Design inspiration" in v)
        self.assertLess(brand_idx, inspiration_idx)
        self.assertLess(system_idx, inspiration_idx)
        # Palette remains locked despite e-commerce domain inspiration
        self.assertEqual(res["protected_properties"]["color_palette"], "locked")


class OrchestratorContractSchemaTests(unittest.TestCase):
    def test_output_schema_structure(self) -> None:
        """Validate output schema against definition in orchestrator.schema.json."""
        schema_file = ROOT / "schemas" / "orchestrator.schema.json"
        self.assertTrue(schema_file.is_file())
        data = json.loads(schema_file.read_text(encoding="utf-8"))
        self.assertIn("OrchestratorOutput", data["definitions"])
        self.assertIn("OrchestratorInput", data["definitions"])

    def test_heuristic_detector_confidence(self) -> None:
        """Verify detector heuristics directly."""
        det = ui_state.HeuristicUIStateDetector()
        # Empty
        res_empty = det.detect({"files": []})
        self.assertEqual(res_empty["ui_state"], "GREENFIELD")
        self.assertGreaterEqual(res_empty["confidence"], 0.9)

        # Established UI
        res_ui = det.detect({
            "files": ["src/components/Button.tsx", "src/components/Header.tsx", "src/styles/app.css"],
        })
        self.assertEqual(res_ui["ui_state"], "EXISTING_UI")
        self.assertGreaterEqual(res_ui["confidence"], 0.9)


if __name__ == "__main__":
    unittest.main()
