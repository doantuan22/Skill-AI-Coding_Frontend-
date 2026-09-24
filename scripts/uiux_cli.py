"""Unified CLI for the Core API: ``python scripts/uiux_cli.py tools`` / ``python scripts/uiux_cli.py call <tool> --params '{...}'``.

Equivalent to ``python -m uiux`` when the package root is on ``sys.path``.
"""
import sys

import _bootstrap  # noqa: F401

from uiux import cli

if __name__ == "__main__":
    raise SystemExit(cli.main(sys.argv[1:]))
