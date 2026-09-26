"""Layout Analyzer: Analyzes global vs local structure, container patterns, grid/flex systems, and rhythm."""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def analyze_layout(
    repo_profile: dict[str, Any],
    snapshot: RepositorySnapshot | None = None,
) -> dict[str, Any]:
    """Examine codebase for global page shell, container conventions, and local composition patterns."""
    components = repo_profile.get("components", {})
    layouts = components.get("layouts", [])
    routes = repo_profile.get("routes", [])

    evidence: list[str] = []

    # 1. Global Structure identification
    app_shell: str | None = None
    header: str | None = None
    sidebar: str | None = None
    footer: str | None = None
    main_container: str | None = None

    for comp in layouts:
        name_lower = comp.lower()
        if "shell" in name_lower or "applayout" in name_lower or "rootlayout" in name_lower:
            app_shell = comp
            evidence.append(f"Identified global app shell layout: {comp}")
        elif "header" in name_lower or "topbar" in name_lower:
            header = comp
            evidence.append(f"Identified global header: {comp}")
        elif "sidebar" in name_lower or "aside" in name_lower:
            sidebar = comp
            evidence.append(f"Identified global sidebar navigation: {comp}")
        elif "footer" in name_lower:
            footer = comp
            evidence.append(f"Identified global footer: {comp}")

    # Inspect routes for layout declarations
    for r in routes:
        layout_file = r.get("layout")
        if layout_file and not app_shell:
            app_shell = layout_file
            evidence.append(f"Route '{r['path']}' declares layout: {layout_file}")

    # 2. Container and Grid Patterns
    container_patterns: list[str] = []
    grid_patterns: list[str] = []
    card_patterns: list[str] = []
    form_patterns: list[str] = []
    section_patterns: list[str] = []

    if snapshot:
        # Sample top layout and page files
        sample_files = [*layouts[:5], *[p["file"] for p in repo_profile.get("pages", [])[:5]]]
        combined_markup = "\n".join(snapshot.read_text(f, max_chars=15_000) for f in sample_files if f)

        # Check for max-width and container classes
        for cw in ("max-w-7xl", "max-w-6xl", "max-w-5xl", "max-w-4xl", "max-w-screen-xl", "container"):
            if cw in combined_markup:
                container_patterns.append(cw)
        if "mx-auto" in combined_markup:
            container_patterns.append("mx-auto (centered)")

        # Grid patterns
        if "grid-cols-" in combined_markup:
            m_grid = re.findall(r'grid-cols-\d+', combined_markup)
            grid_patterns.extend(list(set(m_grid)))
        if "display: grid" in combined_markup or "grid-template-columns" in combined_markup:
            grid_patterns.append("css-grid")
        if "display: flex" in combined_markup or "flex-col" in combined_markup or "flex-row" in combined_markup:
            grid_patterns.append("flexbox-stack")

        # Local patterns
        if any(term in combined_markup for term in ("card", "rounded-lg border", "shadow-sm")):
            card_patterns.append("standard-card-surface")
        if any(term in combined_markup for term in ("form", "space-y-4", "flex flex-col gap-4")):
            form_patterns.append("vertical-stacked-form")
        if any(term in combined_markup for term in ("section", "py-12", "py-16", "py-24")):
            section_patterns.append("padded-vertical-sections")

    container_patterns = container_patterns or ["standard-responsive-container"]
    grid_patterns = grid_patterns or ["flexbox-layout"]
    card_patterns = card_patterns or ["component-surface"]
    form_patterns = form_patterns or ["standard-form-grouping"]
    section_patterns = section_patterns or ["hierarchical-sections"]

    # 3. Spacing rhythm
    spacing_tokens = repo_profile.get("design_tokens", {}).get("spacing", [])
    spacing_rhythm = "8px base rhythm (4/8/16/24/32px)" if any("8" in s or "4" in s for s in spacing_tokens) else "standard-4px-grid"

    # 4. Navigation structure
    nav_type = "sidebar" if sidebar else ("top-navbar" if header else "header-navigation")
    nav_placement = "left" if sidebar else "top"
    nav_items = [r["path"] for r in routes[:6]] if routes else ["/"]

    conf = 0.70
    if app_shell or header or sidebar:
        conf += 0.20
    if len(routes) >= 2:
        conf += 0.05

    return {
        "container_patterns": container_patterns,
        "grid_patterns": grid_patterns,
        "spacing_rhythm": spacing_rhythm,
        "section_hierarchy": ["header/nav", "main content canvas", "supplementary/sidebar", "footer"],
        "navigation_structure": {
            "type": nav_type,
            "placement": nav_placement,
            "items": nav_items,
        },
        "responsive_breakpoints": ["sm (640px)", "md (768px)", "lg (1024px)", "xl (1280px)"],
        "global_structure": {
            "app_shell": app_shell,
            "header": header,
            "sidebar": sidebar,
            "footer": footer,
            "main_container": main_container or (container_patterns[0] if container_patterns else None),
        },
        "local_structure": {
            "card_patterns": card_patterns,
            "form_patterns": form_patterns,
            "section_patterns": section_patterns,
        },
        "confidence": round(min(conf, 0.96), 2),
        "evidence": evidence or ["Standard layout conventions inferred from project structure."],
    }
