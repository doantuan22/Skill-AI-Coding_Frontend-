"""Knowledge Router package: Entry points for context-efficient, framework-aware knowledge routing.

Provides deterministic routing from repository profile, existing UI analysis,
and task intent into a machine-readable Knowledge Load Plan.
"""
from __future__ import annotations

from typing import Any

from uiux.engine.knowledge_router.metadata import (
    DESIGN_SKILLS,
    FRAMEWORK_PACKS,
    PRESERVATION_PACKS,
    RUNTIME_VALIDATION_PACKS,
    STYLING_PACKS,
)
from uiux.engine.knowledge_router.resolver import KnowledgeResolver
from uiux.engine.knowledge_router.router import KnowledgeRouter

_ROUTER_INSTANCE: KnowledgeRouter | None = None


def _get_router() -> KnowledgeRouter:
    global _ROUTER_INSTANCE
    if _ROUTER_INSTANCE is None:
        _ROUTER_INSTANCE = KnowledgeRouter()
    return _ROUTER_INSTANCE


def route_knowledge(request: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    """Route required knowledge packs, skills, preservation invariants, and runtime validation.
    
    Accepts a single dictionary `request` or keyword arguments matching KnowledgeRequest.
    """
    req = dict(request or {})
    req.update(kwargs)
    return _get_router().route(req)


def build_knowledge_plan(
    repo_profile: dict[str, Any] | None = None,
    existing_ui_profile: dict[str, Any] | None = None,
    preservation_profile: dict[str, Any] | None = None,
    task_intent: str | None = None,
    user_request: str = "",
    workflow: str = "existing-ui",
    requested_scope: str = "global",
    explicit_constraints: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a comprehensive machine-readable Knowledge Load Plan."""
    req = {
        "repo_profile": repo_profile or {},
        "existing_ui_profile": existing_ui_profile,
        "preservation_profile": preservation_profile,
        "task_intent": task_intent,
        "user_request": user_request,
        "workflow": workflow,
        "requested_scope": requested_scope,
        "explicit_constraints": explicit_constraints or {},
    }
    return _get_router().route(req)


def resolve_framework_pack(framework_name: str, version: str | None = None) -> dict[str, Any] | None:
    """Resolve a specific framework pack by framework identifier."""
    pack_id = f"framework.{framework_name.lower().strip()}"
    pack = FRAMEWORK_PACKS.get(pack_id)
    if pack:
        res = dict(pack)
        if version:
            res["version"] = str(version)
        return res
    return None


def resolve_styling_pack(styling_name: str) -> dict[str, Any] | None:
    """Resolve a specific styling or UI library pack by system identifier."""
    name_clean = styling_name.lower().strip()
    if f"styling.{name_clean}" in STYLING_PACKS:
        return dict(STYLING_PACKS[f"styling.{name_clean}"])
    if f"ui_library.{name_clean}" in STYLING_PACKS:
        return dict(STYLING_PACKS[f"ui_library.{name_clean}"])
    return None


def resolve_domain_pack(domain_name: str) -> dict[str, Any] | None:
    """Resolve a specific domain pack by domain identifier or alias."""
    from uiux.engine.knowledge_router.domain_registry import resolve_domain_pack as _resolve
    return _resolve(domain_name)


def detect_domain(
    user_request: str = "",
    repo_profile: dict[str, Any] | None = None,
    explicit_domain: str | None = None,
    requested_scope: str = "global",
) -> dict[str, Any]:
    """Detect and classify project domain with evidence and confidence."""
    from uiux.engine.knowledge_router.domain_classifier import classify_domain
    return classify_domain(
        user_request=user_request,
        repo_profile=repo_profile,
        explicit_domain=explicit_domain,
        requested_scope=requested_scope,
    )


def get_pack_registry() -> dict[str, Any]:
    """Return all registered packs across categories."""
    from uiux.engine.knowledge_router.domain_registry import DOMAIN_PACKS

    return {
        "frameworks": dict(FRAMEWORK_PACKS),
        "styling": dict(STYLING_PACKS),
        "domains": dict(DOMAIN_PACKS),
        "preservation": dict(PRESERVATION_PACKS),
        "runtime_validation": dict(RUNTIME_VALIDATION_PACKS),
        "skills": dict(DESIGN_SKILLS),
    }


__all__ = [
    "route_knowledge",
    "build_knowledge_plan",
    "resolve_framework_pack",
    "resolve_styling_pack",
    "resolve_domain_pack",
    "detect_domain",
    "get_pack_registry",
    "KnowledgeRouter",
    "KnowledgeResolver",
]
