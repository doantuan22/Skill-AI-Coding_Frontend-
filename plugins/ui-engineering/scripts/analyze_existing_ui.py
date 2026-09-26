"""CLI entry point for Existing UI Analyzer. Implementation: ``uiux.engine.existing_ui``."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _bootstrap

_bootstrap.alias(__name__, "uiux.engine.existing_ui")

from uiux.engine.existing_ui import analyze_existing_ui, build_preservation_profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Existing UI Analyzer and Preservation Guard CLI")
    parser.add_argument("project", nargs="?", default=".", help="Target project directory")
    parser.add_argument("--format", choices=["json", "summary", "preservation"], default="json", help="Output format")
    args = parser.parse_args(argv)

    profile = analyze_existing_ui(args.project)
    if args.format == "json":
        print(json.dumps(profile, indent=2))
    elif args.format == "preservation":
        preservation = build_preservation_profile(profile)
        print(json.dumps(preservation, indent=2))
    else:
        ident = profile["identity"]
        colors = ident["colors"]
        print(f"Primary Color: {colors.get('primary')} (conf: {ident['confidence']:.2f})")
        print(f"Visual Language: {ident['visual_language']}")
        print(f"Layout Shell: {profile['layout']['global_structure'].get('app_shell') or 'default'}")
        print(f"Component Consistency: {profile['components']['consistency']}")
        print(f"UX Flows: {', '.join(profile['ux']['flows'])}")
        print(f"Design System Maturity: {profile['design_system']['maturity']}")
        print(f"Overall Confidence: {profile['overall_confidence']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
