# Plugin layer

Integration and packaging only. It contains **no** design, knowledge, eval or runtime logic, and the core never imports it.

```text
plugin/
├── manifest/    platform-neutral plugin.json (+ schema); version = root VERSION
├── adapters/    adapter contract, generic adapter, shared experimental MCP stdio transport; platform adapters come later
├── schemas/     package-manifest and build-info schemas
└── packaging/   packaging contract, deterministic build, artifact verification (see packaging/README.md)
```

Everything here talks to the core through `uiux.api` (or `python scripts/uiux_cli.py`). Architecture: [docs/plugin-architecture.md](../docs/plugin-architecture.md).
