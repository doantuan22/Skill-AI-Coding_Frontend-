import os
from pathlib import Path
import re

base = Path("plugins/ui-engineering")

def replace_links(file_path: Path, replacements: list[tuple[str, str]]):
    if not file_path.exists(): return
    text = file_path.read_text(encoding="utf-8")
    for old, new in replacements:
        text = text.replace(old, new)
    file_path.write_text(text, encoding="utf-8")

# skills/ui-orchestrator/workflow.md
replace_links(base / "skills/ui-orchestrator/workflow.md", [
    ("](typography/README.md)", "](../typography/README.md)"),
    ("](03-design-system/workflow.md)", "](../design-system/workflow.md)"),
    ("](visual-language/workflow.md)", "](../visual-language/workflow.md)"),
    ("](motion/README.md)", "](../../knowledge/motion/README.md)"),
    ("](web-patterns/README.md)", "](../../knowledge/web-patterns/README.md)"),
    ("](design-inspiration/pattern-selection.md)", "](../design-inspiration/pattern-selection.md)"),
    ("](04-component-realization/workflow.md)", "](../component-realization/workflow.md)"),
    ("](05-frontend-implementation/workflow.md)", "](../frontend-implementation/workflow.md)"),
    ("](05-frontend-implementation/technology-resolver.md)", "](../frontend-implementation/technology-resolver.md)"),
    ("](05-frontend-implementation/performance-budget.md)", "](../frontend-implementation/performance-budget.md)"),
    ("](06-responsive-interaction/responsive.md)", "](../responsive-interaction/responsive.md)"),
    ("](visual-language/craft-review.md)", "](../visual-language/craft-review.md)"),
    ("](07-visual-qa/browser-loop.md)", "](../visual-qa/browser-loop.md)"),
    ("](../evals/quality/README.md)", "](../../evals/fixtures/quality/README.md)"), # Or where evals is
    ("](08-final-quality-gate/final-gate.md)", "](../final-quality-gate/final-gate.md)")
])

# skills/ux-structure/README.md
replace_links(base / "skills/ux-structure/README.md", [
    ("](../review/phase-1-review.md)", "../../review/phase-1-review.md")
])

# skills/ux-structure/router.md
replace_links(base / "skills/ux-structure/router.md", [
    ("](../phase-2/knowledge/screens/README.md)", "../../knowledge/domains/screens/README.md")
])

# skills/ux-structure/workflow.md
replace_links(base / "skills/ux-structure/workflow.md", [
    ("](../review/phase-1-review.md)", "../../review/phase-1-review.md")
])

# skills/visual-language/craft-review.md
replace_links(base / "skills/visual-language/craft-review.md", [
    ("](../motion/motion-review.md)", "../../knowledge/motion/motion-review.md"),
    ("](../knowledge/composition/premium-quality-model.md)", "../../knowledge/domains/composition/premium-quality-model.md"),
    ("](../knowledge/composition/anti-homogenization.md)", "../../knowledge/domains/composition/anti-homogenization.md")
])
