"""Core API: the stable, public, platform-neutral surface of the skill.

Plugin adapters and external callers use only this module (or the unified CLI ``python scripts/uiux_cli.py``). Every
function takes and returns JSON-serializable values. Implementation modules are imported lazily so importing this
module has no side effects and never touches Playwright, Node or the network.

PUBLIC                          INTERNAL (may change without notice)
resolve_capabilities            uiux.knowledge.catalog (parser, schema validation, index rendering)
retrieve_knowledge / get_*      uiux.core.registry (registry utilities)
resolve_technology              uiux.runtime.evidence / uiux.runtime.probes (evidence internals)
analyze_design_quality          uiux.tooling.validate internals, uiux.engine.retrieval
detect_runtime / run_runtime / accessibility_scan
run_evals / validate_skill
capability_map / self_test / error_contract
list_tools / call_tool / describe_architecture / layer_of / version / get_config / reload_config

Errors (uiux/core/errors.json): every error raised here is a ``ToolError`` (a ``ValueError``) or another
``UiuxError`` with ``code``, ``category``, ``remediation`` and ``envelope()``. ``call_tool`` validates parameters
against the tool's registry schema and turns any unexpected exception into ``INTERNAL_ERROR`` without exposing a
traceback (``UIUX_DEBUG=1`` prints it to stderr). Environmental limits (no Node, Playwright, browser or axe) are not
errors: runtime tools return ``BLOCKED`` results.
"""
from __future__ import annotations

import inspect
import json
import re
from pathlib import Path

from uiux import __version__
from uiux.core.errors import UiuxError

__all__ = [
    "version", "get_config", "reload_config", "list_tools", "describe_architecture", "layer_of", "call_tool",
    "resolve_capabilities", "retrieve_knowledge", "get_knowledge", "knowledge_collections", "resolve_technology",
    "analyze_design_quality", "detect_runtime", "run_runtime", "accessibility_scan", "run_evals", "validate_skill",
    "capability_map", "self_test", "error_contract", "error_envelope", "API_VERSION", "UiuxError", "ToolError",
]

API_VERSION = 1
"""Version of this public API contract (function names, parameters, result shapes, error contract). Adapters declare
the version they were written for (``adapter.json`` -> ``core_api.plugin_api_version``); a breaking change bumps it."""


class ToolError(UiuxError, ValueError):
    """Invalid tool call. ``code``/``category``/``remediation`` come from the error taxonomy (default INVALID_ARGUMENT)."""

    default_code = "INVALID_ARGUMENT"


def _tool_error(exc: BaseException) -> ToolError:
    """Keep the message of a lower-layer error and its registered code (INVALID_ARGUMENT when it has none)."""
    if isinstance(exc, UiuxError):
        return ToolError(exc.message, exc.code, exc.remediation, **exc.details)
    message = str(exc.args[0]) if isinstance(exc, KeyError) and exc.args else str(exc)
    return ToolError(message, getattr(exc, "code", None))


def version() -> str:
    return __version__


def get_config() -> dict:
    """Effective configuration (defaults + uiux.config.json + UIUX_CONFIG)."""
    from uiux.core import config

    return config.get()


def reload_config() -> dict:
    """Re-read configuration (after a host sets UIUX_CONFIG or edits uiux.config.json)."""
    from uiux.core import config

    config.reset()
    return config.get()


def list_tools() -> list[dict]:
    from uiux.core import registry

    return [dict(t) for t in registry.tools()["tools"]]


def describe_architecture() -> dict:
    """Layers, allowed imports and entry points (for adapters, docs and packaging)."""
    from uiux.core import registry, resources

    return {"version": __version__, "package_root": str(resources.get_package_root()),
            "layers": registry.layers()["layers"], "imports": registry.layers()["imports"],
            "tools": [t["id"] for t in registry.tools()["tools"]],
            "entrypoints": {"skill": resources.relative(resources.get_skill_entry()),
                            "knowledge": resources.relative(resources.get_path("knowledge_readme")),
                            "knowledge_registry": resources.relative(resources.get_knowledge_registry_path()),
                            "tool_registry": resources.relative(resources.get_tool_registry_path())}}


def layer_of(relative_path: str) -> str | None:
    """Architecture layer id for a package-relative path (None when unclassified)."""
    from uiux.core import registry

    layer = registry.layer_of(relative_path)
    return layer["id"] if layer else None


# --------------------------------------------------------------------------- engine
def resolve_capabilities(profile: dict) -> dict:
    from uiux.engine import capability_resolver

    try:
        return capability_resolver.resolve(profile)
    except capability_resolver.ProfileError as exc:
        raise _tool_error(exc) from exc


def resolve_technology(capabilities: list[str], existing_dependencies: list[str] | None = None,
                       allow_new_dependencies: bool | None = None) -> dict:
    from uiux.engine import technology

    try:
        return technology.resolve(capabilities, existing_dependencies or [], allow_new_dependencies)
    except ValueError as exc:
        raise _tool_error(exc) from exc


# --------------------------------------------------------------------------- knowledge
def knowledge_collections() -> dict:
    from uiux.knowledge import registry

    return registry.collections()


def retrieve_knowledge(collection: str | None = None, kind: str | None = None, category: str | None = None,
                       ids: list[str] | None = None, text: str | None = None, include_content: bool = False) -> dict:
    from uiux.knowledge import registry

    try:
        rows = registry.query(collection, kind, category, ids, text)
    except KeyError as exc:
        raise _tool_error(exc) from exc
    if include_content:
        rows = [{**row, "content": registry.read(row["id"])} for row in rows]
    return {"count": len(rows), "entries": rows}


def get_knowledge(ident: str) -> dict:
    """One parsed knowledge entry (catalog entries) or component grammar document."""
    from uiux.knowledge import registry

    try:
        return registry.get(ident)
    except KeyError as exc:
        raise _tool_error(exc) from exc


# --------------------------------------------------------------------------- evaluation
def analyze_design_quality(project: str, manifests: list[str] | None = None, visual_intensity: int = 3) -> dict:
    from uiux.evals import quality

    try:
        return quality.analyze(project, manifests or [], visual_intensity)
    except ValueError as exc:
        raise _tool_error(exc) from exc


def run_evals(suites: list[str] | None = None, scenario_ids: list[str] | None = None) -> dict:
    from uiux.evals import runner

    try:
        return runner.run(tuple(suites) if suites else runner.AUTOMATED_SUITES, scenario_ids)
    except ValueError as exc:
        raise _tool_error(exc) from exc


def validate_skill() -> dict:
    from uiux.tooling import validate

    errors = validate.validate()
    return {"status": "FAIL" if errors else "PASS", "errors": errors}


# --------------------------------------------------------------------------- runtime
def detect_runtime(project: str = ".", url: str | None = None, browser: str = "chromium") -> dict:
    from uiux.runtime import capabilities

    return capabilities.detect(project, url, browser)


def run_runtime(request: dict, project: str, dry_run: bool = False, allow_start: bool = False) -> dict:
    """Runtime capture. Returns {exit_code, summary}; the summary matches the runner CLI output."""
    from uiux.runtime import browser

    code, summary = browser.execute(request, Path(project), dry_run=dry_run, allow_start=allow_start)
    return {"exit_code": code, "summary": summary}


def accessibility_scan(request: dict, project: str, dry_run: bool = False) -> dict:
    """axe scan with the project's own Playwright and axe. Returns {exit_code, summary}; the summary matches the
    ``run_accessibility_scan.py`` output. Gated on runtime_state like ``run_runtime``: a runtime that cannot run gives
    ``BLOCKED`` with PLAYWRIGHT_IMPORT_FAILURE, PLAYWRIGHT_BROWSER_UNAVAILABLE, AXE_NOT_AVAILABLE or READINESS_TIMEOUT.
    Never installs, downloads or starts anything."""
    from uiux.runtime import accessibility

    code, summary = accessibility.execute(request, Path(project), dry_run=dry_run)
    return {"exit_code": code, "summary": summary}


# --------------------------------------------------------------------------- discovery and health
def error_contract() -> dict:
    """The error taxonomy (codes, categories, statuses, exit codes, remediation) that adapters map to host errors."""
    from uiux.core import errors

    return json.loads(json.dumps(errors.taxonomy()))


def error_envelope(exc: BaseException, where: str = "adapter") -> dict:
    """Error envelope for any exception (unregistered exceptions become INTERNAL_ERROR, without traceback)."""
    from uiux.core import errors

    return errors.envelope_for(exc, where)


def _runtime_gates() -> dict:
    """Runtime-dependent tool id -> gate(capability report) returning (code, message) or None."""
    from uiux.runtime import accessibility, browser

    return {"run_runtime": browser.blocking_reason, "accessibility_scan": accessibility.blocking_reason}


def capability_map(project: str | None = None) -> dict:
    """What this package can do, derived from the capability map (uiux/core/capabilities.json, referenced by the plugin
    manifest), the tool registry, the knowledge registry, the eval runner and (only when ``project`` is given) the
    read-only runtime detector. Nothing here is declared twice: kinds and availability are computed.

    A tool is ``runtime-dependent`` when its annotations require Node or a browser; a capability is runtime-dependent
    when any of its tools is. Without ``project`` runtime availability is ``UNKNOWN``: nothing is detected.
    """
    from uiux.core import config, errors, registry, resources
    from uiux.evals import runner
    from uiux.knowledge import registry as knowledge
    from uiux.runtime import capabilities as runtime

    declared = registry.capability_map()["capabilities"]
    report = runtime.detect(project) if project is not None else None
    gates = _runtime_gates()
    tools = {}
    for spec in list_tools():
        notes = spec["annotations"]
        runtime_dependent = notes["requires_node"] or notes["requires_browser"]
        entry = {"kind": "runtime-dependent" if runtime_dependent else "static", "visibility": spec["visibility"],
                 "annotations": notes, "availability": "AVAILABLE"}
        if runtime_dependent:
            blocked = gates[spec["id"]](report) if report is not None else None
            entry["availability"] = "UNKNOWN" if report is None else "BLOCKED" if blocked else "AVAILABLE"
            if blocked:
                entry.update(errors.result_annotation(blocked[0]))
        tools[spec["id"]] = entry
    capabilities = {}
    for name in sorted(declared):
        mapped = declared[name]
        runtime_tools = [t for t in mapped["tools"] if tools.get(t, {}).get("kind") == "runtime-dependent"]
        states = {tools[t]["availability"] for t in runtime_tools}
        item = {"kind": "runtime-dependent" if runtime_tools else "static", "tools": list(mapped["tools"]),
                "instructions": list(mapped["instructions"]),
                "availability": "BLOCKED" if "BLOCKED" in states else "UNKNOWN" if "UNKNOWN" in states else "AVAILABLE"}
        blocked_by = {t: tools[t]["error_code"] for t in runtime_tools if "error_code" in tools[t]}
        if blocked_by:
            item["blocked_by"] = blocked_by
        capabilities[name] = item
    runtime_section = {"optional": True, "states": list(runtime.RUNTIME_STATES),
                       "features": {name: bool(value) for name, value in sorted(config.get()["feature_flags"].items())},
                       "requirements": {t["id"]: t["runtime_requirements"] for t in list_tools() if t["runtime_requirements"]},
                       "project": None}
    if report is not None:
        runtime_section["project"] = {"path": report["detector"]["project"],
                                      "runtime_state": report["playwright"]["runtime_state"]["state"],
                                      "node": report["runtime"]["node"]["status"],
                                      "accessibility_strategy": report["accessibility"]["strategy"]}
    counts = knowledge.collections()
    return {"version": __version__,
            "sources": {"capabilities": resources.relative(resources.get_capability_map_path()),
                        "tools": resources.relative(resources.get_tool_registry_path()),
                        "knowledge": resources.relative(resources.get_knowledge_registry_path()),
                        "errors": "uiux/core/errors.json"},
            "capabilities": capabilities, "tools": tools,
            "knowledge": {"collections": counts, "entries": sum(counts.values())},
            "evals": {"automated": list(runner.AUTOMATED_SUITES), "all": list(runner.ALL_SUITES)},
            "runtime": runtime_section}


def _run_check(check_id: str, run) -> dict:
    """One self-test check; an exception becomes FAIL with its code (INTERNAL_ERROR when unregistered)."""
    from uiux.core import errors

    try:
        status, message, *code = run()
        item = {"id": check_id, "status": status, "message": message}
        if code and code[0]:
            item["error_code"] = code[0]
        return item
    except Exception as exc:  # noqa: BLE001 - a self-test reports, it never raises
        failure = exc if isinstance(exc, UiuxError) else errors.internal(exc, f"self_test.{check_id}")
        return {"id": check_id, "status": "FAIL", "message": failure.message, "error_code": failure.code}


def self_test() -> dict:
    """Fast health check. Nothing is installed, downloaded, written or started, except the ``node --version`` probe
    of runtime detection. A missing optional runtime is BLOCKED, never FAIL. When the optional plugin layer is
    packaged alongside the core, its manifest is parsed and checked for version/capability agreement; a core-only
    distribution reports that check as SKIPPED and remains fully usable."""
    from uiux.core import errors, registry, resources
    from uiux.knowledge import registry as knowledge
    from uiux.runtime import capabilities as runtime

    root = resources.get_package_root()

    def version_check():
        found = {"VERSION": (root / "VERSION").read_text(encoding="utf-8").strip(), "uiux.__version__": __version__}
        if len(set(found.values())) != 1:
            return "FAIL", "versions differ: " + ", ".join(f"{k}={v}" for k, v in found.items()), "VERSION_MISMATCH"
        changelog = root / "CHANGELOG.md"
        if changelog.is_file() and not re.search(rf"^## {re.escape(__version__)}(\s|$)",
                                                 changelog.read_text(encoding="utf-8"), re.M):
            return "FAIL", f"CHANGELOG.md has no section for {__version__}", "VERSION_MISMATCH"
        return "PASS", f"{__version__} ({', '.join(found)})"

    def manifest_check():
        """The core has no dependency on plugin/, but a complete plugin package must have a coherent manifest."""
        plugin_root = resources.get_plugin_root()
        if not plugin_root.is_dir():
            return "SKIPPED", "plugin layer is not present (core-only distribution)"
        path = plugin_root / "manifest" / "plugin.json"
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return "FAIL", f"plugin manifest unreadable: {exc}", "MANIFEST_INVALID"
        required = {"manifest_version", "name", "version", "entrypoints", "capabilities", "tools"}
        missing = sorted(required - set(manifest)) if isinstance(manifest, dict) else sorted(required)
        if missing or manifest.get("manifest_version") != 1:
            return "FAIL", f"plugin manifest missing/invalid fields: {', '.join(missing) or 'manifest_version'}", "MANIFEST_INVALID"
        if manifest["version"] != __version__:
            return "FAIL", f"manifest version {manifest['version']} != core {__version__}", "VERSION_MISMATCH"
        if sorted(manifest["capabilities"]) != sorted(registry.capability_map()["capabilities"]):
            return "FAIL", "manifest capabilities differ from the capability map", "MANIFEST_INVALID"
        return "PASS", f"{manifest['name']} manifest parsed (version {manifest['version']})"

    def tools_check():
        problems = registry.check_tools() + registry.check_capability_map()
        if problems:
            return "FAIL", "; ".join(problems[:5]), "REGISTRY_INVALID"
        return "PASS", f"{len(registry.tools()['tools'])} tools, {len(registry.capability_map()['capabilities'])} capabilities"

    def api_check():
        problems = []
        for spec in registry.tools()["tools"]:
            function = _DISPATCH.get(spec["id"])
            if function is None or f"uiux.api:{function.__name__}" != spec["entrypoint"] or function.__name__ not in __all__:
                problems.append(f"{spec['id']}: {spec['entrypoint']} is not a public uiux.api function")
            elif set(inspect.signature(function).parameters) != set(spec["input"]["properties"]):
                problems.append(f"{spec['id']}: function parameters differ from the input schema")
        problems += [f"uiux.api.{name} is not callable" for name in __all__ if name != "API_VERSION" and not callable(globals().get(name))]
        return ("FAIL", "; ".join(problems), "REGISTRY_INVALID") if problems else ("PASS", f"{len(__all__)} public functions")

    def knowledge_check():
        counts = knowledge.collections()
        if sorted(counts) != sorted(knowledge.COLLECTIONS):
            return "FAIL", f"collections {sorted(counts)} != {sorted(knowledge.COLLECTIONS)}", "REGISTRY_INVALID"
        entries = len(knowledge.query())
        if not entries or entries != sum(counts.values()):
            return "FAIL", f"{entries} entries but collection counts sum to {sum(counts.values())}", "REGISTRY_INVALID"
        return "PASS", f"{entries} entries in {len(counts)} collections"

    def capability_check():
        data = capability_map()
        missing = [f for c in data["capabilities"].values() for f in c["instructions"] if not (root / f).is_file()]
        unknown = [t for c in data["capabilities"].values() for t in c["tools"] if t not in data["tools"]]
        if missing or unknown:
            return "FAIL", f"missing instructions {missing}; unknown tools {unknown}", "REGISTRY_INVALID"
        return "PASS", f"{len(data['capabilities'])} capabilities, {len(data['tools'])} tools"

    def error_contract_check():
        data = errors.taxonomy()
        orphans = [code for code, entry in data["codes"].items() if entry["category"] not in data["categories"]]
        if orphans:
            return "FAIL", f"codes with unknown category: {orphans}", "REGISTRY_INVALID"
        probes = (("UNKNOWN_TOOL", "__self_test_unknown_tool__", {}),
                  ("INVALID_ARGUMENT_TYPE", "retrieve_knowledge", {"ids": "style.swiss"}))
        for expected, tool_id, params in probes:
            try:
                call_tool(tool_id, params)
            except UiuxError as exc:
                if exc.code != expected or not exc.envelope()["remediation"]:
                    return "FAIL", f"{tool_id} gave {exc.code}, expected {expected}", "INTERNAL_ERROR"
                continue
            return "FAIL", f"{tool_id} call was not rejected", "INTERNAL_ERROR"
        return "PASS", f"error_contract_version {data['error_contract_version']}, {len(data['codes'])} codes"

    def runtime_check():
        state = runtime.detect(root)["playwright"]["runtime_state"]["state"]
        if state not in runtime.RUNTIME_STATES:
            return "FAIL", f"unknown runtime state {state!r}", "INTERNAL_ERROR"
        return "PASS", f"read-only detector operational (package root runtime_state {state})"

    def optional_runtime_check():
        node = runtime.command_version("node")
        if node["status"] != "AVAILABLE":
            return ("BLOCKED", "Node.js not found: run_runtime and accessibility_scan return BLOCKED; nothing is installed",
                    "PLAYWRIGHT_IMPORT_FAILURE")
        return "PASS", "Node.js available; Playwright readiness is per target project (detect_runtime, capability_map)"

    checks = [_run_check(check_id, run) for check_id, run in (
        ("version", version_check), ("manifest", manifest_check), ("tool_registry", tools_check),
        ("public_api", api_check), ("knowledge_registry", knowledge_check), ("capability_map", capability_check),
        ("error_contract", error_contract_check), ("runtime_detection", runtime_check),
        ("optional_runtime", optional_runtime_check))]
    return {"status": "FAIL" if any(c["status"] == "FAIL" for c in checks) else "PASS", "version": __version__,
            "checks": checks}


# --------------------------------------------------------------------------- dispatch
_DISPATCH = {
    "resolve_capabilities": resolve_capabilities, "retrieve_knowledge": retrieve_knowledge,
    "resolve_technology": resolve_technology, "analyze_design_quality": analyze_design_quality,
    "detect_runtime": detect_runtime, "run_runtime": run_runtime, "accessibility_scan": accessibility_scan,
    "run_evals": run_evals, "validate_skill": validate_skill, "capability_map": capability_map, "self_test": self_test,
}


def _call(tool_id: str, params: object) -> dict:
    from uiux.core import registry, schema
    from uiux.core.errors import RegistryError

    try:
        spec = registry.tool(tool_id)
    except KeyError as exc:
        raise ToolError(str(exc.args[0]), "UNKNOWN_TOOL", tool=tool_id) from exc
    params = schema.validate_arguments(tool_id, spec["input"], {} if params is None else params)
    function = _DISPATCH.get(spec["id"])
    if function is None or f"uiux.api:{function.__name__}" != spec["entrypoint"]:
        raise RegistryError(f"{tool_id}: entrypoint {spec['entrypoint']} is not dispatchable", registry="tools")
    try:
        inspect.signature(function).bind(**params)
    except TypeError as exc:
        raise RegistryError(f"{tool_id}: input schema does not match {spec['entrypoint']}: {exc}", registry="tools") from exc
    return function(**params)


def call_tool(tool_id: str, params: dict | None = None) -> dict:
    """Invoke a registered tool by id with a JSON object of parameters.

    Raises only ``ToolError`` (a ``UiuxError`` and ``ValueError``) for bad calls, broken registries/configuration and
    OS errors (``FILESYSTEM_ERROR``), or ``InternalError`` (``INTERNAL_ERROR``, message without traceback) for anything
    unexpected. BLOCKED and FAIL results are returned, not raised.
    """
    from uiux.core import errors

    try:
        return _call(tool_id, params)
    except ToolError:
        raise
    except UiuxError as exc:
        if exc.code == "INTERNAL_ERROR":
            raise
        raise _tool_error(exc) from exc
    except OSError as exc:
        raise ToolError(f"{tool_id}: {exc}", "FILESYSTEM_ERROR", tool=tool_id) from exc
    except Exception as exc:  # noqa: BLE001 - the public boundary never leaks a raw exception
        raise errors.internal(exc, tool_id) from None
