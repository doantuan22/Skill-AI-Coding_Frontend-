import sys
import json
from pathlib import Path

# Setup paths
REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "plugins" / "ui-engineering"
for p in (REPO_ROOT / "tests", PLUGIN_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from uiux import api

print("=" * 60)
print("BENCHMARK SIMULATION RUNNER (S1-S4, D1-D4, Existing UI)")
print("=" * 60)

results = {}

# S1: Static Basic
print("\n--- Running S1: Static Basic ---")
s1_plan = api.build_knowledge_plan(
    user_request="Build clean static landing page with hero, cards and responsive layout",
    workflow="greenfield",
    repo_profile={"framework": {"name": "static_html", "version": None}, "styling": {"name": "css"}}
)
s1_cats = set(item.get("category") for item in s1_plan.get("selected_knowledge", []))
s1_ids = [item.get("id") for item in s1_plan.get("selected_knowledge", [])]
print(f"S1 Selected Count: {len(s1_ids)}, Categories: {sorted(s1_cats)}")
print(f"S1 Sample IDs: {s1_ids[:6]}")
results["S1"] = {"count": len(s1_ids), "categories": sorted(s1_cats), "ids": s1_ids}

# S2: SaaS Professional
print("\n--- Running S2: SaaS Professional ---")
s2_plan = api.build_knowledge_plan(
    user_request="Design a professional B2B SaaS landing page with pricing table and product FAQ",
    workflow="greenfield",
    repo_profile={"framework": {"name": "react", "version": "18.0.0"}, "domain": "saas_ai"}
)
s2_cats = set(item.get("category") for item in s2_plan.get("selected_knowledge", []))
s2_ids = [item.get("id") for item in s2_plan.get("selected_knowledge", [])]
print(f"S2 Domain: {s2_plan.get('domain_pack', {}).get('domain')}, Count: {len(s2_ids)}, Categories: {sorted(s2_cats)}")
print(f"S2 Sample IDs: {s2_ids[:8]}")
results["S2"] = {"domain": s2_plan.get("domain_pack", {}).get("domain"), "count": len(s2_ids), "categories": sorted(s2_cats), "ids": s2_ids}

# S3: Advanced Visual
print("\n--- Running S3: Advanced Visual ---")
s3_plan = api.build_knowledge_plan(
    user_request="Create visually stunning creative portfolio with glassmorphism effects, gradient meshes, and bold typography",
    workflow="greenfield",
    repo_profile={"framework": {"name": "static_html", "version": None}}
)
s3_cats = set(item.get("category") for item in s3_plan.get("selected_knowledge", []))
s3_ids = [item.get("id") for item in s3_plan.get("selected_knowledge", [])]
print(f"S3 Count: {len(s3_ids)}, Categories: {sorted(s3_cats)}")
print(f"S3 Sample IDs: {s3_ids[:8]}")
results["S3"] = {"count": len(s3_ids), "categories": sorted(s3_cats), "ids": s3_ids}

# S4: Advanced Motion
print("\n--- Running S4: Advanced Motion ---")
s4_plan = api.build_knowledge_plan(
    user_request="Implement animated hero entrance, scroll reveal stagger animations, and micro-interactions with reduced motion support",
    workflow="greenfield",
    repo_profile={"framework": {"name": "react", "version": "18.0.0"}, "dependencies": ["framer-motion"]}
)
s4_cats = set(item.get("category") for item in s4_plan.get("selected_knowledge", []))
s4_ids = [item.get("id") for item in s4_plan.get("selected_knowledge", [])]
print(f"S4 Count: {len(s4_ids)}, Categories: {sorted(s4_cats)}")
print(f"S4 Sample IDs: {s4_ids[:8]}")
results["S4"] = {"count": len(s4_ids), "categories": sorted(s4_cats), "ids": s4_ids}

# D1: React Dashboard
print("\n--- Running D1: React Dashboard ---")
d1_plan = api.build_knowledge_plan(
    user_request="Build full React analytics dashboard with collapsible sidebar, data table, search filters, and detail drawer",
    workflow="greenfield",
    repo_profile={"framework": {"name": "react", "version": "18.2.0"}, "styling": {"name": "tailwind"}}
)
d1_cats = set(item.get("category") for item in d1_plan.get("selected_knowledge", []))
d1_ids = [item.get("id") for item in d1_plan.get("selected_knowledge", [])]
print(f"D1 Count: {len(d1_ids)}, Categories: {sorted(d1_cats)}")
print(f"D1 Sample IDs: {d1_ids[:8]}")
results["D1"] = {"count": len(d1_ids), "categories": sorted(d1_cats), "ids": d1_ids}

# D2: Next.js + Tailwind SaaS
print("\n--- Running D2: Next.js + Tailwind SaaS ---")
d2_plan = api.build_knowledge_plan(
    user_request="Build Next.js Tailwind SaaS user management workspace with audit tables and settings forms",
    workflow="greenfield",
    repo_profile={"framework": {"name": "next", "version": "14.0.0"}, "styling": {"name": "tailwind"}, "package_json": {"dependencies": {"next": "14.0.0", "tailwindcss": "3.3.0"}}}
)
d2_cats = set(item.get("category") for item in d2_plan.get("selected_knowledge", []))
d2_ids = [item.get("id") for item in d2_plan.get("selected_knowledge", [])]
print(f"D2 Count: {len(d2_ids)}, Categories: {sorted(d2_cats)}")
print(f"D2 Sample IDs: {d2_ids[:8]}")
results["D2"] = {"count": len(d2_ids), "categories": sorted(d2_cats), "ids": d2_ids}

# D3: Advanced Interaction
print("\n--- Running D3: Advanced Interaction ---")
d3_plan = api.build_knowledge_plan(
    user_request="Add modal drawer, tabs navigation, quick command search and accessible keyboard shortcuts",
    workflow="existing-ui",
    repo_profile={"framework": {"name": "react", "version": "18.2.0"}}
)
d3_cats = set(item.get("category") for item in d3_plan.get("selected_knowledge", []))
d3_ids = [item.get("id") for item in d3_plan.get("selected_knowledge", [])]
print(f"D3 Count: {len(d3_ids)}, Categories: {sorted(d3_cats)}")
print(f"D3 Sample IDs: {d3_ids[:8]}")
results["D3"] = {"count": len(d3_ids), "categories": sorted(d3_cats), "ids": d3_ids}

# D4: Advanced Motion
print("\n--- Running D4: Advanced Motion ---")
d4_plan = api.build_knowledge_plan(
    user_request="Make responsive animated sidebar with smooth drawer transition and page transitions",
    workflow="existing-ui",
    repo_profile={"framework": {"name": "react", "version": "18.2.0"}}
)
d4_cats = set(item.get("category") for item in d4_plan.get("selected_knowledge", []))
d4_ids = [item.get("id") for item in d4_plan.get("selected_knowledge", [])]
print(f"D4 Count: {len(d4_ids)}, Categories: {sorted(d4_cats)}")
print(f"D4 Sample IDs: {d4_ids[:8]}")
results["D4"] = {"count": len(d4_ids), "categories": sorted(d4_cats), "ids": d4_ids}

# Existing UI Regression Benchmark
print("\n--- Running Existing UI Regression Benchmark ---")
existing_profile = {
    "palette": {"brand_primary": "#2563EB", "locked": True},
    "brand": {"name": "Acme SaaS", "logo_selector": "header .logo"},
    "navigation": {"routes": ["/dashboard", "/analytics", "/settings"]},
}
preservation = api.build_preservation_profile(
    existing_ui_profile=existing_profile,
    permissions={"color_palette": "L0_READONLY", "layout_grid": "L1_EXTEND", "brand_identity": "L0_READONLY"},
    requested_scope="bounded_feature"
)
exist_plan = api.build_knowledge_plan(
    user_request="Modernize dashboard, improve responsiveness and add subtle motion",
    workflow="existing-ui",
    existing_ui_profile=existing_profile,
    preservation_profile=preservation,
    repo_profile={"framework": {"name": "next", "version": "14.0.0"}, "styling": {"name": "tailwind"}}
)
mod_plan = api.plan_modification(
    user_request="Modernize dashboard, improve responsiveness and add subtle motion",
    workflow="existing-ui",
    knowledge_plan=exist_plan,
    preservation_profile=preservation
)
handoff = api.build_validation_handoff(plan=mod_plan)
critic_rep = api.run_runtime_validation(
    modification_plan=mod_plan,
    change_manifest={"files_modified": ["src/components/Dashboard.tsx"]},
    before_evidence=None,
    after_evidence=None,
    workflow="existing-ui",
    validate_only=True
)
eval_res = api.evaluate_runtime_result(critic_report=critic_rep)

print(f"Preservation Locked: {preservation.get('invariants', {}).get('color_palette', {}).get('policy')}")
print(f"Knowledge Plan Count: {len(exist_plan.get('selected_knowledge', []))}")
print(f"Modification Plan Steps: {len(mod_plan.get('implementation_steps', []))}")
print(f"Requires Runtime: {handoff.get('requires_runtime')}")
print(f"Critic Status on Empty Evidence: {eval_res.get('overall_status')}")
print(f"Authorized to Proceed: {eval_res.get('authorized_to_proceed')}")

results["ExistingUI"] = {
    "preservation_locked": True,
    "selected_knowledge_count": len(exist_plan.get("selected_knowledge", [])),
    "steps_count": len(mod_plan.get("implementation_steps", [])),
    "requires_runtime": handoff.get("requires_runtime"),
    "overall_status": eval_res.get("overall_status"),
    "authorized_to_proceed": eval_res.get("authorized_to_proceed"),
}

with open("scratch/benchmarks_summary.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nAll benchmark simulations completed successfully!")
