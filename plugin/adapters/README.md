# Adapters

Adapters bind the platform-neutral core to specific hosts. The contract is [CONTRACT.md](CONTRACT.md).

| Adapter | Status | Notes |
|---|---|---|
| [generic](generic/README.md) | skeleton (working) | Host-agnostic JSON adapter over `uiux.api`; the reference for new adapters |
| [mcp](mcp/README.md) | experimental (working) | Shared stdio MCP transport over `uiux.api`; tools only, no host-specific integration |
| [claude-code](claude-code/README.md) | experimental (working) | Claude Code plugin with MCP tool exposure; structurally verified, live host test not yet run |
| codex | planned | Not implemented in this phase |
| cline | planned | Not implemented in this phase |
| opencode | planned | Not implemented in this phase |
| copilot | planned | Not implemented in this phase |

Planned adapters (codex, cline, opencode, copilot) have no folders yet on purpose: an empty or stubbed adapter would look supported without working. Each one is added through the steps in the contract when its host is targeted.
