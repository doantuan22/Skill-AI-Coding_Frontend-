"""Component Inventory Detector: Categorizes components into shared, layouts, primitives, and wrappers."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot

PRIMITIVE_NAMES = {
    "button", "input", "modal", "dialog", "badge", "avatar", "card",
    "dropdown", "select", "checkbox", "radio", "tooltip", "spinner",
    "toast", "accordion", "table", "tag", "popover", "switch",
}

LAYOUT_NAMES = {
    "header", "footer", "sidebar", "nav", "navbar", "navigation",
    "layout", "applayout", "shell", "container", "topbar",
}


def detect_component_inventory(
    snapshot: RepositorySnapshot,
    framework_name: str,
) -> dict[str, Any]:
    files = snapshot.files

    # Filter candidate component files
    comp_files: list[str] = []
    for f in files:
        ext = Path(f).suffix.lower()
        if ext in (".jsx", ".tsx", ".vue", ".svelte"):
            # Exclude tests, configs, stories
            if any(term in f.lower() for term in (".test.", ".spec.", ".stories.", "setup", "config")):
                continue
            comp_files.append(f)

    shared: list[str] = []
    layouts: list[str] = []
    primitives: list[str] = []
    page_specific: list[str] = []
    library_wrappers: list[str] = []
    duplicates: list[str] = []

    seen_names: dict[str, list[str]] = {}

    for f in comp_files:
        stem = Path(f).stem
        name_lower = stem.lower()
        parts = [p.lower() for p in Path(f).parts]

        seen_names.setdefault(name_lower, []).append(f)

        # 1. Layouts
        if any(ln in name_lower for ln in LAYOUT_NAMES) or "layouts" in parts:
            layouts.append(f)
        # 2. Primitives
        elif name_lower in PRIMITIVE_NAMES or any(name_lower.startswith(pn) or name_lower.endswith(pn) for pn in PRIMITIVE_NAMES):
            primitives.append(f)
        # 3. Page-specific
        elif any(p in parts for p in ("pages", "views", "screens", "routes", "app")):
            page_specific.append(f)
        # 4. Shared
        elif any(p in parts for p in ("components", "ui", "common", "shared", "widgets")):
            shared.append(f)
        else:
            shared.append(f)

        # 5. Check for library wrappers (sampling up to 40 components)
        if len(library_wrappers) < 15:
            text = snapshot.read_text(f, max_chars=10_000)
            if any(lib in text for lib in ("@radix-ui", "@mui", "@chakra-ui", "antd", "lucide-react", "react-aria")):
                library_wrappers.append(f)

    # Detect possible duplicates (same component name in multiple paths)
    for name, occurrences in seen_names.items():
        if len(occurrences) > 1 and name not in ("index", "page", "layout"):
            duplicates.extend(occurrences)

    return {
        "shared": sorted(shared),
        "layouts": sorted(layouts),
        "primitives": sorted(primitives),
        "page_specific": sorted(page_specific),
        "library_wrappers": sorted(library_wrappers),
        "possible_duplicates": sorted(set(duplicates)),
        "total_count": len(comp_files),
    }
