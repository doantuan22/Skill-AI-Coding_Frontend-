# Platform Compatibility Matrix

This document tracks verified integration statuses across AI coding hosts and execution environments.

---

## 1. Supported Platform Matrix

| Platform / Host | Adapter Path | Integration Status | Supported Transports | Known Limitations |
| :--- | :--- | :---: | :---: | :--- |
| **Claude Code** | `.claude-plugin/` | **SUPPORTED** | CLI, Stdio MCP | Requires Node.js if project runs frontend build scripts. |
| **OpenAI Codex** | `.codex-plugin/` | **SUPPORTED** | CLI, File Params | Headless browser execution optional per target project. |
| **Generic CLI / Python** | `adapters/generic/` | **SUPPORTED** | Direct CLI, Subprocess | None. Full API surface exposed. |
| **Model Context Protocol (MCP)** | `adapters/mcp/` | **SUPPORTED** | Stdio JSON-RPC 2.0 | Read-only tool execution unless repair is invoked. |

---

## 2. Status Definitions

- **SUPPORTED**: Manifests verified, adapter integration verified, test suite passes, and public tools parity validated.
- **SUPPORTED_WITH_LIMITATIONS**: Supported with known external runtime requirements (e.g. Playwright browser binaries).
- **EXPERIMENTAL**: Initial scaffolding present but not qualified for production distribution.
- **BLOCKED**: Blocked by host platform limitation or missing environment dependency.
- **UNSUPPORTED**: Platform not within scope of Phase 8 distribution.

---

## 3. Tool Parity Guarantee

All supported adapters expose the identical set of 24 public tools declared in `uiux/core/tools.json`:
- `resolve_capabilities`, `retrieve_knowledge`, `resolve_technology`, `analyze_design_quality`
- `detect_runtime`, `run_browser_execution`, `run_accessibility_scan`, `validate_runtime_evidence`
- `validate_accessibility_evidence`, `get_knowledge`, `list_knowledge_collections`, `search_knowledge`
- `validate_skill`, `self_test`, `orchestrate_ui`, `analyze_repository`, `analyze_existing_ui`
- `build_knowledge_plan`, `plan_modification`, `build_validation_handoff`, `run_runtime_validation`
- `build_critic_report`, `run_targeted_repair`, `recapture_evidence`

No adapter omits any tool unless explicitly marked with an architectural justification.
