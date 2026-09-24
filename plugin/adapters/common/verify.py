"""Common bundle verification primitives."""
from __future__ import annotations

import re
from pathlib import Path


def check_forbidden_files(root: Path) -> list[str]:
    """Verify no development artifacts remain in the bundle."""
    forbidden_dirs = {".git", "tests", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
    forbidden_ext = {".pyc", ".pyo", ".log", ".tmp"}
    
    problems: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        parts = rel.split("/")
        for part in parts:
            if part in forbidden_dirs:
                problems.append(f"forbidden directory in bundle: {rel}")
                break
        if any(rel.endswith(ext) for ext in forbidden_ext):
            problems.append(f"forbidden file type in bundle: {rel}")
            
    return problems


def check_absolute_paths(paths_to_check: list[Path]) -> list[str]:
    """Check overlay files for hardcoded absolute paths."""
    abs_pattern = re.compile(r"""["'](?:[A-Za-z]:[\\\/]|/Users/|/home/|\\\\[A-Za-z0-9])[^"']*["']""")
    problems: list[str] = []
    for check_path in paths_to_check:
        if check_path.is_file():
            text = check_path.read_text(encoding="utf-8")
            if abs_pattern.search(text):
                problems.append(f"absolute path found in {check_path.name}")
    return problems


def check_generic_contract(root: Path) -> list[str]:
    """Ensure the generic payload wasn't corrupted."""
    problems: list[str] = []
    for required in (
        "SKILL.md", "VERSION", "uiux/__init__.py", "uiux/api.py",
        "uiux/core/tools.json", "plugin/manifest/plugin.json",
        "plugin/adapters/mcp/server.py"
    ):
        if not (root / required).is_file():
            problems.append(f"generic payload missing: {required}")
    return problems


def check_version_match(root: Path, target_version: str) -> list[str]:
    """Check that the bundle's VERSION matches the target version."""
    problems: list[str] = []
    version_file = root / "VERSION"
    if version_file.is_file():
        version = version_file.read_text(encoding="utf-8").strip()
        if version != target_version:
            problems.append(f"VERSION file '{version}' != manifest version '{target_version}'")
    else:
        problems.append("VERSION file not found")
    return problems
