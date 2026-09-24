"""Tests for the Design Knowledge System: parser, schemas, references, index, retrieval, resolver, diversity.

Standard library only (PyYAML parity check runs only when PyYAML happens to be installed).
Run: python scripts/test_knowledge.py   (or: cd scripts && python -m unittest test_knowledge)
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import _paths  # noqa: F401
from uiux.engine import capability_resolver as R
from uiux.evals import resolver_scenarios as S
from uiux.knowledge import catalog as K

ROOT = K.ROOT
SCENARIOS = S.scenario_paths()
ENTRIES, LOAD_ERRORS = K.load()


def plan_for(path: Path) -> tuple[dict, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return R.resolve(data["profile"], ENTRIES), data["expect"]


PLANS = {path.stem: plan_for(path) for path in SCENARIOS}


class ParserTests(unittest.TestCase):
    def test_parses_nested_and_lists(self) -> None:
        data = K.parse_block('id: x.y\nlist: [a, "@b/c"]\nnested:\n  cost: low\nseq:\n  - one\n  - two\n')
        self.assertEqual(data["list"], ["a", "@b/c"])
        self.assertEqual(data["nested"], {"cost": "low"})
        self.assertEqual(data["seq"], ["one", "two"])

    def test_rejects_colon_space_in_plain_value(self) -> None:
        with self.assertRaises(K.KnowledgeError):
            K.parse_block("id: x.y\nbad: a: b\n")

    def test_rejects_duplicate_keys_and_tabs(self) -> None:
        with self.assertRaises(K.KnowledgeError):
            K.parse_block("id: x.y\nid: x.z\n")
        with self.assertRaises(K.KnowledgeError):
            K.parse_block("id: x.y\n\tbad: 1\n")

    def test_rejects_indicator_start(self) -> None:
        with self.assertRaises(K.KnowledgeError):
            K.parse_block("id: x.y\nbad: @scoped\n")


class CatalogTests(unittest.TestCase):
    def test_loads_and_validates(self) -> None:
        self.assertEqual(LOAD_ERRORS, [])
        self.assertEqual(K.validate(ENTRIES), [])

    def test_index_is_fresh(self) -> None:
        self.assertEqual((ROOT / K.INDEX_PATH).read_text(encoding="utf-8"), K.render_index(ENTRIES))

    def test_pyyaml_parity_when_available(self) -> None:
        try:
            import yaml  # type: ignore
        except ImportError:
            self.skipTest("PyYAML not installed")
        for rel, line, body in K.iter_entries():
            parsed = yaml.safe_load(body)
            ours = K.parse_block(body, f"{rel}:{line}")
            self.assertEqual(set(parsed), set(ours), f"{rel}:{line}")

    def kinds(self, kind: str) -> list[dict]:
        return [e for e in ENTRIES.values() if e["kind"] == kind]

    def test_required_coverage(self) -> None:
        styles = {e["id"].split(".", 1)[1] for e in self.kinds("style")}
        for name in ("minimal", "swiss", "editorial", "neo-brutalism", "brutalist", "glassmorphism", "liquid-glass", "bento",
                     "futuristic", "calm-futurism", "retro-futurism", "cyberpunk", "y2k", "luxury", "cinematic", "spatial",
                     "tactile", "organic", "monochrome", "gradient-heavy", "developer-tool", "enterprise-saas", "modern-saas",
                     "ai-native", "data-dense", "playful", "experimental", "creative-agency", "ecommerce-premium", "fintech",
                     "productivity"):
            self.assertIn(name, styles)
        tiers = {t: [e for e in self.kinds("motion") if e["tier"] == t] for t in ("M1", "M2", "M3", "M4", "M5")}
        self.assertGreaterEqual(len(tiers["M1"]), 13)
        self.assertGreaterEqual(len(tiers["M2"]), 12)
        self.assertGreaterEqual(len(tiers["M3"]), 9)
        self.assertGreaterEqual(len(tiers["M4"]), 12)
        self.assertGreaterEqual(len(tiers["M5"]), 10)
        self.assertGreaterEqual(len(self.kinds("effect")), 26)
        self.assertGreaterEqual(len(self.kinds("interaction")), 26)
        self.assertGreaterEqual(len(self.kinds("screen")), 28)
        self.assertGreaterEqual(len(self.kinds("recipe")), 12)
        layouts = [e["category"] for e in self.kinds("layout")]
        for category in ("hero", "grid", "storytelling", "application"):
            self.assertGreaterEqual(layouts.count(category), 9, category)
        techs = {e["id"] for e in self.kinds("technology")}
        for tid in ("tech.css", "tech.waapi", "tech.view-transitions", "tech.motion", "tech.gsap", "tech.rive",
                    "tech.lottie", "tech.svg", "tech.canvas", "tech.threejs", "tech.webgl"):
            self.assertIn(tid, techs)

    def test_every_advanced_item_has_when_not_and_fallback(self) -> None:
        for e in self.kinds("technology") + self.kinds("graphics"):
            self.assertTrue(e["when_not_to_use"] and e["fallback"], e["id"])
        for e in self.kinds("motion"):
            self.assertTrue(e["avoid_when"] and e["reduced_motion"], e["id"])


class ResolverScenarioTests(unittest.TestCase):
    def test_scenarios_exist(self) -> None:
        self.assertGreaterEqual(len(SCENARIOS), 8)

    def test_expectations(self) -> None:
        for name, (plan, expect) in PLANS.items():
            with self.subTest(scenario=name):
                self.assertEqual(S.expectation_failures(plan, expect), [])

    def test_every_decision_is_explained(self) -> None:
        for name, (plan, _) in PLANS.items():
            with self.subTest(scenario=name):
                for runner in plan["style"]["runners_up"]:
                    self.assertTrue(runner["why_not"])
                for layout in plan["layouts"]["selected"]:
                    self.assertTrue(layout["why"])
                for section in ("layouts", "motion", "interactions", "effects"):
                    for item in plan[section]["rejected"]:
                        self.assertTrue(item["reason"])

    def test_retrieval_files_exist(self) -> None:
        for name, (plan, _) in PLANS.items():
            for rel in plan["retrieval"]:
                self.assertTrue((ROOT / rel).is_file(), f"{name}: {rel}")


class DiversityTests(unittest.TestCase):
    """Anti-homogenization: different products must not converge on one design language."""

    metrics = S.diversity({name: plan for name, (plan, _) in PLANS.items()})

    def test_primary_styles_are_diverse(self) -> None:
        self.assertGreaterEqual(self.metrics["distinct_primary_styles"], self.metrics["scenarios"] - 1, self.metrics)

    def test_no_two_scenarios_share_a_composition(self) -> None:
        self.assertTrue(self.metrics["unique_compositions"])

    def test_mean_similarity_is_low(self) -> None:
        self.assertLess(self.metrics["mean_jaccard"], 0.2, self.metrics)

    def test_default_tech_look_is_rare(self) -> None:
        self.assertLessEqual(len(self.metrics["default_tech_look"]), 1, self.metrics)


class TechnologyResolutionTests(unittest.TestCase):
    base = {"id": "t", "domain": ["hardware"], "brand_attributes": ["cinematic"], "visual_intensity": 5,
            "interaction_intensity": 3, "density": "low", "contexts": ["marketing"]}

    def resolve_one(self, capability: str, **overrides: object) -> dict:
        profile = R.normalize_profile({**self.base, **overrides}, ENTRIES)
        return R.resolve_technology(ENTRIES, profile, [capability])

    def test_authorized_library_is_used_when_preferred(self) -> None:
        result = self.resolve_one("motion.m4-pinned-section", allow_new_dependencies=True)
        self.assertEqual(result["assignments"]["motion.m4-pinned-section"]["technology"], "tech.gsap")
        self.assertEqual(result["new_dependencies"], ["tech.gsap"])

    def test_native_fallback_without_authorization(self) -> None:
        result = self.resolve_one("motion.m4-pinned-section")
        self.assertEqual(result["assignments"]["motion.m4-pinned-section"]["technology"], "tech.css")
        self.assertEqual(result["new_dependencies"], [])

    def test_existing_dependency_is_reused(self) -> None:
        result = self.resolve_one("motion.m3-layout-reflow", existing_dependencies=["framer-motion"])
        self.assertEqual(result["assignments"]["motion.m3-layout-reflow"]["technology"], "tech.motion")
        self.assertEqual(result["existing_reused"], ["tech.motion"])

    def test_simple_hover_never_needs_a_library(self) -> None:
        result = self.resolve_one("motion.m1-hover", allow_new_dependencies=True, existing_dependencies=["gsap"])
        self.assertEqual(result["assignments"]["motion.m1-hover"]["technology"], "tech.css")


class ProfileValidationTests(unittest.TestCase):
    def test_requires_declaration_fields(self) -> None:
        with self.assertRaises(R.ProfileError):
            R.normalize_profile({"domain": ["saas"], "visual_intensity": 3, "interaction_intensity": 3,
                                 "density": "medium", "contexts": ["marketing"]}, ENTRIES)

    def test_rejects_unknown_vocabulary(self) -> None:
        with self.assertRaises(R.ProfileError):
            R.normalize_profile({"domain": ["spaceships"], "brand_attributes": ["premium"], "visual_intensity": 3,
                                 "interaction_intensity": 3, "density": "medium", "contexts": ["marketing"]}, ENTRIES)


if __name__ == "__main__":
    unittest.main()
