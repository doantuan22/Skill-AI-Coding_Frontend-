"""Eval execution: run the automated eval suites and describe the agent-run (manual) scenario suites.

Automated suites (executed here):
    structure         whole-skill validation (links, IDs, contracts, fixtures, plugin-ready metadata)
    knowledge         catalog schema/vocabulary/reference/index/registry checks
    resolver          resolver scenario expectations + anti-homogenization diversity
    quality-fixtures  analyzer statuses on evals/fixtures/quality against expectations.json

Behavioral scenarios E01-E80 test an *agent's* behavior; they cannot be executed by a script. The ``scenarios``
suite lists them (id, name, category, expected route) with status ``MANUAL`` so an adapter can hand them to an
agent run; it never reports them as passed.
"""
from __future__ import annotations

import json
import re

from uiux.core import resources

AUTOMATED_SUITES = ("structure", "knowledge", "resolver", "quality-fixtures")
ALL_SUITES = AUTOMATED_SUITES + ("scenarios",)


def _structure() -> dict:
    from uiux.tooling import validate  # noqa: PLC0415 - tooling is invoked on demand

    errors = validate.validate()
    return {"status": "FAIL" if errors else "PASS", "errors": errors}


def _knowledge() -> dict:
    from uiux.knowledge import catalog  # noqa: PLC0415

    errors = catalog.check()
    return {"status": "FAIL" if errors else "PASS", "errors": errors}


def _resolver() -> dict:
    from uiux.evals import resolver_scenarios  # noqa: PLC0415

    result = resolver_scenarios.run()
    result.pop("plans")
    return result


def quality_fixture_results() -> dict:
    from uiux.evals import quality  # noqa: PLC0415

    root = resources.get_quality_fixtures_root()
    spec = json.loads((root / "expectations.json").read_text(encoding="utf-8"))
    results = []
    for name, expect in spec["fixtures"].items():
        evals = quality.analyze(root / name)["evals"]
        failures = [f"{eid}: {evals[eid]['status']} != {status}" for eid, status in expect.get("must_equal", {}).items()
                    if evals[eid]["status"] != status]
        failures += [f"{eid}: {evals[eid]['status']} not in {allowed}" for eid, allowed in expect.get("must_be_one_of", {}).items()
                     if evals[eid]["status"] not in allowed]
        failures += [f"{eid}: forbidden status {item['status']}" for eid, item in evals.items() if item["status"] in expect.get("never", [])]
        results.append({"fixture": name, "status": "FAIL" if failures else "PASS", "failures": failures})
    return {"status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL", "results": results}


def _scenario_frontmatter(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    values = {}
    for line in (match.group(1).splitlines() if match else []):
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def scenarios(ids: list[str] | None = None) -> dict:
    rows = []
    for path in sorted(resources.get_scenarios_root().glob("E*.md")):
        meta = _scenario_frontmatter(path.read_text(encoding="utf-8"))
        if ids and meta.get("id") not in ids:
            continue
        rows.append({"id": meta.get("id"), "name": meta.get("name"), "category": meta.get("category"),
                     "expected_route": meta.get("expected_route"), "file": resources.relative(path), "status": "MANUAL"})
    return {"status": "MANUAL", "count": len(rows), "scenarios": rows,
            "note": "Agent-behavior evals: run with an agent and record results with evals/result-template.md."}


def run(suites: list[str] | tuple[str, ...] = AUTOMATED_SUITES, scenario_ids: list[str] | None = None) -> dict:
    unknown = [s for s in suites if s not in ALL_SUITES]
    if unknown:
        raise ValueError(f"unknown eval suites: {', '.join(unknown)}; expected {', '.join(ALL_SUITES)}")
    handlers = {"structure": _structure, "knowledge": _knowledge, "resolver": _resolver,
                "quality-fixtures": quality_fixture_results, "scenarios": lambda: scenarios(scenario_ids)}
    results = {suite: handlers[suite]() for suite in suites}
    automated = [r["status"] for s, r in results.items() if s in AUTOMATED_SUITES]
    status = "FAIL" if "FAIL" in automated else "PASS" if automated else "MANUAL"
    return {"status": status, "suites": results}
