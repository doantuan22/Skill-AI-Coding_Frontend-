"""Compatibility entry point (stable CLI and import name). Implementation: ``uiux.tooling.validate``."""
import sys

import _bootstrap

_impl = _bootstrap.alias(__name__, "uiux.tooling.validate")

if __name__ == "__main__":
    raise SystemExit(_impl.main())
