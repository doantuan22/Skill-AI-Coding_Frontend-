"""Build a self-contained Claude Code plugin bundle from a verified generic artifact.

    python plugin/adapters/claude-code/export.py --source <extracted-artifact-root> --out dist/<version>/adapters/
    python plugin/adapters/claude-code/export.py --dev --out dist/dev/adapters/

The bundle is a ZIP containing the full generic payload plus Claude-specific overlay files
(.claude-plugin/plugin.json, .mcp.json).  It is deterministic: the same source produces the
same archive bytes on the same platform.  Only standard library modules are used; nothing
from ``uiux`` is imported.

Exit codes: 0 built, 1 error (JSON).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TEMPLATES = _HERE / "templates"

# Re-use packaging primitives without importing uiux
_PACKAGING = _HERE.parents[1] / "packaging"
if str(_PACKAGING) not in sys.path:
    sys.path.insert(0, str(_PACKAGING))
import artifact  # noqa: E402
from artifact import PackagingError  # noqa: E402


def _read_version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def _read_manifest_name(root: Path) -> str:
    manifest = json.loads((root / "plugin/manifest/plugin.json").read_text(encoding="utf-8"))
    return manifest["name"]


def _render_template(template_path: Path, variables: dict[str, str]) -> str:
    """Replace {key} placeholders with values.  Only known keys; stray braces are left alone."""
    text = template_path.read_text(encoding="utf-8")
    for key, value in variables.items():
        text = text.replace("{" + key + "}", value)
    return text


def _collect_payload(root: Path) -> list[tuple[str, bytes]]:
    """All files from the source root, excluding VCS metadata and caches."""
    entries: list[tuple[str, bytes]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        parts = rel.split("/")
        if any(part in (".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", "tests", ".github") for part in parts):
            continue
        if rel.endswith((".pyc", ".pyo")):
            continue
        entries.append((rel, path.read_bytes()))
    return entries


def _mcp_json_content(version: str) -> str:
    """Render the .mcp.json with portable ${CLAUDE_PLUGIN_ROOT} paths."""
    return json.dumps({
        "ui-ux-design-mcp": {
            "command": "python3",
            "args": ["${CLAUDE_PLUGIN_ROOT}/plugin/adapters/mcp/server.py"],
            "env": {}
        }
    }, indent=2, ensure_ascii=False) + "\n"


def _claude_plugin_json_content(version: str, name: str, description: str) -> str:
    """Render the .claude-plugin/plugin.json manifest."""
    return json.dumps({
        "name": name,
        "version": version,
        "description": description
    }, indent=2, ensure_ascii=False) + "\n"


def export(source: Path, out_dir: Path, dev: bool = False) -> dict:
    """Build the Claude Code plugin bundle.

    Args:
        source: Extracted generic artifact root or the repository root (with --dev).
        out_dir: Directory to write the bundle ZIP into.
        dev: If True, use the working tree directly (non-release).

    Returns:
        Build result dict with status, path, file count.
    """
    source = source.resolve()
    if not (source / "VERSION").is_file():
        raise PackagingError("MANIFEST_INVALID", f"VERSION not found in {source}")
    if not (source / "SKILL.md").is_file():
        raise PackagingError("MANIFEST_INVALID", f"SKILL.md not found in {source}")
    if not (source / "plugin/adapters/mcp/server.py").is_file():
        raise PackagingError("MANIFEST_INVALID", "shared MCP server not found; build the generic artifact first")

    version = _read_version(source)
    name = _read_manifest_name(source)
    description = json.loads((source / "plugin/manifest/plugin.json").read_text(encoding="utf-8")).get(
        "description", "UI/UX Design Skill"
    )

    # Validate adapter.json is present and schema-valid
    adapter_meta = json.loads((_HERE / "adapter.json").read_text(encoding="utf-8"))
    schema = json.loads((source / "plugin/schemas/adapter.schema.json").read_text(encoding="utf-8"))
    problems = artifact.validate_schema(adapter_meta, schema)
    if problems:
        raise PackagingError("MANIFEST_INVALID", f"adapter.json schema errors: {'; '.join(problems)}")

    # Collect payload files
    entries = _collect_payload(source)

    # Add Claude-specific overlay files
    claude_manifest = _claude_plugin_json_content(version, name, description)
    mcp_config = _mcp_json_content(version)

    entries.append((".claude-plugin/plugin.json", claude_manifest.encode("utf-8")))
    entries.append((".mcp.json", mcp_config.encode("utf-8")))

    # Sort for determinism
    entries.sort(key=lambda item: item[0].encode("utf-8"))

    # Check for conflicts: overlay must not overwrite payload files
    paths = [rel for rel, _ in entries]
    seen: set[str] = set()
    for p in paths:
        if p in seen:
            raise PackagingError("BUNDLE_CONFLICT", f"overlay file {p} already exists in the payload")
        seen.add(p)

    # Build the ZIP
    suffix = "-dev" if dev else ""
    base = f"{name}-{version}{suffix}-claude-code"
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = out_dir / f"{base}.zip"

    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", str(int(time.time()))))
    date_time = time.gmtime(max(epoch, artifact.ZIP_MIN_EPOCH))[:6]

    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel, data in entries:
            info = zipfile.ZipInfo(f"{base}/{rel}", date_time=date_time)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)

    return {
        "status": "BUILT",
        "bundle": str(bundle_path),
        "name": name,
        "version": version,
        "adapter": "claude-code",
        "build_mode": "dev" if dev else "release",
        "file_count": len(entries),
        "sha256": artifact.sha256_file(bundle_path),
        "overlay_files": [".claude-plugin/plugin.json", ".mcp.json"],
    }


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Build a Claude Code plugin bundle")
    parser.add_argument("--source", type=Path, help="extracted generic artifact root or repo root")
    parser.add_argument("--out", type=Path, required=True, help="output directory for the bundle ZIP")
    parser.add_argument("--dev", action="store_true", help="build from the working tree (non-release)")
    args = parser.parse_args(argv)

    source = args.source
    if source is None:
        # Default: the repository root (three levels up from this file)
        source = _HERE.parents[2]

    try:
        result = export(source, args.out, args.dev)
    except PackagingError as exc:
        print(json.dumps(exc.to_dict(), indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
