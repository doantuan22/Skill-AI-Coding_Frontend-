"""Repository-aware UI State Detector: Phase 2 upgrade implementing UIStateDetector extension point.

Uses full repository intelligence (framework, routes, component inventory, styling, tokens)
to accurately classify GREENFIELD, PARTIAL_UI, EXISTING_UI, or UNKNOWN.
"""
from __future__ import annotations

from typing import Any

from uiux.engine.repo_intelligence.profile import build_repo_profile
from uiux.engine.repo_intelligence.scanner import RepositorySnapshot
from uiux.engine.ui_state import (
    EXISTING_UI,
    GREENFIELD,
    PARTIAL_UI,
    UNKNOWN,
    UIStateDetector,
)


class RepositoryUIStateDetector(UIStateDetector):
    """Phase 2 UI State Detector backed by Repo & Framework Intelligence."""

    def detect(self, repo_context: dict[str, Any] | None = None) -> dict[str, Any]:
        if not repo_context:
            return {
                "ui_state": UNKNOWN,
                "confidence": 0.0,
                "signals": {"source": "missing_context", "files_analyzed": 0},
                "reasons": ["No repository context provided for inspection."],
            }

        # 1. Reuse precomputed repo_profile if available in context
        if "repo_profile" in repo_context and isinstance(repo_context["repo_profile"], dict):
            profile = repo_context["repo_profile"]
            ui_state_info = profile.get("existing_ui_state", {})
            return {
                "ui_state": ui_state_info.get("value", UNKNOWN),
                "confidence": float(ui_state_info.get("confidence", 0.5)),
                "signals": {
                    "framework": profile.get("framework", {}).get("name"),
                    "styling": profile.get("styling_system", {}).get("primary"),
                    "components_count": profile.get("components", {}).get("total_count", 0),
                    "routes_count": len(profile.get("routes", [])),
                    "tokens_confidence": profile.get("design_tokens", {}).get("confidence", 0.0),
                },
                "reasons": ui_state_info.get("evidence", ["Derived from precomputed repo_profile."]),
            }

        # 2. Check explicit ui_signals override if provided
        explicit_signals = repo_context.get("ui_signals")
        if isinstance(explicit_signals, dict) and "ui_state" in explicit_signals:
            state = explicit_signals["ui_state"]
            return {
                "ui_state": state,
                "confidence": float(explicit_signals.get("confidence", 0.9)),
                "signals": explicit_signals,
                "reasons": explicit_signals.get("reasons", ["Derived from explicit UI signals in context."]),
            }

        # 3. Build snapshot from context
        files = repo_context.get("files")
        workspace_root = repo_context.get("workspace_root")
        package_json = repo_context.get("package_json")

        has_files_key = "files" in repo_context and files is not None
        if not has_files_key and not workspace_root and not package_json:
            return {
                "ui_state": UNKNOWN,
                "confidence": 0.2,
                "signals": {"files_analyzed": 0},
                "reasons": ["Insufficient context: empty file list and no package manifest."],
            }

        snapshot = RepositorySnapshot(
            workspace_root=workspace_root,
            file_list=files if has_files_key else None,
            package_json_data=package_json,
        )

        profile = build_repo_profile(snapshot)
        ui_state_info = profile["existing_ui_state"]

        return {
            "ui_state": ui_state_info["value"],
            "confidence": ui_state_info["confidence"],
            "signals": {
                "framework": profile["framework"]["name"],
                "styling": profile["styling_system"]["primary"],
                "components_count": profile["components"]["total_count"],
                "routes_count": len(profile["routes"]),
                "tokens_confidence": profile["design_tokens"]["confidence"],
                "ui_files_count": len(snapshot.ui_files),
                "total_files": len(snapshot.files),
            },
            "reasons": ui_state_info["evidence"],
        }
