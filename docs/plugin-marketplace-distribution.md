# Local marketplace distribution

Docs verified date: **2026-09-25**.

## Contracts verified

| Host | Marketplace contract | Installation surfaces | Limitation |
|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json`; kebab-case name, `owner` object with `name`, and plugin `source` | Claude Code CLI; documented VS Code flow | Live VS Code test is not run |
| Codex/OpenAI | `.agents/plugins/marketplace.json`; `name`, `interface.displayName`, local `source.path`, policy, category | Codex CLI discovery; ChatGPT desktop app / Work mode Plugins Directory | `CODEX_VSCODE_MARKETPLACE_SUPPORT = NOT_CLAIMED` |

The authoritative references are Anthropic's [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) and OpenAI's [Package your plugin](https://developers.openai.com/plugins/build/plugins). If either contract changes, the host documentation takes precedence over this repository.

## Shared logical identity

| Host | Marketplace | Plugin | Installation / enable key |
|---|---|---|---|
| Claude | `uiux-local` | `ui-ux-design` | `ui-ux-design@uiux-local` |
| Codex | `uiux-local` | `ui-ux-design` | `ui-ux-design@uiux-local` |

The names match deliberately, but manifests are host-specific and are never shared:
Claude uses `.claude-plugin/marketplace.json`; Codex uses `.agents/plugins/marketplace.json`.
