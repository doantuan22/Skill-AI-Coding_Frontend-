"""Design Token Detector: Identifies token signals, CSS custom properties, theme configurations, and tokens."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot

TOKEN_FILENAME_PATTERNS = (
    "theme.", "tokens.", "colors.", "typography.", "variables.",
    "tailwind.config.", "design-tokens.", "theme.config.",
)


def detect_design_tokens(
    snapshot: RepositorySnapshot,
    styling_info: dict[str, Any],
) -> dict[str, Any]:
    files = snapshot.files

    sources: list[str] = []
    colors: list[str] = []
    typography: list[str] = []
    spacing: list[str] = []
    radius: list[str] = []
    shadows: list[str] = []
    breakpoints: list[str] = []

    # 1. Identify token and theme files
    for f in files:
        name_lower = Path(f).name.lower()
        if any(name_lower.startswith(p) for p in TOKEN_FILENAME_PATTERNS) or "tokens/" in f or "theme/" in f:
            sources.append(f)

    # 2. Extract CSS Custom Properties from stylesheets
    css_files = [f for f in files if f.endswith((".css", ".scss", ".sass", ".less"))][:10]
    for cf in css_files:
        content = snapshot.read_text(cf, max_chars=50_000)
        if "--" in content:
            if cf not in sources:
                sources.append(cf)
            # Find CSS variables: --name: value;
            vars_found = re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', content)
            for var_name, val in vars_found[:40]:
                var_clean = var_name.strip()
                val_clean = val.strip()
                v_lower = var_clean.lower()
                if any(k in v_lower for k in ("color", "bg", "text", "border", "primary", "secondary", "accent", "surface")):
                    colors.append(f"{var_clean}: {val_clean}")
                elif any(k in v_lower for k in ("font", "type", "leading", "family", "size")):
                    typography.append(f"{var_clean}: {val_clean}")
                elif any(k in v_lower for k in ("space", "spacing", "gap", "margin", "padding")):
                    spacing.append(f"{var_clean}: {val_clean}")
                elif "radius" in v_lower or "rounded" in v_lower:
                    radius.append(f"{var_clean}: {val_clean}")
                elif "shadow" in v_lower or "elevation" in v_lower:
                    shadows.append(f"{var_clean}: {val_clean}")

    # 3. Extract tokens from tailwind.config.*
    tw_configs = [f for f in files if "tailwind.config." in f]
    for tw in tw_configs:
        content = snapshot.read_text(tw, max_chars=30_000)
        if "colors" in content or "theme" in content:
            if "colors" in content:
                colors.append("tailwind.theme.colors")
            if "fontSize" in content or "fontFamily" in content:
                typography.append("tailwind.theme.typography")
            if "spacing" in content:
                spacing.append("tailwind.theme.spacing")
            if "borderRadius" in content:
                radius.append("tailwind.theme.borderRadius")
            if "boxShadow" in content:
                shadows.append("tailwind.theme.boxShadow")
            if "screens" in content:
                breakpoints.append("tailwind.theme.screens")

    # 4. Standard breakpoint fallback detection
    for cf in css_files:
        content = snapshot.read_text(cf, max_chars=30_000)
        bps = re.findall(r'@media\s*\([^\)]*min-width:\s*(\d+px)[^\)]*\)', content)
        for bp in bps:
            if bp not in breakpoints:
                breakpoints.append(bp)

    # Calculate token detection confidence
    total_tokens = len(colors) + len(typography) + len(spacing) + len(radius) + len(shadows)
    if sources and total_tokens >= 3:
        confidence = 0.92
    elif sources or total_tokens > 0:
        confidence = 0.72
    else:
        confidence = 0.0

    return {
        "sources": sorted(set(sources)),
        "colors": sorted(set(colors))[:25],
        "typography": sorted(set(typography))[:15],
        "spacing": sorted(set(spacing))[:15],
        "radius": sorted(set(radius))[:10],
        "shadows": sorted(set(shadows))[:10],
        "breakpoints": sorted(set(breakpoints))[:8],
        "confidence": confidence,
    }
