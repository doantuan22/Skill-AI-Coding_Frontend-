"""Knowledge Resolver: Bridges Knowledge Router with the existing Design Knowledge Registry and resources.

Flow:
Knowledge Router -> knowledge IDs -> Existing Knowledge Registry -> Resolver -> actual resource paths.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from uiux.core import resources
from uiux.core.errors import RegistryError
from uiux.engine.knowledge_router.metadata import (
    DESIGN_SKILLS,
    FRAMEWORK_PACKS,
    PRESERVATION_PACKS,
    RUNTIME_VALIDATION_PACKS,
    STYLING_PACKS,
)
from uiux.knowledge import registry


class KnowledgeResolver:
    """Resolves knowledge IDs to resource paths and metadata."""

    def __init__(self) -> None:
        self._pack_registry: dict[str, dict[str, Any]] = {}
        self._pack_registry.update(FRAMEWORK_PACKS)
        self._pack_registry.update(STYLING_PACKS)
        self._pack_registry.update(PRESERVATION_PACKS)
        self._pack_registry.update(RUNTIME_VALIDATION_PACKS)
        self._pack_registry.update(DESIGN_SKILLS)

    def get_pack(self, pack_id: str) -> dict[str, Any] | None:
        """Lookup a pack or skill by ID from the internal pack registry."""
        return self._pack_registry.get(pack_id)

    def get_all_packs(self) -> dict[str, dict[str, Any]]:
        """Return the complete dictionary of registered packs."""
        return dict(self._pack_registry)

    def resolve_source_path(self, pack_or_id: str | dict[str, Any]) -> Path | None:
        """Resolve the absolute filesystem path for a pack source."""
        if isinstance(pack_or_id, str):
            pack = self.get_pack(pack_or_id)
            source = pack.get("source") if pack else None
        else:
            source = pack_or_id.get("source")

        if not source:
            return None

        try:
            return resources.resolve(source)
        except resources.ResourceError:
            return None

    def query_catalog(
        self,
        collection: str | None = None,
        ids: list[str] | None = None,
        text: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query entries from the 261-entry design knowledge registry."""
        try:
            return registry.query(collection=collection, ids=ids, text=text)
        except Exception:
            return []

    def locate_catalog_entry(self, entry_id: str) -> dict[str, Any] | None:
        """Locate a single entry in the design knowledge registry."""
        try:
            return registry.locate(entry_id)
        except Exception:
            return None
