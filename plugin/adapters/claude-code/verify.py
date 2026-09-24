"""Claude Code plugin bundle verification (checks C1-C16).

    python plugin/adapters/claude-code/verify.py <extracted-bundle-root>
    python plugin/adapters/claude-code/verify.py --bundle <bundle.zip>

Checks are structural and subprocess-based.  A live Claude Code session is NOT required.
Exit codes: 0 all PASS, 2 at least one FAIL, 1 unusable input.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_COMMON = _HERE.parent / "common"
if str(_COMMON.parent) not in sys.path:
    sys.path.insert(0, str(_COMMON.parent))

from common import verify, mcp_smoke


# Ensure packaging is importable for artifact.safe_extract
_PACKAGING = _HERE.parents[1] / "packaging"
if str(_PACKAGING) not in sys.path:
    sys.path.insert(0, str(_PACKAGING))
import artifact  # noqa: E402
from artifact import PackagingError  # noqa: E402


CHECKS = {
    "C1": ".claude-plugin/plugin.json exists",
    "C2": "Claude manifest JSON-parseable with required fields",
    "C3": "version matches VERSION",
    "C4": ".mcp.json exists and valid JSON",
    "C5": "MCP config references shared MCP server only",
    "C6": "no absolute developer paths",
    "C7": "${CLAUDE_PLUGIN_ROOT} used correctly in MCP config",
    "C14": "read-only extracted plugin",
    "C15": "no forbidden development files",
    "C16": "generic package contract preserved",
}


def verify_bundle(root: Path, python: str = sys.executable) -> dict:
    """Run C1-C16 on an extracted Claude Code plugin bundle."""
    checks: list[dict] = []

    def record(cid: str, status: str, detail: str = "") -> None:
        name = CHECKS.get(cid, cid)
        checks.append({"id": cid, "name": name, "status": status, "detail": detail})

    def ok(cid: str, problems: list[str]) -> None:
        record(cid, "FAIL" if problems else "PASS", "; ".join(problems) if problems else "")

    # C1: .claude-plugin/plugin.json exists
    claude_manifest_path = root / ".claude-plugin" / "plugin.json"
    ok("C1", [] if claude_manifest_path.is_file() else [f"{claude_manifest_path} not found"])

    # C2: Claude manifest parseable with required fields
    claude_manifest = {}
    c2_problems: list[str] = []
    if claude_manifest_path.is_file():
        try:
            claude_manifest = json.loads(claude_manifest_path.read_text(encoding="utf-8"))
            required = {"name", "version"}
            missing = sorted(required - set(claude_manifest))
            if missing:
                c2_problems.append(f"missing fields: {', '.join(missing)}")
        except (json.JSONDecodeError, OSError) as exc:
            c2_problems.append(f"cannot parse: {exc}")
    else:
        c2_problems.append("file does not exist")
    ok("C2", c2_problems)

    # C3: version matches VERSION (delegate to common)
    manifest_version = claude_manifest.get("version", "")
    ok("C3", verify.check_version_match(root, manifest_version) if manifest_version else ["cannot check version against missing manifest version"])

    # C4: .mcp.json exists and valid JSON
    mcp_path = root / ".mcp.json"
    mcp_config: dict = {}
    c4_problems: list[str] = []
    if mcp_path.is_file():
        try:
            mcp_config = json.loads(mcp_path.read_text(encoding="utf-8"))
            if not isinstance(mcp_config, dict):
                c4_problems.append(".mcp.json is not a JSON object")
        except (json.JSONDecodeError, OSError) as exc:
            c4_problems.append(f"cannot parse .mcp.json: {exc}")
    else:
        c4_problems.append(".mcp.json not found")
    ok("C4", c4_problems)

    # C5: MCP config references shared MCP server only
    c5_problems: list[str] = []
    for server_name, config in mcp_config.items():
        args = config.get("args", [])
        for arg in args:
            if isinstance(arg, str) and "server.py" in arg:
                if "plugin/adapters/mcp/server.py" not in arg:
                    c5_problems.append(f"server '{server_name}' does not use the shared MCP transport: {arg}")
    ok("C5", c5_problems)

    # C6: no absolute developer paths in overlay files (delegate to common)
    ok("C6", verify.check_absolute_paths([claude_manifest_path, mcp_path]))

    # C7: ${CLAUDE_PLUGIN_ROOT} used correctly
    c7_problems: list[str] = []
    if mcp_path.is_file():
        for server_name, config in mcp_config.items():
            args = config.get("args", [])
            for arg in args:
                if isinstance(arg, str) and "server.py" in arg:
                    if "${CLAUDE_PLUGIN_ROOT}" not in arg and not arg.startswith("."):
                        c7_problems.append(f"server '{server_name}' arg does not use ${{CLAUDE_PLUGIN_ROOT}}: {arg}")
    ok("C7", c7_problems)

    # C15: no forbidden development files (delegate to common)
    ok("C15", verify.check_forbidden_files(root))

    # C8-C13: MCP subprocess tests (delegate to common)
    server = root / "plugin" / "adapters" / "mcp" / "server.py"
    mcp_report = mcp_smoke.run_mcp_smoke_test(python, server, root)
    checks.extend(mcp_report["checks"])

    # C14: read-only extracted plugin
    record("C14", "NOT_RUN", "read-only enforcement is covered by generic verification V11; "
           "Claude-specific read-only test deferred to CI with full OS coverage")

    # C16: generic package contract preserved (delegate to common)
    ok("C16", verify.check_generic_contract(root))

    failed = [c["id"] for c in checks if c["status"] == "FAIL"]
    return {
        "status": "FAIL" if failed else "PASS",
        "failed": failed,
        "not_run": [c["id"] for c in checks if c["status"] == "NOT_RUN"],
        "checks": checks,
    }


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Verify a Claude Code plugin bundle (C1-C16)")
    parser.add_argument("root", nargs="?", type=Path, help="extracted bundle root")
    parser.add_argument("--bundle", type=Path, help="bundle ZIP to extract and verify")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv)

    workspace = None
    try:
        if args.bundle:
            workspace = Path(tempfile.mkdtemp(prefix="claude-verify-"))
            root = artifact.safe_extract(args.bundle, workspace / "extract")
        elif args.root:
            root = args.root.resolve()
        else:
            print(json.dumps({"status": "ERROR", "error": "give a bundle root or --bundle <zip>"}))
            return 1

        report = verify_bundle(root, args.python)
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "PASS" else 2
    except PackagingError as exc:
        print(json.dumps(exc.to_dict(), indent=2))
        return 1
    finally:
        if workspace and not args.keep:
            shutil.rmtree(workspace, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())

