# UI Engineering Plugin Documentation

Welcome to the public documentation for the **UI Engineering Plugin**.

## Overview

The UI Engineering Plugin is a comprehensive, production-grade intelligence layer and workflow engine for modern frontend user experience engineering. It provides automated design intelligence, repository profiling, modification planning with invariant preservation, design system and token management, motion & styling patterns, and closed-loop runtime criticism with targeted repairs.

## Documentation Index

- [Installation Guide](INSTALLATION.md): Complete setup instructions for GitHub source distribution, Claude Code, OpenAI Codex, and standalone MCP environments.
- [Compatibility Matrix](COMPATIBILITY.md): Supported platforms, thin adapters, capability coverage, and platform-specific statuses.
- [Thin Adapter Contract](ADAPTER_CONTRACT.md): The architectural contract governing how host platforms interface with the single shared core.
- [Release Notes](RELEASE_NOTES.md): Version highlights, features, bug fixes, and upgrade guidelines.
- [Troubleshooting](TROUBLESHOOTING.md): Guidance for resolving common runtime, schema, and path issues.

## Architecture Principles

1. **One Shared Core, Multiple Thin Adapters**: All reasoning, domain knowledge, capability resolution, planning, and evaluation live in a single canonical core (`plugins/ui-engineering/`). Host adapters provide only metadata, launchers, and transport glue without copying or duplicating core logic.
2. **Preserve First, Improve Second, Redesign Only When Authorized**: The plugin guarantees strict preservation invariants (brand identity, design tokens, color palette, navigation architecture) unless explicit permission is granted.
3. **Repository-Grounded Planning**: The planner exclusively targets files that exist on disk or are explicitly designated with architectural justification (`planned_create: true`).
4. **Honest Runtime Verification**: Runtime criticism strictly requires real browser evidence. If local headless browser environments are unavailable, execution states are honestly reported as `BLOCKED_BROWSER_RUNTIME` without faking verification.
