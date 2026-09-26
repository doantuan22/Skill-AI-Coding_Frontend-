"""Visual Identity Analyzer: Extracts color palette, typography, elevation, radius, and visual language."""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def analyze_visual_identity(
    repo_profile: dict[str, Any],
    snapshot: RepositorySnapshot | None = None,
) -> dict[str, Any]:
    """Extract code-level visual identity facts, palette, typography, and density with evidence."""
    tokens = repo_profile.get("design_tokens", {})
    token_colors = tokens.get("colors", [])
    token_typo = tokens.get("typography", [])
    token_spacing = tokens.get("spacing", [])
    token_radius = tokens.get("radius", [])
    token_shadows = tokens.get("shadows", [])

    evidence: list[str] = []
    conflicts: list[str] = []

    # 1. Colors Extraction
    primary: str | None = None
    secondary: str | None = None
    accent: str | None = None
    neutral: list[str] = []
    background: str | None = None
    surface: str | None = None
    text_color: str | None = None
    semantic: dict[str, str | None] = {"success": None, "warning": None, "error": None, "info": None}

    def _clean_val(s: str) -> str:
        if ":" in s:
            _, val = s.split(":", 1)
            return val.strip().rstrip(";")
        return s.strip().rstrip(";")

    # Inspect token strings
    primary_candidates: list[str] = []
    for c in token_colors:
        c_clean = c.strip()
        c_lower = c_clean.lower()
        val = _clean_val(c_clean)
        if "primary" in c_lower:
            primary_candidates.append(val)
        elif "secondary" in c_lower:
            secondary = val
            evidence.append(f"Detected secondary color token: {val}")
        elif "accent" in c_lower:
            accent = val
            evidence.append(f"Detected accent color token: {val}")
        elif any(k in c_lower for k in ("bg", "background")):
            background = val
        elif any(k in c_lower for k in ("surface", "card")):
            surface = val
        elif any(k in c_lower for k in ("text", "foreground")):
            text_color = val
        elif any(k in c_lower for k in ("gray", "slate", "zinc", "neutral", "muted")):
            neutral.append(val)
        elif "success" in c_lower or "green" in c_lower:
            semantic["success"] = val
        elif "warning" in c_lower or "amber" in c_lower or "yellow" in c_lower:
            semantic["warning"] = val
        elif "error" in c_lower or "danger" in c_lower or "destructive" in c_lower or "red" in c_lower:
            semantic["error"] = val
        elif "info" in c_lower or "cyan" in c_lower:
            semantic["info"] = val

    # Inspect files directly if snapshot available and primary still unknown or to verify hex
    if snapshot:
        # Check stylesheets and config samples for concrete values
        style_files = [f for f in snapshot.files if f.endswith((".css", ".scss", ".ts", ".js")) and any(k in f.lower() for k in ("token", "theme", "global", "variable", "tailwind"))][:5]
        for sf in style_files:
            content = snapshot.read_text(sf, max_chars=20_000)
            # Find definitions like --color-primary: #... or primary: '#...'
            matches = re.findall(r'(?:--color-primary|--primary|primary)\s*[:=]\s*[\'"]?([#a-zA-Z0-9(),.\s]+)[\'"]?;?', content, re.IGNORECASE)
            for m in matches:
                val = m.strip().rstrip(";").strip("\"'")
                if val.startswith("#") or val.startswith("rgb") or val.startswith("hsl"):
                    primary_candidates.append(val)
                    evidence.append(f"Found primary color value '{val}' in {sf}")

    # Check for primary candidates conflict
    distinct_primaries = list(dict.fromkeys(primary_candidates))
    if len(distinct_primaries) > 1:
        # Verify if they are actually different hex/hsl values
        hex_values = [p for p in distinct_primaries if p.startswith("#")]
        if len(set(hex_values)) > 1:
            conflicts.append(f"Conflicting primary color definitions detected: {', '.join(distinct_primaries)}")
            primary = distinct_primaries[0]
            evidence.append(f"Multiple primary colors found; using first detected '{primary}' but confidence penalized")
        else:
            primary = distinct_primaries[0]
            evidence.append(f"Resolved primary color: {primary}")
    elif distinct_primaries:
        primary = distinct_primaries[0]
        evidence.append(f"Resolved primary color: {primary}")

    # 2. Typography Extraction
    font_base: str | None = None
    font_heading: str | None = None
    font_mono: str | None = None
    scale: list[str] = []
    weights: list[str] = []

    for t in token_typo:
        t_lower = t.lower()
        if "mono" in t_lower or "code" in t_lower:
            font_mono = t
        elif "heading" in t_lower or "display" in t_lower or "title" in t_lower:
            font_heading = t
        elif "sans" in t_lower or "base" in t_lower or "body" in t_lower or "font" in t_lower:
            font_base = t
        elif any(sz in t_lower for sz in ("text-", "font-size", "size-")):
            scale.append(t)

    if snapshot:
        # Check for font family declarations
        for f in [f for f in snapshot.files if f.endswith((".css", ".html"))][:5]:
            txt = snapshot.read_text(f, max_chars=10_000)
            m_font = re.search(r'font-family\s*:\s*([^;}{]+);', txt, re.IGNORECASE)
            if m_font and not font_base:
                font_base = m_font.group(1).strip()
                evidence.append(f"Found font-family declaration in {f}: {font_base}")
                break

    # Standard scale if detected tokens or Tailwind
    if repo_profile.get("styling_system", {}).get("primary") == "tailwindcss":
        scale = scale or ["xs", "sm", "base", "lg", "xl", "2xl", "3xl"]
        weights = weights or ["400", "500", "600", "700"]
    else:
        weights = weights or ["400", "600"]

    # 3. Radius & Shadows
    radius_scale = token_radius or (["sm", "md", "lg", "full"] if repo_profile.get("styling_system", {}).get("primary") == "tailwindcss" else ["4px", "8px"])
    default_radius = radius_scale[1] if len(radius_scale) > 1 else (radius_scale[0] if radius_scale else None)

    shadow_scale = token_shadows or (["sm", "md", "lg"] if repo_profile.get("styling_system", {}).get("primary") == "tailwindcss" else [])

    # 4. Density
    comp_count = repo_profile.get("components", {}).get("total_count", 0)
    density: str = "normal"
    if any("compact" in s.lower() or "dense" in s.lower() for s in token_spacing):
        density = "compact"
    elif any("loose" in s.lower() or "spacious" in s.lower() for s in token_spacing):
        density = "spacious"
    elif comp_count > 15:
        density = "compact"

    # 5. Visual Language
    styling_primary = repo_profile.get("styling_system", {}).get("primary") or "plain_css"
    ui_lib = repo_profile.get("ui_library", {}).get("name")
    visual_lang = "card-based modern interface"
    if ui_lib == "shadcn/ui":
        visual_lang = "minimalist accessible component architecture"
    elif styling_primary == "tailwindcss":
        visual_lang = "utility-driven modular design"
    elif "bootstrap" in styling_primary:
        visual_lang = "classic grid and container structure"

    # Confidence calculation
    conf = 0.5
    if primary:
        conf += 0.25
    if font_base:
        conf += 0.15
    if token_colors or token_typo:
        conf += 0.1
    if conflicts:
        conf = max(0.40, conf - 0.25)
        evidence.append(f"Visual identity confidence reduced due to conflicts: {'; '.join(conflicts)}")

    return {
        "colors": {
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
            "neutral": neutral,
            "background": background,
            "surface": surface,
            "text": text_color,
            "semantic": semantic,
        },
        "typography": {
            "font_family_base": font_base,
            "font_family_heading": font_heading,
            "font_family_mono": font_mono,
            "scale": scale,
            "weights": weights,
        },
        "radius": {
            "default": default_radius,
            "scale": radius_scale,
        },
        "shadows": {
            "scale": shadow_scale,
        },
        "density": density,
        "visual_language": visual_lang,
        "confidence": round(min(conf, 0.98), 2),
        "evidence": evidence or ["Basic visual identity derived from framework and styling conventions."],
    }
