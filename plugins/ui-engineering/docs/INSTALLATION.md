# Public Installation Guide

This guide details how to acquire, install, verify, and upgrade the **UI Engineering Plugin** across supported environments.

---

## 1. System Requirements

- **Python**: Version 3.9, 3.10, 3.11, 3.12, or 3.13.
- **Node.js** (Optional): Version 18+ if target projects require local runtime execution or Node-based tooling.
- **Operating System**: Windows, Linux, or macOS.

---

## 2. Installation Methods

### Method A: Install from GitHub Source

Clone the repository and point your host AI coding environment at the canonical plugin root:

```bash
git clone https://github.com/org/Skill-AI-Coding_Frontend.git
cd Skill-AI-Coding_Frontend
```

The canonical plugin directory is located at `plugins/ui-engineering/`.

### Method B: Install from Release Artifact

Download the official release archive `ui-ux-design-<version>.zip` from GitHub Releases and extract it to your preferred tools or plugins directory:

```bash
# Example extraction
unzip ui-ux-design-0.1.0.zip -d ~/.plugins/ui-engineering
```

---

## 3. Platform Setup

### A. Claude Code Setup

Claude Code integrates via the `.claude-plugin/` adapter configuration:

1. Register the plugin path in your Claude Code settings or CLI invocation:
   ```bash
   claude --plugin-dir /path/to/plugins/ui-engineering
   ```
2. Verify that Claude Code detects the plugin manifest at `.claude-plugin/adapter.json` or `plugin.json`.

### B. OpenAI Codex Setup

Codex integrates via `.codex-plugin/` metadata:

1. Point your Codex environment configuration to the plugin directory.
2. The launcher uses `python scripts/uiux_cli.py call <tool_id>` with `--params "@path/to/params.json"` on Windows.

### C. Standalone MCP Server Setup

The plugin provides a native Model Context Protocol (MCP) stdio server:

Add the server to your host MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ui-engineering": {
      "command": "python",
      "args": [
        "-m",
        "adapters.mcp.server"
      ],
      "cwd": "/path/to/plugins/ui-engineering"
    }
  }
}
```

---

## 4. Verification & Health Check

After installation, verify the installation immediately using the public CLI:

```bash
# Run self-test health check
python scripts/uiux_cli.py call self_test

# Expected output:
# {"status": "PASS", "version": "0.1.0", "checks": [...]}
```

---

## 5. Upgrade & Rollback Workflow

### Upgrading
To upgrade to a new version:
1. Obtain the new release archive or pull the latest Git tag.
2. Replace the plugin directory with the new version.
3. Run `python scripts/uiux_cli.py call self_test` to confirm registry and contract integrity.
4. *Note*: Plugin upgrades never modify your target repository files.

### Rollback
If you need to roll back to a previous version:
1. Re-extract or check out the previous release tag (e.g., `v0.1.0`).
2. Run `python scripts/uiux_cli.py call self_test` to verify rollback validity.
