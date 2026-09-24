"""Tests for analyze_design_quality.py against discriminating fixtures; standard library only."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import _paths  # noqa: F401
from uiux.core import resources
from uiux.evals import quality as A
from uiux.evals import runner as eval_runner

FIXTURES = resources.get_quality_fixtures_root()


def evaluate(name: str, manifest: Path | None = None) -> dict:
    signals, _ = A.collect(FIXTURES / name)
    runtime = A.runtime_summary([manifest]) if manifest else None
    return A.evaluate(signals, runtime, 3)


class FixtureTests(unittest.TestCase):
    def test_fixtures_match_expectations(self) -> None:
        """Single source of expected statuses: evals/fixtures/quality/expectations.json (also used by run_evals)."""
        result = eval_runner.quality_fixture_results()
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual({r["fixture"] for r in result["results"]}, {"overanimated", "restrained"})

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
