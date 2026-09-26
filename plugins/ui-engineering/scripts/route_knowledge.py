"""CLI entry point for Knowledge Router. Implementation: ``uiux.engine.knowledge_router``."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _bootstrap

_bootstrap.alias(__name__, "uiux.engine.knowledge_router")

from uiux.engine.existing_ui import analyze_existing_ui, build_preservation_profile
from uiux.engine.knowledge_router import build_knowledge_plan
from uiux.engine.repo_intelligence import analyze_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Knowledge Router CLI")
    parser.add_argument("--project", default=".", help="Target project directory")
    parser.add_argument("--task", default="", help="User request or task description")
    parser.add_argument("--workflow", choices=["greenfield", "existing-ui", "unknown"], default="existing-ui", help="UI Workflow")
    parser.add_argument("--scope", default="global", help="Requested scope (global, page, component)")
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

    plan = build_knowledge_plan(
        repo_profile=repo_profile,
        existing_ui_profile=existing_ui_profile,
        preservation_profile=preservation_profile,
        user_request=args.task,
        workflow=args.workflow,
        requested_scope=args.scope,
    )

    if args.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        fw_packs = [p["id"] for p in plan["selected_packs"]["framework"]]
        st_packs = [p["id"] for p in plan["selected_packs"]["styling"]]
        ui_packs = [p["id"] for p in plan["selected_packs"]["ui_library"]]
        dom_packs = [p["id"] for p in plan["selected_packs"].get("domain", [])]
        rt_packs = [p["id"] for p in plan["selected_packs"]["runtime"]]
        skills = [s["id"] for s in plan["selected_skills"]]
        knowledge = [k["id"] for k in plan["selected_knowledge"]]

        print(f"workflow: {plan['workflow']}")
        print(f"task_intent: {plan['task_intent']}")
        print(f"framework: {', '.join(fw_packs) or 'none'}")
        print(f"styling: {', '.join(st_packs) or 'none'}")
        if ui_packs:
            print(f"ui_library: {', '.join(ui_packs)}")
        if dom_packs:
            print(f"domain: {', '.join(dom_packs)}")
        print("selected:")
        for item_id in plan["load_order"]:
            print(f"  - {item_id}")
        print(f"budget: {plan['context_budget']['used_points']}/{plan['context_budget']['budget_limit_points']} pts ({plan['context_budget']['budget_status']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
