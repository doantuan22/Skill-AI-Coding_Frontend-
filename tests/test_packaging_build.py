"""Artifact builder: release vs dev modes, determinism, metadata, version propagation, protections."""
from __future__ import annotations

import gzip
import json
import tarfile
import tempfile
import time
import unittest
import zipfile
from pathlib import Path

import _packaging_support as S
from _packaging_support import artifact


def snapshot(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): artifact.sha256_file(p) for p in sorted(root.rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(root).parts}


@unittest.skipUnless(S.GIT_AVAILABLE, "git is required for release builds")
class ReleaseBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="uiux-release-")
        base = Path(cls.temp.name)
        cls.repo = S.make_repo(base)
        cls.before = snapshot(cls.repo)
        cls.code_a, cls.result_a = S.run_build(cls.repo, base / "out-a")
        cls.code_b, cls.result_b = S.run_build(cls.repo, base / "out-b")
        cls.out_a, cls.out_b = base / "out-a", base / "out-b"
        cls.head = S.git(cls.repo, "rev-parse", "HEAD").stdout.strip()
        cls.version = (cls.repo / "VERSION").read_text(encoding="utf-8").strip()
        cls.base = f"ui-ux-design-{cls.version}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_release_build_succeeds_and_is_marked_release(self) -> None:
        self.assertEqual((self.code_a, self.result_a["status"]), (0, "BUILT"), self.result_a)
        self.assertEqual(self.result_a["build_mode"], "release")
        self.assertTrue(self.result_a["release"])
        self.assertEqual(self.result_a["commit"], self.head)

    def test_two_builds_are_byte_identical(self) -> None:
        self.assertEqual((self.out_a / "SHA256SUMS").read_bytes(), (self.out_b / "SHA256SUMS").read_bytes())
        for suffix in (".zip", ".tar.gz", ".package-manifest.json"):
            self.assertEqual((self.out_a / f"{self.base}{suffix}").read_bytes(), (self.out_b / f"{self.base}{suffix}").read_bytes())

    def test_version_and_identity_propagate(self) -> None:
        manifest = json.loads((self.out_a / f"{self.base}.package-manifest.json").read_text(encoding="utf-8"))
        plugin = json.loads((self.repo / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], self.version)
        self.assertEqual(manifest["name"], "ui-ux-design")
        self.assertEqual(manifest["skill_name"], "ui-ux-workflow")
        self.assertEqual(manifest["python_package"], "uiux")
        self.assertEqual(manifest["manifest_version"], plugin["manifest_version"])
        self.assertEqual(manifest["source"], {"kind": "git-archive", "commit": self.head, "worktree_clean": True})
        self.assertEqual(manifest["source_date_epoch"], S.COMMIT_EPOCH)
        with zipfile.ZipFile(self.out_a / f"{self.base}.zip") as archive:
            embedded = archive.read(f"{self.base}/PACKAGE-MANIFEST.json")
        self.assertEqual(embedded, (self.out_a / f"{self.base}.package-manifest.json").read_bytes())
        self.assertEqual(artifact.validate_schema(manifest, json.loads(
            (S.ROOT / "schemas/package-manifest.schema.json").read_text(encoding="utf-8"))), [])

    def test_zip_metadata_is_deterministic_and_canonical(self) -> None:
        with zipfile.ZipFile(self.out_a / f"{self.base}.zip") as archive:
            infos = archive.infolist()
        names = [i.filename for i in infos]
        self.assertEqual(names, sorted(names, key=lambda n: n.encode("utf-8")))
        # ZIP stores DOS time with 2-second resolution: odd seconds read back rounded down.
        expected_time = time.gmtime(S.COMMIT_EPOCH - S.COMMIT_EPOCH % 2)[:6]
        for info in infos:
            with self.subTest(member=info.filename):
                self.assertTrue(info.filename.startswith(f"{self.base}/"))
                self.assertNotIn("\\", info.filename)
                self.assertFalse(info.filename.endswith("/"))
                self.assertEqual(info.date_time, expected_time)
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr >> 16, 0o100644)
                artifact.canonical_path(info.filename)

    def test_tar_metadata_is_deterministic(self) -> None:
        path = self.out_a / f"{self.base}.tar.gz"
        header = path.read_bytes()[:10]
        self.assertEqual(header[4:8], b"\x00\x00\x00\x00", "gzip mtime must be 0")
        self.assertEqual(header[3] & 0x08, 0, "gzip header must not store a file name")
        with tarfile.open(path, "r:gz") as archive:
            members = archive.getmembers()
        self.assertEqual([m.name for m in members], sorted((m.name for m in members), key=lambda n: n.encode("utf-8")))
        for member in members:
            with self.subTest(member=member.name):
                self.assertTrue(member.isfile())
                self.assertEqual((member.mtime, member.uid, member.gid, member.uname, member.gname, member.mode),
                                 (S.COMMIT_EPOCH, 0, 0, "", "", 0o644))

    def test_both_formats_hold_identical_content(self) -> None:
        with zipfile.ZipFile(self.out_a / f"{self.base}.zip") as archive:
            from_zip = {i.filename: archive.read(i) for i in archive.infolist()}
        with tarfile.open(self.out_a / f"{self.base}.tar.gz", "r:gz") as archive:
            from_tar = {m.name: archive.extractfile(m).read() for m in archive.getmembers()}
        self.assertEqual(from_zip, from_tar)

    def test_required_included_and_forbidden_excluded(self) -> None:
        with zipfile.ZipFile(self.out_a / f"{self.base}.zip") as archive:
            paths = {n.split("/", 1)[1] for n in archive.namelist()}
        rules = artifact.load_rules(self.repo)
        self.assertLessEqual(set(rules["must_include"]), paths)
        forbidden = [p for p in paths if p.startswith(("tests/", ".git", ".github/", "dist/"))
                     or "__pycache__" in p or p.endswith((".pyc", ".log", ".tmp")) or ".evidence" in p]
        self.assertEqual(forbidden, [])

    def test_checksums_and_build_info(self) -> None:
        lines = (self.out_a / "SHA256SUMS").read_text(encoding="ascii").splitlines()
        listed = dict(reversed(line.split("  ", 1)) for line in lines)
        self.assertEqual(set(listed), {f"{self.base}.zip", f"{self.base}.tar.gz", f"{self.base}.package-manifest.json"})
        for name, digest in listed.items():
            self.assertEqual(artifact.sha256_file(self.out_a / name), digest)
        info = json.loads((self.out_a / f"{self.base}.build-info.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact.validate_schema(info, json.loads(
            (S.ROOT / "schemas/build-info.schema.json").read_text(encoding="utf-8"))), [])
        self.assertEqual(info["content_sha256"], artifact.sha256_file(self.out_a / f"{self.base}.package-manifest.json"))

    def test_source_tree_is_not_modified(self) -> None:
        self.assertEqual(snapshot(self.repo), self.before)
        self.assertFalse((self.repo / "dist").exists())


@unittest.skipUnless(S.GIT_AVAILABLE, "git is required for release builds")
class ProtectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="uiux-protect-")
        cls.base = Path(cls.temp.name)
        cls.repo = S.make_repo(cls.base)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def build_error(self, repo: Path, *args: str) -> dict:
        out = self.base / f"out-{repo.name}"
        code, result = S.run_build(repo, out, *args)
        self.assertEqual(code, 1, result)
        self.assertFalse(out.exists(), "a refused build must not write artifacts")
        return result["error"]

    def test_modified_tracked_file_blocks_release(self) -> None:
        repo = S.clone(self.repo, self.base, "dirty-modified")
        target = (repo / "plugins" / "ui-engineering" / "SKILL.md") if (repo / "plugins" / "ui-engineering").is_dir() else (repo / "SKILL.md")
        target.write_text(target.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
        error = self.build_error(repo)
        self.assertEqual(error["code"], "DIRTY_TREE")
        self.assertEqual(error["details"]["hint"], "COMMIT_REQUIRED_BEFORE_RELEASE_BUILD")

    def test_untracked_file_blocks_release(self) -> None:
        repo = S.clone(self.repo, self.base, "dirty-untracked")
        (repo / "development" / "docs").mkdir(parents=True, exist_ok=True)
        (repo / "development" / "docs" / "scratch-notes.md").write_text("draft\n", encoding="utf-8")
        self.assertEqual(self.build_error(repo)["code"], "DIRTY_TREE")

    def test_dev_build_of_dirty_tree_is_explicit_and_marked(self) -> None:
        repo = S.clone(self.repo, self.base, "dirty-dev")
        (repo / "development" / "docs").mkdir(parents=True, exist_ok=True)
        (repo / "development" / "docs" / "scratch-notes.md").write_text("draft\n", encoding="utf-8")
        out = self.base / "out-dev"
        code, result = S.run_build(repo, out, "--dev")
        self.assertEqual(code, 0, result)
        version = (repo / "VERSION").read_text(encoding="utf-8").strip()
        base = f"ui-ux-design-{version}-dev"
        manifest = json.loads((out / f"{base}.package-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((manifest["build_mode"], manifest["release"]), ("dev", False))
        self.assertEqual(manifest["source"]["kind"], "working-tree")
        self.assertFalse(manifest["source"]["worktree_clean"])
        with zipfile.ZipFile(out / f"{base}.zip") as archive:
            self.assertTrue(all(n.startswith(f"{base}/") for n in archive.namelist()))

    def test_not_a_git_repository(self) -> None:
        plain = self.base / "plain"
        plain.mkdir()
        (plain / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
        for rel in ("packaging/package-rules.json",):
            (plain / rel).parent.mkdir(parents=True, exist_ok=True)
            (plain / rel).write_bytes((self.repo / rel).read_bytes())
        self.assertIn(self.build_error(plain)["code"], {"NOT_A_GIT_REPOSITORY", "NOT_REPOSITORY_ROOT"})

    def test_version_mismatch_blocks_release(self) -> None:
        repo = S.clone(self.repo, self.base, "version-mismatch")
        (repo / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        S.commit_all(repo)
        self.assertEqual(self.build_error(repo)["code"], "VERSION_MISMATCH")

    def test_missing_changelog_section_blocks_release(self) -> None:
        repo = S.clone(self.repo, self.base, "changelog")
        (repo / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        manifest = json.loads((repo / "plugin.json").read_text(encoding="utf-8"))
        manifest["version"] = "9.9.9"
        (repo / "plugin.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        S.commit_all(repo)
        self.assertEqual(self.build_error(repo)["code"], "CHANGELOG_MISSING")

    def test_stale_knowledge_registry_blocks_release(self) -> None:
        repo = S.clone(self.repo, self.base, "stale-registry")
        path = (repo / "plugins/ui-engineering/knowledge/domains/registry.json") if (repo / "plugins/ui-engineering").is_dir() else (repo / "knowledge/domains/registry.json")
        path.write_text(path.read_text(encoding="utf-8").replace('"styles"', '"styles "', 1), encoding="utf-8")
        S.commit_all(repo)
        self.assertEqual(self.build_error(repo)["code"], "REGISTRY_STALE")

    def test_crlf_working_tree_produces_the_same_content_as_the_release(self) -> None:
        repo = S.clone(self.repo, self.base, "crlf")
        target = (repo / "plugins/ui-engineering/SKILL.md") if (repo / "plugins/ui-engineering").is_dir() else (repo / "SKILL.md")
        target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        code_dev, dev = S.run_build(repo, self.base / "out-crlf-dev", "--dev")
        code_rel, rel = S.run_build(self.repo, self.base / "out-crlf-rel")
        self.assertEqual((code_dev, code_rel), (0, 0), (dev, rel))
        def files(result: dict) -> dict:
            return {f["path"]: f["sha256"] for f in json.loads(Path(result["package_manifest"]).read_text(encoding="utf-8"))["files"]}
        self.assertEqual(files(dev)["SKILL.md"], files(rel)["SKILL.md"])
        png = "evals/runtime-fixtures/evidence-valid/pages/PAGE-HOME__mobile__iter-01.png"
        self.assertEqual(files(dev)[png], artifact.sha256_file(repo / png), "binary files must not be transformed")


if __name__ == "__main__":
    unittest.main()
