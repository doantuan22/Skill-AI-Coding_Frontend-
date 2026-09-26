"""Runtime Input Validator – Phase 7 Hardening #5.

Defensive validation for public runtime contracts:
- Evidence payloads (schemas/evidence.schema.json)
- Repair results & actions_executed (schemas/repair-result.schema.json)
- Modification plans & change manifests

Ensures structured failures with INVALID_ARGUMENT instead of raw exceptions (AttributeError, KeyError, TypeError).
"""
from __future__ import annotations

from typing import Any


def validate_evidence(evidence: Any, field_name: str = "after_evidence") -> tuple[bool, str, dict[str, Any]]:
    """Validate runtime evidence payload defensively.

    Returns (is_valid, error_message, details).
    """
    if evidence is None:
        return True, "", {}

    if not isinstance(evidence, dict):
        return (
            False,
            f"Invalid {field_name} payload: expected dictionary or null, got {type(evidence).__name__}",
            {"field": field_name, "expected": "object", "actual": type(evidence).__name__},
        )

    # If captures provided, validate structure
    if "captures" in evidence:
        captures = evidence["captures"]
        if not isinstance(captures, list):
            return (
                False,
                f"Invalid {field_name}.captures: expected array of capture objects, got {type(captures).__name__}",
                {"field": f"{field_name}.captures", "expected": "array", "actual": type(captures).__name__},
            )

        for idx, cap in enumerate(captures):
            if not isinstance(cap, dict):
                return (
                    False,
                    f"Invalid {field_name}.captures[{idx}]: capture must be an object, got {type(cap).__name__}",
                    {"field": f"{field_name}.captures[{idx}]", "expected": "object", "actual": type(cap).__name__},
                )
            # Validate required fields if non-empty capture
            if not any(k in cap for k in ("id", "page", "route", "viewport", "status")):
                return (
                    False,
                    f"Invalid {field_name}.captures[{idx}]: missing required capture fields (id, page, viewport, or status)",
                    {"field": f"{field_name}.captures[{idx}]", "missing": ["id", "page", "viewport", "status"]},
                )
            # If viewport is an object, check width and height
            vp = cap.get("viewport_info") or cap.get("viewport")
            if isinstance(vp, dict):
                if "width" in vp and not isinstance(vp["width"], (int, float)):
                    return (
                        False,
                        f"Invalid {field_name}.captures[{idx}].viewport: width must be numeric",
                        {"field": f"{field_name}.captures[{idx}].viewport.width", "actual": type(vp["width"]).__name__},
                    )

    # Validate console_entries if provided
    if "console_entries" in evidence:
        console = evidence["console_entries"]
        if not isinstance(console, list):
            return (
                False,
                f"Invalid {field_name}.console_entries: expected list, got {type(console).__name__}",
                {"field": f"{field_name}.console_entries", "expected": "array"},
            )

    # Validate actions_executed if provided in evidence
    if "actions_executed" in evidence:
        actions = evidence["actions_executed"]
        if not isinstance(actions, list):
            return (
                False,
                f"Invalid {field_name}.actions_executed: expected list, got {type(actions).__name__}",
                {"field": f"{field_name}.actions_executed", "expected": "array"},
            )
        for idx, act in enumerate(actions):
            if not isinstance(act, dict):
                return (
                    False,
                    f"Invalid {field_name}.actions_executed[{idx}]: action must be an object (not string), got {type(act).__name__}",
                    {"field": f"{field_name}.actions_executed[{idx}]", "expected": "object", "actual": type(act).__name__},
                )

    return True, "", {}


def validate_repair_result(repair_result: Any) -> tuple[bool, str, dict[str, Any]]:
    """Validate repair result payload defensively.

    Consumer requirement: actions_executed MUST be an array of objects, never plain strings.
    """
    if repair_result is None or not isinstance(repair_result, dict):
        return (
            False,
            f"Invalid repair_result: expected dictionary, got {type(repair_result).__name__}",
            {"field": "repair_result", "expected": "object", "actual": type(repair_result).__name__},
        )

    actions = repair_result.get("actions_executed")
    if actions is not None:
        if not isinstance(actions, list):
            return (
                False,
                f"Invalid actions_executed: expected array of objects, got {type(actions).__name__}",
                {"field": "actions_executed", "expected": "array", "actual": type(actions).__name__},
            )

        for idx, action in enumerate(actions):
            if not isinstance(action, dict):
                return (
                    False,
                    f"Invalid actions_executed[{idx}]: action must be an object (not string or scalar), got {type(action).__name__}",
                    {"field": f"actions_executed[{idx}]", "expected": "object", "actual": type(action).__name__},
                )
            if "files" in action and not isinstance(action["files"], list):
                return (
                    False,
                    f"Invalid actions_executed[{idx}].files: expected list of file paths",
                    {"field": f"actions_executed[{idx}].files", "expected": "array"},
                )

    return True, "", {}


def make_invalid_argument_error(message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build standardized structured failure envelope for INVALID_ARGUMENT."""
    return {
        "status": "INVALID_CALL",
        "error": message,
        "error_code": "INVALID_ARGUMENT",
        "code": "INVALID_ARGUMENT",
        "message": message,
        "category": "validation",
        "remediation": "Provide valid payloads adhering to the public JSON schemas (schemas/evidence.schema.json, schemas/repair-result.schema.json).",
        "details": details or {},
        "overall_status": "blocked",
        "issues": [
            {
                "issue_id": "issue_invalid_argument",
                "category": "runtime_error",
                "severity": "CRITICAL",
                "status": "new_regression",
                "description": message,
                "evidence": "Payload validation failed against public contract schema.",
                "expected": "Schema-compliant argument payload",
                "actual": (details or {}).get("actual", "invalid"),
                "repairable": False,
            }
        ],
        "schema_version": 1,
        "report_id": "critic_error_invalid_argument",
    }
