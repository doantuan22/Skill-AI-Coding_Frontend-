"""Resource discovery and configuration: package-relative, cwd-independent, validated."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import _paths
from uiux.core import config, resources


class ResourceDiscoveryTests(unittest.TestCase):
    def test_root_is_the_package_root(self) -> None:
        self.assertEqual(resources.get_package_root(), _paths.PACKAGE_ROOT)
        self.assertTrue(resources.get_skill_entry().is_file())

    def test_all_getters_resolve_to_existing_locations(self) -> None:
        for getter in (resources.get_core_root, resources.get_plugin_root, resources.get_knowledge_root,
                       resources.get_knowledge_registry_path, resources.get_knowledge_index_path,
                       resources.get_components_root, resources.get_runtime_root, resources.get_viewports_path,
                       resources.get_eval_root, resources.get_scenarios_root, resources.get_resolver_scenarios_root,
                       resources.get_quality_fixtures_root, resources.get_templates_root, resources.get_docs_root,
                       resources.get_tool_registry_path, resources.get_layer_map_path):
            with self.subTest(getter=getter.__name__):
                self.assertTrue(getter().exists(), getter())
                self.assertTrue(str(getter()).startswith(str(_paths.PACKAGE_ROOT)))
        for root in resources.get_knowledge_roots():
            self.assertTrue(root.is_dir(), root)

    def test_independent_of_working_directory(self) -> None:
        before = resources.get_knowledge_registry_path()
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary:
            os.chdir(temporary)
            try:
                self.assertEqual(resources.get_knowledge_registry_path(), before)
            finally:
                os.chdir(cwd)

    def test_resolve_rejects_absolute_and_escaping_paths(self) -> None:
        for bad in ("/etc/passwd", "C:/Windows", "../outside", "a/../../b"):
            with self.subTest(path=bad), self.assertRaises(resources.ResourceError):
                resources.resolve(bad)

    def test_invalid_root_override_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            os.environ[resources.ENV_ROOT] = temporary
            try:
                with self.assertRaises(resources.ResourceError):
                    resources.get_package_root()
            finally:
                del os.environ[resources.ENV_ROOT]


class ConfigTests(unittest.TestCase):
    def tearDown(self) -> None:
        os.environ.pop(config.ENV_CONFIG, None)
        config.reset()

    def write(self, data: dict) -> str:
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, handle)
        handle.close()
        self.addCleanup(os.unlink, handle.name)
        return handle.name

    def test_defaults_are_valid_and_complete(self) -> None:
        cfg = config.load()
        for section in ("paths", "browser", "dependency_policy", "motion_budget", "performance_budget", "feature_flags"):
            self.assertIn(section, cfg)
        self.assertFalse(cfg["dependency_policy"]["auto_install"])

    def test_env_override_merges_deeply(self) -> None:
        os.environ[config.ENV_CONFIG] = self.write({"schema_version": 1, "motion_budget": {"max_motion_patterns": 8}})
        config.reset()
        cfg = config.get()
        self.assertEqual(cfg["motion_budget"]["max_motion_patterns"], 8)
        self.assertEqual(cfg["motion_budget"]["max_interactions"], 10)

    def test_explicit_overrides_win(self) -> None:
        self.assertEqual(config.load({"browser": {"headless": False}})["browser"]["headless"], False)

    def test_rejects_absolute_paths_and_auto_install(self) -> None:
        with self.assertRaises(config.ConfigError):
            config.load({"paths": {"evals": "/tmp/evals"}})
        with self.assertRaises(config.ConfigError):
            config.load({"paths": {"knowledge_roots": ["../elsewhere"]}})
        with self.assertRaises(config.ConfigError):
            config.load({"dependency_policy": {"auto_install": True}})
        with self.assertRaises(config.ConfigError):
            config.load({"feature_flags": {"motion_probe": "yes"}})

    def test_budgets_drive_the_resolver(self) -> None:
        from uiux.engine import performance

        self.assertEqual(performance.effect_budget(), {1: 2, 2: 3, 3: 5, 4: 8, 5: 12})
        self.assertEqual(performance.cost_points()["very-high"], 6)


if __name__ == "__main__":
    unittest.main()
