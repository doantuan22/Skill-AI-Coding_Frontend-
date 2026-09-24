"""Knowledge retrieval for a capability plan: the only catalog files an agent should load for the task.

Category gating rules: phase-2/knowledge/retrieval.md.
"""
from __future__ import annotations


def retrieval(entries: dict[str, dict], plan: dict) -> list[str]:
    ids = [plan["style"]["primary"]["id"]]
    if plan["style"]["secondary"]:
        ids.append(plan["style"]["secondary"]["id"])
    for section, key in (("layouts", "selected"), ("screens", None), ("motion", "selected"),
                         ("interactions", "selected"), ("effects", "selected")):
        items = plan[section] if key is None else plan[section][key]
        ids += [i["id"] for i in items]
    ids += plan["technology"]["technologies"] + [plan["recipe"]["anchor"]]
    files: list[str] = []
    for i in ids:
        f = entries[i]["_file"]
        if f not in files:
            files.append(f)
    return files
