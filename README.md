# UI Engineering Plugin

A structured AI coding plugin for frontend engineering, design systems, and UI/UX implementation.

## Architecture

This repository uses a shared plugin core (`plugins/ui-engineering`) with thin platform adapters for different AI agents (e.g., Claude Code, Codex, MCP).

- `plugins/ui-engineering`: Core plugin implementation (skills, knowledge, workflows, tooling)
- `.claude-plugin/`: Claude Code specific adapter
- `.codex-plugin/`: Codex specific adapter
- `adapters/mcp/`: MCP protocol transport

Please see `development/architecture/` for detailed architectural documentation.
