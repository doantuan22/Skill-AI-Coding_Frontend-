"""Scope Resolver: Determines the exact, minimal scope of a modification request.

Prevents scope creep:
- Component task ("Fix Button spacing") -> component scope.
- Section task ("Fix mobile navbar") -> section / component scope.
- Page task ("Improve checkout flow") -> page scope.
- Global redesign ("Rebuild entire site") -> global scope (requires L3 permission).
- Monorepo multi-app target resolution.
"""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.preservation import is_vague_enhancement

VALID_SCOPES = (
    "global",
    "application",
    "page",
    "section",
    "component",
    "token",
    "local",
)


def resolve_scope(
    user_goal: str,
    requested_scope: str = "global",
    task_intent: str = "general_ui",
    repo_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve and normalize the modification scope.
    
    Returns:
    {
        "scope": str,
        "is_unbounded": bool,
        "application_target": str | None,
        "target_entity": str | None,
        "is_insufficient_context": bool,
        "reasons": list[str],
    }
    """
    reasons: list[str] = []
    goal_lower = (user_goal or "").lower().strip()
    active_profile = repo_profile or {}

    # 1. Monorepo application scoping
    applications = active_profile.get("applications", {})
    application_target: str | None = None
    is_insufficient_context = False

    if applications and isinstance(applications, dict):
        app_names = list(applications.keys())
        if requested_scope in app_names:
            application_target = requested_scope
            reasons.append(f"Explicit application scope '{requested_scope}' selected.")
        else:
            # Check if user goal mentions an application
            matched_apps = [name for name in app_names if re.search(r'\b' + re.escape(name) + r'\b', goal_lower)]
            if len(matched_apps) == 1:
                application_target = matched_apps[0]
                reasons.append(f"Inferred application target '{application_target}' from user request.")
            elif len(matched_apps) > 1:
                is_insufficient_context = True
                reasons.append(f"Ambiguous target: request mentions multiple apps ({', '.join(matched_apps)}).")
            else:
                # If requested scope is generic "global" but repo has multiple apps without clear target
                if requested_scope == "global" and len(app_names) > 1 and not any(k in goal_lower for k in ("toàn bộ", "all apps", "entire monorepo")):
                    is_insufficient_context = True
                    reasons.append(f"Repository contains {len(app_names)} applications ({', '.join(app_names)}). Target application must be specified.")

    # 2. Scope classification based on user goal and task intent
    # Component-level keywords
    component_pattern = r'\b(button|card|modal|dialog|navbar|header|footer|sidebar|input|dropdown|select|badge|table|avatar|tabs?|accordion|drawer)\b'
    comp_match = re.search(component_pattern, goal_lower)

    # Token/Design system keywords
    token_pattern = r'\b(token|spacing|color|palette|font|typography|radius|theme|shadow)\b'
    token_match = re.search(token_pattern, goal_lower)

    # Page-level keywords
    page_pattern = r'\b(page|checkout|cart|login|register|dashboard|pricing|landing|profile|settings|home)\b'
    page_match = re.search(page_pattern, goal_lower)

    # Global redesign patterns
    global_pattern = r'\b(entire|all\s+pages|whole\s+site|toàn\s+bộ|tất\s+cả|system-wide|full\s+redesign)\b'
    global_match = re.search(global_pattern, goal_lower)

    resolved_scope = requested_scope

    # If requested_scope was passed as generic "global", refine it based on goal
    if requested_scope == "global":
        if global_match and not comp_match:
            resolved_scope = "global"
            reasons.append("Global scope requested for full product redesign.")
        elif page_match and not comp_match:
            resolved_scope = "page"
            reasons.append(f"Narrowed scope to 'page' based on entity mention '{page_match.group(1)}'.")
        elif comp_match:
            if comp_match.group(1) in ("navbar", "header", "footer", "sidebar"):
                resolved_scope = "section"
                reasons.append(f"Narrowed scope to 'section' for structural component '{comp_match.group(1)}'.")
            else:
                resolved_scope = "component"
                reasons.append(f"Narrowed scope to 'component' for '{comp_match.group(1)}'.")
        elif token_match and any(w in goal_lower for w in ("standardize", "đồng bộ", "tokens", "scale")):
            resolved_scope = "token"
            reasons.append("Token / Design system scope identified.")
        elif task_intent in ("component_refactor", "visual_polish", "consistency_fix"):
            resolved_scope = "component"
            reasons.append("Narrowed scope to 'component' matching task intent.")
        elif task_intent in ("page_redesign", "form_ux"):
            resolved_scope = "page"
            reasons.append("Narrowed scope to 'page' matching task intent.")
        elif task_intent == "responsive_fix":
            resolved_scope = "section"
            reasons.append("Responsive fix scoped to affected sections.")
        else:
            resolved_scope = "component"
            reasons.append("Defaulted to safe minimal 'component' scope.")
    elif requested_scope not in VALID_SCOPES and requested_scope != application_target:
        resolved_scope = "component"
        reasons.append(f"Unrecognized scope '{requested_scope}', defaulted to 'component'.")

    # Anti-creep check: Vague enhancement words must NEVER widen scope
    if is_vague_enhancement(user_goal) and resolved_scope == "global":
        resolved_scope = "page"
        reasons.append("Vague enhancement request ('modernize'/'clean up') suppressed from widening to global scope.")

    target_entity: str | None = None
    if comp_match:
        target_entity = comp_match.group(1)
    elif page_match:
        target_entity = page_match.group(1)

    return {
        "scope": resolved_scope,
        "is_unbounded": resolved_scope == "global" and bool(global_match),
        "application_target": application_target,
        "target_entity": target_entity,
        "is_insufficient_context": is_insufficient_context,
        "reasons": reasons,
    }
