"""Tests for Phase 2: Repo & Framework Intelligence.

Covers all 24 mandatory cases specified for Phase 2:
- Case 1: React + Vite + plain CSS
- Case 2: Next.js + Tailwind
- Case 3: Vue / Nuxt
- Case 4: Svelte / SvelteKit
- Case 5: Angular
- Case 6: Spring Boot + Thymeleaf
- Case 7: Static HTML/CSS
- Case 8: Bootstrap dependency declared but no source usage
- Case 9: Tailwind + CSS Modules (multi-styling systems)
- Case 10: Shared components + multiple pages (Component Inventory)
- Case 11: CSS variables / theme tokens (Design Token Detector)
- Case 12: Empty UI repo -> GREENFIELD
- Case 13: 1-2 scaffold pages -> PARTIAL_UI
- Case 14: Mature UI -> EXISTING_UI
- Case 15: Conflicting framework signals -> reduced confidence & conflicts listed
- Case 16: Insufficient evidence -> UNKNOWN
- Case 17: Monorepo with React and Vue sub-apps
- Case 18: Ignored directories (node_modules, dist, .next)
- Case 19: package.json dev/build/test scripts detected
- Case 20: No runtime commands -> null / unknown (never fabricated)
- Case 21: Playwright dependency / config -> playwright_available = True
- Case 22: Playwright absent -> no auto-install, browser_validation = manual
- Case 23: Phase 1 vague "modernize UI" + Phase 2 EXISTING_UI -> palette remains locked
- Case 24: Phase 1 explicit redesign + Phase 2 EXISTING_UI -> L3 granted
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import _paths
from uiux import api
from uiux.engine import repo_intelligence
from uiux.engine.repo_intelligence.scanner import RepositorySnapshot

ROOT = _paths.PACKAGE_ROOT


class RepoIntelligenceTests(unittest.TestCase):
    def test_case_1_react_vite_plain_css(self) -> None:
        """CASE 1: React + Vite + plain CSS."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "vite.config.ts", "index.html",
                    "src/main.tsx", "src/App.tsx", "src/index.css",
                    "src/components/Header.tsx",
                ],
                "package_json": {
                    "dependencies": {"react": "^18.2.0", "react-dom": "^18.2.0"},
                    "devDependencies": {"vite": "^5.0.0"},
                },
            }
        )
        self.assertEqual(profile["framework"]["name"], "react")
        self.assertGreaterEqual(profile["framework"]["confidence"], 0.85)
        self.assertEqual(profile["styling_system"]["primary"], "plain_css")
        self.assertIn(profile["existing_ui_state"]["value"], ("EXISTING_UI", "PARTIAL_UI"))

    def test_case_2_nextjs_tailwind(self) -> None:
        """CASE 2: Next.js + Tailwind."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "next.config.mjs", "tailwind.config.ts",
                    "app/layout.tsx", "app/page.tsx", "app/dashboard/page.tsx",
                    "app/globals.css",
                ],
                "package_json": {
                    "dependencies": {"next": "^14.1.0", "react": "^18.2.0", "tailwindcss": "^3.4.1"},
                },
            }
        )
        self.assertEqual(profile["framework"]["name"], "nextjs")
        self.assertEqual(profile["styling_system"]["primary"], "tailwindcss")
        route_paths = [r["path"] for r in profile["routes"]]
        self.assertIn("/", route_paths)
        self.assertIn("/dashboard", route_paths)

    def test_case_3_vue_nuxt(self) -> None:
        """CASE 3: Vue / Nuxt."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "nuxt.config.ts",
                    "pages/index.vue", "pages/about.vue",
                    "components/AppHeader.vue",
                ],
                "package_json": {"dependencies": {"nuxt": "^3.10.0", "vue": "^3.4.0"}},
            }
        )
        self.assertEqual(profile["framework"]["name"], "nuxt")
        self.assertEqual(len(profile["pages"]), 2)
        route_paths = [r["path"] for r in profile["routes"]]
        self.assertIn("/", route_paths)
        self.assertIn("/about", route_paths)

    def test_case_4_svelte_sveltekit(self) -> None:
        """CASE 4: Svelte / SvelteKit."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "svelte.config.js",
                    "src/routes/+layout.svelte", "src/routes/+page.svelte",
                    "src/routes/settings/+page.svelte",
                ],
                "package_json": {"dependencies": {"@sveltejs/kit": "^2.0.0", "svelte": "^4.2.0"}},
            }
        )
        self.assertEqual(profile["framework"]["name"], "sveltekit")
        route_paths = [r["path"] for r in profile["routes"]]
        self.assertIn("/", route_paths)
        self.assertIn("/settings", route_paths)

    def test_case_5_angular(self) -> None:
        """CASE 5: Angular."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "angular.json",
                    "src/app/app.module.ts", "src/app/app-routing.module.ts",
                    "src/app/app.component.ts", "src/app/app.component.html",
                ],
                "package_json": {"dependencies": {"@angular/core": "^17.0.0"}},
            }
        )
        self.assertEqual(profile["framework"]["name"], "angular")
        self.assertGreaterEqual(profile["framework"]["confidence"], 0.90)

    def test_case_6_spring_boot_thymeleaf(self) -> None:
        """CASE 6: Spring Boot + Thymeleaf."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "pom.xml",
                    "src/main/resources/templates/index.html",
                    "src/main/resources/templates/users.html",
                    "src/main/resources/static/css/style.css",
                ],
                "file_contents": {
                    "pom.xml": "<project><dependencies><dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-thymeleaf</artifactId></dependency></dependencies></project>",
                },
            }
        )
        self.assertEqual(profile["framework"]["name"], "spring_thymeleaf")
        route_paths = [r["path"] for r in profile["routes"]]
        self.assertIn("/", route_paths)
        self.assertIn("/users", route_paths)

    def test_case_7_static_html(self) -> None:
        """CASE 7: Static HTML/CSS."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["index.html", "about.html", "contact.html", "css/style.css", "js/main.js"],
            }
        )
        self.assertEqual(profile["framework"]["name"], "static_html")
        route_paths = [r["path"] for r in profile["routes"]]
        self.assertIn("/", route_paths)
        self.assertIn("/about", route_paths)

    def test_case_8_bootstrap_declared_without_usage_penalized(self) -> None:
        """CASE 8: Repo has Bootstrap in package.json but zero source usage -> confidence penalized."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json", "src/App.jsx"],
                "package_json": {"dependencies": {"bootstrap": "^5.3.0", "react": "^18.0.0"}},
                "file_contents": {
                    "src/App.jsx": "export default function App() { return <div>Plain Div</div>; }",
                },
            }
        )
        bootstrap_info = next((d for d in profile["styling_system"]["evidence"] if "[bootstrap]" in d), "")
        self.assertIn("WARNING", bootstrap_info)
        # Confidence must be low because package is not used in code
        self.assertLessEqual(profile["styling_system"]["confidence"], 0.65)

    def test_case_9_tailwind_plus_css_modules(self) -> None:
        """CASE 9: Repo uses Tailwind + CSS Modules -> multi-styling systems preserved."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "tailwind.config.js",
                    "src/Button.module.css", "src/Card.module.css",
                    "src/globals.css",
                ],
                "package_json": {"dependencies": {"tailwindcss": "^3.0.0"}},
                "file_contents": {
                    "src/globals.css": "@tailwind base; @tailwind components; @tailwind utilities;",
                },
            }
        )
        detected = profile["styling_system"]["detected"]
        self.assertIn("tailwindcss", detected)
        self.assertIn("css_modules", detected)
        self.assertIsNotNone(profile["styling_system"]["secondary"])

    def test_case_10_component_inventory(self) -> None:
        """CASE 10: Shared components + multiple pages -> component inventory categorizes cleanly."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "src/components/ui/Button.tsx",
                    "src/components/ui/Input.tsx",
                    "src/components/layout/Header.tsx",
                    "src/components/layout/Sidebar.tsx",
                    "src/pages/dashboard/DashboardCard.tsx",
                ],
                "package_json": {"dependencies": {"react": "^18.0.0"}},
            }
        )
        comps = profile["components"]
        self.assertGreaterEqual(len(comps["primitives"]), 1)
        self.assertGreaterEqual(len(comps["layouts"]), 1)
        self.assertGreaterEqual(comps["total_count"], 5)

    def test_case_11_design_tokens_detected(self) -> None:
        """CASE 11: CSS variables / theme tokens detected."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["src/styles/theme.css", "tailwind.config.js"],
                "file_contents": {
                    "src/styles/theme.css": """
                    :root {
                        --color-primary: #3b82f6;
                        --color-bg-surface: #0f172a;
                        --font-sans: 'Inter', sans-serif;
                        --spacing-md: 16px;
                        --radius-lg: 8px;
                    }
                    """,
                },
            }
        )
        tokens = profile["design_tokens"]
        self.assertGreaterEqual(tokens["confidence"], 0.7)
        self.assertTrue(any("--color-" in c for c in tokens["colors"]))
        self.assertTrue(any("--font-" in t for t in tokens["typography"]))

    def test_case_12_empty_repo_is_greenfield(self) -> None:
        """CASE 12: Repo with no UI -> GREENFIELD."""
        profile = repo_intelligence.analyze_repository(
            options={"files": ["main.py", "requirements.txt", "README.md"]}
        )
        self.assertEqual(profile["existing_ui_state"]["value"], "GREENFIELD")
        self.assertGreaterEqual(profile["existing_ui_state"]["confidence"], 0.90)

    def test_case_13_one_scaffold_page_is_partial_ui(self) -> None:
        """CASE 13: Bare 1-2 scaffold files -> PARTIAL_UI."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json", "src/App.tsx", "src/index.css"],
                "package_json": {"dependencies": {"react": "^18.0.0"}},
            }
        )
        self.assertEqual(profile["existing_ui_state"]["value"], "PARTIAL_UI")

    def test_case_14_mature_ui_is_existing_ui(self) -> None:
        """CASE 14: Established components + pages -> EXISTING_UI."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "tailwind.config.js",
                    "src/components/Header.tsx", "src/components/Sidebar.tsx",
                    "src/components/Button.tsx", "src/pages/Home.tsx",
                    "src/pages/Settings.tsx", "src/styles/globals.css",
                ],
                "package_json": {"dependencies": {"react": "^18.0.0", "tailwindcss": "^3.0.0"}},
            }
        )
        self.assertEqual(profile["existing_ui_state"]["value"], "EXISTING_UI")
        self.assertGreaterEqual(profile["existing_ui_state"]["confidence"], 0.90)

    def test_case_15_conflicting_signals(self) -> None:
        """CASE 15: Conflicting framework signals -> confidence reduced / conflicts populated."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json", "next.config.js", "nuxt.config.ts"],
                "package_json": {"dependencies": {"next": "^14.0.0", "nuxt": "^3.0.0"}},
            }
        )
        self.assertTrue(len(profile["conflicts"]) > 0 or len(profile["framework"]["conflicting_signals"]) > 0)

    def test_case_16_insufficient_evidence_is_unknown(self) -> None:
        """CASE 16: Ambiguous files with no recognized manifests/code -> UNKNOWN."""
        profile = repo_intelligence.analyze_repository(
            options={"files": ["binary.dat", "core.dump"]}
        )
        self.assertEqual(profile["existing_ui_state"]["value"], "UNKNOWN")

    def test_case_17_monorepo_multiple_apps(self) -> None:
        """CASE 17: Monorepo with React and Vue sub-apps -> detected without collapse."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "package.json", "pnpm-workspace.yaml",
                    "apps/web/package.json", "apps/web/next.config.js", "apps/web/app/page.tsx",
                    "apps/admin/package.json", "apps/admin/src/App.vue",
                ],
                "package_json": {"workspaces": ["apps/*"]},
            }
        )
        self.assertTrue(profile["repository_signals"]["is_monorepo"])
        app_names = [a["name"] for a in profile["repository_signals"]["apps"]]
        self.assertIn("web", app_names)
        self.assertIn("admin", app_names)

    def test_case_18_ignored_directories_filtered_out(self) -> None:
        """CASE 18: node_modules, dist, .next are ignored."""
        snapshot = RepositorySnapshot(
            file_list=[
                "src/App.tsx",
                "node_modules/react/index.js",
                "dist/bundle.js",
                ".next/static/chunks/main.js",
            ]
        )
        # In custom file_list, scanner loads files as given, but UI scanner ignores non-UI files
        self.assertEqual(len(snapshot.ui_files), 1)
        self.assertIn("src/App.tsx", snapshot.ui_files)

    def test_case_19_runtime_commands_detected(self) -> None:
        """CASE 19: package.json scripts detected accurately."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json", "pnpm-lock.yaml"],
                "package_json": {
                    "scripts": {
                        "dev": "vite",
                        "build": "vite build",
                        "test": "vitest",
                        "lint": "eslint .",
                        "typecheck": "tsc --noEmit",
                    }
                },
            }
        )
        rt = profile["runtime"]
        self.assertEqual(rt["package_manager"], "pnpm")
        self.assertEqual(rt["dev_command"], "pnpm dev")
        self.assertEqual(rt["build_command"], "pnpm build")
        self.assertEqual(rt["test_command"], "pnpm test")
        self.assertEqual(rt["lint_command"], "pnpm lint")
        self.assertEqual(rt["typecheck_command"], "pnpm typecheck")

    def test_case_20_no_runtime_commands_are_null(self) -> None:
        """CASE 20: Missing scripts result in null, never fabricated."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json"],
                "package_json": {"name": "my-library"},
            }
        )
        rt = profile["runtime"]
        self.assertIsNone(rt["dev_command"])
        self.assertIsNone(rt["build_command"])

    def test_case_21_playwright_available_when_present(self) -> None:
        """CASE 21: Playwright dependency/config exists -> playwright_available = True."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json", "playwright.config.ts"],
                "package_json": {"devDependencies": {"@playwright/test": "^1.40.0"}},
            }
        )
        self.assertTrue(profile["runtime"]["playwright_available"])
        self.assertEqual(profile["runtime"]["browser_validation"], "playwright")

    def test_case_22_playwright_not_present_no_autoinstall(self) -> None:
        """CASE 22: Playwright absent -> playwright_available = False, no auto-install."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["package.json", "src/App.tsx"],
                "package_json": {"dependencies": {"react": "^18.0.0"}},
            }
        )
        self.assertFalse(profile["runtime"]["playwright_available"])
        self.assertEqual(profile["runtime"]["browser_validation"], "manual")

    def test_case_23_phase1_vague_request_plus_existing_ui_keeps_palette_lock(self) -> None:
        """CASE 23: Phase 1 vague request 'modernize UI' + Phase 2 EXISTING_UI -> palette remains locked."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": [
                    "src/components/Button.tsx",
                    "src/components/Header.tsx",
                    "src/styles/theme.css",
                    "src/pages/Dashboard.tsx",
                ],
                "package_json": {"dependencies": {"react": "^18.0.0"}},
            }
        )
        request = {
            "user_request": "modernize the UI and make it look clean",
            "repo_context": {
                "repo_profile": profile,
                "files": ["src/components/Button.tsx", "src/components/Header.tsx"],
            },
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertEqual(res["protected_properties"]["color_palette"], "locked")
        self.assertFalse(res["permissions_detail"]["palette_editable"])
        self.assertNotEqual(res["allowed_change_level"]["max_level"], "L3")

    def test_case_24_phase1_explicit_redesign_plus_existing_ui_allows_l3(self) -> None:
        """CASE 24: Phase 1 explicit redesign permission + Phase 2 EXISTING_UI -> L3 granted."""
        profile = repo_intelligence.analyze_repository(
            options={
                "files": ["src/components/Header.tsx", "src/pages/Home.tsx", "src/styles/app.css"],
                "package_json": {"dependencies": {"react": "^18.0.0"}},
            }
        )
        request = {
            "user_request": "redesign toàn bộ giao diện và đổi sang tông đen tím",
            "repo_context": {"repo_profile": profile},
        }
        res = api.orchestrate_ui(request)
        self.assertEqual(res["workflow"], "existing-ui")
        self.assertEqual(res["allowed_change_level"]["max_level"], "L3")
        self.assertTrue(res["permissions_detail"]["palette_editable"])
        self.assertEqual(res["protected_properties"]["color_palette"], "unlocked")


if __name__ == "__main__":
    unittest.main()
