"""Tests for Phase 3: Existing UI Analyzer, Preservation Profile, and Preservation Guard.

Covers all 30 mandatory test cases:
- CASE 1: Existing UI with CSS variables -> identity palette extracted
- CASE 2: Tailwind theme -> design tokens + colors + breakpoints detected
- CASE 3: Typography variables -> font family/scale extracted
- CASE 4: Shared radius/shadow tokens -> design system extraction
- CASE 5: Multiple conflicting primary colors -> conflict noted + confidence reduced
- CASE 6: Consistent shared components -> consistency analysis passes without false anomalies
- CASE 7: Button variants inconsistent -> component inconsistency detected
- CASE 8: Global shell/navbar/sidebar -> overall layout identity extracted
- CASE 9: Responsive fixed-width hazard -> responsive risk detected
- CASE 10: Missing form label -> accessibility signal detected
- CASE 11: Existing UI default -> palette locked
- CASE 12: User 'modernize UI' -> palette remains locked, L3 denied
- CASE 13: User 'đổi toàn bộ màu sang đen tím' -> palette unlocked, scoped L3 granted
- CASE 14: User permits layout change only -> layout editable, palette locked
- CASE 15: User permits palette change only -> palette unlocked, navigation/IA protected
- CASE 16: L2 change with justification trace -> valid pass/warn
- CASE 17: L2 change without justification trace -> evaluator violation
- CASE 18: L3 change without explicit permission -> fail
- CASE 19: L3 change with explicit permission -> allowed
- CASE 20: Navigation route changed outside plan -> fail
- CASE 21: Global palette token changed outside permission -> fail
- CASE 22: Small accessibility contrast adjustment -> not flagged as full palette redesign
- CASE 23: Local component task -> global architecture rewrite blocked
- CASE 24: Design inspiration differs from brand -> existing brand wins
- CASE 25: No clear design system -> maturity = fragmented/partial/unknown
- CASE 26: Runtime unavailable -> code-level analysis operational
- CASE 27: Monorepo with 2 apps -> separate profiles preserved
- CASE 28: Analyzer partial failure -> partial results preserved, diagnostics populated
- CASE 29: Phase 1 regression: vague modernize -> L3 blocked
- CASE 30: Phase 2 regression: repo_profile remains valid
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import _paths
from uiux import api
from uiux.core import schema
from uiux.engine import existing_ui, preservation, repo_intelligence

ROOT = _paths.PACKAGE_ROOT


class ExistingUIAnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_schema = json.loads((ROOT / "schemas/existing-ui-profile.schema.json").read_text(encoding="utf-8"))
        self.preservation_schema = json.loads((ROOT / "schemas/preservation-profile.schema.json").read_text(encoding="utf-8"))
        self.eval_schema = json.loads((ROOT / "schemas/preservation-evaluation.schema.json").read_text(encoding="utf-8"))

    def test_case_1_css_variables_identity_extracted(self) -> None:
        """CASE 1: Existing UI has CSS variables -> identity palette extracted accurately."""
        options = {
            "files": ["package.json", "src/App.tsx", "src/tokens.css"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/tokens.css": ":root { --color-primary: #2563eb; --color-secondary: #64748b; --color-accent: #f59e0b; }",
                "src/App.tsx": "export default function App() { return <div style={{color: 'var(--color-primary)'}}>App</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        colors = ui_prof["identity"]["colors"]
        self.assertEqual(colors["primary"], "#2563eb")
        self.assertTrue(ui_prof["identity"]["confidence"] >= 0.70)
        self.assertTrue(any("#2563eb" in e for e in ui_prof["identity"]["evidence"]))

    def test_case_2_tailwind_theme_detected(self) -> None:
        """CASE 2: Tailwind theme -> design tokens + colors + breakpoints detected."""
        options = {
            "files": ["package.json", "tailwind.config.js", "src/App.tsx", "src/index.css"],
            "package_json": {"dependencies": {"react": "^18.0.0", "tailwindcss": "^3.4.0"}},
            "file_contents": {
                "tailwind.config.js": "module.exports = { theme: { extend: { colors: { primary: '#3b82f6', secondary: '#10b981' } } } }",
                "src/index.css": "@tailwind base; @tailwind components; @tailwind utilities;",
                "src/App.tsx": "export default function App() { return <div className='bg-primary text-secondary'>Tailwind App</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        self.assertEqual(ui_prof["identity"]["colors"]["primary"], "#3b82f6")
        self.assertTrue(len(ui_prof["responsive"]["breakpoints"]) >= 3)
        self.assertIn("sm: 640px", ui_prof["responsive"]["breakpoints"][0])

    def test_case_3_typography_variables_extracted(self) -> None:
        """CASE 3: Typography variables -> font family and scale extracted."""
        options = {
            "files": ["package.json", "src/styles/fonts.css", "src/App.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/styles/fonts.css": ":root { --font-sans: 'Inter', sans-serif; --font-mono: 'JetBrains Mono', monospace; } body { font-family: var(--font-sans); }",
                "src/App.tsx": "export default function App() { return <h1>Title</h1>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        typo = ui_prof["identity"]["typography"]
        self.assertIsNotNone(typo["font_family_base"])
        self.assertIn("Inter", typo["font_family_base"])

    def test_case_4_shared_radius_shadow_tokens(self) -> None:
        """CASE 4: Shared radius/shadow tokens -> design system extraction correct."""
        options = {
            "files": ["package.json", "src/tokens.css", "src/App.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/tokens.css": ":root { --radius-sm: 4px; --radius-md: 8px; --shadow-lg: 0 10px 15px rgba(0,0,0,0.1); }",
                "src/App.tsx": "export default function App() { return <div>Tokens</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        ds = ui_prof["design_system"]
        self.assertTrue(any("--radius-md" in r for r in ds["radius_scale"]))
        self.assertTrue(any("--shadow-lg" in s for s in ds["tokens"]["shadows"]["scale"]))

    def test_case_5_conflicting_primary_colors(self) -> None:
        """CASE 5: Multiple conflicting primary colors -> conflict noted + confidence penalized."""
        options = {
            "files": ["package.json", "src/themeA.css", "src/themeB.css", "src/App.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/themeA.css": ":root { --color-primary: #2563eb; }",
                "src/themeB.css": ":root { --color-primary: #dc2626; }",
                "src/App.tsx": "export default function App() { return <div>Conflict</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        self.assertLessEqual(ui_prof["identity"]["confidence"], 0.70)
        self.assertTrue(any("Conflicting" in e for e in ui_prof["identity"]["evidence"]))

    def test_case_6_consistent_shared_components(self) -> None:
        """CASE 6: Consistent shared components -> consistency analysis detects no false anomalies."""
        options = {
            "files": ["package.json", "src/components/ui/Button.tsx", "src/components/ui/Input.tsx", "src/pages/Home.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/components/ui/Button.tsx": "export function Button(props) { return <button {...props} className='btn' />; }",
                "src/components/ui/Input.tsx": "export function Input(props) { return <input {...props} className='input' />; }",
                "src/pages/Home.tsx": "import { Button } from '../components/ui/Button'; export default function Home() { return <Button>Click</Button>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        comps = ui_prof["components"]
        self.assertIn(comps["consistency"], ("high", "moderate"))
        self.assertEqual(len(comps["anomalies"]), 0)

    def test_case_7_button_variants_inconsistent(self) -> None:
        """CASE 7: Raw ad-hoc buttons bypassing shared component -> anomaly detected."""
        options = {
            "files": ["package.json", "src/components/ui/Button.tsx", "src/pages/A.tsx", "src/pages/B.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/components/ui/Button.tsx": "export function Button() { return <button className='btn'>Standard</button>; }",
                "src/pages/A.tsx": "export default function A() { return <button className='bg-red-500 p-2 rounded'>Ad-hoc A</button>; }",
                "src/pages/B.tsx": "export default function B() { return <button className='bg-blue-500 p-4 rounded-xl'>Ad-hoc B</button>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        comps = ui_prof["components"]
        self.assertTrue(len(comps["anomalies"]) > 0)
        self.assertIn(comps["severity"], ("medium", "high"))

    def test_case_8_global_shell_and_navigation(self) -> None:
        """CASE 8: Global shell/navbar/sidebar -> overall layout identity extracted."""
        options = {
            "files": ["package.json", "src/layouts/AppShell.tsx", "src/components/Sidebar.tsx", "src/components/Header.tsx", "src/pages/Dashboard.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/layouts/AppShell.tsx": "export function AppShell({children}) { return <div className='shell'>{children}</div>; }",
                "src/components/Sidebar.tsx": "export function Sidebar() { return <aside>Sidebar</aside>; }",
                "src/components/Header.tsx": "export function Header() { return <header>Header</header>; }",
                "src/pages/Dashboard.tsx": "export default function Dashboard() { return <div>Dashboard</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        glob = ui_prof["layout"]["global_structure"]
        self.assertIsNotNone(glob["app_shell"])
        self.assertIsNotNone(glob["sidebar"])
        self.assertIsNotNone(glob["header"])
        self.assertEqual(ui_prof["layout"]["navigation_structure"]["type"], "sidebar")

    def test_case_9_responsive_fixed_width_hazard(self) -> None:
        """CASE 9: Responsive fixed-width hazard -> risk detected."""
        options = {
            "files": ["package.json", "src/App.tsx", "src/styles.css"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/styles.css": ".container { width: 1200px; }",
                "src/App.tsx": "export default function App() { return <div className='container'>Content</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        resp = ui_prof["responsive"]
        self.assertTrue(len(resp["risks"]) > 0)
        self.assertEqual(resp["severity"], "high")
        self.assertTrue(any("Fixed-width" in r for r in resp["risks"]))

    def test_case_10_missing_form_label_accessibility(self) -> None:
        """CASE 10: Missing form label -> accessibility signal detected."""
        options = {
            "files": ["package.json", "src/Form.tsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/Form.tsx": "export function Form() { return <form><input type='text' name='username' /></form>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        a11y = ui_prof["accessibility"]
        self.assertTrue(len(a11y["missing_form_labels"]) > 0)

    def test_case_11_existing_ui_default_palette_locked(self) -> None:
        """CASE 11: Existing UI default -> palette locked in preservation profile."""
        ui_prof = {
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": ["max-w-7xl"], "navigation_structure": {"items": ["/"]}},
            "overall_confidence": 0.95,
        }
        pres_prof = existing_ui.build_preservation_profile(ui_prof)
        self.assertEqual(pres_prof["protected_design"]["color_palette"]["policy"], "locked")
        self.assertEqual(pres_prof["protected_design"]["brand_identity"]["policy"], "locked")
        self.assertEqual(pres_prof["allowed_changes"]["L3"]["policy"], "explicit_user_permission_only")

    def test_case_12_user_modernize_keeps_palette_locked(self) -> None:
        """CASE 12: Vague request 'modernize UI' -> palette remains locked, L3 denied."""
        perms = preservation.extract_explicit_permissions(user_request="Please modernize the UI and make it look clean")
        ui_prof = {
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        }
        pres_prof = existing_ui.build_preservation_profile(ui_prof, permissions=perms)
        self.assertEqual(pres_prof["protected_design"]["color_palette"]["policy"], "locked")
        self.assertFalse(pres_prof["user_permissions"]["explicit_l3_granted"])

    def test_case_13_explicit_palette_change_unlocked(self) -> None:
        """CASE 13: Explicit permission 'đổi toàn bộ màu sang đen tím' -> palette unlocked, scoped L3 granted."""
        perms = preservation.extract_explicit_permissions(user_request="đổi toàn bộ màu sang đen tím")
        ui_prof = {
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        }
        pres_prof = existing_ui.build_preservation_profile(ui_prof, permissions=perms)
        self.assertEqual(pres_prof["protected_design"]["color_palette"]["policy"], "unlocked")
        # Layout and navigation must still be protected
        self.assertEqual(pres_prof["protected_design"]["overall_layout_identity"]["policy"], "protected")
        self.assertEqual(pres_prof["protected_design"]["navigation_model"]["policy"], "protected")

    def test_case_14_layout_change_only_keeps_palette_locked(self) -> None:
        """CASE 14: User permits layout change only -> layout editable, palette still locked."""
        perms = preservation.extract_explicit_permissions(user_request="được phép thay đổi layout")
        ui_prof = {
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        }
        pres_prof = existing_ui.build_preservation_profile(ui_prof, permissions=perms)
        self.assertEqual(pres_prof["protected_design"]["overall_layout_identity"]["policy"], "editable")
        self.assertEqual(pres_prof["protected_design"]["color_palette"]["policy"], "locked")

    def test_case_15_palette_change_only_keeps_navigation_protected(self) -> None:
        """CASE 15: User permits palette change only -> palette unlocked, navigation/IA protected."""
        perms = preservation.extract_explicit_permissions(user_request="change the color palette to emerald")
        ui_prof = {
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        }
        pres_prof = existing_ui.build_preservation_profile(ui_prof, permissions=perms)
        self.assertEqual(pres_prof["protected_design"]["color_palette"]["policy"], "unlocked")
        self.assertEqual(pres_prof["protected_design"]["navigation_model"]["policy"], "protected")
        self.assertEqual(pres_prof["protected_design"]["information_architecture"]["policy"], "protected")

    def test_case_16_l2_change_with_justification_passes(self) -> None:
        """CASE 16: L2 change with justification trace -> valid pass/warn."""
        pres_prof = existing_ui.build_preservation_profile({
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        })
        proposed = {
            "level": "L2",
            "change_reason": {
                "issue": "Form layout causes input misalignment on desktop",
                "affected_scope": "RegistrationForm",
                "why_local_structure_change_needed": "Group billing fields into two-column grid",
            }
        }
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertIn(res["status"], ("pass", "warn"))
        self.assertEqual(len(res["violations"]), 0)

    def test_case_17_l2_change_without_justification_violates(self) -> None:
        """CASE 17: L2 change without justification trace -> evaluator violation."""
        pres_prof = existing_ui.build_preservation_profile({
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        })
        proposed = {"level": "L2", "change_reason": None}
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertEqual(res["status"], "warn")
        self.assertTrue(any(v["rule"] == "L2_JUSTIFICATION_TRACE" for v in res["violations"]))

    def test_case_18_l3_change_without_permission_fails(self) -> None:
        """CASE 18: L3 change without explicit permission -> fail."""
        pres_prof = existing_ui.build_preservation_profile({
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        })
        proposed = {"level": "L3", "layout_changes": {"is_full_rebuild": True}}
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertEqual(res["status"], "fail")
        self.assertTrue(any(v["rule"] == "L3_EXPLICIT_PERMISSION_TRACE" for v in res["violations"]))

    def test_case_19_l3_change_with_permission_allowed(self) -> None:
        """CASE 19: L3 change with explicit permission -> allowed."""
        pres_prof = existing_ui.build_preservation_profile(
            {"identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
             "layout": {"container_patterns": [], "navigation_structure": {}}, "overall_confidence": 0.95},
            permissions={"explicit_l3_granted": True, "allow_rebuild": True}
        )
        proposed = {
            "level": "L3",
            "permission_trace": {"user_instruction": "rebuild from scratch", "allowed_properties": ["rebuild"]},
        }
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertIn(res["status"], ("pass", "warn"))
        self.assertFalse(any(v["rule"] == "L3_EXPLICIT_PERMISSION_TRACE" for v in res["violations"]))

    def test_case_20_navigation_route_modified_outside_plan_fails(self) -> None:
        """CASE 20: Navigation route changed outside plan -> fail."""
        pres_prof = existing_ui.build_preservation_profile({
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {"items": ["/dashboard", "/settings"]}},
            "overall_confidence": 0.95,
        })
        proposed = {
            "navigation_changes": {"routes_removed": ["/dashboard"], "routes_modified": ["/settings -> /account"]}
        }
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertEqual(res["status"], "fail")
        self.assertTrue(any(v["rule"] == "NAVIGATION_PRESERVATION" for v in res["violations"]))

    def test_case_21_global_palette_token_changed_outside_permission_fails(self) -> None:
        """CASE 21: Global palette token changed outside permission -> fail."""
        pres_prof = existing_ui.build_preservation_profile({
            "identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        })
        proposed = {
            "palette_changes": {"old": "#2563eb", "new": "#ec4899"}
        }
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertEqual(res["status"], "fail")
        self.assertTrue(any(v["rule"] == "PALETTE_PRESERVATION" for v in res["violations"]))

    def test_case_22_accessibility_contrast_adjustment_allowed(self) -> None:
        """CASE 22: Small accessibility contrast adjustment -> not flagged as palette redesign."""
        pres_prof = existing_ui.build_preservation_profile({
            "identity": {"colors": {"primary": "#3b82f6"}, "visual_language": "modern", "evidence": []},
            "layout": {"container_patterns": [], "navigation_structure": {}},
            "overall_confidence": 0.95,
        })
        proposed = {
            "palette_changes": {"old": "#3b82f6", "new": "#2563eb"},
            "is_accessibility_contrast_adjustment": True,
        }
        res = existing_ui.evaluate_preservation(pres_prof, proposed)
        self.assertIn(res["status"], ("pass", "warn"))
        self.assertFalse(any(v["rule"] == "PALETTE_PRESERVATION" for v in res["violations"]))
        self.assertTrue(any("contrast adjustment" in w for w in res["warnings"]))

    def test_case_23_local_component_task_blocks_global_architecture_rewrite(self) -> None:
        """CASE 23: Local component task -> global architecture rewrite blocked."""
        pres_prof = existing_ui.build_preservation_profile(
            {"identity": {"colors": {"primary": "#2563eb"}, "visual_language": "modern", "evidence": []},
             "layout": {"container_patterns": [], "navigation_structure": {}}, "overall_confidence": 0.95},
            requested_scope="component",
        )
        proposed = {
            "layout_changes": {"is_global_rewrite": True},
            "architecture_changes": {"ia_changed": True},
        }
        res = existing_ui.evaluate_preservation(pres_prof, proposed, requested_scope="component")
        self.assertEqual(res["status"], "fail")
        self.assertTrue(any(v["rule"] == "SCOPE_CONFINEMENT" for v in res["violations"]))

    def test_case_24_design_inspiration_overruled_by_brand(self) -> None:
        """CASE 24: Design inspiration suggesting different style is overruled by existing brand."""
        # Precedence hierarchy: 2. Brand identity > 7. Design inspiration
        self.assertLess(
            preservation.PRECEDENCE_HIERARCHY.index("2. Existing brand identity"),
            preservation.PRECEDENCE_HIERARCHY.index("7. Design inspiration"),
        )
        resolved = preservation.resolve_precedence(
            existing_brand="Enterprise Blue Brand",
            design_inspiration="Cyberpunk Neon",
        )
        self.assertEqual(resolved["chosen"], "Enterprise Blue Brand")
        self.assertEqual(resolved["winner_rank"], 2)

    def test_case_25_no_clear_design_system_fragmented_or_unknown(self) -> None:
        """CASE 25: No clear design system -> maturity is fragmented/partial/unknown, no hallucinations."""
        options = {
            "files": ["package.json", "src/App.jsx"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/App.jsx": "export default function App() { return <div style={{padding: '13px', color: '#123456'}}>No System</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        ds = ui_prof["design_system"]
        self.assertIn(ds["maturity"], ("fragmented", "partial", "unknown"))
        self.assertNotEqual(ds["maturity"], "mature")

    def test_case_26_runtime_unavailable_code_level_analyzer_operates(self) -> None:
        """CASE 26: Runtime unavailable -> code-level analyzer operates without error."""
        options = {
            "files": ["package.json", "src/App.tsx", "src/index.css"],
            "package_json": {"dependencies": {"react": "^18.0.0"}},
            "file_contents": {
                "src/index.css": ":root { --color-primary: #059669; }",
                "src/App.tsx": "export default function App() { return <div>Offline App</div>; }",
            },
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        # Ensure playwright_available is False in this fixture
        repo_prof["runtime"]["playwright_available"] = False
        repo_prof["runtime"]["browser_validation"] = "none"

        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)
        self.assertEqual(ui_prof["identity"]["colors"]["primary"], "#059669")
        self.assertGreaterEqual(ui_prof["overall_confidence"], 0.60)

    def test_case_27_monorepo_separate_profiles(self) -> None:
        """CASE 27: Monorepo with 2 apps -> separate sub-profiles preserved."""
        options = {
            "files": [
                "package.json", "pnpm-workspace.yaml",
                "apps/storefront/package.json", "apps/storefront/src/tokens.css", "apps/storefront/src/App.tsx",
                "apps/admin/package.json", "apps/admin/src/theme.css", "apps/admin/src/App.tsx",
            ],
            "file_contents": {
                "apps/storefront/src/tokens.css": ":root { --color-primary: #ec4899; }",
                "apps/storefront/src/App.tsx": "export default function App() { return <div>Storefront</div>; }",
                "apps/admin/src/theme.css": ":root { --color-primary: #1e293b; }",
                "apps/admin/src/App.tsx": "export default function App() { return <div>Admin</div>; }",
            }
        }
        repo_prof = repo_intelligence.analyze_repository(options=options)
        ui_prof = existing_ui.analyze_existing_ui(repo_profile=repo_prof, options=options)

        self.assertIn("applications", ui_prof)
        self.assertIn("apps/storefront", ui_prof["applications"])
        self.assertIn("apps/admin", ui_prof["applications"])

    def test_case_28_analyzer_partial_failure_preserved(self) -> None:
        """CASE 28: Analyzer partial failure -> partial results preserved, diagnostics populated."""
        # Simulated profile with malformed or missing sections
        repo_prof = {
            "design_tokens": {"colors": [], "typography": [], "spacing": [], "radius": [], "shadows": [], "confidence": 0.0},
            "components": None,  # Causes comp analysis to degrade safely
            "routes": [],
            "pages": [],
            "styling_system": {"primary": None, "confidence": 0.0},
            "ui_library": {},
            "repository_signals": {"is_monorepo": False, "apps": []},
        }
        ui_prof = existing_ui.build_existing_ui_profile(repo_prof)
        self.assertIn("ComponentAnalyzer", "; ".join(ui_prof["diagnostics"]["analyzer_failures"]))
        # Other analyzers must still produce output
        self.assertIsNotNone(ui_prof["identity"])
        self.assertIsNotNone(ui_prof["layout"])

    def test_case_29_phase_1_regression_vague_modernize(self) -> None:
        """CASE 29: Phase 1 regression: vague modernize keeps L3 blocked."""
        req = {
            "user_request": "modernize the UI and make it look clean",
            "repo_context": {
                "files": ["package.json", "src/App.tsx", "src/components/Header.tsx", "src/index.css"],
                "package_json": {"dependencies": {"react": "^18.0.0"}},
            }
        }
        res = api.orchestrate_ui(req)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertEqual(res["protected_properties"]["color_palette"], "locked")
        self.assertEqual(res["allowed_change_level"]["major_redesign"], "explicit_user_permission_only")

    def test_case_30_phase_2_regression_repo_profile_valid(self) -> None:
        """CASE 30: Phase 2 regression: analyze_repository produces valid profile."""
        profile = api.analyze_repository(options={"files": ["package.json", "src/App.tsx", "src/index.css"]})
        self.assertIn("framework", profile)
        self.assertIn("styling_system", profile)
        self.assertIn("existing_ui_state", profile)
        self.assertIn("runtime", profile)
        self.assertIn(profile["existing_ui_state"]["value"], ("PARTIAL_UI", "EXISTING_UI"))


if __name__ == "__main__":
    unittest.main()
