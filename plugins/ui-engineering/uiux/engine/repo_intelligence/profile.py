"""Normalized Repository Profile Builder: Orchestrates all detectors into a single coherent profile."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from uiux.engine.repo_intelligence.components import detect_component_inventory
from uiux.engine.repo_intelligence.framework import detect_framework
from uiux.engine.repo_intelligence.routes import detect_routes_and_pages
from uiux.engine.repo_intelligence.runtime import detect_runtime_capabilities
from uiux.engine.repo_intelligence.scanner import RepositorySnapshot
from uiux.engine.repo_intelligence.styling import detect_styling
from uiux.engine.repo_intelligence.tokens import detect_design_tokens

KNOWN_UI_LIBRARIES = {
    "@radix-ui/react-slot": "Radix UI",
    "@mui/material": "Material UI",
    "@chakra-ui/react": "Chakra UI",
    "antd": "Ant Design",
    "@mantine/core": "Mantine",
    "@nextui-org/react": "NextUI",
    "semantic-ui-react": "Semantic UI",
    "shadcn": "shadcn/ui",
}

KNOWN_ICON_LIBRARIES = {
    "lucide-react": "Lucide",
    "lucide-vue-next": "Lucide",
    "@heroicons/react": "Heroicons",
    "@fortawesome/fontawesome-svg-core": "FontAwesome",
    "react-icons": "React Icons",
    "@tabler/icons-react": "Tabler Icons",
}

KNOWN_MOTION_LIBRARIES = {
    "framer-motion": "Framer Motion",
    "motion": "Motion One",
    "gsap": "GSAP",
    "animejs": "Anime.js",
    "@react-spring/web": "React Spring",
}


def build_repo_profile(snapshot: RepositorySnapshot) -> dict[str, Any]:
    deps = snapshot.get_dependencies()
    warnings: list[str] = []
    detector_failures: list[str] = []
    unsupported_signals: list[str] = []
    conflicts: list[str] = []

    # 1. Framework detection
    try:
        framework_data = detect_framework(snapshot)
    except Exception as exc:
        framework_data = {"name": "unknown", "version": None, "confidence": 0.0, "evidence": [], "conflicting_signals": []}
        detector_failures.append(f"FrameworkDetector: {exc}")

    conflicts.extend(framework_data.get("conflicting_signals", []))

    # 2. Styling detection
    try:
        styling_data = detect_styling(snapshot)
    except Exception as exc:
        styling_data = {"primary": None, "secondary": None, "detected": [], "confidence": 0.0, "evidence": []}
        detector_failures.append(f"StylingDetector: {exc}")

    # 3. Routes & Pages detection
    try:
        routes, pages = detect_routes_and_pages(snapshot, framework_data["name"])
    except Exception as exc:
        routes, pages = [], []
        detector_failures.append(f"RoutePageDetector: {exc}")

    # 4. Component Inventory
    try:
        comp_inventory = detect_component_inventory(snapshot, framework_data["name"])
    except Exception as exc:
        comp_inventory = {"shared": [], "layouts": [], "primitives": [], "page_specific": [], "library_wrappers": [], "possible_duplicates": [], "total_count": 0}
        detector_failures.append(f"ComponentDetector: {exc}")

    # 5. Design Tokens
    try:
        token_data = detect_design_tokens(snapshot, styling_data)
    except Exception as exc:
        token_data = {"sources": [], "colors": [], "typography": [], "spacing": [], "radius": [], "shadows": [], "breakpoints": [], "confidence": 0.0}
        detector_failures.append(f"TokenDetector: {exc}")

    # 6. UI / Icon / Motion Libraries
    ui_lib_name, ui_lib_version, ui_lib_conf = None, None, 0.0
    ui_lib_ev = []
    for pkg_id, display_name in KNOWN_UI_LIBRARIES.items():
        if pkg_id in deps:
            ui_lib_name = display_name
            ui_lib_version = deps.get(pkg_id)
            ui_lib_conf = 0.94
            ui_lib_ev.append(f"Found {pkg_id} in dependencies")
            break

    icon_lib_name, icon_lib_conf = None, 0.0
    for pkg_id, display_name in KNOWN_ICON_LIBRARIES.items():
        if pkg_id in deps:
            icon_lib_name = display_name
            icon_lib_conf = 0.95
            break

    motion_lib_name, motion_lib_conf = None, 0.0
    for pkg_id, display_name in KNOWN_MOTION_LIBRARIES.items():
        if pkg_id in deps:
            motion_lib_name = display_name
            motion_lib_conf = 0.95
            break

    # 7. Runtime capability detection
    try:
        runtime_data = detect_runtime_capabilities(snapshot)
    except Exception as exc:
        runtime_data = {
            "package_manager": None, "install_command": None, "dev_command": None,
            "build_command": None, "test_command": None, "lint_command": None,
            "typecheck_command": None, "browser_validation": "none",
            "playwright_available": False, "commands_source": None, "confidence": 0.0,
        }
        detector_failures.append(f"RuntimeDetector: {exc}")

    # 8. Monorepo & Multi-app Handling (Case 17)
    apps: list[dict[str, str]] = []
    if snapshot.is_monorepo:
        warnings.append("Monorepo structure detected. Inspect sub-applications individually.")
        for sub in snapshot.sub_apps:
            # Quick check framework of sub-app
            sub_root = sub["root"]
            sub_files = [f for f in snapshot.files if f.startswith(sub_root + "/")]
            sub_framework = "unknown"
            if any("next.config." in f for f in sub_files):
                sub_framework = "nextjs"
            elif any(f.endswith(".vue") for f in sub_files):
                sub_framework = "vue"
            elif any(f.endswith((".tsx", ".jsx")) for f in sub_files):
                sub_framework = "react"
            elif any(f.endswith(".svelte") for f in sub_files):
                sub_framework = "svelte"
            apps.append({"root": sub_root, "name": sub["name"], "framework": sub_framework})

    # 9. UI State Classification
    ui_files_count = len(snapshot.ui_files)
    total_files = len(snapshot.files)

    ui_state_val: str
    ui_state_conf: float
    ui_state_evidence: list[str] = []

    if total_files == 0:
        ui_state_val = "GREENFIELD"
        ui_state_conf = 0.96
        ui_state_evidence.append("Empty repository with 0 files; ready for greenfield development.")
    elif ui_files_count == 0:
        has_recognized_code = any(
            Path(f).suffix.lower() in (
                ".py", ".go", ".rs", ".java", ".c", ".cpp", ".cs", ".php",
                ".rb", ".md", ".txt", ".json", ".yaml", ".yml", ".toml",
            )
            for f in snapshot.files
        )
        if has_recognized_code and framework_data["name"] in ("unknown", "static_html") and not deps:
            ui_state_val = "GREENFIELD"
            ui_state_conf = 0.95
            ui_state_evidence.append("Active non-UI codebase detected with 0 UI components, pages, or styling.")
        else:
            ui_state_val = "UNKNOWN"
            ui_state_conf = 0.30
            ui_state_evidence.append("Insufficient evidence: repository contains ambiguous files without recognized manifests or source code.")
    elif ui_files_count in (1, 2) and comp_inventory["total_count"] <= 1 and len(pages) <= 1:
        ui_state_val = "PARTIAL_UI"
        ui_state_conf = 0.85
        ui_state_evidence.append(f"Partial UI scaffold detected: {ui_files_count} UI files, {comp_inventory['total_count']} components.")
    elif comp_inventory["total_count"] >= 2 or len(pages) >= 2 or (styling_data["confidence"] >= 0.7 and ui_files_count >= 3):
        ui_state_val = "EXISTING_UI"
        ui_state_conf = 0.95
        ui_state_evidence.append(
            f"Mature UI footprint: {comp_inventory['total_count']} components, {len(pages)} routes/pages, active {styling_data['primary']} styling."
        )
    elif framework_data["confidence"] < 0.3 and total_files > 0:
        ui_state_val = "UNKNOWN"
        ui_state_conf = 0.35
        ui_state_evidence.append("Ambiguous signals: unable to classify UI presence with high confidence.")
    else:
        ui_state_val = "EXISTING_UI"
        ui_state_conf = 0.80
        ui_state_evidence.append(f"Established UI files detected ({ui_files_count} UI files).")

    # If conflicts present, reduce confidence
    if conflicts:
        ui_state_conf = max(0.45, ui_state_conf - 0.20)
        warnings.append(f"Conflicting signals detected: {'; '.join(conflicts)}")

    # UI Density
    if ui_files_count == 0:
        density = "none"
    elif ui_files_count <= 3:
        density = "low"
    elif ui_files_count <= 25:
        density = "medium"
    else:
        density = "high"

    # Overall Confidence
    confidences = [
        framework_data["confidence"],
        styling_data["confidence"] if styling_data["primary"] else 0.5,
        ui_state_conf,
    ]
    overall_confidence = round(sum(confidences) / len(confidences), 2)

    return {
        "schema_version": 1,
        "framework": framework_data,
        "styling_system": styling_data,
        "ui_library": {
            "name": ui_lib_name,
            "version": ui_lib_version,
            "confidence": ui_lib_conf,
            "evidence": ui_lib_ev,
        },
        "icon_library": {
            "name": icon_lib_name,
            "confidence": icon_lib_conf,
        },
        "motion_library": {
            "name": motion_lib_name,
            "confidence": motion_lib_conf,
        },
        "routes": routes,
        "pages": pages,
        "components": comp_inventory,
        "design_tokens": token_data,
        "existing_ui_state": {
            "value": ui_state_val,
            "confidence": ui_state_conf,
            "evidence": ui_state_evidence,
        },
        "runtime": runtime_data,
        "repository_signals": {
            "is_monorepo": snapshot.is_monorepo,
            "apps": apps,
            "ui_density": density,
            "total_files": total_files,
            "ui_files_count": ui_files_count,
        },
        "conflicts": conflicts,
        "diagnostics": {
            "warnings": warnings,
            "detector_failures": detector_failures,
            "unsupported_signals": unsupported_signals,
        },
        "overall_confidence": overall_confidence,
    }
