"""UI State detection abstraction and Phase 1 heuristic detector.

Phase 1 provides a clean abstraction and heuristic classification for UI State:
- GREENFIELD: Repository has no significant existing UI/UX, or is a brand-new project.
- PARTIAL_UI: Minimal or prototype UI elements exist (e.g. single component or bare scaffold).
- EXISTING_UI: Significant existing UI presence (components, layouts, stylesheets, design tokens).
- UNKNOWN: Ambiguous signals or insufficient repository context (confidence < threshold).

Architecture Extension Point:
This module defines the UIStateDetector contract. Phase 2 (Repo/Framework Intelligence) and
Phase 3 (Existing UI Analyzer) can replace or enhance the detector implementation without
modifying workflow core or orchestrator routing logic.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

# UI State Constants
GREENFIELD = "GREENFIELD"
PARTIAL_UI = "PARTIAL_UI"
EXISTING_UI = "EXISTING_UI"
UNKNOWN = "UNKNOWN"

UI_STATES = (GREENFIELD, PARTIAL_UI, EXISTING_UI, UNKNOWN)

# File extension patterns recognized for UI heuristics
UI_FILE_EXTENSIONS = {
    ".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro",
    ".css", ".scss", ".sass", ".less", ".styl",
}

UI_CONFIG_FILENAMES = {
    "tailwind.config.js", "tailwind.config.ts", "tailwind.config.cjs", "tailwind.config.mjs",
    "postcss.config.js", "postcss.config.cjs", "postcss.config.mjs",
    "uno.config.ts", "uno.config.js", "vite.config.ts", "vite.config.js",
    "next.config.js", "next.config.mjs", "next.config.ts", "nuxt.config.ts", "nuxt.config.js",
}

UI_DIRECTORY_MARKERS = {
    "components", "views", "pages", "screens", "styles", "ui", "layouts", "design-system",
}

NON_UI_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".nuxt", "__pycache__", ".cache", "out",
}


class UIStateDetector(ABC):
    """Abstract interface for UI state detection."""

    @abstractmethod
    def detect(self, repo_context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Inspect repo context and return a dictionary with:
        - ui_state: GREENFIELD | PARTIAL_UI | EXISTING_UI | UNKNOWN
        - confidence: float 0.0 .. 1.0
        - signals: dict of detected cues
        - reasons: list of explanation strings
        """
        raise NotImplementedError


class HeuristicUIStateDetector(UIStateDetector):
    """Lightweight, deterministic Phase 1 heuristic detector.

    Uses static signal counters and path heuristics without deep AST or framework parsing.
    Safe fallback to UNKNOWN when confidence is below 0.5.
    """

    def __init__(self, confidence_threshold: float = 0.5) -> None:
        self.confidence_threshold = confidence_threshold

    def detect(self, repo_context: dict[str, Any] | None = None) -> dict[str, Any]:
        if not repo_context:
            return {
                "ui_state": UNKNOWN,
                "confidence": 0.0,
                "signals": {"source": "missing_context", "files_analyzed": 0},
                "reasons": ["No repository context or file list provided for inspection."],
            }

        # Check explicit ui_signals override if provided by caller or test fixture
        explicit_signals = repo_context.get("ui_signals")
        if isinstance(explicit_signals, dict) and "ui_state" in explicit_signals:
            state = explicit_signals["ui_state"]
            if state in UI_STATES:
                return {
                    "ui_state": state,
                    "confidence": float(explicit_signals.get("confidence", 0.9)),
                    "signals": explicit_signals,
                    "reasons": explicit_signals.get("reasons", ["Derived from explicit UI signals in context."]),
                }

        has_files_key = "files" in repo_context and repo_context["files"] is not None
        files: list[str] = repo_context.get("files") if has_files_key else []
        workspace_root_str = repo_context.get("workspace_root")
        package_json = repo_context.get("package_json") or {}

        # If files were not passed explicitly but workspace_root is provided and exists, gather files
        if not has_files_key and workspace_root_str:
            root_path = Path(workspace_root_str)
            if root_path.is_dir():
                files = self._scan_directory(root_path)
                has_files_key = True

        if not has_files_key and not package_json and not workspace_root_str:
            return {
                "ui_state": UNKNOWN,
                "confidence": 0.2,
                "signals": {"files_analyzed": 0},
                "reasons": ["Insufficient context: empty file list and no package manifest."],
            }

        # Count signals
        ui_files = [f for f in files if self._is_ui_file(f)]
        ui_configs = [f for f in files if Path(f).name in UI_CONFIG_FILENAMES]
        component_files = [f for f in ui_files if self._is_component_file(f)]
        style_files = [f for f in ui_files if self._is_style_file(f)]
        page_files = [f for f in ui_files if self._is_page_file(f)]

        # Analyze package.json dependencies if available
        pkg_ui_deps = self._detect_ui_dependencies(package_json)

        signals = {
            "total_files": len(files),
            "ui_file_count": len(ui_files),
            "ui_config_count": len(ui_configs),
            "component_count": len(component_files),
            "style_count": len(style_files),
            "page_count": len(page_files),
            "ui_dependencies": pkg_ui_deps,
            "has_ui_dependencies": bool(pkg_ui_deps),
        }

        reasons = []

        # Decision heuristics
        # 1. Clear Greenfield: 0 UI files, no UI dependencies, empty or purely non-UI
        if len(ui_files) == 0 and not pkg_ui_deps and len(ui_configs) == 0:
            reasons.append("No UI files, stylesheets, components, or UI dependencies detected.")
            return {
                "ui_state": GREENFIELD,
                "confidence": 0.95,
                "signals": signals,
                "reasons": reasons,
            }

        # 2. Existing UI: Significant UI files (components, styles, or pages)
        is_substantial_ui = (
            len(component_files) >= 2 or
            (len(page_files) >= 1 and len(style_files) >= 1) or
            len(ui_files) >= 4 or
            (bool(pkg_ui_deps) and len(ui_files) >= 2)
        )

        if is_substantial_ui:
            reasons.append(
                f"Detected established UI footprint: {len(component_files)} components, "
                f"{len(page_files)} pages, {len(style_files)} stylesheets."
            )
            if pkg_ui_deps:
                reasons.append(f"Detected UI dependencies: {', '.join(pkg_ui_deps)}.")
            return {
                "ui_state": EXISTING_UI,
                "confidence": 0.92,
                "signals": signals,
                "reasons": reasons,
            }

        # 3. Partial UI: Bare scaffold, 1 single component or 1 style file with no rich structure
        is_partial_ui = (
            (len(ui_files) in (1, 2, 3) and len(component_files) <= 1) or
            (bool(pkg_ui_deps) and len(ui_files) == 0) or
            (len(ui_configs) >= 1 and len(ui_files) <= 1)
        )

        if is_partial_ui:
            reasons.append(
                f"Detected partial/starter UI presence ({len(ui_files)} UI files, "
                f"{len(component_files)} components). Not a mature design system."
            )
            return {
                "ui_state": PARTIAL_UI,
                "confidence": 0.75,
                "signals": signals,
                "reasons": reasons,
            }

        # 4. Fallback when ambiguous
        return {
            "ui_state": UNKNOWN,
            "confidence": 0.4,
            "signals": signals,
            "reasons": ["Ambiguous UI cues; cannot determine if greenfield or existing UI with high confidence."],
        }

    def _is_ui_file(self, path_str: str) -> bool:
        ext = Path(path_str).suffix.lower()
        return ext in UI_FILE_EXTENSIONS or Path(path_str).name in UI_CONFIG_FILENAMES

    def _is_component_file(self, path_str: str) -> bool:
        p = Path(path_str)
        parts = [part.lower() for part in p.parts]
        if any(marker in parts for marker in ("components", "ui", "widgets")):
            return True
        ext = p.suffix.lower()
        if ext in (".jsx", ".tsx", ".vue", ".svelte"):
            return True
        return False

    def _is_style_file(self, path_str: str) -> bool:
        ext = Path(path_str).suffix.lower()
        return ext in (".css", ".scss", ".sass", ".less", ".styl")

    def _is_page_file(self, path_str: str) -> bool:
        p = Path(path_str)
        parts = [part.lower() for part in p.parts]
        return any(marker in parts for marker in ("pages", "views", "screens", "app", "routes"))

    def _detect_ui_dependencies(self, package_json: dict[str, Any]) -> list[str]:
        if not isinstance(package_json, dict):
            return []
        deps = package_json.get("dependencies", {})
        dev_deps = package_json.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}
        known_ui_libs = (
            "react", "react-dom", "vue", "svelte", "@angular/core", "solid-js",
            "tailwindcss", "@tailwind/typography", "bootstrap", "@mui/material",
            "chakra-ui", "@chakra-ui/react", "shadcn", "lucide-react", "styled-components",
        )
        return [lib for lib in known_ui_libs if lib in all_deps]

    def _scan_directory(self, root: Path, max_depth: int = 4) -> list[str]:
        found: list[str] = []
        for dirpath, dirnames, filenames in os.walk(root):
            # Prune non-UI / bulky directories
            dirnames[:] = [d for d in dirnames if d not in NON_UI_DIRS]
            rel_dir = Path(dirpath).relative_to(root)
            if len(rel_dir.parts) > max_depth:
                continue
            for f in filenames:
                rel_file = str(rel_dir / f).replace("\\", "/")
                found.append(rel_file)
        return found


# Module-level default detector instance
_current_detector: UIStateDetector = HeuristicUIStateDetector()


def get_ui_state_detector() -> UIStateDetector:
    return _current_detector


def set_ui_state_detector(detector: UIStateDetector) -> None:
    global _current_detector
    _current_detector = detector


def detect_ui_state(repo_context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Public helper to detect UI state using active detector."""
    return get_ui_state_detector().detect(repo_context)
