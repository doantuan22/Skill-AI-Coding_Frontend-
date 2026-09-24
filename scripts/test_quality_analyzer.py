"""Tests for analyze_design_quality.py against discriminating fixtures; standard library only."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_design_quality as A  # noqa: E402

FIXTURES = Path(__file__).resolve().parents[1] / "evals/fixtures/quality"


def evaluate(name: str, manifest: Path | None = None) -> dict:
    signals, _ = A.collect(FIXTURES / name)
    runtime = A.runtime_summary([manifest]) if manifest else None
    return A.evaluate(signals, runtime, 3)


class FixtureTests(unittest.TestCase):
    def test_overanimated_fails_where_expected(self) -> None:
        evals = evaluate("overanimated")
        for eid in ("E66", "E67", "E68", "E69", "E72", "E77", "E79"):
            self.assertEqual(evals[eid]["status"], "FAIL", f"{eid}: {evals[eid]}")
        self.assertIn(evals["E76"]["status"], {"FAIL", "WARN"})

    def test_restrained_passes_or_needs_review(self) -> None:
        evals = evaluate("restrained")
        for eid in ("E65", "E66", "E67", "E69", "E72", "E74", "E76"):
            self.assertEqual(evals[eid]["status"], "PASS", f"{eid}: {evals[eid]}")
        for eid, item in evals.items():
            self.assertNotEqual(item["status"], "FAIL", f"{eid}: {item}")

    def test_statuses_are_honest_without_runtime(self) -> None:
        evals = evaluate("restrained")
        self.assertEqual(evals["E68"]["status"], "NEEDS_RUNTIME")
        self.assertEqual(evals["E78"]["status"], "NEEDS_RUNTIME")


class RuntimeMergeTests(unittest.TestCase):
    def manifest(self, captures: list[dict]) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump({"schema_version": 1, "captures": captures}, handle)
        handle.close()
        return Path(handle.name)

    def probe(self, total: int, infinite: int = 0, cls: float = 0.0) -> dict:
        return {"schema_version": 1, "animations": {"total": total, "infinite": infinite, "items": []},
                "effects": {"backdrop_filter": 0, "filter_blur": 0, "will_change": 0},
                "transition_all_elements": 0, "cumulative_layout_shift": cls}

    def test_runtime_evidence_resolves_needs_runtime(self) -> None:
        path = self.manifest([
            {"viewport": "desktop", "motion_probe": self.probe(4)},
            {"viewport": "mobile", "motion_probe": self.probe(2)},
            {"viewport": "desktop", "reduced_motion": "reduce", "motion_probe": self.probe(0)},
        ])
        try:
            evals = evaluate("restrained", path)
        finally:
            path.unlink()
        self.assertEqual(evals["E68"]["status"], "PASS")
        self.assertEqual(evals["E78"]["status"], "PASS")

    def test_runtime_layout_shift_fails_performance(self) -> None:
        path = self.manifest([{"viewport": "desktop", "motion_probe": self.probe(3, cls=0.3)}])
        try:
            evals = evaluate("restrained", path)
        finally:
            path.unlink()
        self.assertEqual(evals["E67"]["status"], "FAIL")

    def test_loops_under_reduced_motion_warn(self) -> None:
        path = self.manifest([{"viewport": "desktop", "reduced_motion": "reduce", "motion_probe": self.probe(3, infinite=2)}])
        try:
            evals = evaluate("restrained", path)
        finally:
            path.unlink()
        self.assertEqual(evals["E68"]["status"], "WARN")


if __name__ == "__main__":
    unittest.main()
