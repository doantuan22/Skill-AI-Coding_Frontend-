"""Deterministic bundle assembly utilities."""
from __future__ import annotations

import json
import os
import re
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
    manifest_file = root / "plugin.json"
    if not manifest_file.is_file():
        raise RuntimeError(f"plugin.json not found in {root}/")
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

    # A stable epoch is the default.  Releases can opt into their declared
    # SOURCE_DATE_EPOCH without sacrificing byte-for-byte reproducibility.
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", str(artifact.ZIP_MIN_EPOCH)))
    artifact.write_zip(
        bundle_path,
        [(f"{base}/{rel}", data) for rel, data in entries],
        epoch=epoch,
        mode=0o644,
        level=9,
    )

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


def validate_marketplace_source_path(source_path: object, marketplace_root: Path) -> tuple[Path | None, list[str]]:
    """Resolve a local marketplace source without allowing a root escape.

    Marketplace manifests deliberately use ``./``-prefixed POSIX paths.  Resolve
    the path so that a symlink pointing outside the marketplace is rejected too.
    """
    problems: list[str] = []
    if not isinstance(source_path, str):
        return None, ["source.path must be a string"]
    if not source_path.startswith("./"):
        problems.append("source.path must start with './'")
    if "\\" in source_path:
        problems.append("source.path must use '/' separators")
    if source_path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", source_path):
        problems.append("source.path must be relative")
    parts = source_path.split("/")
    if any(part in ("", ".", "..") for part in parts[1:]):
        problems.append("source.path cannot contain empty, '.' or '..' segments")
    if problems:
        return None, problems

    root = marketplace_root.resolve()
    candidate = (root / source_path[2:]).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, ["source.path escapes marketplace root"]
    return candidate, []


def assemble_marketplace_bundle(
    *,
    name: str,
    version: str,
    adapter_id: str,
    marketplace_manifest_path: str,
    marketplace_manifest: dict,
    plugin_payload: list[tuple[str, bytes]],
    plugin_name: str,
    out_dir: Path,
    dev: bool = False,
) -> dict:
    """Create a self-contained deterministic marketplace archive.

    ``plugin_payload`` is the exact payload passed to the host bundle builder;
    marketplace assembly only prefixes it under ``plugins/<plugin_name>/``.
    """
    artifact = _import_artifact()
    try:
        artifact.canonical_path(marketplace_manifest_path)
    except artifact.PackagingError as exc:
        raise RuntimeError(f"Unsafe marketplace manifest path: {exc}") from exc

    entries: list[tuple[str, bytes]] = [
        (marketplace_manifest_path, artifact.canonical_json(marketplace_manifest))
    ]
    prefix = f"plugins/{plugin_name}"
    for rel, data in plugin_payload:
        try:
            safe_rel = artifact.canonical_path(rel)
            marketplace_rel = artifact.canonical_path(f"{prefix}/{safe_rel}")
        except artifact.PackagingError as exc:
            raise RuntimeError(f"Unsafe marketplace payload path '{rel}': {exc}") from exc
        entries.append((marketplace_rel, data))

    entries.sort(key=lambda item: item[0].encode("utf-8"))
    paths = [path for path, _ in entries]
    if len(paths) != len(set(paths)):
        raise RuntimeError("BUNDLE_CONFLICT: marketplace contains duplicate paths")

    suffix = "-dev" if dev else ""
    base = f"{name}-{version}{suffix}-{adapter_id}-marketplace"
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = out_dir / f"{base}.zip"
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", str(artifact.ZIP_MIN_EPOCH)))
    artifact.write_zip(
        bundle_path,
        [(f"{base}/{rel}", data) for rel, data in entries],
        epoch=epoch,
        mode=0o644,
        level=9,
    )
    return {
        "marketplace_bundle": str(bundle_path),
        "marketplace_file_count": len(entries),
        "marketplace_sha256": artifact.sha256_file(bundle_path),
    }
