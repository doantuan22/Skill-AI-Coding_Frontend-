"""Styling Detector: Evidence-backed detection of styling systems with multi-system support.

Supported systems:
- plain_css
- css_modules
- sass_scss
- tailwindcss
- bootstrap
- styled_components
- emotion
- mui
- shadcn_ui
- other css_in_js
- unknown

Ensures that declared packages without source usage signals are penalized in confidence (Case 8).
"""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def detect_styling(snapshot: RepositorySnapshot) -> dict[str, Any]:
    deps = snapshot.get_dependencies()
    files = snapshot.file_set
    all_files = snapshot.files

    systems: dict[str, dict[str, Any]] = {}

    # Sample source contents for usage verification (bounded to 20 files)
    sample_files = [
        f for f in all_files
        if f.endswith((".jsx", ".tsx", ".vue", ".svelte", ".html", ".css", ".scss"))
    ][:25]

    sample_texts = [snapshot.read_text(f, max_chars=40_000) for f in sample_files]
    combined_samples = "\n".join(sample_texts)

    # 1. Tailwind CSS
    has_tw_dep = "tailwindcss" in deps or "@tailwindcss/typography" in deps
    has_tw_config = any("tailwind.config." in f for f in files)
    has_tw_directives = "@tailwind" in combined_samples or "tailwind" in combined_samples
    has_tw_utility_classes = bool(re.search(r'\b(?:flex|grid|p-\d|m-\d|text-\w+-\d+|bg-\w+-\d+|rounded-\w+)\b', combined_samples))

    if has_tw_dep or has_tw_config or has_tw_directives:
        score = 0.5
        ev = []
        if has_tw_dep:
            score += 0.25
            ev.append(f"package.json declares tailwindcss: {deps.get('tailwindcss')}")
        if has_tw_config:
            score += 0.2
            ev.append("Found tailwind.config.* configuration file")
        if has_tw_directives:
            score += 0.1
            ev.append("Found @tailwind directives in stylesheets")
        if has_tw_utility_classes:
            score += 0.05
            ev.append("Found Tailwind utility classes in component markup")
        systems["tailwindcss"] = {"confidence": min(score, 0.98), "evidence": ev}

    # 2. CSS Modules (*.module.css, *.module.scss)
    module_files = [f for f in files if re.search(r'\.module\.(?:css|scss|sass|less)$', f, re.I)]
    if module_files:
        score = min(0.75 + (0.05 * len(module_files)), 0.96)
        systems["css_modules"] = {
            "confidence": score,
            "evidence": [f"Found {len(module_files)} CSS Module files (e.g. {module_files[0]})"],
        }

    # 3. Sass / SCSS
    has_sass_dep = "sass" in deps or "node-sass" in deps
    sass_files = [f for f in files if f.endswith((".scss", ".sass"))]
    if has_sass_dep or sass_files:
        score = 0.5
        ev = []
        if has_sass_dep:
            score += 0.25
            ev.append(f"package.json declares sass dependency: {deps.get('sass') or deps.get('node-sass')}")
        if sass_files:
            score += 0.25
            ev.append(f"Found {len(sass_files)} Sass/SCSS files")
        systems["sass_scss"] = {"confidence": min(score, 0.95), "evidence": ev}

    # 4. Bootstrap
    has_bootstrap_dep = "bootstrap" in deps or "react-bootstrap" in deps or "bootstrap-vue" in deps
    has_bootstrap_usage = bool(re.search(
        r'\b(?:container|row|col-\d+|btn-primary|btn-secondary|card-body|navbar-brand|alert-danger)\b',
        combined_samples,
    )) or "bootstrap" in combined_samples.lower()

    if has_bootstrap_dep:
        if has_bootstrap_usage:
            systems["bootstrap"] = {
                "confidence": 0.92,
                "evidence": [
                    f"package.json declares bootstrap: {deps.get('bootstrap') or deps.get('react-bootstrap')}",
                    "Found Bootstrap classes or imports in components/markup",
                ],
            }
        else:
            # Case 8: Dependency present but NO usage in code -> low confidence & clear note
            systems["bootstrap"] = {
                "confidence": 0.35,
                "evidence": [
                    f"WARNING: package.json declares bootstrap ({deps.get('bootstrap') or deps.get('react-bootstrap')}) but no active usage signals detected in source code or stylesheets",
                ],
            }
    elif has_bootstrap_usage and any(f.endswith(".html") for f in files):
        # Static HTML with CDN link
        if "bootstrap" in combined_samples:
            systems["bootstrap"] = {
                "confidence": 0.85,
                "evidence": ["Detected Bootstrap CDN link or classes in HTML"],
            }

    # 5. styled-components
    if "styled-components" in deps or "import styled" in combined_samples:
        has_usage = "styled." in combined_samples or "styled(" in combined_samples
        score = 0.95 if has_usage else 0.45
        ev = [f"styled-components in package: {deps.get('styled-components')}"]
        if has_usage:
            ev.append("Found styled.div/styled() component definitions in source files")
        else:
            ev.append("WARNING: No styled component definitions detected in source samples")
        systems["styled_components"] = {"confidence": score, "evidence": ev}

    # 6. Emotion
    if "@emotion/react" in deps or "@emotion/styled" in deps:
        has_usage = "@emotion" in combined_samples or "css=" in combined_samples
        score = 0.95 if has_usage else 0.45
        ev = ["@emotion declared in dependencies"]
        if has_usage:
            ev.append("Found Emotion css prop or styled definitions in source code")
        systems["emotion"] = {"confidence": score, "evidence": ev}

    # 7. Material UI (MUI)
    if "@mui/material" in deps or "@material-ui/core" in deps:
        has_usage = "@mui" in combined_samples or "Material" in combined_samples
        score = 0.95 if has_usage else 0.45
        ev = ["MUI package declared in dependencies"]
        if has_usage:
            ev.append("Found @mui component imports in source files")
        systems["mui"] = {"confidence": score, "evidence": ev}

    # 8. shadcn/ui
    has_shadcn_components = any(f.startswith("components/ui/") or "/components/ui/" in f for f in files)
    has_components_json = "components.json" in files
    if has_components_json or has_shadcn_components:
        score = 0.7
        ev = []
        if has_components_json:
            score += 0.2
            ev.append("Found components.json (shadcn/ui configuration)")
        if has_shadcn_components:
            score += 0.1
            ev.append("Found components/ui directory with primitive components")
        systems["shadcn_ui"] = {"confidence": min(score, 0.96), "evidence": ev}

    # 9. Plain CSS
    plain_css_files = [
        f for f in files
        if f.endswith(".css") and not f.endswith(".module.css")
    ]
    if plain_css_files:
        score = min(0.65 + (0.05 * len(plain_css_files)), 0.95)
        systems["plain_css"] = {
            "confidence": score,
            "evidence": [f"Found {len(plain_css_files)} standalone CSS stylesheets"],
        }

    # Multi-system ranking
    if not systems:
        return {
            "primary": None,
            "secondary": None,
            "detected": [],
            "confidence": 0.0,
            "evidence": ["No known styling system, stylesheets, or configuration detected."],
        }

    # Sort systems by confidence descending
    sorted_systems = sorted(systems.items(), key=lambda item: item[1]["confidence"], reverse=True)
    primary_name, primary_data = sorted_systems[0]
    secondary_name = sorted_systems[1][0] if len(sorted_systems) > 1 and sorted_systems[1][1]["confidence"] >= 0.5 else None

    all_evidence: list[str] = []
    for name, data in sorted_systems:
        all_evidence.extend([f"[{name}] {e}" for e in data["evidence"]])

    return {
        "primary": primary_name,
        "secondary": secondary_name,
        "detected": [name for name, _ in sorted_systems],
        "confidence": primary_data["confidence"],
        "evidence": all_evidence,
    }
