# Plugin schemas

| Schema | Describes | Produced by | Checked by |
|---|---|---|---|
| [package-manifest.schema.json](package-manifest.schema.json) | `PACKAGE-MANIFEST.json`, embedded in every artifact and published next to it: identity, provenance and per-file sha256 | `plugin/packaging/build.py` | `plugin/packaging/verify.py` (V1) |
| [build-info.schema.json](build-info.schema.json) | `<artifact>.build-info.json`: the build environment record (outside the archive, not in `SHA256SUMS`) | `build.py` | tests |
| [adapter.schema.json](adapter.schema.json) | Host-neutral adapter metadata, including the MCP protocol pin/method list when an adapter exposes `mcp-stdio` | adapter metadata | V10 / tests |
| [orchestrator.schema.json](orchestrator.schema.json) | UI Orchestrator machine-readable contract: inputs, routing outputs, UI state, change budgets (L1/L2/L3) and preservation rules | `uiux.engine.orchestrator` | `tests/test_orchestrator.py` |
| [repo-profile.schema.json](repo-profile.schema.json) | Repo Intelligence normalized repository profile: framework, styling, routes, components, tokens, UI state, and runtime capabilities | `uiux.engine.repo_intelligence` | `tests/test_repo_intelligence.py` |
| [existing-ui-profile.schema.json](existing-ui-profile.schema.json) | Existing UI Analyzer comprehensive profile: identity, layout, components, UX flows, responsive, accessibility, and design system | `uiux.engine.existing_ui` | `tests/test_existing_ui.py` |
| [preservation-profile.schema.json](preservation-profile.schema.json) | Baseline preservation requirements, protected invariants, allowed change budgets (L1/L2/L3), and merged user permissions | `uiux.engine.existing_ui` | `tests/test_existing_ui.py` |
| [preservation-evaluation.schema.json](preservation-evaluation.schema.json) | Preservation Guard evaluation output: pass/warn/fail status, rule violations, and justification traces | `uiux.engine.existing_ui` | `tests/test_existing_ui.py` |
| [knowledge-plan.schema.json](knowledge-plan.schema.json) | Knowledge Router machine-readable load plan: framework/styling packs, design skills, preservation context, budget, and runtime validation | `uiux.engine.knowledge_router` | `tests/test_knowledge_router.py` |

The plugin manifest schema stays at [../manifest/plugin.schema.json](../manifest/plugin.schema.json). Validation uses the JSON Schema subset implemented in `plugin/packaging/artifact.py` (`validate_schema`), so no third-party validator is needed.
