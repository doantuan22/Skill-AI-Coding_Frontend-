"""Tests for the common adapter framework."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import _paths

ROOT = _paths.PACKAGE_ROOT
COMMON_DIR = ROOT / "plugin" / "adapters" / "common"

# Ensure we can import the common framework
if str(COMMON_DIR.parent) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR.parent))

from adapters.common import bundle, descriptor, mcp_smoke, verify


class DescriptorTests(unittest.TestCase):
    def test_load_and_validate_success(self) -> None:
        # We can test against the existing claude-code adapter.json
        adapter_dir = ROOT / ".claude-plugin"
        schema_dir = ROOT / "plugin" / "schemas"
        data = descriptor.load_and_validate(adapter_dir, schema_dir)
        self.assertEqual(data["id"], "claude-code")
        self.assertEqual(data["status"], "experimental")

    def test_load_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            with self.assertRaisesRegex(RuntimeError, "Adapter metadata not found"):
                descriptor.load_and_validate(tmp_path, ROOT / "plugin" / "schemas")


class BundleTests(unittest.TestCase):
    def test_collect_generic_payload(self) -> None:
        payload = bundle.collect_generic_payload(ROOT)
        paths = [rel for rel, _ in payload]
        # Should include SKILL.md
        self.assertIn("SKILL.md", paths)
        # Should not include tests
        self.assertFalse(any(p.startswith("tests/") for p in paths))
        # Should not include .git
        self.assertFalse(any(p.startswith(".git/") for p in paths))
        # Should not include __pycache__
        self.assertFalse(any("__pycache__" in p for p in paths))

    def test_assemble_bundle_success(self) -> None:
        payload = [("generic/file1.txt", b"hello"), ("SKILL.md", b"skill")]
        overlay = [(".claude-plugin/plugin.json", b"{}")]
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            result = bundle.assemble_bundle("test-plugin", "1.0.0", "test-adapter", payload, overlay, out_dir, dev=True)
            self.assertEqual(result["status"], "BUILT")
            self.assertEqual(result["file_count"], 3)
            
            bundle_path = Path(result["bundle"])
            self.assertTrue(bundle_path.is_file())
            
            with zipfile.ZipFile(bundle_path) as zf:
                names = zf.namelist()
                base = "test-plugin-1.0.0-dev-test-adapter"
                self.assertIn(f"{base}/generic/file1.txt", names)
                self.assertIn(f"{base}/.claude-plugin/plugin.json", names)

    def test_assemble_bundle_collision(self) -> None:
        payload = [("file1.txt", b"payload")]
        overlay = [("file1.txt", b"overlay")]
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            with self.assertRaisesRegex(RuntimeError, "BUNDLE_CONFLICT"):
                bundle.assemble_bundle("test", "1.0", "adp", payload, overlay, out_dir)

    def test_assemble_bundle_unsafe_path(self) -> None:
        payload = [("file1.txt", b"payload")]
        # Overlay contains absolute path
        unsafe_rel = "/etc/passwd" if os.name == "posix" else "C:\\Windows\\System32"
        overlay = [(unsafe_rel, b"overlay")]
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            with self.assertRaisesRegex(RuntimeError, "Unsafe overlay path"):
                bundle.assemble_bundle("test", "1.0", "adp", payload, overlay, out_dir)


class VerifyTests(unittest.TestCase):
    def test_check_forbidden_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "tests").mkdir()
            (tmp / "tests" / "test_1.py").write_text("pass", encoding="utf-8")
            (tmp / "valid.txt").write_text("pass", encoding="utf-8")
            problems = verify.check_forbidden_files(tmp)
            self.assertEqual(len(problems), 1)
            self.assertIn("tests/test_1.py", problems[0])

    def test_check_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            file1 = tmp / "file1.txt"
            file1.write_text("no absolute paths here", encoding="utf-8")
            
            file2 = tmp / "file2.txt"
            file2.write_text('this is an absolute path "/home/user/file"', encoding="utf-8")
            
            problems = verify.check_absolute_paths([file1, file2])
            self.assertEqual(len(problems), 1)
            self.assertIn("file2.txt", problems[0])

    def test_check_generic_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            # missing all files
            problems = verify.check_generic_contract(tmp)
            self.assertGreater(len(problems), 5)
            
            # create one
            (tmp / "SKILL.md").write_text("", encoding="utf-8")
            problems2 = verify.check_generic_contract(tmp)
            self.assertEqual(len(problems2), len(problems) - 1)


class MCPSmokeTests(unittest.TestCase):
    def test_clean_env(self) -> None:
        env = mcp_smoke.clean_env()
        self.assertNotIn("PYTHONPATH", env)
        self.assertEqual(env["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertEqual(env["PYTHONIOENCODING"], "utf-8")

    def test_run_mcp_smoke_test_missing_server(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            missing_server = tmp / "server.py"
            report = mcp_smoke.run_mcp_smoke_test(sys.executable, missing_server, tmp)
            
            fails = [c for c in report["checks"] if c["status"] == "FAIL"]
            self.assertGreater(len(fails), 3)
            self.assertEqual(fails[0]["detail"], "MCP server not found in bundle")


if __name__ == "__main__":
    unittest.main()
