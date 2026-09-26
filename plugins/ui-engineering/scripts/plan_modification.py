"""CLI entry point for Modification Planner. Implementation: ``uiux.engine.modification_planner``."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _bootstrap

_bootstrap.alias(__name__, "uiux.engine.modification_planner")

from uiux.engine.existing_ui import analyze_existing_ui, build_preservation_profile
from uiux.engine.knowledge_router import build_knowledge_plan
from uiux.engine.modification_planner import plan_modification
from uiux.engine.repo_intelligence import analyze_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Modification Planner CLI")
    parser.add_argument("--project", default=".", help="Target project directory")
    parser.add_argument("--task", default="", help="User goal or task description")
    parser.add_argument("--workflow", choices=["greenfield", "existing-ui"], default="existing-ui", help="UI Workflow")
    parser.add_argument("--scope", default="global", help="Requested scope (global, page, section, component)")
    parser.add_argument("--plan-only", action="store_true", help="Generate plan without execution")
    parser.add_argument("--format", choices=["json", "summary"], default="summary", help="Output format")
    args = parser.parse_args(argv)

    repo_profile = analyze_repository(args.project)
    existing_ui_profile = None
    preservation_profile = None

    if args.workflow == "existing-ui":
        try:
            existing_ui_profile = analyze_existing_ui(project=args.project, repo_profile=repo_profile)
            preservation_profile = build_preservation_profile(existing_ui_profile)
        except Exception:
            pass

    knowledge_plan = build_knowledge_plan(
        repo_profile=repo_profile,
        existing_ui_profile=existing_ui_profile,
        preservation_profile=preservation_profile,
        user_request=args.task,
        workflow=args.workflow,
        requested_scope=args.scope,
    )

    plan = plan_modification(
        user_request=args.task,
        workflow=args.workflow,
        repo_profile=repo_profile,
        existing_ui_profile=existing_ui_profile,
        preservation_profile=preservation_profile,
        knowledge_plan=knowledge_plan,
        requested_scope=args.scope,
        plan_only=args.plan_only,
    )

    if args.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        print(f"Plan ID: {plan['plan_id']}")
        print(f"Status: {plan['status'].upper()}")
        print(f"Scope: {plan['request']['requested_scope']}")
        print(f"Change Level: {plan['change_classification']['overall_level']}")
        print(f"Allowed Files ({len(plan['blast_radius']['allowed_files'])}):")
        for f in plan['blast_radius']['allowed_files']:
            print(f"  - {f}")
        print(f"Protected Files ({len(plan['blast_radius']['protected_files'])}):")
        for f in plan['blast_radius']['protected_files']:
            print(f"  - {f}")
        print(f"Steps: {len(plan['implementation_steps'])}")
        for step in plan['implementation_steps']:
            deps = f" (depends: {', '.join(step['dependencies'])})" if step['dependencies'] else ""
            print(f"  [{step['batch']}] {step['id']}: {step['action']} {step['target']}{deps}")
        print(f"Validation: {', '.join(plan['validation']['required_checks'])}")
        if plan['status_reasons']:
            print("Status Reasons:")
            for r in plan['status_reasons']:
                print(f"  * {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
