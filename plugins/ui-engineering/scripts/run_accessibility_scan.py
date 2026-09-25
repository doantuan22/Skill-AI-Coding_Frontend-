"""Compatibility entry point (stable CLI and import name). Implementation: ``uiux.runtime.accessibility``."""
import sys

import _bootstrap

_impl = _bootstrap.alias(__name__, "uiux.runtime.accessibility")

if __name__ == "__main__":
    raise SystemExit(_impl.main())
