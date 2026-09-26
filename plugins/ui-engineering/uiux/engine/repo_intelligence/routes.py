"""Route and Page Detector: Inventory of pages, routes, layouts, and templates across frameworks."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def detect_routes_and_pages(
    snapshot: RepositorySnapshot,
    framework_name: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Extract route definitions and page inventory adapted to framework conventions."""
    routes: list[dict[str, Any]] = []
    pages: list[dict[str, Any]] = []
    files = snapshot.files

    # 1. Next.js App Router (app/**/page.*)
    app_page_files = [
        f for f in files
        if re.search(r'(?:^|/)app/(?:(.+)/)?page\.(?:tsx|jsx|js)$', f)
    ]
    if app_page_files:
        for f in app_page_files:
            m = re.search(r'(?:^|/)app/(?:(.+)/)?page\.(?:tsx|jsx|js)$', f)
            sub = m.group(1) if m and m.group(1) else ""
            # Strip route groups like (marketing)
            route_parts = [p for p in sub.split("/") if p and not (p.startswith("(") and p.endswith(")"))]
            path = "/" + "/".join(route_parts)
            # Find associated layout if exists
            layout_file = f.replace("page.", "layout.")
            layout_name = layout_file if layout_file in snapshot.file_set else None

            routes.append({
                "path": path,
                "source_file": f,
                "page_component": Path(f).stem,
                "layout": layout_name,
                "confidence": 0.95,
            })
            pages.append({
                "id": f"page_{len(pages) + 1}",
                "file": f,
                "route": path,
                "type": "app_route",
            })

    # 2. Next.js Pages Router or Nuxt / Vue Pages (pages/**)
    pages_dir_files = [
        f for f in files
        if re.search(r'(?:^|/)pages/(.+)\.(?:tsx|jsx|vue|js)$', f)
        and not any(f.endswith(skip) for skip in ("_app.tsx", "_app.jsx", "_app.js", "_document.tsx", "_document.jsx"))
        and not "/api/" in f
    ]
    if pages_dir_files:
        for f in pages_dir_files:
            m = re.search(r'(?:^|/)pages/(.+)\.(?:tsx|jsx|vue|js)$', f)
            rel_route = m.group(1) if m else "index"
            if rel_route == "index":
                route_path = "/"
            elif rel_route.endswith("/index"):
                route_path = "/" + rel_route[:-6]
            else:
                route_path = "/" + rel_route

            # Replace [param] with :param
            route_path = re.sub(r'\[(\w+)\]', r':\1', route_path)

            routes.append({
                "path": route_path,
                "source_file": f,
                "page_component": Path(f).stem,
                "layout": None,
                "confidence": 0.94,
            })
            pages.append({
                "id": f"page_{len(pages) + 1}",
                "file": f,
                "route": route_path,
                "type": "pages_route",
            })

    # 3. SvelteKit (src/routes/**/+page.svelte)
    sveltekit_pages = [
        f for f in files
        if re.search(r'(?:^|/)routes/(?:(.+)/)?\+page\.svelte$', f)
    ]
    if sveltekit_pages:
        for f in sveltekit_pages:
            m = re.search(r'(?:^|/)routes/(?:(.+)/)?\+page\.svelte$', f)
            sub = m.group(1) if m and m.group(1) else ""
            route_parts = [p for p in sub.split("/") if p and not (p.startswith("(") and p.endswith(")"))]
            path = "/" + "/".join(route_parts)
            layout_file = f.replace("+page.svelte", "+layout.svelte")
            layout_name = layout_file if layout_file in snapshot.file_set else None

            routes.append({
                "path": path,
                "source_file": f,
                "page_component": "+page",
                "layout": layout_name,
                "confidence": 0.95,
            })
            pages.append({
                "id": f"page_{len(pages) + 1}",
                "file": f,
                "route": path,
                "type": "sveltekit_page",
            })

    # 4. Spring Boot / Thymeleaf (templates/**/*.html)
    thymeleaf_templates = [
        f for f in files
        if ("templates/" in f or f.startswith("templates/")) and f.endswith(".html")
    ]
    if thymeleaf_templates and framework_name == "spring_thymeleaf":
        for f in thymeleaf_templates:
            m = re.search(r'templates/(.+)\.html$', f)
            view_name = m.group(1) if m else Path(f).stem
            route_path = "/" if view_name in ("index", "home") else f"/{view_name}"
            routes.append({
                "path": route_path,
                "source_file": f,
                "page_component": view_name,
                "layout": None,
                "confidence": 0.88,
            })
            pages.append({
                "id": f"page_{len(pages) + 1}",
                "file": f,
                "route": route_path,
                "type": "thymeleaf_template",
            })

    # 5. Static HTML files (if static_html or no other routes detected)
    if not routes:
        html_files = [
            f for f in files
            if f.endswith((".html", ".htm")) and not any(d in f for d in ("templates/", "node_modules/", "dist/"))
        ]
        for f in html_files:
            stem = Path(f).stem
            route_path = "/" if stem == "index" else f"/{stem}"
            routes.append({
                "path": route_path,
                "source_file": f,
                "page_component": stem,
                "layout": None,
                "confidence": 0.90,
            })
            pages.append({
                "id": f"page_{len(pages) + 1}",
                "file": f,
                "route": route_path,
                "type": "static_html",
            })

    # 6. React Router / Client Router discovery fallback if still empty
    if not routes and framework_name in ("react", "angular", "vue"):
        router_files = [
            f for f in files
            if any(term in f.lower() for term in ("route", "app.tsx", "app.jsx", "main.tsx", "main.jsx"))
        ][:5]
        for rf in router_files:
            text = snapshot.read_text(rf)
            # Find <Route path="..." element=... /> or path: "..."
            matches = re.findall(r'path=[\'"]([^\'"]+)[\'"]|path:\s*[\'"]([^\'"]+)[\'"]', text)
            for m in matches:
                p = m[0] or m[1]
                if p and p != "*":
                    routes.append({
                        "path": p,
                        "source_file": rf,
                        "page_component": None,
                        "layout": None,
                        "confidence": 0.82,
                    })
                    pages.append({
                        "id": f"page_{len(pages) + 1}",
                        "file": rf,
                        "route": p,
                        "type": "client_route",
                    })

    # De-duplicate routes by path
    seen_paths = set()
    unique_routes: list[dict[str, Any]] = []
    for r in routes:
        if r["path"] not in seen_paths:
            seen_paths.add(r["path"])
            unique_routes.append(r)

    return unique_routes, pages
