"""``python -m uiux`` (requires the package root on sys.path); see uiux.cli."""
import sys

from uiux.cli import main

raise SystemExit(main(sys.argv[1:]))
