# Changelog

Versions follow semantic versioning; `VERSION` is the single source (see `plugins/ui-engineering/schemas/plugin-manifest-README.md`).
The repository root `VERSION` mirrors `plugins/ui-engineering/VERSION`. Paths below are relative to the repository root; the plugin package lives in `plugins/ui-engineering/`.

## Unreleased

Repository restructure and distribution follow-ups.

- Repository layout: the shared plugin core moved to `plugins/ui-engineering/` (skills, workflows, knowledge, templates, `uiux` package, adapters, packaging, schemas); tests stay in `tests/`, development docs, fixtures and the benchmark harness in `development/`. The former `plugin/…`, `phase-2/…` and root `docs/…` paths no longer exist.
- Host adapters: experimental Claude Code (`plugins/ui-engineering/.claude-plugin/`) and Codex (`plugins/ui-engineering/.codex-plugin/`) bundle exporters and verifiers on top of the shared MCP transport; marketplace descriptors in `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
- Tests: `tests/test_distribution_phase8.py` (Phase 8 distribution gates) now builds and verifies a developer artifact in a temporary directory instead of requiring a pre-built, git-ignored `dist/dev/` artifact; the artifact tests are skipped when the suite runs against an extracted artifact (`UIUX_TEST_ROOT`).

### Plugin packaging (P0–P2)

Plugin Packaging Phase P0–P2 (build, verification and contract hardening; see `development/docs/plugin-packaging-spec.md`).

- `.gitattributes`: LF for all text files, binaries marked; `.gitignore` covers staging and build outputs.
- `plugins/ui-engineering/packaging/package-rules.json` is the single packaging contract (selection, required, forbidden, artifact metadata); new `artifact-metadata` layer for the generated `PACKAGE-MANIFEST.json`; `.github/**` classified as development.
- `plugins/ui-engineering/packaging/build.py`: deterministic release builds from `git archive` of a clean commit (refuses dirty trees with `COMMIT_REQUIRED_BEFORE_RELEASE_BUILD`) and explicitly marked developer builds (`-dev`, `release: false`); zip + tar.gz, `PACKAGE-MANIFEST.json`, `SHA256SUMS`, build-info.
- `plugins/ui-engineering/packaging/verify.py`: V1–V13 on the extracted artifact (V14 in CI), including read-only and without-plugin runs.
- `plugins/ui-engineering/schemas/`: package-manifest and build-info schemas; `plugins/ui-engineering/schemas/plugin.schema.json` is now a full schema.
- Tests: `UIUX_TEST_ROOT` runs the suite against an extracted artifact; new packaging build, verification and portability tests.
- CI configuration: `.github/workflows/ci.yml` (Windows/Linux/macOS × Python 3.9/3.11/3.13) and `package.yml` (build + verify on two OSes, reproducibility comparison).
- Contract hardening: centralized additive error taxonomy/envelopes (`status` and string `error` preserved), typed tool-schema validation, `INTERNAL_ERROR` public-boundary guard, and debug-only tracebacks.
- Public discovery: tool annotations, `accessibility_scan` with shared runtime-state gating, `capability_map`, `self_test`, `error_contract`, and generic-adapter metadata/self-test. Missing optional runtime is reported as `BLOCKED`, never auto-installed.
- Shared MCP transport: experimental stdio JSON-RPC 2.0 server pinned to MCP `2025-06-18`; registry-derived tools and annotation mapping, public-API-only invocation, structured results/error envelopes, `BLOCKED` preservation, EOF lifecycle and extracted-artifact smoke coverage. Host-specific adapters were added later (see above).

## 0.1.0 — plugin-ready architecture

- Layered, platform-neutral Python core package `uiux` (core foundation, knowledge, engine, runtime, evals, tooling) with a public Core API (`uiux.api`) and unified CLI (`plugins/ui-engineering/scripts/uiux_cli.py`).
- Resource discovery and configuration layer (`plugins/ui-engineering/uiux/core/resources.py`, `config.py`, `defaults.json`); all paths are package-relative and cwd-independent.
- Knowledge registry (now `plugins/ui-engineering/knowledge/domains/registry.json`) covering styles, layouts, screens, motion, interactions, effects, recipes, graphics, technologies and component grammars.
- Tool registry (`plugins/ui-engineering/uiux/core/tools.json`) and architecture layer map (`plugins/ui-engineering/uiux/core/layers.json`).
- Plugin layer: platform-neutral manifest, adapter contract, working generic adapter, packaging boundary (dry run).
- Runtime: Playwright readiness states (`NOT_DECLARED`, `DECLARED_NOT_INSTALLED`, `PACKAGE_AVAILABLE_BROWSER_MISSING`, `READY`). The runner now reports `BLOCKED` with `PLAYWRIGHT_IMPORT_FAILURE` or `PLAYWRIGHT_BROWSER_UNAVAILABLE` before attempting a capture when the runtime is not ready, as the runtime-error contract and E30 already specified.
- Scripts in `plugins/ui-engineering/scripts/` remain as backward-compatible CLIs and import names; tests moved to `tests/`.
- `plugins/ui-engineering/scripts/validate_skill.py` without an argument now validates this package's root instead of the current working directory.
