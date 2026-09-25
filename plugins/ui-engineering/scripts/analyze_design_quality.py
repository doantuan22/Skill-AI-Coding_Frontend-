"""Compatibility entry point (stable CLI and import name). Implementation: ``uiux.evals.quality``."""
import sys

import _bootstrap

_impl = _bootstrap.alias(__name__, "uiux.evals.quality")

if __name__ == "__main__":
    raise SystemExit(_impl.main(sys.argv[1:]))
