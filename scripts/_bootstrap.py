"""Make the ``uiux`` package importable for the compatibility scripts in this folder.

The package root is the parent of this folder; the ``uiux`` package derives every other path itself
(``uiux.core.resources``), so this is the only path computation outside the package.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

PACKAGE_ROOT = str(Path(__file__).resolve().parents[1])
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)


def alias(wrapper: str, target: str):
    """Import ``target``; when imported (not run), register it under the legacy module name so old imports
    (``import knowledge_lib``) see the implementation module itself, including its private helpers."""
    module = importlib.import_module(target)
    if wrapper != "__main__":
        sys.modules[wrapper] = module
    return module
