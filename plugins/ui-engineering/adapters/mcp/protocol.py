"""Minimal JSON-RPC 2.0 primitives for the pinned MCP stdio protocol revision.

Only protocol-envelope validation belongs here. Tool argument validation remains the responsibility of
``uiux.api.call_tool`` and its registry schema.
"""
from __future__ import annotations

from typing import Any

JSONRPC = "2.0"
MCP_PROTOCOL_VERSION = "2025-06-18"

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
NOT_INITIALIZED = -32002


def error(identifier: str | int | None, code: int, message: str, data: object | None = None) -> dict[str, object]:
    """One JSON-RPC error response. ``data`` stays structured and never includes a traceback."""
    body: dict[str, object] = {"code": code, "message": message}
    if data is not None:
        body["data"] = data
    return {"jsonrpc": JSONRPC, "id": identifier, "error": body}


def result(identifier: str | int, value: dict[str, object]) -> dict[str, object]:
    return {"jsonrpc": JSONRPC, "id": identifier, "result": value}


def valid_id(value: object) -> bool:
    """MCP request identifiers are non-null strings or integers; bool is not an integer identifier."""
    return isinstance(value, str) or (isinstance(value, int) and not isinstance(value, bool))


def request_problem(message: object) -> tuple[str | int | None, str | None]:
    """Return ``(id, problem)`` after validating the JSON-RPC envelope, or ``(id, None)`` when valid."""
    if not isinstance(message, dict):
        return None, "request must be a JSON object"
    identifier = message.get("id")
    if message.get("jsonrpc") != JSONRPC:
        return identifier if valid_id(identifier) else None, "jsonrpc must be '2.0'"
    if not isinstance(message.get("method"), str) or not message["method"]:
        return identifier if valid_id(identifier) else None, "method must be a non-empty string"
    if "id" in message and not valid_id(identifier):
        return None, "id must be a string or integer"
    if "params" in message and not isinstance(message["params"], dict):
        return identifier if valid_id(identifier) else None, "params must be an object"
    return identifier if valid_id(identifier) else None, None


def text_content(value: object) -> dict[str, str]:
    """Canonical JSON text content accompanying every structured MCP tool result."""
    import json

    return {"type": "text", "text": json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                                                default=str)}
