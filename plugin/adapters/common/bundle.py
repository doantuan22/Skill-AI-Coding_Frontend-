"""Deterministic bundle assembly utilities."""
from __future__ import annotations

import json
import os
import re
import time
import zipfile
from pathlib import Path


def get_packaging_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "packaging"


def _import_artifact():
    import sys
    pkg_dir = get_packaging_dir()
    if str(pkg_dir) not in sys.path:
        sys.path.insert(0, str(pkg_dir))
    import artifact
    return artifact


def read_version(root: Path) -> str:
    version_file = root / "VERSION"
    if not version_file.is_file():
        raise RuntimeError(f"VERSION not found in {root}")
    return version_file.read_text(encoding="utf-8").strip()


def read_manifest_name(root: Path) -> str:
    manifest_file = root / "plugin" / "manifest" / "plugin.json"
    if not manifest_file.is_file():
        raise RuntimeError(f"plugin.json not found in {root}/plugin/manifest/")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    return manifest["name"]


def render_template(template_path: Path, variables: dict[str, str]) -> str:
    """Replace {key} placeholders with values. Only known keys; stray braces left alone."""
    text = template_path.read_text(encoding="utf-8")
    for key, value in variables.items():
        text = text.replace("{" + key + "}", value)
    return text


def collect_generic_payload(root: Path) -> list[tuple[str, bytes]]:
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


def assemble_bundle(
    name: str,
    version: str,
    adapter_id: str,
    payload: list[tuple[str, bytes]],
    overlay: list[tuple[str, bytes]],
    out_dir: Path,
    dev: bool = False
) -> dict:
    """Safely combine payload and overlay into a deterministic ZIP bundle.
    
    Args:
        name: The plugin name (e.g., ui-ux-design)
        version: The semantic version
        adapter_id: Host adapter ID (e.g., claude-code)
        payload: List of generic payload files
        overlay: List of adapter-specific overlay files
        out_dir: Target directory for the ZIP
        dev: True if building a developer bundle
        
    Returns:
        Build info dictionary.
        
    Raises:
        RuntimeError: On path traversal, absolute path, or payload collision.
    """
    artifact = _import_artifact()
    
    entries: list[tuple[str, bytes]] = []
    entries.extend(payload)
    
    # Path safety validation on overlay
    for rel, data in overlay:
        # Check canonical format
        try:
            artifact.canonical_path(rel)
        except artifact.PackagingError as exc:
            raise RuntimeError(f"Unsafe overlay path '{rel}': {exc}")
        
        entries.append((rel, data))

    # Sort for determinism
    entries.sort(key=lambda item: item[0].encode("utf-8"))

    # Check for collisions
    paths = [rel for rel, _ in entries]
    seen: set[str] = set()
    for p in paths:
        if p in seen:
            raise RuntimeError(f"BUNDLE_CONFLICT: overlay file {p} overwrites generic payload")
        seen.add(p)

    # Build the ZIP
    suffix = "-dev" if dev else ""
    base = f"{name}-{version}{suffix}-{adapter_id}"
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
        "adapter": adapter_id,
        "build_mode": "dev" if dev else "release",
        "file_count": len(entries),
        "sha256": artifact.sha256_file(bundle_path),
        "overlay_files": [rel for rel, _ in overlay],
    }
