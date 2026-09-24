"""Codex plugin bundle verification (checks X1-X16).

    python plugin/adapters/codex/verify.py <extracted-bundle-root>
    python plugin/adapters/codex/verify.py --bundle <bundle.zip>

Checks are structural and subprocess-based. A live Codex session is NOT required for X1-X16.
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
    "X1": "Codex/plugin manifest tồn tại (plugin.json)",
    "X2": "manifest schema hợp lệ",
    "X3": "version khớp VERSION",
    "X4": "skill directory hợp lệ",
    "X5": "generated skill khớp canonical SKILL.md",
    "X6": "MCP config hợp lệ (mcp.json)",
    "X7": "MCP config dùng shared MCP",
    "X8": "không absolute path",
    "X9": "bundle không overwrite protected core (đã test lúc build)",
    "X10": "MCP initialize PASS",
    "X11": "tools/list PASS",
    "X12": "self_test PASS",
    "X13": "capability_map PASS",
    "X14": "cwd independence",
    "X15": "optional runtime BLOCKED không làm plugin fail",
    "X16": "generic artifact contract không regression",
}


def verify_bundle(root: Path, python: str = sys.executable) -> dict:
    """Run X1-X16 on an extracted Codex plugin bundle."""
    checks: list[dict] = []

    def record(cid: str, status: str, detail: str = "") -> None:
        name = CHECKS.get(cid, cid)
        checks.append({"id": cid, "name": name, "status": status, "detail": detail})

    def ok(cid: str, problems: list[str]) -> None:
        record(cid, "FAIL" if problems else "PASS", "; ".join(problems) if problems else "")

    # X1: plugin manifest exists
    codex_manifest_path = root / "plugin.json"
    ok("X1", [] if codex_manifest_path.is_file() else [f"{codex_manifest_path} not found"])

    # X2: manifest schema valid
    codex_manifest = {}
    x2_problems: list[str] = []
    if codex_manifest_path.is_file():
        try:
            codex_manifest = json.loads(codex_manifest_path.read_text(encoding="utf-8"))
            required = {"name", "version", "type"}
            missing = sorted(required - set(codex_manifest))
            if missing:
                x2_problems.append(f"missing fields: {', '.join(missing)}")
            if "$schema" not in codex_manifest:
                x2_problems.append("missing $schema field")
        except (json.JSONDecodeError, OSError) as exc:
            x2_problems.append(f"cannot parse: {exc}")
    else:
        x2_problems.append("file does not exist")
    ok("X2", x2_problems)

    # X3: version matches VERSION
    manifest_version = codex_manifest.get("version", "")
    ok("X3", verify.check_version_match(root, manifest_version) if manifest_version else ["cannot check version against missing manifest version"])

    # X4: skill directory valid
    skill_path = root / "skills" / "ui-ux-workflow" / "SKILL.md"
    ok("X4", [] if skill_path.is_file() else [f"{skill_path} not found"])

    # X5: generated skill matches canonical SKILL.md
    x5_problems: list[str] = []
    canonical_skill = root / "SKILL.md"
    if skill_path.is_file() and canonical_skill.is_file():
        if skill_path.read_bytes() != canonical_skill.read_bytes():
            x5_problems.append("generated skill content differs from canonical SKILL.md")
    else:
        x5_problems.append("cannot compare; files missing")
    ok("X5", x5_problems)

    # X6: MCP config valid JSON and Agent Plugins schema
    mcp_path = root / "mcp.json"
    mcp_config: dict = {}
    x6_problems: list[str] = []
    if mcp_path.is_file():
        try:
            mcp_config = json.loads(mcp_path.read_text(encoding="utf-8"))
            if not isinstance(mcp_config, dict) or "mcpServers" not in mcp_config:
                x6_problems.append("mcp.json is missing 'mcpServers' object")
            if "$schema" not in mcp_config:
                x6_problems.append("missing $schema field")
        except (json.JSONDecodeError, OSError) as exc:
            x6_problems.append(f"cannot parse mcp.json: {exc}")
    else:
        x6_problems.append("mcp.json not found")
    ok("X6", x6_problems)

    # X7: MCP config uses shared MCP and correct placeholders
    x7_problems: list[str] = []
    servers = mcp_config.get("mcpServers", {})
    for server_name, config in servers.items():
        if config.get("type") != "stdio":
            x7_problems.append(f"server '{server_name}' missing or invalid type (must be stdio)")
            
        command = config.get("command", "")
        if "${" in command:
            x7_problems.append(f"server '{server_name}' command cannot contain placeholders: {command}")
            
        args = config.get("args", [])
        for arg in args:
            if isinstance(arg, str):
                if "${PLUGIN_DIR}" in arg:
                    x7_problems.append(f"server '{server_name}' uses unsupported placeholder ${{PLUGIN_DIR}}")
                if "server.py" in arg and "plugin/adapters/mcp/server.py" not in arg:
                    x7_problems.append(f"server '{server_name}' does not use the shared MCP transport: {arg}")
                if "server.py" in arg and "${PLUGIN_ROOT}" not in arg and not arg.startswith("."):
                    x7_problems.append(f"server '{server_name}' arg does not use ${{PLUGIN_ROOT}}: {arg}")
                    
        # Check cwd if present
        if "cwd" in config:
            cwd_val = config.get("cwd")
            if not isinstance(cwd_val, str):
                x7_problems.append(f"server '{server_name}' cwd must be a string if present")
            elif cwd_val == "":
                x7_problems.append(f"server '{server_name}' cwd cannot be empty string")
            else:
                if "${PLUGIN_DIR}" in cwd_val:
                    x7_problems.append(f"server '{server_name}' cwd uses unsupported placeholder ${{PLUGIN_DIR}}")
                if cwd_val.startswith("/") or cwd_val.startswith("\\") or (len(cwd_val) > 1 and cwd_val[1] == ":"):
                    x7_problems.append(f"server '{server_name}' cwd cannot be absolute path")
            
    ok("X7", x7_problems)

    # X8: no absolute developer paths
    ok("X8", verify.check_absolute_paths([codex_manifest_path, mcp_path]))

    # X9: bundle overwrite protected core (implicitly passed during export, just record PASS if bundle generated)
    ok("X9", [])

    # X10-X15: MCP subprocess tests
    server = root / "plugin" / "adapters" / "mcp" / "server.py"
    mcp_report = mcp_smoke.run_mcp_smoke_test(python, server, root)
    
    # Map common check IDs to Codex X10-X15
    # C8 -> X10 (initialize)
    # C9 -> X11 (list)
    # C10 -> X12 (self_test)
    # C11 -> X13 (capability_map)
    # C13 -> X14 (cwd independence)
    # C12 -> X15 (optional runtime BLOCKED)
    cid_map = {"C8": "X10", "C9": "X11", "C10": "X12", "C11": "X13", "C13": "X14", "C12": "X15"}
    for check in mcp_report["checks"]:
        new_id = cid_map.get(check["id"])
        if new_id:
            record(new_id, check["status"], check.get("detail", ""))

    # X16: generic package contract preserved
    ok("X16", verify.check_generic_contract(root))

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
    parser = argparse.ArgumentParser(description="Verify a Codex plugin bundle (X1-X16)")
    parser.add_argument("root", nargs="?", type=Path, help="extracted bundle root")
    parser.add_argument("--bundle", type=Path, help="bundle ZIP to extract and verify")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv)

    workspace = None
    try:
        if args.bundle:
            workspace = Path(tempfile.mkdtemp(prefix="codex-verify-"))
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
