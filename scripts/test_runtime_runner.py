"""Standard-library tests for runner input and path safety; no Playwright required."""
from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
