"""Framework Detector: Deterministic, evidence-first detection of frontend framework and stack.

Supported targets:
- React
- Next.js
- Vue
- Nuxt
- Svelte
- SvelteKit
- Angular
- static HTML/CSS/JS (static_html)
- Spring Boot + Thymeleaf (spring_thymeleaf)
- unknown
"""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def detect_framework(snapshot: RepositorySnapshot) -> dict[str, Any]:
    """Inspect snapshot and determine primary framework with confidence and evidence."""
    deps = snapshot.get_dependencies()
    files = snapshot.file_set

    evidence: list[str] = []
    conflicting_signals: list[str] = []
    detected_candidates: list[dict[str, Any]] = []

    # 1. Next.js
    if "next" in deps or any(f.startswith("next.config.") for f in files) or any("next.config." in f for f in files):
        score = 0.5
        ev = []
        if "next" in deps:
            score += 0.3
            ev.append(f"package.json declares 'next': {deps.get('next')}")
        if any("next.config." in f for f in files):
            score += 0.18
            ev.append("Found next.config configuration file")
        if any(f.startswith("app/") or "/app/" in f for f in files) and any(f.endswith((".tsx", ".jsx", ".js")) for f in files):
            score += 0.1
            ev.append("Detected Next.js App Router conventions")
        elif any(f.startswith("pages/") or "/pages/" in f for f in files) and any(f.endswith((".tsx", ".jsx", ".js")) for f in files):
            score += 0.1
            ev.append("Detected Next.js Pages Router conventions")
        detected_candidates.append({
            "name": "nextjs",
            "version": deps.get("next"),
            "confidence": min(score, 0.98),
            "evidence": ev,
        })

    # 2. Nuxt
    if "nuxt" in deps or "nuxt3" in deps or any("nuxt.config." in f for f in files):
        score = 0.5
        ev = []
        if "nuxt" in deps or "nuxt3" in deps:
            v = deps.get("nuxt") or deps.get("nuxt3")
            score += 0.35
            ev.append(f"package.json declares Nuxt: {v}")
        if any("nuxt.config." in f for f in files):
            score += 0.14
            ev.append("Found nuxt.config configuration file")
        detected_candidates.append({
            "name": "nuxt",
            "version": deps.get("nuxt") or deps.get("nuxt3"),
            "confidence": min(score, 0.98),
            "evidence": ev,
        })

    # 3. SvelteKit
    if "@sveltejs/kit" in deps or any("svelte.config." in f for f in files):
        score = 0.55
        ev = []
        if "@sveltejs/kit" in deps:
            score += 0.35
            ev.append(f"package.json declares '@sveltejs/kit': {deps.get('@sveltejs/kit')}")
        if any("svelte.config." in f for f in files):
            score += 0.08
            ev.append("Found svelte.config configuration file")
        detected_candidates.append({
            "name": "sveltekit",
            "version": deps.get("@sveltejs/kit"),
            "confidence": min(score, 0.98),
            "evidence": ev,
        })

    # 4. Svelte (Standalone if not SvelteKit)
    if "svelte" in deps and not any(c["name"] == "sveltekit" for c in detected_candidates):
        score = 0.5
        ev = [f"package.json declares 'svelte': {deps.get('svelte')}"]
        svelte_files = [f for f in files if f.endswith(".svelte")]
        if svelte_files:
            score += 0.4
            ev.append(f"Found {len(svelte_files)} .svelte files")
        detected_candidates.append({
            "name": "svelte",
            "version": deps.get("svelte"),
            "confidence": min(score, 0.95),
            "evidence": ev,
        })

    # 5. Angular
    if "@angular/core" in deps or "angular.json" in files:
        score = 0.5
        ev = []
        if "@angular/core" in deps:
            score += 0.35
            ev.append(f"package.json declares '@angular/core': {deps.get('@angular/core')}")
        if "angular.json" in files:
            score += 0.14
            ev.append("Found angular.json configuration file")
        detected_candidates.append({
            "name": "angular",
            "version": deps.get("@angular/core"),
            "confidence": min(score, 0.98),
            "evidence": ev,
        })

    # 6. React (if not Next.js)
    if ("react" in deps or "react-dom" in deps) and not any(c["name"] == "nextjs" for c in detected_candidates):
        score = 0.45
        ev = []
        if "react" in deps:
            score += 0.3
            ev.append(f"package.json declares 'react': {deps.get('react')}")
        jsx_files = [f for f in files if f.endswith((".jsx", ".tsx"))]
        if jsx_files:
            score += 0.2
            ev.append(f"Found {len(jsx_files)} React JSX/TSX source files")
        if any("vite.config." in f for f in files):
            score += 0.04
            ev.append("Found Vite configuration file (React+Vite)")
        detected_candidates.append({
            "name": "react",
            "version": deps.get("react"),
            "confidence": min(score, 0.96),
            "evidence": ev,
        })

    # 7. Vue (if not Nuxt)
    if "vue" in deps and not any(c["name"] == "nuxt" for c in detected_candidates):
        score = 0.45
        ev = [f"package.json declares 'vue': {deps.get('vue')}"]
        vue_files = [f for f in files if f.endswith(".vue")]
        if vue_files:
            score += 0.45
            ev.append(f"Found {len(vue_files)} .vue single-file components")
        detected_candidates.append({
            "name": "vue",
            "version": deps.get("vue"),
            "confidence": min(score, 0.96),
            "evidence": ev,
        })

    # 8. Spring Boot + Thymeleaf
    is_spring = False
    spring_ev = []
    spring_version = None
    if "pom.xml" in files:
        pom_text = snapshot.read_text("pom.xml")
        if "spring-boot" in pom_text:
            is_spring = True
            spring_ev.append("pom.xml contains spring-boot references")
            if "thymeleaf" in pom_text or "spring-boot-starter-thymeleaf" in pom_text:
                spring_ev.append("pom.xml contains spring-boot-starter-thymeleaf")
    if "build.gradle" in files or "build.gradle.kts" in files:
        gradle_text = snapshot.read_text("build.gradle") or snapshot.read_text("build.gradle.kts")
        if "org.springframework.boot" in gradle_text:
            is_spring = True
            spring_ev.append("build.gradle contains spring-boot plugin/dependencies")
            if "thymeleaf" in gradle_text:
                spring_ev.append("build.gradle contains thymeleaf dependency")

    thymeleaf_templates = [f for f in files if "templates/" in f and f.endswith(".html")]
    if is_spring and (thymeleaf_templates or any("thymeleaf" in e for e in spring_ev)):
        score = 0.85
        if thymeleaf_templates:
            score += 0.1
            spring_ev.append(f"Detected {len(thymeleaf_templates)} Thymeleaf HTML templates in templates/ directory")
        detected_candidates.append({
            "name": "spring_thymeleaf",
            "version": spring_version,
            "confidence": min(score, 0.96),
            "evidence": spring_ev,
        })

    # 9. Static HTML/CSS/JS (no framework dependencies, has html files)
    html_files = [f for f in files if f.endswith((".html", ".htm")) and not any(t in f for t in ("templates/", "node_modules/"))]
    if html_files and not detected_candidates:
        score = 0.85
        ev = [f"Found {len(html_files)} static HTML entry files without framework dependencies"]
        if any(f.endswith(".css") for f in files):
            ev.append("Found standalone CSS files")
        if any(f.endswith(".js") for f in files):
            ev.append("Found vanilla JS files")
        detected_candidates.append({
            "name": "static_html",
            "version": None,
            "confidence": min(score, 0.92),
            "evidence": ev,
        })

    # Conflict check
    if len(detected_candidates) > 1:
        # Sort by confidence descending
        detected_candidates.sort(key=lambda c: c["confidence"], reverse=True)
        winner = detected_candidates[0]
        others = detected_candidates[1:]
        # Note conflicts
        for other in others:
            conflicting_signals.append(
                f"Candidate '{other['name']}' (conf: {other['confidence']:.2f}) conflicts with selected '{winner['name']}'"
            )
        # If confidence gap is very small (< 0.1), lower winner confidence
        if winner["confidence"] - others[0]["confidence"] < 0.1:
            winner["confidence"] = max(0.5, winner["confidence"] - 0.15)
        return {
            "name": winner["name"],
            "version": winner["version"],
            "confidence": winner["confidence"],
            "evidence": winner["evidence"],
            "conflicting_signals": conflicting_signals,
        }

    if len(detected_candidates) == 1:
        winner = detected_candidates[0]
        return {
            "name": winner["name"],
            "version": winner["version"],
            "confidence": winner["confidence"],
            "evidence": winner["evidence"],
            "conflicting_signals": [],
        }

    # No candidates found
    return {
        "name": "unknown",
        "version": None,
        "confidence": 0.0,
        "evidence": ["No known framework dependencies, configuration files, or conventions detected."],
        "conflicting_signals": [],
    }
