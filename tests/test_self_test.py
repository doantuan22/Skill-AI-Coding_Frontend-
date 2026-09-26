"""Public self_test contract: fast, cwd-independent and honest about optional runtime/plugin failures."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import _paths
from uiux import api
from uiux.runtime import capabilities

ROOT = _paths.PACKAGE_ROOT


class SelfTestContractTests(unittest.TestCase):
    def test_healthy_repository_checks_manifest(self) -> None:
        result = api.self_test()
        checks = {check["id"]: check for check in result["checks"]}
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(checks["manifest"]["status"], "PASS")

    def test_missing_optional_runtime_is_blocked_not_failed(self) -> None:
        unavailable = {"status": "NOT_AVAILABLE", "version": None, "confidence": "confirmed"}
        with mock.patch.object(capabilities, "command_version", return_value=unavailable):
            result = api.self_test()
        optional = next(check for check in result["checks"] if check["id"] == "optional_runtime")
        self.assertEqual((result["status"], optional["status"], optional["error_code"]),
                         ("PASS", "BLOCKED", "PLAYWRIGHT_IMPORT_FAILURE"))

    def test_corrupt_registry_and_version_mismatch_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "skill"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "dist", "build"))
            cases = ((copy / "uiux/core/tools.json", "{", "tool_registry", "REGISTRY_INVALID"),
                     (copy / "VERSION", "9.9.9\n", "version", "VERSION_MISMATCH"))
            for target, content, check_id, code in cases:
                with self.subTest(check=check_id):
                    target.write_text(content, encoding="utf-8")
                    result = self._subprocess_self_test(copy)
                    check = next(item for item in result["checks"] if item["id"] == check_id)
                    self.assertEqual((result["status"], check["status"], check["error_code"]), ("FAIL", "FAIL", code))
                    if check_id == "tool_registry":
                        target.write_text((ROOT / "uiux/core/tools.json").read_text(encoding="utf-8"), encoding="utf-8")
                    else:
                        target.write_text((ROOT / "VERSION").read_text(encoding="utf-8"), encoding="utf-8")

    def test_is_independent_of_current_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as cwd:
            result = self._subprocess_self_test(ROOT, cwd)
        self.assertEqual(result["status"], "PASS")

    @staticmethod
    def _subprocess_self_test(root: Path, cwd: str | None = None) -> dict:
        code = "import json; from uiux import api; print(json.dumps(api.self_test()))"
        env = {**os.environ, "UIUX_ROOT": str(root), "PYTHONPATH": str(ROOT)}
        process = subprocess.run([sys.executable, "-c", code], cwd=cwd, env=env, capture_output=True, text=True,
                                 encoding="utf-8")
        if process.returncode:
            raise AssertionError(process.stderr)
        return json.loads(process.stdout)
