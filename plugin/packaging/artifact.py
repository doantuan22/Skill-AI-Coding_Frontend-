"""Packaging primitives shared by build.py, verify.py and package_files.py (standard library only).

Integration tooling only: path matching, text normalization, hashing, deterministic archive writing, safe
extraction and a small JSON-Schema subset validator. No design, knowledge, eval or runtime logic, and no import
of ``uiux``: the build and verification run the *target tree's own* code in subprocesses instead.
"""
from __future__ import annotations

import fnmatch
import gzip
import hashlib
import io
import json
import re
import tarfile
import time
import zipfile
from pathlib import Path, PurePosixPath

RULES_RELATIVE = "plugin/packaging/package-rules.json"
ZIP_MIN_EPOCH = 315532800  # 1980-01-01T00:00:00Z, the earliest timestamp a ZIP entry can hold


class PackagingError(Exception):
    """A packaging failure with a stable machine-readable code."""

    def __init__(self, code: str, message: str, **details: object) -> None:
        super().__init__(message)
        self.code, self.message, self.details = code, message, details

    def to_dict(self) -> dict:
        return {"status": "ERROR", "error": {"code": self.code, "message": self.message, "details": self.details}}


# --------------------------------------------------------------------------- rules and paths
def load_rules(root: Path) -> dict:
    """The packaging contract (single source): selection, required/forbidden files and artifact metadata."""
    return json.loads((root / RULES_RELATIVE).read_text(encoding="utf-8"))


def match(rel: str, pattern: str) -> bool:
    """POSIX glob semantics: '**/x' matches x at any depth; 'a/**' matches everything under a/."""
    if pattern.startswith("**/"):
        parts = rel.split("/")
        return any(match("/".join(parts[i:]), pattern[3:]) for i in range(len(parts)))
    if pattern.endswith("/**"):
        base = pattern[:-3]
        return rel == base or rel.startswith(base + "/")
    return fnmatch.fnmatchcase(rel, pattern)


def matches_any(rel: str, patterns: list[str]) -> bool:
    return any(match(rel, pattern) for pattern in patterns)


def canonical_path(rel: str) -> str:
    """Validate and return a canonical archive path: relative, '/'-separated, no '.'/'..'/empty segments."""
    if not rel or "\\" in rel or rel.startswith("/") or re.match(r"^[A-Za-z]:", rel):
        raise PackagingError("UNSAFE_PATH", f"not a canonical relative path: {rel!r}")
    parts = rel.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise PackagingError("UNSAFE_PATH", f"not a canonical relative path: {rel!r}")
    return str(PurePosixPath(*parts))


# --------------------------------------------------------------------------- content
def is_binary(rel: str, data: bytes, binary_globs: list[str]) -> bool:
    return matches_any(rel, binary_globs) or b"\x00" in data[:8192]


def normalize(rel: str, data: bytes, binary_globs: list[str]) -> bytes:
    """Text files are stored with LF endings (CRLF -> LF); binary files are returned untouched."""
    return data if is_binary(rel, data, binary_globs) else data.replace(b"\r\n", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(data: object) -> bytes:
    """Stable JSON bytes (sorted keys, LF, trailing newline) for embedded and published metadata."""
    return (json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


# --------------------------------------------------------------------------- deterministic archives
def _zip_time(epoch: int) -> tuple[int, int, int, int, int, int]:
    return time.gmtime(max(epoch, ZIP_MIN_EPOCH))[:6]


def write_zip(path: Path, entries: list[tuple[str, bytes]], epoch: int, mode: int, level: int) -> None:
    """Entries must already be sorted; every entry gets the same timestamp, permissions and host system."""
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=_zip_time(epoch))
            info.create_system = 3  # always "Unix" so Windows and Linux builds write identical headers
            info.external_attr = (0o100000 | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=level)


def write_targz(path: Path, entries: list[tuple[str, bytes]], epoch: int, mode: int, level: int) -> None:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, data in entries:
            info = tarfile.TarInfo(name)
            info.size, info.mtime, info.mode = len(data), epoch, mode
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.type = tarfile.REGTYPE
            archive.addfile(info, io.BytesIO(data))
    with path.open("wb") as raw:
        # mtime=0 and an empty filename keep the gzip header identical across machines.
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=level) as compressed:
            compressed.write(buffer.getvalue())


def archive_members(path: Path) -> list[str]:
    if path.name.endswith(".zip"):
        with zipfile.ZipFile(path) as archive:
            return [info.filename for info in archive.infolist()]
    with tarfile.open(path, "r:gz") as archive:
        return [member.name for member in archive.getmembers()]


def safe_extract(path: Path, destination: Path) -> Path:
    """Extract a zip/tar.gz after validating every member path; returns the single top-level directory."""
    destination.mkdir(parents=True, exist_ok=True)
    if path.name.endswith(".zip"):
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                canonical_path(info.filename.rstrip("/"))
                if info.external_attr >> 16 & 0o170000 == 0o120000:
                    raise PackagingError("UNSAFE_ARCHIVE", f"symlink in archive: {info.filename}")
            archive.extractall(destination)
    elif path.name.endswith(".tar.gz"):
        with tarfile.open(path, "r:gz") as archive:
            members = archive.getmembers()
            for member in members:
                canonical_path(member.name.rstrip("/"))
                if not (member.isfile() or member.isdir()):
                    raise PackagingError("UNSAFE_ARCHIVE", f"non-regular member in archive: {member.name}")
            extra = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}  # Python >= 3.12 hardening
            archive.extractall(destination, members=members, **extra)
    else:
        raise PackagingError("UNSUPPORTED_ARCHIVE", f"unsupported archive type: {path.name}")
    tops = [p for p in destination.iterdir()]
    if len(tops) != 1 or not tops[0].is_dir():
        raise PackagingError("UNSAFE_ARCHIVE", "archive must contain exactly one top-level directory")
    return tops[0]


# --------------------------------------------------------------------------- JSON Schema subset
_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def _type_ok(value: object, expected: str) -> bool:
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[expected])


def validate_schema(value: object, schema: dict, where: str = "$") -> list[str]:
    """Validate against the subset used by this repository's schemas: type, const, enum, pattern, minLength,
    minimum, required, properties, additionalProperties (bool or schema), items, minItems, uniqueItems."""
    errors: list[str] = []
    expected = schema.get("type")
    if expected is not None:
        options = expected if isinstance(expected, list) else [expected]
        if not any(_type_ok(value, option) for option in options):
            return [f"{where}: expected {expected}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{where}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{where}: must be one of {schema['enum']}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{where}: does not match {schema['pattern']}")
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{where}: shorter than {schema['minLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema and value < schema["minimum"]:
        errors.append(f"{where}: below minimum {schema['minimum']}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{where}: missing required property {key!r}")
        properties = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for key, item in value.items():
            if key in properties:
                errors += validate_schema(item, properties[key], f"{where}.{key}")
            elif extra is False:
                errors.append(f"{where}: unexpected property {key!r}")
            elif isinstance(extra, dict):
                errors += validate_schema(item, extra, f"{where}.{key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{where}: fewer than {schema['minItems']} items")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f"{where}: items are not unique")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors += validate_schema(item, schema["items"], f"{where}[{index}]")
    return errors
