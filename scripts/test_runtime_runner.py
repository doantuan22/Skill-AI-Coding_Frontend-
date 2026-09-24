"""Standard-library tests for runner input and path safety; no Playwright required."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import run_browser_execution as runner


def request(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "session_id": "safe-session", "base_url": "http://127.0.0.1:4173",
        "routes": [{"page_id": "PAGE-HOME", "route": "/"}],
        "viewports": ["desktop"], "iteration": 1,
    }
    value.update(overrides)
    return value


class RunnerInputTests(unittest.TestCase):
    def test_valid_request_uses_project_evidence_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, session = runner.validate(request(), root)
            self.assertEqual(session, root / ".evidence" / "safe-session")

    def test_rejects_unknown_viewport(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "unknown viewport"):
                runner.validate(request(viewports=["phone-xl"]), Path(temporary))

    def test_rejects_path_outside_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, "inside project root"):
                runner.validate(request(output_dir=str(root.parent / "outside")), root)

    def test_rejects_unsafe_session_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "invalid session_id"):
                runner.validate(request(session_id="../unsafe"), Path(temporary))


class RunnerMotionOptionTests(unittest.TestCase):
    def test_accepts_reduced_motion_and_probe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            options = {"reduced_motion": "reduce", "motion_probe": True, "probe_wait_ms": 500}
            raw, _ = runner.validate(request(options=options), Path(temporary))
            self.assertEqual(raw["options"]["reduced_motion"], "reduce")

    def test_rejects_invalid_reduced_motion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "reduced_motion"):
                runner.validate(request(options={"reduced_motion": "less"}), Path(temporary))

    def test_rejects_invalid_probe_wait(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "probe_wait_ms"):
                runner.validate(request(options={"motion_probe": True, "probe_wait_ms": 60000}), Path(temporary))

    def test_non_object_options_remain_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            raw, _ = runner.validate(request(options=None), Path(temporary))
            self.assertIsNone(raw["options"])

    def test_default_behavior_unchanged_without_options(self) -> None:
        self.assertIn("if(i.reduced_motion)co.reducedMotion", runner.HELPER)
        self.assertIn("if(i.motion_probe)", runner.HELPER)
        self.assertNotIn("__PROBE__", runner.HELPER)

    @unittest.skipUnless(shutil.which("node"), "node not available")
    def test_helper_is_valid_javascript(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False, encoding="utf-8") as handle:
            handle.write(runner.HELPER)
        try:
            result = subprocess.run(["node", "--check", handle.name], capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
        finally:
            os.unlink(handle.name)


if __name__ == "__main__":
    unittest.main()
