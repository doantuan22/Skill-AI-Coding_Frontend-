"""Lightweight structural validator for the UI/UX workflow skill; standard library only."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SCENARIO_FIELDS = {
    "id", "name", "category", "project_state", "user_request", "expected_route",
    "required_artifacts", "forbidden_behavior", "expected_context",
    "success_conditions", "failure_conditions",
}
STATES = {
    "INITIAL", "ANALYZING", "PHASE_1", "PHASE_1_REVIEW", "STRUCTURE_LOCKED",
    "PHASE_2", "PHASE_2_REVIEW", "FINAL_REVIEW", "DONE", "BLOCKED",
}
REQUIRED_FILES = {
    "SKILL.md", "workflow/execution-contract.md", "workflow/reference-loading.md",
    "workflow/reference-index.md", "workflow/change-impact.md", "workflow/rollback-matrix.md",
    "workflow/chunking-strategy.md", "templates/ARTIFACT-REGISTRY.md",
    "templates/CONTEXT-MANIFEST.md", "templates/TASK-SCOPE.md",
    "templates/COMPLETION-EVIDENCE.md", "evals/framework.md", "evals/rubric.md",
    "evals/result-template.md", "evals/failure-taxonomy.md", "evals/reports/EVAL-SUMMARY.md",
    "execution/README.md", "execution/capability-detection.md", "execution/execution-router.md",
    "execution/execution-requirement.md", "execution/application-runtime.md", "execution/browser-contract.md",
    "execution/evidence-contract.md", "execution/viewports.md", "execution/failure-handling.md",
    "execution/adapters/playwright.md", "execution/adapters/manual.md",
    "workflow/execution-requirement.md", "templates/TOOL-CAPABILITY-MANIFEST.md",
    "templates/EXECUTION-REPORT.md", "docs/execution-layer.md",
    "execution/viewports.json", "execution/runtime/README.md", "execution/runtime/runner-contract.md",
    "execution/runtime/runtime-input.md", "execution/runtime/runtime-output.md", "execution/runtime/session-lifecycle.md",
    "execution/runtime/runtime-errors.md", "execution/storage/README.md", "execution/storage/manifest-schema.md",
    "execution/storage/evidence-layout.md", "execution/storage/retention.md", "docs/execution-runtime.md",
    "scripts/run_browser_execution.py", "scripts/validate_runtime_evidence.py",
    "docs/research/visual-skill-integration-analysis.md", "templates/VISUAL-GRAMMAR.md",
    "evals/reports/VISUAL-LANGUAGE-DRY-RUN.md",
    "phase-2/visual-language/README.md", "phase-2/visual-language/workflow.md",
    "phase-2/visual-language/visual-grammar.md", "phase-2/visual-language/craft-review.md",
    "phase-2/visual-language/adversarial-review.md", "phase-2/visual-language/ai-tell-density.md",
    "phase-2/visual-language/components/buttons.md", "phase-2/visual-language/components/feedback.md",
    "phase-2/visual-language/components/iconography.md",
}
INSPIRATION_FILES = {
    "phase-2/design-inspiration/README.md", "phase-2/design-inspiration/workflow.md",
    "phase-2/design-inspiration/archetypes.md", "phase-2/design-inspiration/reference-profiles.md",
    "phase-2/design-inspiration/reference-extraction.md", "phase-2/design-inspiration/pattern-selection.md",
    "phase-2/design-inspiration/anti-copying.md",
    "phase-2/typography/README.md", "phase-2/typography/typography-archetypes.md",
    "phase-2/typography/font-selection.md", "phase-2/typography/font-pairing.md",
    "phase-2/typography/display-type.md", "phase-2/typography/body-type.md",
    "phase-2/typography/technical-type.md", "phase-2/typography/typography-rhythm.md",
    "phase-2/typography/typographic-composition.md", "phase-2/typography/typography-review.md",
    "phase-2/motion/README.md", "phase-2/motion/motion-principles.md", "phase-2/motion/motion-character.md",
    "phase-2/motion/motion-vocabulary.md", "phase-2/motion/scroll-motion.md", "phase-2/motion/microinteractions.md",
    "phase-2/motion/spatial-motion.md", "phase-2/motion/text-motion.md", "phase-2/motion/reduced-motion.md",
    "phase-2/motion/performance-safety.md", "phase-2/motion/motion-review.md",
    "phase-2/web-patterns/README.md", "phase-2/web-patterns/hero/hero-patterns.md",
    "phase-2/web-patterns/sections/section-patterns.md", "phase-2/web-patterns/storytelling/storytelling-patterns.md",
    "phase-2/web-patterns/navigation/navigation-patterns.md",
    "phase-2/web-patterns/product-showcase/interaction-patterns.md",
    "phase-2/web-patterns/conversion/conversion-patterns.md", "phase-2/web-patterns/content/content-patterns.md",
    "phase-2/web-patterns/composition/composition-patterns.md",
    "phase-2/web-patterns/motion-composition/motion-composition.md",
    "templates/DESIGN-INSPIRATION.md", "templates/MOTION-SYSTEM.md",
    "evals/reports/INSPIRATION-DRY-RUN.md",
}
REQUIRED_FILES |= INSPIRATION_FILES
INSPIRATION_MODULES = ("phase-2/design-inspiration", "phase-2/typography", "phase-2/motion", "phase-2/web-patterns")
KNOWLEDGE_FILES = {
    "phase-2/knowledge/README.md", "phase-2/knowledge/schema.md", "phase-2/knowledge/retrieval.md", "phase-2/knowledge/INDEX.md",
    "phase-2/knowledge/advanced-accessibility.md", "phase-2/knowledge/styles/README.md", "phase-2/knowledge/effects/README.md",
    "phase-2/knowledge/interactions/README.md", "phase-2/knowledge/screens/README.md", "phase-2/knowledge/graphics/techniques.md",
    "phase-2/knowledge/composition/README.md", "phase-2/knowledge/composition/recipes.md",
    "phase-2/knowledge/composition/anti-homogenization.md", "phase-2/knowledge/composition/premium-quality-model.md",
    "phase-2/capability-resolver/README.md", "phase-2/capability-resolver/resolver.md",
    "phase-2/05-frontend-implementation/technology-resolver.md", "phase-2/05-frontend-implementation/performance-budget.md",
    "phase-2/motion/layout-motion.md", "phase-2/motion/cinematic-motion.md", "phase-2/motion/responsive-motion.md",
    "phase-2/web-patterns/grid/grid-patterns.md", "phase-2/web-patterns/storytelling/story-layouts.md",
    "phase-2/web-patterns/application/application-layouts.md", "phase-2/visual-language/components/README.md",
    "phase-2/visual-language/components/ai-interfaces.md", "phase-2/visual-language/components/command-search.md",
    "phase-2/visual-language/components/data-display.md",
    "templates/CAPABILITY-PLAN.md", "templates/DESIGN-QUALITY-REPORT.md", "evals/quality/README.md",
    "docs/design-knowledge-system.md", "docs/benchmark-protocol.md", "evals/reports/DESIGN-KNOWLEDGE-DRY-RUN.md",
    "scripts/knowledge_lib.py", "scripts/resolve_capabilities.py", "scripts/analyze_design_quality.py",
    "scripts/test_knowledge.py", "scripts/test_quality_analyzer.py",
    "evals/fixtures/quality/overanimated/index.html", "evals/fixtures/quality/restrained/index.html",
}
REQUIRED_FILES |= KNOWLEDGE_FILES
KNOWLEDGE_MODULES = ("phase-2/knowledge", "phase-2/capability-resolver")
DESIGN_QUALITY_SECTIONS = ("## Purpose", "## Input", "## Evidence", "## Heuristics", "## Pass / fail criteria",
                           "## Limitations", "## False positives")
KNOWLEDGE_CODES = ("SCROLL_HIJACKING", "MOTION_LAYOUT_INSTABILITY", "COMPETING_MOTION_DIRECTIONS", "CAPABILITY_PLAN_MISSING",
                   "HOMOGENIZED_DESIGN", "STYLE_INCOHERENCE", "PREMIUM_BY_EFFECTS", "EFFECT_OVERUSE",
                   "INTERACTION_FEEDBACK_MISSING", "HOVER_ONLY_INTERACTION", "HIDDEN_INTERACTION",
                   "HEAVY_DEPENDENCY_FOR_SIMPLE_EFFECT")
ARCHETYPES = ("premium-product", "modern-saas", "developer-tool", "technical-platform", "editorial-product",
              "creative-portfolio", "marketplace", "travel-commerce", "luxury", "consumer-tech",
              "data-heavy-product", "minimal-product")
TYPE_ARCHETYPES = ("neutral-product", "premium-modern", "editorial", "technical", "developer",
                   "friendly-consumer", "luxury", "dense-transactional", "expressive-marketing")
REVIEW_CODES = (
    "GENERIC_TEMPLATE_COMPOSITION", "REFERENCE_COPYING", "INSPIRATION_DIRECTION_MISSING",
    "INCOMPATIBLE_REFERENCE_MIX", "PATTERN_MISUSE", "VISUAL_STORYTELLING_WEAK",
    "TYPOGRAPHY_CHARACTER_MISSING", "WEAK_TYPE_HIERARCHY", "EXCESSIVE_FONT_FAMILIES", "DISPLAY_FONT_MISUSE",
    "POOR_READING_MEASURE", "MONO_OVERUSE", "TYPE_STYLE_DRIFT",
    "MOTION_FOR_DECORATION", "EXCESSIVE_ENTRANCE_ANIMATION", "EVERYTHING_ANIMATED", "SLOW_INTERACTION",
    "SCROLL_JANK_RISK", "MOTION_WITHOUT_REDUCED_MODE", "MOTION_STYLE_DRIFT", "UNJUSTIFIED_PARALLAX",
)
# Binary/media/font assets are allowed only in research checkouts and runtime evidence fixtures.
ASSET_EXTENSIONS = {".woff", ".woff2", ".ttf", ".otf", ".eot", ".png", ".jpg", ".jpeg", ".gif", ".webp",
                    ".avif", ".svg", ".mp4", ".webm", ".mov", ".lottie"}
FONT_EXTENSIONS = {".woff", ".woff2", ".ttf", ".otf", ".eot"}
ASSET_ALLOWED_ROOTS = ("external-references/", "evals/runtime-fixtures/")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")
    for path in root.rglob("*.md"):
        for target in pattern.findall(text(path)):
            if re.match(r"^[a-z]+:", target):
                continue
            if not (path.parent / target).exists():
                errors.append(f"broken link: {path.relative_to(root)} -> {target}")
    return errors


def frontmatter(path: Path) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", text(path), re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def scenario_checks(root: Path) -> list[str]:
    errors: list[str] = []
    ids: dict[str, Path] = {}
    scenarios = sorted((root / "evals/scenarios").glob("E*.md"))
    for path in scenarios:
        values = frontmatter(path)
        missing = SCENARIO_FIELDS - values.keys()
        if missing:
            errors.append(f"scenario missing fields: {path.name}: {', '.join(sorted(missing))}")
        scenario_id = values.get("id", "")
        if not re.fullmatch(r"E\d{2}", scenario_id):
            errors.append(f"invalid scenario id: {path.name}: {scenario_id or '<missing>'}")
        elif scenario_id in ids:
            errors.append(f"duplicate scenario id: {scenario_id} in {ids[scenario_id].name} and {path.name}")
        else:
            ids[scenario_id] = path
    expected = {f"E{i:02d}" for i in range(1, 81)}
    if set(ids) != expected:
        errors.append(f"scenario suite must contain E01-E80; found {', '.join(sorted(ids))}")
    return errors


def workflow_checks(root: Path) -> list[str]:
    errors: list[str] = []
    state_machine = text(root / "workflow/state-machine.md")
    transitions = text(root / "workflow/phase-transition.md")
    phase2 = text(root / "phase-2/README.md")
    for state in STATES:
        if state not in state_machine:
            errors.append(f"unreachable or undocumented state: {state}")
    for transition in ("INITIAL → ANALYZING", "PHASE_1_REVIEW (pass) → STRUCTURE_LOCKED",
                       "STRUCTURE_LOCKED → PHASE_2", "PHASE_2_REVIEW (pass) → FINAL_REVIEW",
                       "FINAL_REVIEW (pass) → DONE"):
        if transition not in transitions:
            errors.append(f"missing required transition: {transition}")
    if "do not change business flows" not in phase2.lower() or "STRUCTURE-LOCK" not in phase2:
        errors.append("Phase 2 Structure Lock immutability rule missing")
    visual_router = text(root / "phase-2/router.md")
    visual_workflow = text(root / "phase-2/workflow.md")
    visual_readme = text(root / "phase-2/visual-language/README.md")
    for phrase in ("visual-language/components/buttons.md", "components/feedback.md", "components/iconography.md", "anti-slop/global.md"):
        if phrase not in visual_router:
            errors.append(f"Phase 2 selective visual-language route missing: {phrase}")
    for phrase in ("visual language", "craft review", "adversarial review"):
        if phrase not in visual_workflow.lower():
            errors.append(f"Phase 2 visual-language workflow step missing: {phrase}")
    for phrase in ("Design System", "Visual Grammar", "Component Spec"):
        if phrase not in visual_readme:
            errors.append(f"Visual-language source-of-truth boundary missing: {phrase}")
    # The documented dependency DAG mirrors the artifact contract's one-way lifecycle.
    graph = {
        "requirements": {"phase_1"}, "phase_1": {"structure_lock"},
        "structure_lock": {"phase_2"}, "phase_2": {"reviews"}, "reviews": {"final_review"},
        "final_review": set(),
    }
    visiting, visited = set(), set()
    def visit(node: str) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        result = all(visit(child) for child in graph[node])
        visiting.remove(node)
        visited.add(node)
        return result
    if not all(visit(node) for node in graph):
        errors.append("artifact circular dependency detected")
    for phase in ("phase-1/references", "phase-2/references"):
        headings: dict[str, Path] = {}
        for path in (root / phase).rglob("*.md"):
            heading = next((line[2:].strip().lower() for line in text(path).splitlines() if line.startswith("# ")), "")
            if heading in headings:
                errors.append(f"duplicate reference purpose: {phase}/{path.name} and {headings[heading].name}")
            headings[heading] = path
    return errors


def execution_checks(root: Path) -> list[str]:
    errors: list[str] = []
    router = text(root / "execution/execution-router.md")
    browser = text(root / "execution/browser-contract.md")
    fallback = text(root / "execution/adapters/manual.md")
    viewports = text(root / "execution/viewports.md")
    gate = text(root / "phase-2/08-final-quality-gate/final-gate.md")
    for phrase in ("Existing agent-provided supported browser/tool capability", "Existing project Playwright setup", "Manual fallback"):
        if phrase not in router:
            errors.append(f"execution strategy priority missing: {phrase}")
    for operation in ("open(url)", "navigate(route)", "set_viewport(width, height)", "capture()", "close()"):
        if operation not in browser:
            errors.append(f"browser contract operation missing: {operation}")
    if "never implies" not in fallback:
        errors.append("manual fallback honesty rule missing")
    for viewport in ("desktop_wide", "desktop", "tablet", "mobile"):
        if not re.search(rf"^{viewport}:\n\s+width: \d+\n\s+height: \d+", viewports, re.MULTILINE):
            errors.append(f"invalid or missing viewport registry entry: {viewport}")
    if "execution evidence" not in gate.lower() or "required execution was not completed" not in gate or "is forbidden" not in gate:
        errors.append("final quality execution-evidence gate missing")
    try:
        registry = json.loads((root / "execution/viewports.json").read_text(encoding="utf-8"))
        if registry.get("schema_version") != 1:
            errors.append("viewport JSON schema_version must be 1")
        for viewport in ("desktop_wide", "desktop", "tablet", "mobile"):
            value = registry.get(viewport, {})
            if not isinstance(value.get("width"), int) or not isinstance(value.get("height"), int):
                errors.append(f"invalid viewport JSON entry: {viewport}")
    except (OSError, json.JSONDecodeError):
        errors.append("viewport JSON is invalid")
    for fixture in ("evals/runtime-fixtures/static-page/index.html", "evals/runtime-fixtures/playwright-ready/package.json",
                    "evals/runtime-fixtures/requests/two-viewports.json", "evals/runtime-fixtures/evidence-valid/manifest.json"):
        if not (root / fixture).is_file(): errors.append(f"missing runtime fixture: {fixture}")
    for item in ("execution/accessibility/README.md", "execution/accessibility/gate.md", "execution/accessibility/manual-review.md", "execution/accessibility/evidence-schema.md", "scripts/run_accessibility_scan.py", "scripts/validate_accessibility_evidence.py", "templates/ACCESSIBILITY-REPORT.md"):
        if not (root / item).is_file(): errors.append(f"missing accessibility runtime file: {item}")
    return errors


def inspiration_checks(root: Path) -> list[str]:
    errors: list[str] = []
    router = text(root / "phase-2/router.md")
    for module in ("design-inspiration/", "typography/", "motion/", "web-patterns/", "reference-extraction.md", "anti-copying.md"):
        if module not in router:
            errors.append(f"Phase 2 router does not route to: {module}")
    skill = text(root / "SKILL.md")
    for module in INSPIRATION_MODULES:
        if module + "/README.md" not in skill:
            errors.append(f"SKILL.md does not link module: {module}")
    index = text(root / "workflow/reference-index.md")
    for target in re.findall(r"^\s+file: (\S+)$", index, re.MULTILINE):
        if not (root / target).is_file():
            errors.append(f"reference index points to missing file: {target}")
    for module in INSPIRATION_MODULES:
        if module + "/" not in index:
            errors.append(f"reference index missing entry for: {module}")
    archetypes = text(root / "phase-2/design-inspiration/archetypes.md")
    for name in ARCHETYPES:
        if f"## {name}" not in archetypes:
            errors.append(f"design archetype missing: {name}")
    type_archetypes = text(root / "phase-2/typography/typography-archetypes.md")
    for name in TYPE_ARCHETYPES:
        if f"`{name}`" not in type_archetypes:
            errors.append(f"typography archetype missing: {name}")
    profiles = text(root / "phase-2/design-inspiration/reference-profiles.md")
    profile_count = len(re.findall(r"^## .+\(.+-like\)$", profiles, re.MULTILINE))
    if profile_count == 0 or profile_count != profiles.count("never_transfer:"):
        errors.append("every reference profile needs a never_transfer list")
    if "Vietnamese" not in text(root / "phase-2/typography/font-selection.md"):
        errors.append("font selection lacks Vietnamese coverage rules")
    if "## Intensity budget" not in text(root / "phase-2/motion/motion-principles.md"):
        errors.append("motion intensity budget missing")
    if "prefers-reduced-motion" not in text(root / "phase-2/motion/reduced-motion.md"):
        errors.append("reduced-motion rule missing")
    taxonomy = text(root / "evals/failure-taxonomy.md")
    for code in REVIEW_CODES:
        if f"`{code}`" not in taxonomy:
            errors.append(f"failure taxonomy missing code: {code}")
    craft = text(root / "phase-2/visual-language/craft-review.md")
    for lens in ("typography-review", "motion-review", "anti-copying", "GENERIC_TEMPLATE_COMPOSITION"):
        if lens not in craft:
            errors.append(f"craft review missing inspiration lens: {lens}")
    # Single source of truth: Visual Language delegates; typography lives in DESIGN-SYSTEM.md.
    for path, owner in (("phase-2/visual-language/typography-character.md", "../typography/README.md"),
                        ("phase-2/visual-language/motion-character.md", "../motion/README.md")):
        if owner not in text(root / path):
            errors.append(f"{path} must delegate to {owner}")
    if (root / "templates/TYPOGRAPHY-SYSTEM.md").exists():
        errors.append("duplicate source of truth: typography belongs in DESIGN-SYSTEM.md")
    if "## Typography system" not in text(root / "templates/DESIGN-SYSTEM.md"):
        errors.append("DESIGN-SYSTEM template lacks Typography system section")
    # Knowledge only: no runtime dependency on external websites, no bundled/copied assets.
    for module in INSPIRATION_MODULES + KNOWLEDGE_MODULES:
        for path in (root / module).rglob("*"):
            if path.is_file() and path.suffix != ".md":
                errors.append(f"non-knowledge file in {module}: {path.relative_to(root)}")
            elif path.is_file() and re.search(r"https?://", text(path)):
                errors.append(f"external URL (runtime dependency) in {path.relative_to(root)}")
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in ASSET_EXTENSIONS:
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in FONT_EXTENSIONS and not rel.startswith("external-references/"):
            errors.append(f"vendored font file: {rel}")
        elif not rel.startswith(ASSET_ALLOWED_ROOTS):
            errors.append(f"unexpected media asset (possible copied reference asset): {rel}")
    return errors


def knowledge_checks(root: Path) -> list[str]:
    """Design Knowledge System: catalogs, routing, resolver scenarios, quality evals."""
    errors: list[str] = []
    try:
        sys.path.insert(0, str(root / "scripts"))
        import knowledge_lib  # noqa: PLC0415 - validator stays importable without the knowledge base
        errors += [f"knowledge: {e}" for e in knowledge_lib.check(root)]
    except Exception as exc:  # report, never crash the validator
        errors.append(f"knowledge base could not be validated: {exc}")
    router = text(root / "phase-2/router.md")
    for phrase in ("capability-resolver/README.md", "knowledge/retrieval.md", "technology-resolver.md", "performance-budget.md",
                   "cinematic-motion.md", "layout-motion.md", "evals/quality/README.md"):
        if phrase not in router:
            errors.append(f"Phase 2 router does not route to: {phrase}")
    skill = text(root / "SKILL.md")
    for phrase in ("phase-2/knowledge/README.md", "phase-2/capability-resolver/README.md"):
        if phrase not in skill:
            errors.append(f"SKILL.md does not link: {phrase}")
    index = text(root / "workflow/reference-index.md")
    for phrase in ("phase-2/knowledge/", "phase-2/capability-resolver/", "technology-resolver.md", "evals/quality/README.md"):
        if phrase not in index:
            errors.append(f"reference index missing entry for: {phrase}")
    scenarios = list((root / "evals/resolver-scenarios").glob("*.json"))
    if len(scenarios) < 8:
        errors.append("at least 8 resolver scenarios are required")
    for path in scenarios:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not {"profile", "expect"} <= set(data):
                errors.append(f"resolver scenario lacks profile/expect: {path.name}")
        except json.JSONDecodeError:
            errors.append(f"resolver scenario is invalid JSON: {path.name}")
    for number in range(65, 81):
        matches = list((root / "evals/scenarios").glob(f"E{number}-*.md"))
        if matches:
            body = text(matches[0])
            missing = [s for s in DESIGN_QUALITY_SECTIONS if s not in body]
            if missing:
                errors.append(f"design quality eval E{number} missing sections: {', '.join(missing)}")
    taxonomy = text(root / "evals/failure-taxonomy.md")
    for code in KNOWLEDGE_CODES:
        if f"`{code}`" not in taxonomy:
            errors.append(f"failure taxonomy missing code: {code}")
    framework = text(root / "evals/framework.md")
    if "DESIGN_QUALITY = E65–E80" not in framework or "FULL = E01–E80" not in framework:
        errors.append("eval framework suites not updated for E65-E80")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors = [f"missing required file: {item}" for item in REQUIRED_FILES if not (root / item).is_file()]
    errors += markdown_links(root)
    errors += scenario_checks(root)
    errors += workflow_checks(root)
    errors += execution_checks(root)
    errors += inspiration_checks(root)
    errors += knowledge_checks(root)
    if errors:
        print("Validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Skill hardening validation passed.")
    print("- required files, links, workflow states/transitions, lock rule, and dependency DAG valid")
    print("- E01-E80 IDs, required scenario fields, execution/runtime/accessibility/visual-language contracts, and fixtures valid")
    print("- inspiration/typography/motion/web-pattern modules, routing, taxonomy, single source of truth, no vendored fonts or copied assets")
    print("- design knowledge catalogs (schema, vocabularies, references, index), resolver scenarios, E65-E80 eval sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
