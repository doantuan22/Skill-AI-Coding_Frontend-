# Benchmark protocol: with vs without the Design Knowledge System

Prepares an A/B benchmark in which coding agents build the **same technology website from the same requirement**, once without and once with the Design Knowledge System. No benchmark website is included in this repository.

## Arms

| Arm | Agent context |
|---|---|
| A — baseline | The skill *without* `phase-2/knowledge/`, `phase-2/capability-resolver/`, the technology resolver, the performance budget, the extended motion catalogs and E65–E80 (e.g., checkout of the commit before this milestone), or no skill |
| B — knowledge system | The current skill, following the Phase 2 router, resolver and retrieval rules |

Keep the model, agent, tool permissions, time budget, requirement text and starter project identical. Run several seeds per arm (at least 3) because generation varies.

## Requirement set

Use the profiles in `evals/resolver-scenarios/` as briefs (their `intent`, attributes and content), at minimum:
`premium-ai-saas`, `developer-tool`, `enterprise-analytics-dashboard`, `luxury-ecommerce`, `creative-agency`. Give both arms the same natural-language brief. Only arm B uses the profile JSON through the resolver.

## Measures

| Measure | How | Source |
|---|---|---|
| Style diversity | Distinct primary visual languages across briefs, and pairwise similarity of selected style/layout/effect sets | Reviewer classification against the style catalog; arm B also has CAPABILITY-PLAN |
| Homogenization | Count of default-tell items (dark + purple gradient + glass + bento + giant heading, glow, particles) per site | Reviewer checklist + analyzer effect signals |
| Layout sophistication | E73 | Captures + review |
| Motion quality | E65, E66, E67, E68, E77, E78 | Analyzer + runner probes |
| Interaction quality | E69, E70, E79 | Analyzer + manual pass |
| Effect quality | E71, E72 | Analyzer + captures |
| Composition coherence | E75, E80 | Review against brief (arm A) or plan (arm B) |
| Premium detail | E76 | Analyzer detail signals + checklist |
| Accessibility | Existing accessibility gate (axe + manual) | Accessibility runtime |

## Procedure

1. For each brief, arm and seed: run the agent to completion in a fresh copy of the starter project.
2. Capture evidence with the existing runner (desktop + mobile, `motion_probe: true`, plus one reduced-motion capture). If no project-local Playwright exists, record `BLOCKED` and use static evidence only for that run. Do not install tools.
3. Run `python scripts/analyze_design_quality.py <site> --manifest <manifest> --visual-intensity <from brief>`.
4. Have two reviewers, blind to the arm, fill in `templates/DESIGN-QUALITY-REPORT.md` for the `NEEDS_REVIEW` items.
5. Aggregate: status distribution per eval per arm, homogenization counts, and diversity across briefs. Report variance across seeds; do not collapse results into one vanity score.

## Readiness checklist

- [x] Deterministic resolver with scenario tests and a diversity test (`tests/test_knowledge.py`)
- [x] Quality evals E65–E80 with evidence, heuristics, limitations and false positives
- [x] Static analyzer with discriminating fixtures (`tests/test_quality_analyzer.py`)
- [x] Runner options for motion probes and reduced-motion captures (unit-tested; browser execution pending a project-local Playwright)
- [ ] Starter project and briefs frozen for the benchmark run (to be created when the benchmark is scheduled)
- [ ] Live runtime verification of `motion_probe` in an environment with project-local Playwright
