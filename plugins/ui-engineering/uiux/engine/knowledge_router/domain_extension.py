"""Phase 5 Domain Intelligence implementation.

Exports domain pack resolution and metadata retrieval functions.
Seamlessly replaces the Phase 4 extension stub with real domain pack implementations.
"""
from __future__ import annotations

from typing import Any

from uiux.engine.knowledge_router.domain_classifier import (
    DOMAINS,
    classify_domain,
)
from uiux.engine.knowledge_router.domain_registry import (
    DOMAIN_PACKS,
    get_domain_pack,
    list_domain_packs,
    query_domain_subtopics,
    resolve_domain_pack,
)

get_domain_pack_metadata = get_domain_pack

__all__ = [
    "DOMAINS",
    "DOMAIN_PACKS",
    "classify_domain",
    "get_domain_pack",
    "get_domain_pack_metadata",
    "list_domain_packs",
    "resolve_domain_pack",
    "query_domain_subtopics",
]
