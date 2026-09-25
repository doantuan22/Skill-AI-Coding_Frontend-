"""Common Adapter Framework.

Provides generic orchestration for building and verifying host adapters.
Host adapters (like Claude Code, Codex, etc.) use this framework to assemble
their bundles and verify common constraints without duplicating deterministic
packaging logic or MCP smoke test harnesses.
"""
