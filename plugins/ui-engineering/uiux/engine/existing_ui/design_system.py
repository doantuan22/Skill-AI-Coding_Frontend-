"""Design System Extractor: Synthesizes design tokens and component conventions into a normalized design system representation."""
from __future__ import annotations

from typing import Any


def extract_design_system(
    repo_profile: dict[str, Any],
    identity_data: dict[str, Any],
    component_data: dict[str, Any],
) -> dict[str, Any]:
    """Compile token sources, scales, and component conventions into a formal design system view."""
    raw_tokens = repo_profile.get("design_tokens", {})
    sources = raw_tokens.get("sources", [])
    colors_info = identity_data.get("colors", {})
    typo_info = identity_data.get("typography", {})
    radius_info = identity_data.get("radius", {})
    shadows_info = identity_data.get("shadows", {})

    evidence: list[str] = []

    # 1. Classify Design System Maturity
    # Mature: formal tokens defined in files + high component consistency + high confidence
    # Partial: some styling system or Tailwind active without centralized token files
    # Fragmented: multiple conflicting tokens, ad-hoc styles, or duplicate primitives
    # Unknown: 0 token sources, no formal styling system
    maturity: str
    conf = raw_tokens.get("confidence", 0.0)

    if not sources and conf == 0.0 and repo_profile.get("styling_system", {}).get("confidence", 0.0) < 0.4:
        maturity = "unknown"
        evidence.append("No design system token files or recognized styling conventions found.")
    elif component_data.get("consistency") == "inconsistent" or len(component_data.get("anomalies", [])) >= 3:
        maturity = "fragmented"
        evidence.append("Fragmented styling: multiple inconsistent component patterns and token variations detected.")
    elif sources and conf >= 0.75 and component_data.get("consistency") in ("high", "moderate"):
        maturity = "mature"
        evidence.append(f"Mature design system detected across {len(sources)} token source files.")
    else:
        maturity = "partial"
        evidence.append("Partial design system footprint: active styling conventions present without complete centralized token architecture.")

    return {
        "tokens": {
            "sources": sources,
            "colors": colors_info,
            "typography": typo_info,
            "radius": radius_info,
            "shadows": shadows_info,
        },
        "component_conventions": {
            "canonical_primitives": component_data.get("canonical_patterns", {}),
            "variants": component_data.get("variants", {}),
        },
        "typography_scale": typo_info.get("scale", []),
        "spacing_scale": raw_tokens.get("spacing", []),
        "radius_scale": radius_info.get("scale", []),
        "semantic_colors": colors_info.get("semantic", {}),
        "maturity": maturity,
        "confidence": round(max(0.30, min(conf + 0.1, 0.98)), 2),
        "evidence": evidence,
    }
