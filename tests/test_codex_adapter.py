"""Tests for the Codex adapter build and verification."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

import _paths

ROOT = _paths.PACKAGE_ROOT
CODEX_ADAPTER = ROOT / "plugin" / "adapters" / "codex"


class CodexAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="codex-test-")
        self.workspace = Path(self.tmpdir)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_export_success(self) -> None:
        # Import the export module and run it
        from plugin.adapters.codex import export
        
        result = export.export(ROOT, self.workspace, dev=True)
        self.assertEqual(result["status"], "BUILT")
        self.assertEqual(result["adapter"], "codex")
        self.assertEqual(result["build_mode"], "dev")
        
        bundle = Path(result["bundle"])
        self.assertTrue(bundle.is_file())
        
        # Verify bundle contents
        with zipfile.ZipFile(bundle) as zf:
            names = zf.namelist()
            base = f"{result['name']}-{result['version']}-dev-codex"
            
            # Check for overlay files
            self.assertIn(f"{base}/plugin.json", names)
            self.assertIn(f"{base}/mcp.json", names)
            self.assertIn(f"{base}/skills/ui-ux-workflow/SKILL.md", names)
            
            # Check for generic payload
            self.assertIn(f"{base}/SKILL.md", names)
            self.assertIn(f"{base}/uiux/__init__.py", names)

    def test_verify_checks(self) -> None:
        from plugin.adapters.codex import export, verify
        import sys
        
        # First export a valid bundle
        result = export.export(ROOT, self.workspace, dev=True)
        bundle_path = Path(result["bundle"])
        
        # Now verify it
        from plugin.packaging import artifact
        extract_dir = self.workspace / "extract"
        artifact.safe_extract(bundle_path, extract_dir)
        
        base = f"{result['name']}-{result['version']}-dev-codex"
        report = verify.verify_bundle(extract_dir / base, sys.executable)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["failed"]), 0)
        
        # Ensure X1-X16 are present
        check_ids = [c["id"] for c in report["checks"]]
        for i in range(1, 17):
            self.assertIn(f"X{i}", check_ids)
            
        # Ensure X5 passed
        x5 = next(c for c in report["checks"] if c["id"] == "X5")
        self.assertEqual(x5["status"], "PASS")

    def test_verify_x5_failure_when_skill_mutated(self) -> None:
        from plugin.adapters.codex import export, verify
        import sys
        
        result = export.export(ROOT, self.workspace, dev=True)
        bundle_path = Path(result["bundle"])
        
        from plugin.packaging import artifact
        extract_dir = self.workspace / "extract"
        artifact.safe_extract(bundle_path, extract_dir)
        
        base = f"{result['name']}-{result['version']}-dev-codex"
        
        # Mutate the generated skill
        skill = extract_dir / base / "skills" / "ui-ux-workflow" / "SKILL.md"
        skill.write_text("mutated", encoding="utf-8")
        
        report = verify.verify_bundle(extract_dir / base, sys.executable)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("X5", report["failed"])

    def test_verify_missing_python(self) -> None:
        from plugin.adapters.codex import export, verify
        import sys
        
        result = export.export(ROOT, self.workspace, dev=True)
        bundle_path = Path(result["bundle"])
        
        from plugin.packaging import artifact
        extract_dir = self.workspace / "extract"
        artifact.safe_extract(bundle_path, extract_dir)
        base = f"{result['name']}-{result['version']}-dev-codex"
        
        # Pass a fake python path
        report = verify.verify_bundle(extract_dir / base, "/path/to/nonexistent/python3")
        self.assertEqual(report["status"], "FAIL")
        
        # Check that X10 fails with the expected missing python message
        x10 = next(c for c in report["checks"] if c["id"] == "X10")
        self.assertEqual(x10["status"], "FAIL")
        self.assertIn("Python executable '/path/to/nonexistent/python3' not found", x10["detail"])
        self.assertIn("(Missing Python runtime)", x10["detail"])

    def test_verify_placeholder_and_cwd_rules(self) -> None:
        from plugin.adapters.codex import export, verify
        import sys
        
        result = export.export(ROOT, self.workspace, dev=True)
        bundle_path = Path(result["bundle"])
        
        from plugin.packaging import artifact
        extract_dir = self.workspace / "extract"
        artifact.safe_extract(bundle_path, extract_dir)
        base = extract_dir / f"{result['name']}-{result['version']}-dev-codex"
        
        mcp_file = base / "mcp.json"
        
        # Test 1: cwd omitted -> PASS
        # The generated mcp.json already omits cwd, verify should PASS
        report = verify.verify_bundle(base, sys.executable)
        x7 = next(c for c in report["checks"] if c["id"] == "X7")
        self.assertEqual(x7["status"], "PASS")
        
        # Helper to test modifying mcp.json
        def check_mcp_mutation(mutation_fn, expected_problem):
            original = json.loads(mcp_file.read_text(encoding="utf-8"))
            mutation_fn(original)
            mcp_file.write_text(json.dumps(original), encoding="utf-8")
            r = verify.verify_bundle(base, sys.executable)
            x7_check = next(c for c in r["checks"] if c["id"] == "X7")
            self.assertEqual(x7_check["status"], "FAIL")
            self.assertTrue(any(expected_problem in p for p in x7_check["detail"].split("; ")))
            # Restore
            mcp_file.write_text(json.dumps(original), encoding="utf-8") # wait, need to restore original, not mutated
        
        def restore_mcp():
            export.export(ROOT, self.workspace, dev=True)
            artifact.safe_extract(bundle_path, extract_dir)
            
        # Test 2: cwd: "" -> FAIL
        def mutate_empty_cwd(data):
            data["mcpServers"]["ui-ux-design-mcp"]["cwd"] = ""
        check_mcp_mutation(mutate_empty_cwd, "cwd cannot be empty string")
        restore_mcp()
        
        # Test 3: absolute cwd -> FAIL
        def mutate_absolute_cwd(data):
            data["mcpServers"]["ui-ux-design-mcp"]["cwd"] = "/absolute/path"
        check_mcp_mutation(mutate_absolute_cwd, "cwd cannot be absolute path")
        restore_mcp()
        
        # Test 4: ${PLUGIN_DIR} -> FAIL
        def mutate_plugin_dir(data):
            data["mcpServers"]["ui-ux-design-mcp"]["cwd"] = "${PLUGIN_DIR}"
        check_mcp_mutation(mutate_plugin_dir, "uses unsupported placeholder ${PLUGIN_DIR}")
        restore_mcp()
        
        # Test 5: placeholder in command -> FAIL
        def mutate_command_placeholder(data):
            data["mcpServers"]["ui-ux-design-mcp"]["command"] = "${PLUGIN_ROOT}/bin/python3"
        check_mcp_mutation(mutate_command_placeholder, "command cannot contain placeholders")
        restore_mcp()
if __name__ == "__main__":
    unittest.main()
