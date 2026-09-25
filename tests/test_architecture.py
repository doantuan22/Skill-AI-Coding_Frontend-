"""Architecture boundaries: import direction, core independence from the plugin, portable paths, no startup effects."""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

import _paths

ROOT = _paths.PACKAGE_ROOT
LAYERS = json.loads((ROOT / "uiux/core/layers.json").read_text(encoding="utf-8"))


def module_name(path: Path) -> str:
    rel = path.relative_to(ROOT).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def rule_for(module: str) -> tuple[str, list[str]]:
    """Most specific import rule for a module (uiux.api, uiux.engine, plugin, ...)."""
    if module.startswith("plugin"):
        return "plugin", LAYERS["imports"]["plugin"]
    candidates = [key for key in LAYERS["imports"] if module == key or module.startswith(key + ".")]
    if not candidates:
        return "uiux", ["uiux.core"]  # package __init__
    key = max(candidates, key=len)
    return key, LAYERS["imports"][key]


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return {n for n in names if n == "uiux" or n.startswith("uiux.") or n.startswith("plugin")}


def allowed(target: str, own: str, rules: list[str]) -> bool:
    if target == own or target.startswith(own + "."):
        return True
    return any(target == r or target.startswith(r + ".") for r in rules) or target == "uiux.__version__"


class ImportDirectionTests(unittest.TestCase):
    def python_files(self) -> list[Path]:
        return sorted((ROOT / "uiux").rglob("*.py")) + sorted((ROOT / "plugin").rglob("*.py"))

    def test_layers_only_import_downward(self) -> None:
        violations = []
        for path in self.python_files():
            module = module_name(path)
            own, rules = rule_for(module)
            for target in imported_modules(path):
                # "from uiux.core import config" yields uiux.core and uiux.core.config; both must be allowed
                if not allowed(target, own, rules):
                    violations.append(f"{module} imports {target}")
        self.assertEqual(violations, [])

    def test_core_never_imports_or_reads_the_plugin_layer(self) -> None:
        # The whole-package validator may check plugin files, but only when plugin/ exists (proven by the core-only
        # copy in test_plugin_layer); nothing else in the core may reference the plugin layer.
        conditional_checker = {"validate.py"}
        for path in sorted((ROOT / "uiux").rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, r"(?m)^\s*(from|import)\s+plugin\b", "core imports plugin")
                if path.name not in conditional_checker:
                    self.assertNotIn("plugin/manifest", text)
                    self.assertNotIn("adapters", text)

    def test_adapters_use_only_the_public_api(self) -> None:
        for path in sorted((ROOT / "plugin").rglob("*.py")):
            for target in imported_modules(path):
                with self.subTest(path=path.name, target=target):
                    self.assertIn(target, {"uiux", "uiux.api", "uiux.__version__"})

    def test_mcp_transport_has_no_dynamic_execution_or_internal_api_bypass(self) -> None:
        source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "adapters/mcp").glob("*.py"))
        for forbidden in ("uiux.core", "uiux.engine", "uiux.runtime", "uiux.knowledge", "uiux.evals",
                          "importlib", "eval(", "exec(", "subprocess", "os.system", "shell=True"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)


class PortabilityTests(unittest.TestCase):
    # drive-letter paths, home directories and UNC shares (\\server\share) inside string literals
    ABSOLUTE = re.compile(r"""["'](?:[A-Za-z]:[\\/]|/Users/|/home/|\\\\[A-Za-z0-9])[^"']*["']""")

    def test_no_machine_specific_absolute_paths_in_code_or_config(self) -> None:
        files = [*sorted((ROOT / "uiux").rglob("*.py")), *sorted((ROOT / "uiux").rglob("*.json")),
                 *sorted((ROOT / "plugin").rglob("*.py")), *sorted((ROOT / "plugin").rglob("*.json")),
                 *sorted((ROOT / "scripts").glob("*.py"))]
        for path in files:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIsNone(self.ABSOLUTE.search(path.read_text(encoding="utf-8")))

    def test_only_resources_and_bootstraps_derive_the_root_from_file_location(self) -> None:
        allowed_files = {"uiux/core/resources.py", "uiux/__init__.py", "scripts/_bootstrap.py",
                         "adapters/generic/adapter.py", "adapters/mcp/server.py",
                         ".claude-plugin/export.py", ".claude-plugin/verify.py",
                         ".codex-plugin/export.py", ".codex-plugin/verify.py",
                         "adapters/common/bundle.py",
                         "packaging/package_files.py"}
        pattern = re.compile(r"__file__\)\.resolve\(\)\.parents\[")
        for path in [*(ROOT / "uiux").rglob("*.py"), *(ROOT / "scripts").glob("*.py"), *(ROOT / "plugin").rglob("*.py")]:
            rel = path.relative_to(ROOT).as_posix()
            if pattern.search(path.read_text(encoding="utf-8")):
                self.assertIn(rel, allowed_files)

    def test_declared_internal_modules_exist_and_are_not_used_by_adapters(self) -> None:
        import importlib

        for name in LAYERS["internal_modules"]:
            with self.subTest(module=name):
                self.assertIsNotNone(importlib.import_module(name))

    def test_no_script_shadows_the_package(self) -> None:
        # scripts/ is sys.path[0] when a CLI runs; a scripts/uiux.py would shadow the uiux package.
        self.assertFalse((ROOT / "scripts" / "uiux.py").exists())
        self.assertFalse((ROOT / "scripts" / "uiux").exists())

    def test_every_repository_file_belongs_to_a_layer(self) -> None:
        from uiux import api

        if _paths.IS_GIT_WORK_TREE:
            tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
            files = tracked.stdout.split() if tracked.returncode == 0 else []
            files += [p.relative_to(ROOT).as_posix() for p in (ROOT / "uiux").rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        else:  # extracted artifact (no git): classify every file that is actually present
            files = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
        unclassified = sorted({f for f in files if api.layer_of(f) is None})
        self.assertEqual(unclassified, [])


class StartupTests(unittest.TestCase):
    def test_importing_the_api_has_no_runtime_side_effects(self) -> None:
        code = ("import sys; sys.path.insert(0, sys.argv[1]); import uiux.api; "
                "heavy=[m for m in sys.modules if m.startswith(('uiux.runtime', 'uiux.engine', 'uiux.evals', 'uiux.tooling', 'subprocess_marker'))]; "
                "print(heavy)")
        result = subprocess.run([sys.executable, "-c", code, str(ROOT)], capture_output=True, text=True, cwd=str(ROOT.parent))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]")

    def test_nothing_imports_playwright(self) -> None:
        for path in sorted((ROOT / "uiux").rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            names = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            names |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
            self.assertFalse({n for n in names if "playwright" in n}, path.name)


if __name__ == "__main__":
    unittest.main()
