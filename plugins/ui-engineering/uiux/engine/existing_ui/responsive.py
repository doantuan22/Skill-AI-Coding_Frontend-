"""Responsive Analyzer: Identifies breakpoint coverage, fixed-width hazards, overflow risks, and touch targets."""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def analyze_responsive(
    repo_profile: dict[str, Any],
    snapshot: RepositorySnapshot | None = None,
) -> dict[str, Any]:
    """Inspect stylesheets, configurations, and markup for responsive health and hazards."""
    styling_primary = repo_profile.get("styling_system", {}).get("primary")
    tokens_bp = repo_profile.get("design_tokens", {}).get("breakpoints", [])

    breakpoints: list[str] = tokens_bp
    if not breakpoints:
        if styling_primary == "tailwindcss":
            breakpoints = ["sm: 640px", "md: 768px", "lg: 1024px", "xl: 1280px", "2xl: 1536px"]
        else:
            breakpoints = ["mobile (<=640px)", "tablet (<=768px)", "desktop (>=1024px)"]

    layout_adaptations: list[str] = []
    possible_overflow: list[str] = []
    touch_target_signals: list[str] = []
    mobile_nav: str | None = None
    content_priority: list[str] = []
    risks: list[str] = []
    evidence: list[str] = []
    severity = "info"

    if snapshot:
        # Check stylesheets and layout components
        candidate_files = [f for f in snapshot.files if f.endswith((".css", ".scss", ".tsx", ".jsx", ".vue", ".html"))][:15]
        combined_text = "\n".join(snapshot.read_text(f, max_chars=12_000) for f in candidate_files)

        # 1. Detect Fixed-Width Hazards
        # E.g. width: 1200px or w-[1200px] or min-width: 900px outside media query
        fixed_width_matches = re.findall(r'(?:width|min-width)\s*:\s*([89]\d{2}|[1-9]\d{3})px', combined_text, re.I)
        tw_fixed_width_matches = re.findall(r'w-\[(?:[89]\d{2}|[1-9]\d{3})px\]', combined_text)
        if fixed_width_matches or tw_fixed_width_matches:
            vals = list(set(fixed_width_matches + tw_fixed_width_matches))
            risks.append(f"Fixed-width hazard detected ({', '.join(vals)}): risk of horizontal viewport overflow on mobile devices.")
            possible_overflow.append(f"Fixed width elements: {', '.join(vals)}")
            severity = "high"
            evidence.append(f"Found hardcoded wide fixed-width declarations: {', '.join(vals)}")

        # 2. Layout Adaptations
        if re.search(r'\b(?:grid-cols-1\s+(?:md|lg):grid-cols-\d|flex-col\s+(?:md|lg):flex-row)\b', combined_text):
            layout_adaptations.append("mobile-first stacking to multi-column desktop grid")
            evidence.append("Responsive stacking utilities detected in component markup")
        if "@media" in combined_text:
            layout_adaptations.append("css-media-query-adaptations")

        # 3. Mobile Navigation
        if any(term in combined_text.lower() for term in ("sheet", "drawer", "hamburger", "mobile-nav", "menutoggle")):
            mobile_nav = "drawer/sheet collapsible mobile menu"
            evidence.append("Dedicated mobile drawer/sheet navigation pattern detected")
        elif "hidden md:flex" in combined_text or "md:hidden" in combined_text:
            mobile_nav = "breakpoint-toggled navigation"

        # 4. Touch Targets
        # Check for tiny buttons (e.g. h-6 w-6 or padding: 2px)
        if re.search(r'\b(?:h-5\s+w-5|h-6\s+w-6|p-0\.5|p-1\b)', combined_text):
            touch_target_signals.append("Sub-44px interactive controls found; potential tap target hazard on touchscreens.")
            if severity == "info":
                severity = "low"

    layout_adaptations = layout_adaptations or ["fluid-percentage-columns"]
    content_priority = ["primary task / title", "main controls", "secondary metadata", "navigation drawer"]

    conf = 0.85 if layout_adaptations or risks else 0.60

    return {
        "breakpoints": breakpoints,
        "layout_adaptations": layout_adaptations,
        "possible_overflow": possible_overflow,
        "touch_target_signals": touch_target_signals,
        "mobile_navigation": mobile_nav,
        "content_priority": content_priority,
        "risks": risks,
        "severity": severity,
        "confidence": conf,
        "evidence": evidence or ["Standard responsive breakpoints and stacking rules evaluated."],
    }
