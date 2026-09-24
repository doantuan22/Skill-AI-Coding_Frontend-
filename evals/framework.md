# Evaluation contract

Each scenario has a stable ID and describes initial project state, user request, expected route, minimum artifacts/context, prohibited behavior, success conditions, and failure conditions. Evals may be run by Codex, Claude Code, Cline, Roo Code, OpenCode, or another agent without agent-specific commands.

Assess observable decisions and artifacts, not chain-of-thought: route/mode, selected files/references, artifact status/version/reuse, scope, issue handling, final state, and evidence. Use `PASS`, `FAIL`, `PARTIAL`, or `NOT_APPLICABLE` per criterion; do not compress results into an arbitrary vanity score.

Suites: `SMOKE = E01,E02,E06,E08,E12`; `CORE = E01–E12`; `EXECUTION = E21–E28`; `RUNTIME = E29–E36`; `ACCESSIBILITY = E37–E44`; `VISUAL_LANGUAGE = E45–E52`; `INSPIRATION = E53–E64`; `DESIGN_QUALITY = E65–E80`; `FULL = E01–E80`. Any hardening/routing/contract change must rerun at least SMOKE; execution-layer changes rerun EXECUTION; runner/storage changes rerun RUNTIME; visual-language changes rerun VISUAL_LANGUAGE; inspiration/typography/motion/pattern changes rerun INSPIRATION and VISUAL_LANGUAGE; knowledge, resolver or analyzer changes rerun DESIGN_QUALITY plus `python tests/test_knowledge.py` and `python tests/test_quality_analyzer.py`; broad changes rerun FULL.
