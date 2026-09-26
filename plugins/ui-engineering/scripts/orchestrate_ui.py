"""Compatibility entry point (stable CLI and import name). Implementation: ``uiux.engine.orchestrator``."""
import sys

import _bootstrap

_impl = _bootstrap.alias(__name__, "uiux.engine.orchestrator")

if __name__ == "__main__":
    raise SystemExit(_impl.main(sys.argv[1:]))
