"""Artifact verification on extracted archives: full pipeline plus targeted negative cases."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import _packaging_support as S
from _packaging_support import artifact, verify


@unittest.skipUnless(S.GIT_AVAILABLE, "git is required for release builds")
class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="uiux-verify-test-")
        cls.base = Path(cls.temp.name)
        cls.repo = S.make_repo(cls.base)
        code, result = S.run_build(cls.repo, cls.base / "release")
        assert code == 0, result
        cls.zip = Path([a for a in result["artifacts"] if a.endswith(".zip")][0])
        cls.targz = Path([a for a in result["artifacts"] if a.endswith(".tar.gz")][0])
        cls.full = verify.verify(cls.zip, require_release=True, tests_dir=None, report_path=cls.base / "full-report.json")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def status(self, report: dict) -> dict:
        return {c["id"]: c["status"] for c in report["checks"]}

    def quick(self, archive: Path, **kwargs) -> dict:
        return verify.verify(archive, tests_dir=None, quick=True, report_path=self.base / f"{archive.stem}.json", **kwargs)

    def mutated(self, name: str, mutate) -> Path:
        target = self.base / "mutations" / name / self.zip.name
        target.parent.mkdir(parents=True)
        S.rewrite_zip(self.zip, target, mutate)
        return target

    # ------------------------------------------------------------------ positive
    def test_full_pipeline_passes_on_the_extracted_release(self) -> None:
        statuses = self.status(self.full)
        self.assertEqual(self.full["status"], "PASS", json.dumps(self.full["checks"], indent=1)[-3000:])
        for cid in ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12"):
            self.assertEqual(statuses[cid], "PASS", cid)
        self.assertEqual(statuses["V13"], "NOT_RUN")  # tests are not packaged; not requested here
        self.assertEqual(statuses["V14"], "NOT_RUN")  # needs a second operating system
        self.assertEqual(set(self.full["not_run"]), {"V13", "V14"})
        self.assertTrue((self.base / "full-report.json").is_file())

    def test_tar_gz_passes_structural_checks(self) -> None:
        report = self.quick(self.targz, require_release=True)
        self.assertEqual(report["status"], "PASS", report["checks"])

    def test_artifact_runs_without_the_source_repository(self) -> None:
        with tempfile.TemporaryDirectory() as extract, tempfile.TemporaryDirectory() as cwd:
            root = artifact.safe_extract(self.zip, Path(extract))
            result = subprocess.run([sys.executable, str(root / "scripts/uiux_cli.py"), "call", "retrieve_knowledge",
                                     "--params", '{"ids": ["style.swiss"]}'], capture_output=True, text=True,
                                    encoding="utf-8", cwd=cwd, env=S.build.clean_env())
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["entries"][0]["id"], "style.swiss")
            described = subprocess.run([sys.executable, str(root / "scripts/uiux_cli.py"), "architecture"],
                                       capture_output=True, text=True, encoding="utf-8", cwd=cwd, env=S.build.clean_env())
            self.assertEqual(Path(json.loads(described.stdout)["package_root"]).resolve(), root.resolve())
            self.assertNotIn(str(S.ROOT), described.stdout)

    def test_installed_root_ignores_bytecode_but_not_other_files(self) -> None:
        with tempfile.TemporaryDirectory() as extract:
            root = artifact.safe_extract(self.zip, Path(extract))
            (root / "uiux" / "__pycache__").mkdir(exist_ok=True)
            (root / "uiux" / "__pycache__" / "api.cpython-311.pyc").write_bytes(b"cache")
            self.assertEqual(verify.verify(installed=root, tests_dir=None, quick=True)["status"], "PASS")
            (root / "docs" / "stray.md").write_text("stray\n", encoding="utf-8")
            report = verify.verify(installed=root, tests_dir=None, quick=True)
            self.assertEqual(self.status(report)["V1"], "FAIL")

    # ------------------------------------------------------------------ negative
    def test_corrupted_file_fails_integrity(self) -> None:
        corrupted = self.base / "corrupted" / self.zip.name
        corrupted.parent.mkdir()
        with zipfile.ZipFile(self.zip) as source, zipfile.ZipFile(corrupted, "w") as target:
            for info in source.infolist():
                data = source.read(info)
                if info.filename.endswith("/SKILL.md"):
                    data += b"\ntampered\n"
                target.writestr(info, data)
        report = self.quick(corrupted)
        self.assertEqual(self.status(report)["V1"], "FAIL")
        self.assertTrue(any("SKILL.md" in d for d in self.status_detail(report, "V1")))
        self.assertEqual(report["status"], "FAIL")

    def test_missing_required_file_fails_whitelist(self) -> None:
        archive = self.mutated("missing-required", lambda files: files.pop("evals/fixtures/quality/expectations.json"))
        report = self.quick(archive)
        self.assertEqual(self.status(report)["V1"], "PASS")
        self.assertEqual(self.status(report)["V2"], "FAIL")
        self.assertTrue(any("expectations.json" in d for d in self.status_detail(report, "V2")))

    def test_forbidden_file_fails_whitelist(self) -> None:
        def add(files: dict) -> None:
            files["tests/test_leak.py"] = b"leak = True\n"
            files["uiux/__pycache__/api.cpython-311.pyc"] = b"\x00cache"
        report = self.quick(self.mutated("forbidden", add))
        self.assertEqual(self.status(report)["V2"], "FAIL")
        detail = " ".join(self.status_detail(report, "V2"))
        self.assertIn("tests/test_leak.py", detail)
        self.assertIn("__pycache__", detail)

    def test_version_mismatch_fails_identity(self) -> None:
        report = self.quick(self.mutated("version", lambda files: files.__setitem__("VERSION", b"9.9.9\n")))
        self.assertEqual(self.status(report)["V4"], "FAIL")
        self.assertTrue(any("version mismatch" in d for d in self.status_detail(report, "V4")))

    def test_invalid_manifest_fails(self) -> None:
        def break_manifest(files: dict) -> None:
            manifest = json.loads(files["plugin/manifest/plugin.json"])
            del manifest["tools"]
            files["plugin/manifest/plugin.json"] = json.dumps(manifest).encode("utf-8")
        report = self.quick(self.mutated("manifest", break_manifest))
        self.assertEqual(self.status(report)["V5"], "FAIL")

    def test_dev_artifact_is_rejected_when_a_release_is_required(self) -> None:
        code, result = S.run_build(self.repo, self.base / "dev", "--dev")
        self.assertEqual(code, 0, result)
        dev_zip = Path([a for a in result["artifacts"] if a.endswith(".zip")][0])
        self.assertEqual(self.quick(dev_zip)["status"], "PASS")
        report = self.quick(dev_zip, require_release=True)
        self.assertEqual(self.status(report)["V4"], "FAIL")
        self.assertTrue(any("NOT_A_RELEASE" in d for d in self.status_detail(report, "V4")))

    def test_unsafe_archive_paths_are_rejected(self) -> None:
        evil = self.base / "evil.zip"
        with zipfile.ZipFile(evil, "w") as archive:
            archive.writestr("ui-ux-design-0.1.0/../../escaped.txt", b"x")
        report = verify.verify(evil, tests_dir=None, quick=True, report_path=self.base / "evil.json")
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("UNSAFE_PATH" in d for d in self.status_detail(report, "V1")))
        self.assertFalse((self.base.parent / "escaped.txt").exists())

    def test_structural_failure_skips_behavioral_checks(self) -> None:
        archive = self.mutated("skip", lambda files: files.__setitem__("VERSION", b"9.9.9\n"))
        report = verify.verify(archive, tests_dir=None, report_path=self.base / "skip.json")
        statuses = self.status(report)
        self.assertEqual(statuses["V4"], "FAIL")
        self.assertTrue(all(statuses[c] == "NOT_RUN" for c in ("V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13")))

    def status_detail(self, report: dict, cid: str) -> list[str]:
        detail = next(c["detail"] for c in report["checks"] if c["id"] == cid)
        return detail if isinstance(detail, list) else [str(detail)]


if __name__ == "__main__":
    unittest.main()
