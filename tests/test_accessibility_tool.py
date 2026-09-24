"""accessibility_scan: public tool gated on playwright.runtime_state; blocks honestly, never installs or downloads."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _paths
from uiux import api
from uiux.core import errors
from uiux.runtime import accessibility, capabilities

ROOT = _paths.PACKAGE_ROOT
NODE = {"status": "AVAILABLE", "version": "v20.0.0", "confidence": "confirmed"}


def request(**overrides: object) -> dict:
    value = {"session_id": "a11y", "base_url": "http://127.0.0.1:9", "routes": [{"page_id": "HOME", "route": "/"}],
             "viewports": ["desktop"]}
    value.update(overrides)
    return value


class RuntimeStateGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "app"
        self.project.mkdir()
        self.cache = Path(self.temp.name) / "browsers"
        self.cache.mkdir()
        patcher = mock.patch.dict(os.environ, {"PLAYWRIGHT_BROWSERS_PATH": str(self.cache)})
        patcher.start()
        self.addCleanup(patcher.stop)
        node = mock.patch.object(capabilities, "command_version", lambda command: dict(NODE))  # no subprocess, node "present"
        node.start()
        self.addCleanup(node.stop)

    def declare(self, *packages: str) -> None:
        deps = {name: "^1.0.0" for name in packages}
        (self.project / "package.json").write_text(json.dumps({"devDependencies": deps}), encoding="utf-8")

    def install(self) -> None:
        package = self.project / "node_modules" / "@playwright" / "test"
        package.mkdir(parents=True)
        (package / "package.json").write_text("{}", encoding="utf-8")

    def blocked(self) -> tuple[str, dict]:
        before = sorted(p.name for p in self.cache.iterdir())
        result = api.call_tool("accessibility_scan", {"request": request(), "project": str(self.project)})
        self.assertEqual((result["exit_code"], result["summary"]["status"]), (2, "BLOCKED"))
        manifest = json.loads(Path(result["summary"]["manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(manifest["errors"][0]["code"], result["summary"]["error_code"])
        self.assertEqual(manifest["runtime_state"], result["summary"]["runtime_state"])
        self.assertEqual(sorted(p.name for p in self.cache.iterdir()), before, "no browser download")
        return result["summary"]["runtime_state"], result["summary"]

    def test_not_declared(self) -> None:
        self.declare("@axe-core/playwright")
        state, summary = self.blocked()
        self.assertEqual((state, summary["error_code"]), ("NOT_DECLARED", "PLAYWRIGHT_IMPORT_FAILURE"))
        self.assertFalse((self.project / "node_modules").exists(), "no install")

    def test_declared_not_installed(self) -> None:
        self.declare("@playwright/test", "@axe-core/playwright")
        state, summary = self.blocked()
        self.assertEqual((state, summary["error_code"]), ("DECLARED_NOT_INSTALLED", "PLAYWRIGHT_IMPORT_FAILURE"))
        self.assertFalse((self.project / "node_modules").exists(), "no install")

    def test_package_available_browser_missing(self) -> None:
        self.declare("@playwright/test", "@axe-core/playwright")
        self.install()
        state, summary = self.blocked()
        self.assertEqual((state, summary["error_code"]), ("PACKAGE_AVAILABLE_BROWSER_MISSING", "PLAYWRIGHT_BROWSER_UNAVAILABLE"))
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_ready_passes_the_runtime_gate(self) -> None:
        self.declare("@playwright/test", "@axe-core/playwright")
        self.install()
        (self.cache / "chromium-1100").mkdir()
        plan = api.accessibility_scan(request(), str(self.project), dry_run=True)["summary"]
        self.assertEqual((plan["runtime_state"], plan["strategy"]), ("READY", "axe-playwright"))
        self.assertNotIn("blocked_by", plan)
        state, summary = self.blocked()  # READY, but nothing listens on base_url: never starts a server
        self.assertEqual((state, summary["error_code"]), ("READY", "READINESS_TIMEOUT"))

    def test_ready_without_axe(self) -> None:
        self.declare("@playwright/test")
        self.install()
        (self.cache / "chromium-1100").mkdir()
        state, summary = self.blocked()
        self.assertEqual((state, summary["error_code"]), ("READY", "AXE_NOT_AVAILABLE"))

    def test_runner_and_scanner_share_the_runtime_gate(self) -> None:
        from uiux.runtime import browser

        for setup in ((), ("@playwright/test",)):
            self.declare(*setup, "axe-core")
            report = capabilities.detect(self.project)
            self.assertEqual(accessibility.blocking_reason(report)[0], browser.blocking_reason(report)[0])

    def test_blocked_codes_are_dependency_errors_with_remediation(self) -> None:
        for code in ("PLAYWRIGHT_IMPORT_FAILURE", "PLAYWRIGHT_BROWSER_UNAVAILABLE", "AXE_NOT_AVAILABLE"):
            info = errors.result_annotation(code)
            self.assertEqual(info["category"], "dependency")
            self.assertIn("never", info["remediation"])

    def test_dry_run_writes_nothing(self) -> None:
        self.declare("@playwright/test")
        result = api.call_tool("accessibility_scan", {"request": request(), "project": str(self.project), "dry_run": True})
        self.assertEqual((result["exit_code"], result["summary"]["status"], result["summary"]["strategy"]), (0, "DRY_RUN", "BLOCKED"))
        self.assertEqual(result["summary"]["blocked_by"], "PLAYWRIGHT_IMPORT_FAILURE")
        self.assertFalse((self.project / ".evidence").exists())

    def test_invalid_input_is_a_result(self) -> None:
        for bad in (request(session_id="../x"), request(viewports=["phone-xl"]), {"routes": []}):
            result = api.accessibility_scan(bad, str(self.project))
            self.assertEqual((result["exit_code"], result["summary"]["status"]), (3, "INVALID_INPUT"))
        outside = api.accessibility_scan(request(output_dir=str(self.project.parent / "elsewhere")), str(self.project))
        self.assertEqual(outside["summary"], {"status": "INVALID_INPUT", "error": "output_dir must remain inside project root"})


class CompatibilityScriptTests(unittest.TestCase):
    """scripts/run_accessibility_scan.py keeps its CLI: arguments, INVALID_INPUT exit 3, dry run exit 0."""

    SCRIPT = str(ROOT / "scripts/run_accessibility_scan.py")

    def run_script(self, *args: str, cwd: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, self.SCRIPT, *args], capture_output=True, text=True, encoding="utf-8", cwd=cwd)

    def test_cli_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, "req.json").write_text(json.dumps(request()), encoding="utf-8")
            Path(temporary, "bad.json").write_text("{", encoding="utf-8")
            dry = self.run_script("--input", "req.json", "--project", ".", "--dry-run", cwd=temporary)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertEqual(json.loads(dry.stdout)["status"], "DRY_RUN")
            invalid = self.run_script("--input", "bad.json", cwd=temporary)
            self.assertEqual((invalid.returncode, json.loads(invalid.stdout)["status"]), (3, "INVALID_INPUT"))
            missing = self.run_script(cwd=temporary)
            self.assertEqual(missing.returncode, 2)  # argparse: --input is required
            self.assertFalse(Path(temporary, ".evidence").exists())


if __name__ == "__main__":
    unittest.main()
