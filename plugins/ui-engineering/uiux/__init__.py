"""UI/UX design skill: platform-neutral core package.

Layers (imports only flow downward; see uiux/core/layers.json):
    uiux.api / uiux.cli   Core API facade (the only surface plugin adapters use)
    uiux.tooling          validation and packaging tools
    uiux.evals            evaluation (quality analyzer, eval runner)
    uiux.engine           design engine (capability resolver, technology, retrieval, performance)
    uiux.runtime          runtime engine (capability detection, browser runner, evidence, probes)
    uiux.knowledge        knowledge layer (catalog parser, registry, query)
    uiux.core             foundation (resource discovery, configuration, registries)

Importing this package has no side effects: no subprocesses, no Playwright, no network.
"""
from __future__ import annotations

from pathlib import Path

__version__ = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
__all__ = ["__version__"]
