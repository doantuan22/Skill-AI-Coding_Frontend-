# Thin Adapter Contract & Specification

This document defines the architectural contract governing how platform-specific adapters interface with the shared UI Engineering Plugin core.

---

## 1. Architectural Invariant

**ONE SHARED CORE, MULTIPLE THIN ADAPTERS.**

All business logic, design intelligence, planning engines, preservation invariants, knowledge catalogs, and runtime criticism reside exclusively in the shared core (`plugins/ui-engineering/`).

An adapter must NEVER:
- Duplicate or copy skill markdown files (`skills/`).
- Duplicate or copy knowledge catalogs (`knowledge/`).
- Duplicate or copy runtime execution engines (`uiux/`).
- Implement independent reasoning or planning logic.
- Hard-code machine-specific or developer absolute paths.

---

## 2. Adapter Responsibilities

An adapter is strictly responsible for:
1. **Platform Discovery**: Providing platform-specific manifest files (e.g. `adapter.json`, `templates/mcp.json`, `templates/claude-plugin.json`).
2. **Environment & Root Resolution**: Resolving the plugin root path relative to the adapter or through standard environment variables (`UIUX_ROOT`).
3. **Transport Glue**: Routing platform tool invocations to the shared public API (`uiux.api` or `scripts/uiux_cli.py`).
4. **Capability Translation**: Exposing tools and command entry points in the schema expected by the host platform.
5. **Clean Error Propagation**: Wrapping internal failures in structured, platform-safe error envelopes.

---

## 3. Directory Structure for Adapters

```
plugins/ui-engineering/
├── adapters/
│   ├── CONTRACT.md
│   ├── README.md
│   ├── common/               # Shared transport utilities
│   ├── generic/              # Generic CLI/Python adapter
│   └── mcp/                  # Stdio-based MCP server adapter
├── .claude-plugin/           # Claude Code thin adapter
│   ├── adapter.json
│   ├── export.py
│   └── templates/
└── .codex-plugin/            # OpenAI Codex thin adapter
    ├── adapter.json
    ├── export.py
    └── templates/
```

---

## 4. Path Portability Rules

1. Use POSIX-style relative paths in manifests and configs.
2. Resolve paths dynamically at runtime using `__file__` or `os.environ.get("UIUX_ROOT")`.
3. Support paths containing spaces on Windows and POSIX systems.
4. Support the `--params "@file.json"` pattern to bypass shell escaping limitations.

---

## 5. Adding New Platform Adapters (Phase 9 Readiness)

When adding support for new platforms in future phases:
1. Create a dedicated adapter directory under `adapters/<platform>/` or `.<platform>-plugin/`.
2. Define the platform manifest adhering to `schemas/adapter.schema.json`.
3. Implement transport glue that delegates directly to `uiux.api.call_tool()`.
4. Ensure the verifier passes with zero duplicated core files.
