"""Repo & Framework Intelligence: Structural, deterministic, evidence-based repository analysis."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from uiux.engine.repo_intelligence.framework import detect_framework
from uiux.engine.repo_intelligence.profile import build_repo_profile
from uiux.engine.repo_intelligence.scanner import RepositorySnapshot
from uiux.engine.repo_intelligence.ui_state_detector import RepositoryUIStateDetector

__all__ = [
    "analyze_repository",
    "detect_framework",
    "RepositorySnapshot",
    "RepositoryUIStateDetector",
    "build_repo_profile",
]


def analyze_repository(
    project: str | Path = ".",
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Primary entry point for Repo Intelligence.

    Inspects repository context, runs detectors, resolves conflicts, and generates
    the normalized `repo_profile` adhering to schemas/repo-profile.schema.json.
    """
    opts = options or {}
    has_files_override = "files" in opts
    files_override = opts.get("files")
    package_json_override = opts.get("package_json")
    file_contents_override = opts.get("file_contents")

    snapshot = RepositorySnapshot(
        workspace_root=project if not has_files_override else None,
        file_list=files_override if has_files_override else None,
        package_json_data=package_json_override,
        file_contents=file_contents_override,
    )

    return build_repo_profile(snapshot)
