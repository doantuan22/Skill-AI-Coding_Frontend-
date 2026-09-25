"""Compatibility entry point (stable CLI and import name). Implementation: ``uiux.runtime.browser``."""
import sys

import _bootstrap

_impl = _bootstrap.alias(__name__, "uiux.runtime.browser")

if __name__ == "__main__":
    raise SystemExit(_impl.main())
