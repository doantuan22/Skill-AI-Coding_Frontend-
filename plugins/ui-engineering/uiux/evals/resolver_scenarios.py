"""Resolver scenario evaluation: expectations and anti-homogenization diversity over evals/resolver-scenarios/.

Shared by ``uiux.evals.runner`` (the ``resolver`` suite) and tests/test_knowledge.py.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

from uiux.core import resources
from uiux.engine import capability_resolver as R


def scenario_paths() -> list[Path]:
    return sorted(resources.get_resolver_scenarios_root().glob("*.json"))


def load(path: Path) -> tuple[dict, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["profile"], data["expect"]


def expectation_failures(plan: dict, expect: dict) -> list[str]:
    """Human-readable failures of one plan against its scenario expectations (empty list = pass)."""
    failures: list[str] = []
    primary = plan["style"]["primary"]["id"]
    styles = {primary} | ({plan["style"]["secondary"]["id"]} if plan["style"]["secondary"] else set())
    effects = {e["id"] for e in plan["effects"]["selected"]}
    tiers = {m["tier"] for m in plan["motion"]["selected"]}
    interactions = {i["id"] for i in plan["interactions"]["selected"]}
    tech = plan["technology"]
    if "primary_style_any" in expect and primary not in expect["primary_style_any"]:
        failures.append(f"primary style {primary} not in {expect['primary_style_any']}")
    if styles & set(expect.get("exclude_styles", [])):
        failures.append(f"excluded styles selected: {sorted(styles & set(expect['exclude_styles']))}")
    if effects & set(expect.get("exclude_effects", [])):
        failures.append(f"excluded effects selected: {sorted(effects & set(expect['exclude_effects']))}")
    if tiers & set(expect.get("forbid_tiers", [])):
        failures.append(f"forbidden motion tiers selected: {sorted(tiers & set(expect['forbid_tiers']))}")
    if "require_tiers_any" in expect and not tiers & set(expect["require_tiers_any"]):
        failures.append(f"none of the required tiers {expect['require_tiers_any']} selected")
    if "include_interactions_any" in expect and not interactions & set(expect["include_interactions_any"]):
        failures.append(f"none of the interactions {expect['include_interactions_any']} selected")
    if "max_new_dependencies" in expect and len(tech["new_dependencies"]) > expect["max_new_dependencies"]:
        failures.append(f"too many new dependencies: {tech['new_dependencies']}")
    if "new_dependencies_subset" in expect and not set(tech["new_dependencies"]) <= set(expect["new_dependencies_subset"]):
        failures.append(f"unexpected new dependencies: {tech['new_dependencies']}")
    for reuse in expect.get("reuse_technologies", []):
        if reuse not in tech["existing_reused"]:
            failures.append(f"existing technology {reuse} not reused")
    for excluded in expect.get("retrieval_excludes", []):
        if excluded in plan["retrieval"]:
            failures.append(f"retrieval loads excluded file {excluded}")
    if plan["guards"]["homogenized"]:
        failures.append("plan is homogenized")
    if sum(1 for m in plan["motion"]["selected"] if m["intensity"] == "high") > R.MAX_HIGH_REGIONS:
        failures.append("more HIGH motion regions than the budget allows")
    if plan["effects"]["budget"]["used"] > plan["effects"]["budget"]["limit"]:
        failures.append("effect budget exceeded")
    if not plan["style"]["primary"]["why"]:
        failures.append("primary style has no WHY")
    return failures


def signature(plan: dict) -> set[str]:
    return ({plan["style"]["primary"]["id"]} | {l["id"] for l in plan["layouts"]["selected"]}
            | {e["id"] for e in plan["effects"]["selected"]})


def diversity(plans: dict[str, dict]) -> dict:
    """Anti-homogenization metrics across scenario plans."""
    sets = [signature(p) for p in plans.values()]
    pairs = list(itertools.combinations(sets, 2))
    mean = sum(len(a & b) / len(a | b) for a, b in pairs) / len(pairs) if pairs else 0.0
    primaries = [p["style"]["primary"]["id"] for p in plans.values()]
    keys = [(p["style"]["primary"]["id"], tuple(l["id"] for l in p["layouts"]["selected"]), p["effects"]["signature"])
            for p in plans.values()]
    default_look = {"layout.grid-bento", "effect.gradient", "effect.glass"}
    return {"scenarios": len(plans), "distinct_primary_styles": len(set(primaries)),
            "unique_compositions": len(set(keys)) == len(keys), "mean_jaccard": round(mean, 4),
            "default_tech_look": sorted(n for n, p in plans.items() if default_look <= signature(p))}


def run(entries: dict[str, dict] | None = None) -> dict:
    """Resolve every scenario and check expectations + diversity. status is PASS or FAIL."""
    plans, results = {}, []
    for path in scenario_paths():
        profile, expect = load(path)
        plan = R.resolve(profile, entries)
        plans[path.stem] = plan
        failures = expectation_failures(plan, expect)
        results.append({"scenario": path.stem, "status": "FAIL" if failures else "PASS", "failures": failures,
                        "primary_style": plan["style"]["primary"]["id"]})
    metrics = diversity(plans)
    diversity_failures = []
    if metrics["distinct_primary_styles"] < metrics["scenarios"] - 1:
        diversity_failures.append("primary styles are not diverse enough")
    if not metrics["unique_compositions"]:
        diversity_failures.append("two scenarios share a composition")
    if metrics["mean_jaccard"] >= 0.2:
        diversity_failures.append(f"mean Jaccard {metrics['mean_jaccard']} >= 0.2")
    if len(metrics["default_tech_look"]) > 1:
        diversity_failures.append(f"default tech look in {metrics['default_tech_look']}")
    ok = all(r["status"] == "PASS" for r in results) and not diversity_failures
    return {"status": "PASS" if ok else "FAIL", "results": results, "diversity": metrics,
            "diversity_failures": diversity_failures, "plans": plans}
