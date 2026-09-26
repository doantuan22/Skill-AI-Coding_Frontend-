# Plugin schemas

| Schema | Describes | Produced by | Checked by |
|---|---|---|---|
| [package-manifest.schema.json](package-manifest.schema.json) | `PACKAGE-MANIFEST.json`, embedded in every artifact and published next to it: identity, provenance and per-file sha256 | `plugin/packaging/build.py` | `plugin/packaging/verify.py` (V1) |
| [build-info.schema.json](build-info.schema.json) | `<artifact>.build-info.json`: the build environment record (outside the archive, not in `SHA256SUMS`) | `build.py` | tests |
| [adapter.schema.json](adapter.schema.json) | Host-neutral adapter metadata, including the MCP protocol pin/method list when an adapter exposes `mcp-stdio` | adapter metadata | V10 / tests |
| [orchestrator.schema.json](orchestrator.schema.json) | UI Orchestrator machine-readable contract: inputs, routing outputs, UI state, change budgets (L1/L2/L3) and preservation rules | `uiux.engine.orchestrator` | `tests/test_orchestrator.py` |

The plugin manifest schema stays at [../manifest/plugin.schema.json](../manifest/plugin.schema.json). Validation uses the JSON Schema subset implemented in `plugin/packaging/artifact.py` (`validate_schema`), so no third-party validator is needed.
