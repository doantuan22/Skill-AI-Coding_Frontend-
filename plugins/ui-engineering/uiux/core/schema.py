"""Tool input validation: a small, deterministic subset of JSON Schema (stdlib only).

Supported keywords: ``type`` (a name or a list of names; ``"null"`` makes a value nullable), ``enum``, ``minimum``,
``maximum``, ``items``, ``properties``, ``required``, ``additionalProperties: false``, ``description``, ``default``.
Objects and arrays are checked recursively. Anything else in a tool schema is a registry error (``check_schema``), so
the registry cannot silently promise more validation than is performed. Errors are ``UiuxError`` with the codes
MISSING_REQUIRED_ARGUMENT, UNEXPECTED_ARGUMENT, INVALID_ARGUMENT_TYPE and INVALID_ARGUMENT; the first error in a
fixed order wins (required, unexpected, then each declared property in order).
"""
from __future__ import annotations

from uiux.core.errors import UiuxError

TYPES = ("string", "integer", "number", "boolean", "array", "object", "null")
KEYWORDS = {"type", "enum", "minimum", "maximum", "items", "properties", "required", "additionalProperties",
            "description", "default"}


def type_of(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _types(schema: dict) -> list[str]:
    declared = schema.get("type", [])
    return [declared] if isinstance(declared, str) else list(declared)


def _matches(value: object, allowed: list[str]) -> bool:
    actual = type_of(value)
    return not allowed or actual in allowed or (actual == "integer" and "number" in allowed)


def _check_value(value: object, schema: dict, where: str) -> None:
    allowed = _types(schema)
    if not _matches(value, allowed):
        raise UiuxError(f"{where} must be {' or '.join(allowed)}, got {type_of(value)}", "INVALID_ARGUMENT_TYPE",
                        argument=where, expected=allowed, actual=type_of(value))
    if value is None:
        return
    if "enum" in schema and value not in schema["enum"]:
        raise UiuxError(f"{where} must be one of {', '.join(str(v) for v in schema['enum'] if v is not None)}", "INVALID_ARGUMENT",
                        argument=where, allowed=schema["enum"])
    if (("minimum" in schema and value < schema["minimum"]) or
            ("maximum" in schema and value > schema["maximum"])):
        raise UiuxError(f"{where} must be between {schema.get('minimum', '-inf')} and {schema.get('maximum', 'inf')}",
                        "INVALID_ARGUMENT", argument=where)
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            _check_value(item, schema["items"], f"{where}[{index}]")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = [name for name in required if name not in value]
        if missing:
            raise UiuxError(f"{where}: missing required properties: {', '.join(missing)}", "MISSING_REQUIRED_ARGUMENT",
                            argument=where, missing=missing)
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise UiuxError(f"{where}: unknown properties: {', '.join(unknown)}", "UNEXPECTED_ARGUMENT",
                                argument=where, unexpected=unknown)
        for name, sub in properties.items():
            if name in value:
                _check_value(value[name], sub, f"{where}.{name}")


def validate_arguments(tool_id: str, schema: dict, params: object) -> dict:
    """Validate call parameters against a tool's ``input`` schema; returns the parameters unchanged."""
    if not isinstance(params, dict):
        raise UiuxError("params must be a JSON object", "INVALID_ARGUMENT_TYPE", expected=["object"], actual=type_of(params))
    properties = schema.get("properties", {})
    missing = [name for name in schema.get("required", []) if name not in params]
    if missing:
        raise UiuxError(f"{tool_id}: missing required parameters: {', '.join(missing)}", "MISSING_REQUIRED_ARGUMENT",
                        tool=tool_id, missing=missing)
    unknown = sorted(set(params) - set(properties))
    if unknown:
        raise UiuxError(f"{tool_id}: unknown parameters: {', '.join(unknown)}", "UNEXPECTED_ARGUMENT",
                        tool=tool_id, unexpected=unknown)
    for name, sub in properties.items():
        if name in params:
            _check_value(params[name], sub, f"{tool_id}.{name}")
    return params


def check_schema(schema: object, where: str = "input", top: bool = True) -> list[str]:
    """Problems that make a tool input schema unusable by ``validate_arguments`` (empty list when valid).

    The top-level schema is always a closed object of named parameters. Nested objects are optional, but when a nested
    schema declares ``properties``/``required``/``additionalProperties: false`` they are enforced recursively too.
    """
    if not isinstance(schema, dict):
        return [f"{where}: schema must be an object"]
    errors = [f"{where}: unsupported keyword {key!r}" for key in sorted(set(schema) - KEYWORDS)]
    if top and (schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        errors.append(f"{where}: a tool input must be an object schema with additionalProperties false")
    declared = _types(schema)
    if not declared or any(t not in TYPES for t in declared):
        errors.append(f"{where}: type must name one or more of {', '.join(TYPES)}")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        errors.append(f"{where}: enum must be a non-empty list")
    if "items" in schema:
        if "array" not in declared:
            errors.append(f"{where}: items requires array type")
        errors += check_schema(schema["items"], f"{where}.items", top=False)
    if "properties" in schema:
        if "object" not in declared:
            errors.append(f"{where}: properties requires object type")
        if not isinstance(schema["properties"], dict):
            errors.append(f"{where}: properties must be an object")
        else:
            for name, sub in schema["properties"].items():
                errors += check_schema(sub, f"{where}.{name}", top=False)
            errors += [f"{where}: required property {name!r} is not declared" for name in schema.get("required", [])
                       if name not in schema["properties"]]
    if "additionalProperties" in schema and schema["additionalProperties"] is not False:
        errors.append(f"{where}: additionalProperties may only be false")
    if "required" in schema and not isinstance(schema["required"], list):
        errors.append(f"{where}: required must be a list")
    if "minimum" in schema or "maximum" in schema:
        if not any(item in ("integer", "number") for item in declared):
            errors.append(f"{where}: minimum/maximum requires integer or number type")
        for key in ("minimum", "maximum"):
            if key in schema and (isinstance(schema[key], bool) or not isinstance(schema[key], (int, float))):
                errors.append(f"{where}: {key} must be a number")
    return errors
