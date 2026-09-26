"""Resource discovery: the single place that knows where things live.

Every path is derived from the package root (the directory containing SKILL.md and the ``uiux`` package), never
from the current working directory or a machine-specific absolute path. Layout-specific locations come from the
configuration (``paths`` section), so a relocated or re-packaged tree only needs a config change.

Set ``UIUX_ROOT`` to point the code at a different package root (e.g., a vendored copy of the skill data).
"""
from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

from uiux.core.errors import UiuxError

ENV_ROOT = "UIUX_ROOT"
_PACKAGE_ROOT = Path(__file__).resolve().parents[2]


class ResourceError(UiuxError, LookupError):
    default_code = "PACKAGE_ROOT_NOT_FOUND"


def get_package_root() -> Path:
    """Root of the skill/plugin package (contains SKILL.md and VERSION)."""
    env = os.environ.get(ENV_ROOT)
    root = Path(env).resolve() if env else _PACKAGE_ROOT
    if not (root / "SKILL.md").is_file():
        raise ResourceError(f"package root {root} does not contain SKILL.md")
    return root


def _paths() -> dict:
    from uiux.core import config  # local import: config depends on get_package_root above

    return config.get()["paths"]


def resolve(relative: str) -> Path:
    """Resolve a package-relative path, refusing absolute paths and escapes outside the package root."""
    pure = PurePosixPath(relative.replace("\\", "/"))
    if pure.is_absolute() or ".." in pure.parts or ":" in relative:
        raise ResourceError(f"not a package-relative path: {relative!r}", "CONFIG_INVALID")
    return get_package_root().joinpath(*pure.parts)


def relative(path: Path) -> str:
    """Package-relative POSIX path of a file inside the package."""
    return path.resolve().relative_to(get_package_root()).as_posix()


def get_path(name: str) -> Path:
    try:
        return resolve(_paths()[name])
    except KeyError as exc:
        raise ResourceError(f"unknown configured path: {name}", "CONFIG_INVALID") from exc


def get_core_root() -> Path:
    """Core skill root: SKILL.md, workflows/, skills/, knowledge/, review/, templates/."""
    return get_package_root()


def get_skill_entry() -> Path:
    return get_path("skill_entry")


def get_plugin_root() -> Path:
    """Plugin layer location. Core code never needs it; it may not exist in a core-only distribution."""
    return get_path("plugin")


def get_knowledge_roots() -> list[Path]:
    return [resolve(p) for p in _paths()["knowledge_roots"]]


def get_knowledge_root() -> Path:
    """Primary knowledge directory (knowledge README, INDEX.md and registry.json live here)."""
    return get_path("knowledge_readme").parent


def get_knowledge_registry_path() -> Path:
    return get_path("knowledge_registry")


def get_knowledge_index_path() -> Path:
    return get_path("knowledge_index")


def get_components_root() -> Path:
    return get_path("components")


def get_runtime_root() -> Path:
    """Runtime contracts (execution/)."""
    return get_path("runtime_contracts")


def get_viewports_path() -> Path:
    return get_path("viewports")


def get_eval_root() -> Path:
    return get_path("evals")


def get_scenarios_root() -> Path:
    return get_path("scenarios")


def get_resolver_scenarios_root() -> Path:
    return get_path("resolver_scenarios")


def get_quality_fixtures_root() -> Path:
    return get_path("quality_fixtures")


def get_templates_root() -> Path:
    return get_path("templates")


def get_docs_root() -> Path:
    return get_path("docs")


def get_tool_registry_path() -> Path:
    return get_path("tool_registry")


def get_layer_map_path() -> Path:
    return get_path("layer_map")


def get_capability_map_path() -> Path:
    return get_path("capability_map")
