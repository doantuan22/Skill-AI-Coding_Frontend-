"""Configuration layer.

Resolution order (later wins): packaged defaults (uiux/core/defaults.json) → optional ``uiux.config.json`` at the
package root → file named by the ``UIUX_CONFIG`` environment variable → explicit overrides passed by a caller
(e.g., a plugin adapter). Every path value is relative to the package root; absolute paths and ``..`` escapes are
rejected so the package stays relocatable. Automatic dependency installation cannot be enabled.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path, PurePosixPath

from uiux.core import resources
from uiux.core.errors import UiuxError

DEFAULTS_PATH = Path(__file__).with_name("defaults.json")
LOCAL_CONFIG_NAME = "uiux.config.json"
ENV_CONFIG = "UIUX_CONFIG"
_cache: dict | None = None


class ConfigError(UiuxError, ValueError):
    default_code = "CONFIG_INVALID"


def _merge(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _check_relative(name: str, value: object) -> None:
    values = value if isinstance(value, list) else [value]
    for item in values:
        if not isinstance(item, str) or not item:
            raise ConfigError(f"paths.{name} must be a non-empty relative path")
        pure = PurePosixPath(item.replace("\\", "/"))
        if pure.is_absolute() or ":" in item or ".." in pure.parts:
            raise ConfigError(f"paths.{name} must be relative to the package root without '..': {item!r}")


def validate(config: dict) -> dict:
    if config.get("schema_version") != 1:
        raise ConfigError("config schema_version must be 1")
    for name, value in config.get("paths", {}).items():
        _check_relative(name, value)
    if config.get("dependency_policy", {}).get("auto_install") is not False:
        raise ConfigError("dependency_policy.auto_install must be false: the skill never installs packages or browsers",
                          "CONFIG_UNSUPPORTED")
    for flag, value in config.get("feature_flags", {}).items():
        if not isinstance(value, bool):
            raise ConfigError(f"feature_flags.{flag} must be boolean")
    budget = config.get("performance_budget", {}).get("effect_budget_by_visual_intensity", {})
    if sorted(budget) != ["1", "2", "3", "4", "5"] or not all(isinstance(v, int) and v >= 0 for v in budget.values()):
        raise ConfigError("performance_budget.effect_budget_by_visual_intensity needs integer budgets for 1..5")
    for key, value in config.get("motion_budget", {}).items():
        if not isinstance(value, int) or value < 0:
            raise ConfigError(f"motion_budget.{key} must be a non-negative integer")
    return config


def _read(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read config {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"config {path.name} must be a JSON object")
    return data


def load(overrides: dict | None = None) -> dict:
    """Return the effective configuration (defaults + local file + UIUX_CONFIG + overrides)."""
    config = _read(DEFAULTS_PATH)
    local = resources.get_package_root() / LOCAL_CONFIG_NAME
    if local.is_file():
        config = _merge(config, _read(local))
    env = os.environ.get(ENV_CONFIG)
    if env:
        config = _merge(config, _read(Path(env)))
    if overrides:
        config = _merge(config, overrides)
    return validate(config)


def get() -> dict:
    """Cached effective configuration without caller overrides."""
    global _cache
    if _cache is None:
        _cache = load()
    return _cache


def reset() -> None:
    """Drop the cache (tests, or after changing UIUX_CONFIG)."""
    global _cache
    _cache = None
