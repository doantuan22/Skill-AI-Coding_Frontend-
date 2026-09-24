"""Compatibility entry point (stable CLI and import name). Implementation: ``uiux.knowledge.catalog``."""
import sys

import _bootstrap

_impl = _bootstrap.alias(__name__, "uiux.knowledge.catalog")

if __name__ == "__main__":
    raise SystemExit(_impl.main(sys.argv))
