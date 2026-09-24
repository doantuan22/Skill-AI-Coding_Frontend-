"""Executable entry points and backward-compatible scripts, run from an unrelated working directory."""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import _paths

ROOT = _paths.PACKAGE_ROOT
SCRIPTS = ROOT / "scripts"
WRAPPERS = {
    "knowledge_lib": "uiux.knowledge.catalog", "resolve_capabilities": "uiux.engine.capability_resolver",
    "analyze_design_quality": "uiux.evals.quality", "run_browser_execution": "uiux.runtime.browser",
    "detect_capabilities": "uiux.runtime.capabilities", "run_accessibility_scan": "uiux.runtime.accessibility",
    "validate_runtime_evidence": "uiux.runtime.evidence", "validate_accessibility_evidence": "uiux.runtime.evidence",
    "validate_skill": "uiux.tooling.validate",
}


def run(args: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=cwd, encoding="utf-8")


class CompatibilityImportTests(unittest.TestCase):
    def test_legacy_module_names_alias_the_implementation(self) -> None:
        sys.path.insert(0, str(SCRIPTS))
        try:
            for legacy, target in WRAPPERS.items():
                with self.subTest(legacy=legacy):
                    sys.modules.pop(legacy, None)
                    self.assertIs(importlib.import_module(legacy), importlib.import_module(target))
            import knowledge_lib  # noqa: PLC0415
            self.assertTrue(hasattr(knowledge_lib, "_as_list") and hasattr(knowledge_lib, "ROOT"))
        finally:
            sys.path.remove(str(SCRIPTS))


class CliFromAnotherDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cwd = tempfile.TemporaryDirectory()
        self.addCleanup(self.cwd.cleanup)

    def ok(self, *args: str) -> subprocess.CompletedProcess:
        result = run(list(args), self.cwd.name)
        self.assertEqual(result.returncode, 0, result.stdout[-1500:] + result.stderr[-1500:])
        return result

    def test_validate_skill_defaults_to_package_root(self) -> None:
        self.assertIn("validation passed", self.ok(str(SCRIPTS / "validate_skill.py")).stdout)

    def test_knowledge_and_resolver(self) -> None:
        self.assertIn("Knowledge validation passed", self.ok(str(SCRIPTS / "knowledge_lib.py"), "check").stdout)
        plan = json.loads(self.ok(str(SCRIPTS / "resolve_capabilities.py"), "--profile",
                                  str(ROOT / "evals/resolver-scenarios/premium-ai-saas.json")).stdout)
        self.assertEqual(plan["style"]["primary"]["id"], "style.calm-futurism")

    def test_analyzer_and_evidence_validators(self) -> None:
        report = json.loads(self.ok(str(SCRIPTS / "analyze_design_quality.py"), str(ROOT / "evals/fixtures/quality/restrained")).stdout)
        self.assertEqual(report["evals"]["E66"]["status"], "PASS")
        self.ok(str(SCRIPTS / "validate_runtime_evidence.py"), str(ROOT / "evals/runtime-fixtures/evidence-valid"))
        self.ok(str(SCRIPTS / "validate_accessibility_evidence.py"), str(ROOT / "evals/runtime-fixtures/accessibility/evidence-valid"))

    def test_detector_and_runner_dry_runs(self) -> None:
        project = ROOT / "evals/runtime-fixtures/playwright-ready"
        detected = json.loads(self.ok(str(SCRIPTS / "detect_capabilities.py"), str(project)).stdout)
        self.assertIn(detected["playwright"]["runtime_state"]["state"],
                      {"DECLARED_NOT_INSTALLED", "PACKAGE_AVAILABLE_BROWSER_MISSING", "READY"})
        request = Path(self.cwd.name, "request.json")
        request.write_text(json.dumps({"session_id": "dry", "base_url": "http://127.0.0.1:9", "routes": [{"page_id": "P", "route": "/"}],
                                       "viewports": ["desktop"]}), encoding="utf-8")
        plan = json.loads(self.ok(str(SCRIPTS / "run_browser_execution.py"), "--input", str(request), "--project", str(project), "--dry-run").stdout)
        self.assertEqual(plan["status"], "DRY_RUN")
        a11y = json.loads(self.ok(str(SCRIPTS / "run_accessibility_scan.py"), "--input", str(request), "--project", str(project), "--dry-run").stdout)
        self.assertEqual(a11y["status"], "DRY_RUN")
        self.assertFalse((project / ".evidence").exists(), "dry runs must not write evidence")

    def test_unified_cli_and_module_entry(self) -> None:
        tools = json.loads(self.ok(str(SCRIPTS / "uiux_cli.py"), "tools").stdout)["tools"]
        self.assertGreaterEqual(len(tools), 7)
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        result = subprocess.run([sys.executable, "-m", "uiux", "version"], capture_output=True, text=True, cwd=self.cwd.name, env=env)
        self.assertEqual(json.loads(result.stdout)["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
