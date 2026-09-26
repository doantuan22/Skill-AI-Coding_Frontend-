"""CLI entry point for Repo & Framework Intelligence. Implementation: ``uiux.engine.repo_intelligence``."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _bootstrap

_bootstrap.alias(__name__, "uiux.engine.repo_intelligence")

from uiux.engine.repo_intelligence import analyze_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repo & Framework Intelligence analyzer")
    parser.add_argument("project", nargs="?", default=".", help="Target project directory")
    parser.add_argument("--format", choices=["json", "summary"], default="json", help="Output format")
    args = parser.parse_args(argv)

    profile = analyze_repository(args.project)
    if args.format == "json":
        print(json.dumps(profile, indent=2))
    else:
        print(f"Framework: {profile['framework']['name']} (conf: {profile['framework']['confidence']:.2f})")
        print(f"Styling: {profile['styling_system']['primary']}")
        print(f"UI State: {profile['existing_ui_state']['value']} (conf: {profile['existing_ui_state']['confidence']:.2f})")
        print(f"Components: {profile['components']['total_count']}")
        print(f"Routes/Pages: {len(profile['routes'])}")
        print(f"Runtime Commands Source: {profile['runtime']['commands_source']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
