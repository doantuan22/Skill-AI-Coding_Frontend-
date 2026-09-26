"""Surface Resolver: Identifies affected files, components, tokens, and routes.

Determines the concrete blast radius boundary:
- Allowed files vs Protected files
- Shared components vs Local components
- Route & Token surfaces
"""
from __future__ import annotations

import os
from typing import Any


def resolve_surface(
    user_goal: str,
    scope_info: dict[str, Any],
    repo_profile: dict[str, Any] | None = None,
    existing_ui_profile: dict[str, Any] | None = None,
    preservation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve the concrete surface of affected files, components, tokens, and routes.
    
    Returns:
    {
        "files": list[str],
        "pages": list[str],
        "components": list[str],
        "tokens": list[str],
        "routes": list[str],
        "is_shared_component": bool,
        "shared_component_usage_count": int,
        "allowed_files": list[str],
        "allowed_components": list[str],
        "protected_files": list[str],
        "protected_routes": list[str],
        "protected_tokens": list[str],
    }
    """
    active_repo = repo_profile or {}
    active_ui = existing_ui_profile or {}
    active_pres = preservation_profile or {}

    app_target = scope_info.get("application_target")
    if app_target and "applications" in active_repo and app_target in active_repo["applications"]:
        active_repo = active_repo["applications"][app_target].get("repo_profile", active_repo)

    target_entity = (scope_info.get("target_entity") or "").lower()
    scope = scope_info.get("scope", "component")

    # 1. Discover components
    repo_components = active_repo.get("components", [])
    matched_components: list[dict[str, Any]] = []
    
    for comp in repo_components:
        c_name = comp.get("name", "") if isinstance(comp, dict) else str(comp)
        if target_entity and target_entity in c_name.lower():
            matched_components.append(comp if isinstance(comp, dict) else {"name": c_name})

    # If no specific component matched, but entity exists, create synthesized record
    if not matched_components and target_entity:
        matched_components.append({"name": target_entity.capitalize(), "path": f"src/components/{target_entity.capitalize()}.tsx"})

    # Evaluate shared component status
    is_shared = False
    usage_count = 1
    if matched_components:
        first_comp = matched_components[0]
        # Check usage in existing UI profile or repo
        usage_count = first_comp.get("usage_count", 1)
        if usage_count > 1 or scope in ("token", "global") or "shared" in first_comp.get("path", "").lower():
            is_shared = True

    # 2. Discover routes & pages
    repo_routes = active_repo.get("routes", [])
    repo_pages = active_repo.get("pages", [])
    
    affected_routes: list[str] = []
    affected_pages: list[str] = []

    for r in repo_routes:
        r_path = r.get("path", "") if isinstance(r, dict) else str(r)
        if target_entity and target_entity in r_path.lower():
            affected_routes.append(r_path)
            affected_pages.append(r_path)

    for p in repo_pages:
        p_name = p.get("name", "") if isinstance(p, dict) else str(p)
        if target_entity and target_entity in p_name.lower():
            if p_name not in affected_pages:
                affected_pages.append(p_name)

    if not affected_pages and scope == "page" and target_entity:
        affected_pages.append(f"/{target_entity}")
        affected_routes.append(f"/{target_entity}")

    # 3. Discover files
    affected_files: list[str] = []
    for comp in matched_components:
        c_path = comp.get("path")
        if c_path and c_path not in affected_files:
            affected_files.append(c_path)
        elif not c_path:
            c_name = comp.get("name", "Component")
            affected_files.append(f"src/components/{c_name}.tsx")

    if not affected_files and target_entity:
        affected_files.append(f"src/components/{target_entity.capitalize()}.tsx")

    # 4. Discover tokens
    affected_tokens: list[str] = []
    repo_tokens = active_repo.get("design_tokens", {})
    if scope == "token" or "spacing" in user_goal.lower():
        affected_tokens.extend(["--spacing-xs", "--spacing-sm", "--spacing-md", "--spacing-lg"])
    if "color" in user_goal.lower() or "palette" in user_goal.lower():
        affected_tokens.extend(["--color-primary", "--color-secondary", "--color-background"])

    # 5. Boundaries (Allowed vs Protected)
    allowed_files = list(affected_files)
    allowed_components = [c.get("name", target_entity.capitalize()) for c in matched_components] if matched_components else ([target_entity.capitalize()] if target_entity else [])

    protected_files: list[str] = []
    protected_routes = [r.get("path", "") if isinstance(r, dict) else str(r) for r in repo_routes if r not in affected_routes]
    protected_tokens: list[str] = []

    # Preservation rules for protected files & tokens
    palette_locked = active_pres.get("granular_permissions", {}).get("palette") == "locked" or active_pres.get("protected_invariants", {}).get("palette_locked", True)
    if palette_locked:
        protected_files.extend(["src/theme.ts", "src/styles/theme.css", "tailwind.config.js"])
        protected_tokens.extend(["--color-primary", "--color-brand", "primaryColor"])

    nav_protected = active_pres.get("granular_permissions", {}).get("navigation") == "protected"
    if nav_protected:
        protected_files.extend(["src/router.tsx", "src/routes.ts", "src/navigation.tsx"])

    # Clean duplicates while preserving order
    def _dedupe(items: list[str]) -> list[str]:
        return list(dict.fromkeys([i for i in items if i]))

    return {
        "files": _dedupe(affected_files),
        "pages": _dedupe(affected_pages),
        "components": _dedupe(allowed_components),
        "tokens": _dedupe(affected_tokens),
        "routes": _dedupe(affected_routes),
        "is_shared_component": is_shared,
        "shared_component_usage_count": usage_count,
        "allowed_files": _dedupe(allowed_files),
        "allowed_components": _dedupe(allowed_components),
        "protected_files": _dedupe(protected_files),
        "protected_routes": _dedupe(protected_routes),
        "protected_tokens": _dedupe(protected_tokens),
    }
