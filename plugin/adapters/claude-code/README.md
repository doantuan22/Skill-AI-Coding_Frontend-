# Claude Code adapter

Status: **experimental** (structurally verified; live Claude Code host test not yet run)

This adapter bundles the platform-neutral UI/UX Design Skill as a Claude Code plugin with MCP tool exposure through the shared stdio transport. It contains no design, knowledge, eval or runtime logic (see [CONTRACT.md](../CONTRACT.md)).

## Plugin structure

```text
<plugin-root>/
├── .claude-plugin/
│   └── plugin.json          # Claude plugin manifest (name, version, description)
├── .mcp.json                 # MCP server declaration for the shared transport
├── SKILL.md                  # Skill entry point (reused unchanged)
├── VERSION
├── uiux/                     # Core package
├── plugin/                   # Plugin layer (manifest, adapters, packaging, schemas)
├── workflow/                 # Workflow definitions
├── phase-1/                  # Phase 1 knowledge
├── phase-2/                  # Phase 2 knowledge (incl. Design Knowledge System)
├── review/                   # Review gates
├── templates/                # Artifact templates
├── execution/                # Execution contracts
├── evals/                    # Eval scenarios and fixtures
├── docs/                     # Documentation
├── scripts/                  # CLI tools
└── CHANGELOG.md
```

The plugin root IS the package root. `SKILL.md` and all its relative links work without rewriting.

## Name mapping

| Context | Name | Source |
|---|---|---|
| Skill name (frontmatter) | `ui-ux-workflow` | `SKILL.md` |
| Package / plugin id | `ui-ux-design` | `plugin/manifest/plugin.json` |
| Claude plugin name | `ui-ux-design` | `.claude-plugin/plugin.json` |
| MCP server name | `ui-ux-design-mcp` | `.mcp.json` key |
| Python package | `uiux` | `uiux/` |

## Installation

### Development (recommended for testing)

```bash
claude --plugin-dir <path-to-extracted-bundle>
```

The agent will discover `SKILL.md`, connect to the MCP server, and expose all public tools.

### Local packaged bundle

1. Build the generic artifact: `python plugin/packaging/build.py --dev`
2. Build the Claude bundle: `python plugin/adapters/claude-code/export.py --source . --out dist/dev/adapters/ --dev`
3. Extract the bundle ZIP to a directory
4. `claude --plugin-dir <extracted-directory>`

### Marketplace / distribution

**NOT IMPLEMENTED.** The architecture supports future marketplace distribution through the Claude plugin ecosystem. The bundle is self-contained and can be distributed as a ZIP archive.

## MCP configuration

The `.mcp.json` at the plugin root declares one MCP server:

```json
{
  "ui-ux-design-mcp": {
    "command": "python3",
    "args": ["${CLAUDE_PLUGIN_ROOT}/plugin/adapters/mcp/server.py"],
    "env": {}
  }
}
```

- `${CLAUDE_PLUGIN_ROOT}` is resolved by Claude Code to the plugin installation directory
- The command launches the **shared** MCP stdio transport; no second MCP implementation exists
- On Windows, `python3` may need to be `python` or `py -3` — see Python runtime below

## Python runtime

The plugin requires Python 3.9+ on PATH. No Python runtime is bundled or auto-installed.

| OS | Typical executable | Notes |
|---|---|---|
| Linux | `python3` | Most distributions ship `python3` |
| macOS | `python3` | Homebrew, system, or pyenv `python3` |
| Windows | `python` or `py -3` | Python Launcher for Windows (`py`) is standard |

If Python is not found, the MCP server will fail to start and Claude Code will report the MCP server as unavailable. The error message will indicate that Python 3 is required.

**To configure a non-standard Python path**, edit `.mcp.json` in the extracted bundle:

```json
{
  "ui-ux-design-mcp": {
    "command": "/path/to/python3",
    "args": ["${CLAUDE_PLUGIN_ROOT}/plugin/adapters/mcp/server.py"],
    "env": {}
  }
}
```

## Tool exposure

All public tools are exposed through MCP `tools/list`:

| Tool | Read-only | Description |
|---|---|---|
| `resolve_capabilities` | ✓ | Turn a design profile into a capability plan |
| `retrieve_knowledge` | ✓ | Query the Design Knowledge System (248 entries, 10 collections) |
| `resolve_technology` | ✓ | Choose the simplest technology for capabilities |
| `analyze_design_quality` | ✓ | Static design quality analysis (E65-E80) |
| `detect_runtime` | ✓ | Read-only Playwright/Node capability detection |
| `run_runtime` | | Capture rendered evidence (writes to target project) |
| `accessibility_scan` | | axe accessibility scan (writes to target project) |
| `run_evals` | ✓ | Run automated eval suites |
| `validate_skill` | ✓ | Structural validation |
| `capability_map` | ✓ | Discover capabilities, tools, knowledge, runtime |
| `self_test` | ✓ | Fast health check |

Tool permissions are driven by MCP annotations (`readOnlyHint`, `destructiveHint`, etc.) and the extended `_meta["uiux.dev/annotations"]` metadata. Tools are not pre-approved via wildcard.

## Skill integration

Claude Code reads `SKILL.md` at the plugin root. The skill instructs the agent to:
1. Follow the workflow state machine
2. Load knowledge progressively through `retrieve_knowledge`
3. Use capability and technology resolvers before design decisions
4. Gate phase transitions on review criteria
5. Use runtime tools only when the target project has Playwright

No duplicate skill content exists in the adapter. The canonical `SKILL.md` is reused directly.

## Verification

### Automated (no Claude Code required)

```bash
# Structural + subprocess verification (C1-C16)
python plugin/adapters/claude-code/verify.py <extracted-bundle>
python plugin/adapters/claude-code/verify.py --bundle <bundle.zip>
```

### Live host test (requires Claude Code)

```bash
claude --plugin-dir <extracted-bundle>
# In session: verify plugin load, tool discovery, read-only call, self_test
```

If Claude Code is not available: `CLAUDE_CODE_LIVE_TEST = NOT_RUN`

## Limitations

- Claude Code live host test has not been executed; structural and subprocess verification only
- No `min_version` for Claude Code is declared (docs verified 2026-09-25, no pinned host release)
- Python 3 must be available on PATH
- On Windows, `.mcp.json` uses `python3`; users may need to adjust to `python` or `py -3`
- Tool auto-approval is not configured (Claude Code manages this through its own permission system)

## Docs checked

Claude Code plugin documentation verified: **2026-09-25**
- `.claude-plugin/plugin.json`: manifest with `name`, `version`, `description`
- `.mcp.json`: MCP server declarations at plugin root
- `${CLAUDE_PLUGIN_ROOT}`: portable path variable
- `claude --plugin-dir`: local plugin testing
- `skills/` auto-discovery: subdirectories with `SKILL.md`
- Plugin validation: `claude plugin validate`
