"""Registry utilities (internal): tool registry and architecture layer map.

Callers outside the package use ``uiux.api.list_tools`` / ``uiux.api.describe_architecture``.
"""
from __future__ import annotations

import fnmatch
import json
import re
from functools import lru_cache
from pathlib import Path

from uiux.core import resources, schema
from uiux.core.errors import RegistryError

TOOL_KEYS = ("id", "visibility", "description", "entrypoint", "cli", "input", "output", "dependencies",
             "runtime_requirements", "side_effects", "annotations")
ANNOTATIONS = {"read_only": bool, "writes_to": ("none", "target-project"), "may_start_process": bool, "deterministic": bool,
               "network_access": bool, "filesystem_read": ("package", "target-project", "browser-cache"),
               "requires_node": bool, "requires_browser": bool, "long_running": bool}
ENTRYPOINT_RE = re.compile(r"^uiux\.api:[a-z_][a-z0-9_]*$")


def load_json(path: Path, registry: str) -> dict:
    """Parse a registry file; any read or JSON problem is a REGISTRY_INVALID error naming the registry."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RegistryError(f"{registry} registry unreadable: {exc}", registry=registry) from exc
    if not isinstance(data, dict):
        raise RegistryError(f"{registry} registry must be a JSON object", registry=registry)
    return data


@lru_cache(maxsize=1)
def tools() -> dict:
    data = load_json(resources.get_tool_registry_path(), "tools")
    if not isinstance(data.get("tools"), list):
        raise RegistryError("tools registry has no 'tools' list", registry="tools")
    return data


def check_tools(data: dict | None = None) -> list[str]:
    """Structural problems of the tool registry (empty when valid). Entrypoint resolution is checked by uiux.api."""
    data = tools() if data is None else data
    errors, seen = [], set()
    for index, item in enumerate(data.get("tools", [])):
        where = f"tools[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        where = f"tool {item.get('id', index)}"
        errors += [f"{where}: missing {key}" for key in TOOL_KEYS if key not in item]
        errors += [f"{where}: unexpected key {key}" for key in sorted(set(item) - set(TOOL_KEYS))]
        if item.get("id") in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(item.get("id"))
        if not ENTRYPOINT_RE.match(str(item.get("entrypoint", ""))):
            errors.append(f"{where}: entrypoint must be uiux.api:<function>")
        if item.get("visibility") not in ("public", "internal"):
            errors.append(f"{where}: visibility must be public or internal")
        errors += [f"{where}: {problem}" for problem in schema.check_schema(item.get("input"))]
        output = item.get("output")
        if not isinstance(output, dict) or output.get("type") != "object" or not isinstance(output.get("required", []), list):
            errors.append(f"{where}: output must be an object contract with an optional required list")
        annotations = item.get("annotations")
        if not isinstance(annotations, dict) or set(annotations) != set(ANNOTATIONS):
            errors.append(f"{where}: annotations must have exactly {', '.join(ANNOTATIONS)}")
            continue
        for key, rule in ANNOTATIONS.items():
            value = annotations[key]
            if rule is bool and not isinstance(value, bool):
                errors.append(f"{where}: annotations.{key} must be boolean")
            elif isinstance(rule, tuple) and not (value in rule if isinstance(value, str) else
                                                  isinstance(value, list) and all(v in rule for v in value)):
                errors.append(f"{where}: annotations.{key} must use {', '.join(rule)}")
        if annotations["read_only"] != (annotations["writes_to"] == "none"):
            errors.append(f"{where}: read_only must be true exactly when writes_to is none")
    return errors


def tool(tool_id: str) -> dict:
    for item in tools()["tools"]:
        if item["id"] == tool_id:
            return item
    raise KeyError(f"unknown tool: {tool_id}")


@lru_cache(maxsize=1)
def capability_map() -> dict:
    data = load_json(resources.get_capability_map_path(), "capabilities")
    if not isinstance(data.get("capabilities"), dict):
        raise RegistryError("capability map has no 'capabilities' object", registry="capabilities")
    return data


def check_capability_map(data: dict | None = None, tool_data: dict | None = None, root: Path | None = None) -> list[str]:
    """Every capability maps to registered tools and existing package files (empty when valid)."""
    data = capability_map() if data is None else data
    known = {item.get("id") for item in (tools() if tool_data is None else tool_data)["tools"]}
    errors = []
    for name, entry in data.get("capabilities", {}).items():
        if not isinstance(entry, dict) or set(entry) != {"tools", "instructions"}:
            errors.append(f"capability {name}: needs exactly tools and instructions")
            continue
        errors += [f"capability {name}: unknown tool {t}" for t in entry["tools"] if t not in known]
        for path in entry["instructions"]:
            try:
                target = resources.resolve(path) if root is None else root / resources.resolve(path).relative_to(resources.get_package_root())
            except resources.ResourceError:
                target = None
            if target is None or not target.is_file():
                errors.append(f"capability {name}: instruction file {path} not found")
        if not entry["tools"] and not entry["instructions"]:
            errors.append(f"capability {name}: maps to nothing")
    return errors


@lru_cache(maxsize=1)
def layers() -> dict:
    return load_json(resources.get_layer_map_path(), "layers")


def _match(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        return path == pattern[:-3] or path.startswith(pattern[:-2])
    return fnmatch.fnmatchcase(path, pattern)


def layer_of(relative_path: str) -> dict | None:
    """First layer whose path globs match a package-relative POSIX path, or None."""
    for layer in layers()["layers"]:
        if any(_match(relative_path, pattern) for pattern in layer["paths"]):
            return layer
    return None
