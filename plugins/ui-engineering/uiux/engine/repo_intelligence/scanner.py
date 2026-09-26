"""Repository Scanner & Snapshot: Single-pass, bounded, read-only repository inspection.

Provides normalized signals to all specialized detectors without redundant filesystem traversals.
Strictly ignores vendor, cache, and build directories.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

IGNORED_DIRS = {
    "node_modules", "dist", "build", ".next", ".nuxt", "coverage", ".git",
    "__pycache__", ".cache", "out", "vendor", ".turbo", ".svelte-kit",
    ".output", "target", "bin", "obj", ".idea", ".vscode", "tmp",
}

UI_FILE_EXTENSIONS = {
    ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".html", ".htm",
    ".css", ".scss", ".sass", ".less", ".styl",
}

CONFIG_FILENAMES = {
    "package.json", "tsconfig.json", "jsconfig.json", "pom.xml", "build.gradle",
    "build.gradle.kts", "Makefile", "angular.json", "playwright.config.js",
    "playwright.config.ts", "pnpm-workspace.yaml", "lerna.json",
}

CONFIG_PATTERNS = (
    "vite.config.", "next.config.", "nuxt.config.", "svelte.config.",
    "tailwind.config.", "postcss.config.", "webpack.config.",
)


class RepositorySnapshot:
    """Read-only, cached in-memory snapshot of repository structure and key manifests."""

    def __init__(
        self,
        workspace_root: str | Path | None = None,
        file_list: list[str] | None = None,
        package_json_data: dict[str, Any] | None = None,
        file_contents: dict[str, str] | None = None,
        max_scan_files: int = 5000,
    ) -> None:
        self.workspace_root: Path | None = Path(workspace_root).resolve() if workspace_root else None
        self.file_contents_override: dict[str, str] = file_contents or {}
        self._content_cache: dict[str, str] = {}
        self.max_scan_files = max_scan_files

        # 1. Resolve files list
        if file_list is not None:
            self.files: list[str] = [f.replace("\\", "/") for f in file_list]
        elif self.workspace_root and self.workspace_root.is_dir():
            self.files = self._scan_filesystem(self.workspace_root)
        else:
            self.files = []

        self.file_set: set[str] = set(self.files)

        # 2. Extract UI source files and configuration manifests
        self.config_files: list[str] = [f for f in self.files if self._is_config_file(f)]
        self.ui_files: list[str] = [
            f for f in self.files if Path(f).suffix.lower() in UI_FILE_EXTENSIONS
        ]

        # 3. Resolve package.json
        if package_json_data is not None:
            self.package_json = package_json_data
        elif self.workspace_root and (self.workspace_root / "package.json").is_file():
            self.package_json = self._load_json(self.workspace_root / "package.json")
        elif "package.json" in self.file_contents_override:
            try:
                self.package_json = json.loads(self.file_contents_override["package.json"])
            except Exception:
                self.package_json = {}
        else:
            self.package_json = {}

        # 4. Monorepo detection
        self.is_monorepo, self.sub_apps = self._detect_monorepo()

    def _is_config_file(self, rel_path: str) -> bool:
        name = Path(rel_path).name.lower()
        if name in CONFIG_FILENAMES:
            return True
        return any(name.startswith(p) for p in CONFIG_PATTERNS)

    def _scan_filesystem(self, root: Path) -> list[str]:
        collected: list[str] = []
        for dirpath, dirnames, filenames in os.walk(root):
            # Prune ignored directories in-place
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
            rel_dir = Path(dirpath).relative_to(root)
            for f in filenames:
                if len(collected) >= self.max_scan_files:
                    break
                rel_path = str(rel_dir / f).replace("\\", "/") if str(rel_dir) != "." else f
                collected.append(rel_path)
            if len(collected) >= self.max_scan_files:
                break
        return collected

    def read_text(self, rel_path: str, max_chars: int = 150_000) -> str:
        """Safely read text file with caching and size limit."""
        norm_path = rel_path.replace("\\", "/")
        if norm_path in self._content_cache:
            return self._content_cache[norm_path]

        if norm_path in self.file_contents_override:
            text = self.file_contents_override[norm_path][:max_chars]
            self._content_cache[norm_path] = text
            return text

        if self.workspace_root:
            full_path = self.workspace_root / norm_path
            if full_path.is_file():
                try:
                    text = full_path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
                    self._content_cache[norm_path] = text
                    return text
                except Exception:
                    return ""
        return ""

    def _load_json(self, path: Path) -> dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            return {}

    def _detect_monorepo(self) -> tuple[bool, list[dict[str, str]]]:
        sub_apps: list[dict[str, str]] = []
        is_mono = False

        # Workspaces in package.json
        if isinstance(self.package_json, dict) and "workspaces" in self.package_json:
            is_mono = True

        # Check workspace config files
        if any(f in self.file_set for f in ("pnpm-workspace.yaml", "lerna.json")):
            is_mono = True

        # Find package.json files in subdirectories (packages/*, apps/*, etc.)
        for f in self.files:
            if f.endswith("/package.json") and f != "package.json":
                parts = f.split("/")
                if len(parts) >= 2 and parts[0] in ("apps", "packages", "modules", "frontend", "client"):
                    is_mono = True
                    app_root = "/".join(parts[:-1])
                    app_name = parts[-2]
                    sub_apps.append({"root": app_root, "name": app_name, "framework": "unknown"})

        return is_mono, sub_apps

    def get_dependencies(self) -> dict[str, str]:
        """Aggregate dependencies and devDependencies from root package.json."""
        if not isinstance(self.package_json, dict):
            return {}
        deps = self.package_json.get("dependencies", {}) or {}
        dev_deps = self.package_json.get("devDependencies", {}) or {}
        peer_deps = self.package_json.get("peerDependencies", {}) or {}
        return {**deps, **dev_deps, **peer_deps}
