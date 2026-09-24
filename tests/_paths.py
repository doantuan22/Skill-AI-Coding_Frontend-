"""Test bootstrap: put the package root on sys.path (tests live outside the ``uiux`` package).

``UIUX_TEST_ROOT`` points the suite at another package root, e.g. an extracted release artifact
(plugin/packaging/verify.py V13). Without it the root is the parent of this directory.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PACKAGE_ROOT = Path(os.environ.get("UIUX_TEST_ROOT") or Path(__file__).resolve().parents[1]).resolve()
SCRIPTS = PACKAGE_ROOT / "scripts"
IS_GIT_WORK_TREE = (PACKAGE_ROOT / ".git").exists()
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))
