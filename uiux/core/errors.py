"""Error contract: the central taxonomy (errors.json) and the exception type every layer raises.

Envelope (additive over the 0.x CLI shape ``{"status", "error"}``)::

    {"status": "INVALID_CALL" | "ERROR", "error": "<message>", "error_code": "<CODE>",
     "category": "<category>", "remediation": "<what to do>", "details": {...}}

Status and exit code come from the category: ``internal`` is ``ERROR``/exit 1, every other category keeps the 0.x
``INVALID_CALL``/exit 3. Codes are declared once in errors.json; ``UiuxError`` rejects unknown codes so modules cannot invent codes ad hoc.
Debug detail (tracebacks) is never part of an envelope: it is logged to the ``uiux`` logger and printed to stderr
only when ``UIUX_DEBUG=1``.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import traceback
from functools import lru_cache
from pathlib import Path

LOGGER = logging.getLogger("uiux")
ENV_DEBUG = "UIUX_DEBUG"
_TAXONOMY_PATH = Path(__file__).with_name("errors.json")


@lru_cache(maxsize=1)
def taxonomy() -> dict:
    return json.loads(_TAXONOMY_PATH.read_text(encoding="utf-8"))


def describe(code: str) -> dict:
    """Category, status, exit code, scope and remediation of a code."""
    data = taxonomy()
    entry = data["codes"][code]
    category = data["categories"][entry["category"]]
    return {"code": code, "category": entry["category"], "status": category["status"],
            "exit_code": category["exit_code"], "scope": entry["scope"], "remediation": entry["remediation"]}


class UiuxError(Exception):
    """An error with a registered code. ``message`` is the human-readable text kept in the ``error`` field."""

    default_code = "INTERNAL_ERROR"

    def __init__(self, message: str, code: str | None = None, remediation: str | None = None, **details: object) -> None:
        super().__init__(message)
        self.code = code or self.default_code
        if self.code not in taxonomy()["codes"]:
            raise ValueError(f"unregistered error code {self.code!r}; add it to uiux/core/errors.json")
        info = describe(self.code)
        self.message, self.category, self.status = message, info["category"], info["status"]
        self.exit_code = info["exit_code"]
        self.remediation = remediation or info["remediation"]
        self.details = {k: v for k, v in details.items() if v is not None}

    def envelope(self) -> dict:
        data = {"status": self.status, "error": self.message, "error_code": self.code, "category": self.category,
                "remediation": self.remediation}
        if self.details:
            data["details"] = self.details
        return data


class InternalError(UiuxError, RuntimeError):
    default_code = "INTERNAL_ERROR"


class RegistryError(UiuxError, ValueError):
    """A registry file is missing, unreadable or malformed (a ValueError, so existing handlers keep working)."""

    default_code = "REGISTRY_INVALID"


def debug_enabled() -> bool:
    return os.environ.get(ENV_DEBUG) == "1"


def internal(exc: BaseException, where: str) -> InternalError:
    """Wrap an unexpected exception: logged (and printed to stderr in debug mode), never exposed in the envelope."""
    LOGGER.debug("unexpected error in %s", where, exc_info=(type(exc), exc, exc.__traceback__))
    if debug_enabled():
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
    return InternalError(f"internal error in {where}", exception_type=type(exc).__name__)


def envelope_for(exc: BaseException, where: str = "call") -> dict:
    """Envelope for any exception: registered errors keep their code; anything else becomes INTERNAL_ERROR."""
    return (exc if isinstance(exc, UiuxError) else internal(exc, where)).envelope()


def result_annotation(code: str) -> dict:
    """Category and remediation of a code reported inside a BLOCKED result (the result itself is not an error)."""
    info = describe(code)
    return {"error_code": code, "category": info["category"], "remediation": info["remediation"]}
