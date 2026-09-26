"""Existing UI Analyzer & Preservation Guard: Deep analysis of identity, layout, components, and hard invariant preservation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from uiux.engine.existing_ui.evaluator import PreservationEvaluator
from uiux.engine.existing_ui.preservation_profile import build_preservation_profile
from uiux.engine.existing_ui.profile import build_existing_ui_profile
from uiux.engine.repo_intelligence import analyze_repository
from uiux.engine.repo_intelligence.scanner import RepositorySnapshot

__all__ = [
    "analyze_existing_ui",
    "build_preservation_profile",
    "evaluate_preservation",
    "PreservationEvaluator",
    "build_existing_ui_profile",
]


def analyze_existing_ui(
    project: str | Path = ".",
    repo_profile: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Primary entry point for Existing UI Analysis.

    Reuses Phase 2 repo_profile and RepositorySnapshot, performing deep code-level
    extraction of visual identity, layout hierarchy, component consistency, UX flows,
    responsive health, accessibility landmarks, and design system maturity.
    """
    opts = options or {}

    # 1. Resolve or reuse repo_profile
    if repo_profile is None:
        repo_profile = analyze_repository(project=project, options=opts)

    # 2. Resolve RepositorySnapshot
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

    # 3. Monorepo handling: if multiple apps detected, analyze them separately if requested
    signals = repo_profile.get("repository_signals", {})
    if signals.get("is_monorepo") and signals.get("apps"):
        apps_profiles: dict[str, Any] = {}
        for app in signals["apps"]:
            app_root = app["root"]
            sub_files = [f for f in snapshot.files if f.startswith(app_root + "/")]
            sub_snapshot = RepositorySnapshot(
                file_list=sub_files,
                file_contents=snapshot.file_contents_override,
            )
            sub_repo_prof = analyze_repository(
                options={"files": sub_files, "file_contents": snapshot.file_contents_override}
            )
            sub_prof = build_existing_ui_profile(sub_repo_prof, sub_snapshot)
            apps_profiles[app["name"]] = sub_prof
            apps_profiles[app_root] = sub_prof

        # Primary application profile
        base_profile = build_existing_ui_profile(repo_profile, snapshot)
        base_profile["applications"] = apps_profiles
        return base_profile

    return build_existing_ui_profile(repo_profile, snapshot)


def evaluate_preservation(
    baseline_profile: dict[str, Any],
    proposed_changes: dict[str, Any],
    permissions: dict[str, Any] | None = None,
    requested_scope: str | None = None,
) -> dict[str, Any]:
    """Evaluate planned or implemented changes against baseline preservation invariants."""
    evaluator = PreservationEvaluator()
    return evaluator.evaluate(
        baseline_profile=baseline_profile,
        proposed_changes=proposed_changes,
        permissions=permissions,
        requested_scope=requested_scope,
    )
