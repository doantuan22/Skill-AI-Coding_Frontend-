"""Cross-platform assumptions of the packaging layer (run on every OS in CI; see .github/workflows)."""
from __future__ import annotations

import ast
import json
import re
import tempfile
import unittest
from pathlib import Path

import _packaging_support as S
from _packaging_support import artifact

PACKAGING_FILES = sorted(S.PACKAGING.glob("*.py"))


class CanonicalPathTests(unittest.TestCase):
    def test_accepts_relative_posix_paths(self) -> None:
        self.assertEqual(artifact.canonical_path("knowledge/domains/INDEX.md"), "knowledge/domains/INDEX.md")

    def test_rejects_platform_specific_or_escaping_paths(self) -> None:
        for bad in ("a\\b.md", "/etc/passwd", "C:/x", "c:x", "../x", "a/../b", "a//b", "./a", ""):
            with self.subTest(path=bad), self.assertRaises(artifact.PackagingError):
                artifact.canonical_path(bad)


class NormalizationTests(unittest.TestCase):
    def test_crlf_text_becomes_lf(self) -> None:
        self.assertEqual(artifact.normalize("a.md", b"x\r\ny\r\n", []), b"x\ny\n")

    def test_binary_content_is_untouched(self) -> None:
        png = b"\x89PNG\r\n\x1a\n\x00\x00\r\n"
        self.assertEqual(artifact.normalize("p.png", png, ["**/*.png"]), png)
        self.assertEqual(artifact.normalize("blob.bin", b"\x00\r\n", []), b"\x00\r\n")
        self.assertEqual(artifact.normalize("x.png", b"text\r\n", ["**/*.png"]), b"text\r\n")

    def test_glob_semantics(self) -> None:
        self.assertTrue(artifact.match("a/b/__pycache__/c.pyc", "**/*.pyc"))
        self.assertTrue(artifact.match("evals/results/x.json", "evals/results/**"))
        self.assertFalse(artifact.match("evals/resultsx/x.json", "evals/results/**"))

    def test_canonical_json_is_stable(self) -> None:
        self.assertEqual(artifact.canonical_json({"b": 1, "a": [2]}), b'{\n "a": [\n  2\n ],\n "b": 1\n}\n')


class OrderingTests(unittest.TestCase):
    def test_selection_is_sorted_by_utf8_bytes(self) -> None:
        paths = S.package_files.compute(S.ROOT)["included"]
        self.assertEqual(paths, sorted(paths, key=lambda p: p.encode("utf-8")))
        self.assertTrue(all("\\" not in p for p in paths))

    def test_zip_writer_is_deterministic(self) -> None:
        entries = [("t/a.md", b"a\n"), ("t/b.md", b"b\n")]
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary, "1.zip"), Path(temporary, "2.zip")
            artifact.write_zip(first, entries, 1767323045, 0o644, 9)
            artifact.write_zip(second, entries, 1767323045, 0o644, 9)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            first_tar, second_tar = Path(temporary, "1.tar.gz"), Path(temporary, "2.tar.gz")
            artifact.write_targz(first_tar, entries, 1767323045, 0o644, 9)
            artifact.write_targz(second_tar, entries, 1767323045, 0o644, 9)
            self.assertEqual(first_tar.read_bytes(), second_tar.read_bytes())


class SourceHygieneTests(unittest.TestCase):
    def test_packaging_code_has_no_os_specific_path_literals(self) -> None:
        pattern = re.compile(r"""["'](?:[A-Za-z]:[\\/]|/tmp/|/home/|/Users/|\\\\\\\\)""")
        for path in PACKAGING_FILES:
            with self.subTest(path=path.name):
                self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")))

    def test_packaging_code_uses_no_os_sep_joins(self) -> None:
        for path in PACKAGING_FILES:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("os.sep", text)
                self.assertNotIn("os.path.join", text)

    def test_packaging_code_imports_only_the_public_api_from_uiux(self) -> None:
        for path in PACKAGING_FILES:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            imported |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
            with self.subTest(path=path.name):
                self.assertTrue({m for m in imported if m.startswith("uiux")} <= {"uiux"})
                self.assertFalse({m for m in imported if "adapters" in m})

    @unittest.skipUnless(S._paths.IS_GIT_WORK_TREE, "repository metadata is not part of an artifact")
    def test_line_ending_policy_and_ci_matrix_exist(self) -> None:
        attributes = (S._paths.REPO_ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn("* text=auto eol=lf", attributes)
        self.assertRegex(attributes, r"(?m)^\*\.png\s+binary")
        for workflow in ("ci.yml", "package.yml"):
            text = (S._paths.REPO_ROOT / ".github/workflows" / workflow).read_text(encoding="utf-8")
            with self.subTest(workflow=workflow):
                self.assertIn("windows-latest", text)
                self.assertIn("ubuntu-latest", text)

    def test_rules_are_the_single_packaging_contract(self) -> None:
        rules = json.loads((S.ROOT / "packaging/package-rules.json").read_text(encoding="utf-8"))
        for key in ("exclude_layers", "exclude_dirs", "exclude_globs", "must_include", "must_exclude_prefixes", "artifact"):
            self.assertIn(key, rules)
        for path in PACKAGING_FILES:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                # file lists live only in package-rules.json: no script repeats the required list
                self.assertNotIn('"uiux/core/defaults.json"', text)


if __name__ == "__main__":
    unittest.main()
