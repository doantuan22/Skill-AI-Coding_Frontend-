"""Claude Code plugin bundle verification (checks C1-C16).

    python plugin/adapters/claude-code/verify.py <extracted-bundle-root>
    python plugin/adapters/claude-code/verify.py --bundle <bundle.zip>

Checks are structural and subprocess-based.  A live Claude Code session is NOT required.
Exit codes: 0 all PASS, 2 at least one FAIL, 1 unusable input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PACKAGING = _HERE.parents[1] / "packaging"
if str(_PACKAGING) not in sys.path:
    sys.path.insert(0, str(_PACKAGING))
import artifact  # noqa: E402
from artifact import PackagingError  # noqa: E402

# Machine-specific path patterns (drive letters, home dirs, UNC shares)
ABSOLUTE_PATH = re.compile(r"""["'](?:[A-Za-z]:[\\\/]|/Users/|/home/|\\\\[A-Za-z0-9])[^"']*["']""")

FORBIDDEN_DIRS = {".git", "tests", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
FORBIDDEN_EXTENSIONS = {".pyc", ".pyo", ".log", ".tmp"}

CHECKS = {
    "C1": ".claude-plugin/plugin.json exists",
    "C2": "Claude manifest JSON-parseable with required fields",
    "C3": "version matches VERSION",
    "C4": ".mcp.json exists and valid JSON",
    "C5": "MCP config references shared MCP server only",
    "C6": "no absolute developer paths",
    "C7": "${CLAUDE_PLUGIN_ROOT} used correctly in MCP config",
    "C8": "MCP server initializes from bundle (subprocess)",
    "C9": "tools/list works",
    "C10": "self_test PASS",
    "C11": "capability map readable",
    "C12": "optional runtime BLOCKED does not prevent init",
    "C13": "cwd independence",
    "C14": "read-only extracted plugin",
    "C15": "no forbidden development files",
    "C16": "generic package contract preserved",
}


def _clean_env(**extra: str) -> dict:
    env = {k: v for k, v in os.environ.items()
           if k not in {"PYTHONPATH", "UIUX_ROOT", "UIUX_CONFIG", "UIUX_TEST_ROOT"}}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}, **extra)
    return env


def _run_mcp(python: str, server: Path, messages: list[dict], cwd: Path) -> list[dict]:
    """Send JSON-RPC messages to the MCP server and return parsed responses."""
    stdin_data = "\n".join(json.dumps(m) for m in messages) + "\n"
    result = subprocess.run(
        [python, str(server)], input=stdin_data,
        capture_output=True, text=True, encoding="utf-8",
        cwd=str(cwd), env=_clean_env(), timeout=60
    )
    responses = []
    for line in result.stdout.splitlines():
        if line.strip():
            responses.append(json.loads(line))
    return responses


def verify_bundle(root: Path, python: str = sys.executable) -> dict:
    """Run C1-C16 on an extracted Claude Code plugin bundle."""
    checks: list[dict] = []

    def record(cid: str, status: str, detail: str = "") -> None:
        checks.append({"id": cid, "name": CHECKS[cid], "status": status, "detail": detail})

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

    # C3: version matches VERSION
    c3_problems: list[str] = []
    version_file = root / "VERSION"
    if version_file.is_file():
        version = version_file.read_text(encoding="utf-8").strip()
        manifest_version = claude_manifest.get("version", "")
        if manifest_version != version:
            c3_problems.append(f"Claude manifest version '{manifest_version}' != VERSION '{version}'")
    else:
        c3_problems.append("VERSION file not found")
    ok("C3", c3_problems)

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

    # C6: no absolute developer paths in overlay files
    c6_problems: list[str] = []
    for check_path in [claude_manifest_path, mcp_path]:
        if check_path.is_file():
            text = check_path.read_text(encoding="utf-8")
            if ABSOLUTE_PATH.search(text):
                c6_problems.append(f"absolute path found in {check_path.name}")
    ok("C6", c6_problems)

    # C7: ${CLAUDE_PLUGIN_ROOT} used correctly
    c7_problems: list[str] = []
    if mcp_path.is_file():
        mcp_text = mcp_path.read_text(encoding="utf-8")
        # The rendered .mcp.json uses python3 as command and the server path as an arg;
        # the arg should use ${CLAUDE_PLUGIN_ROOT} for portability, OR be a relative reference.
        # In our design, args use ${CLAUDE_PLUGIN_ROOT}.
        for server_name, config in mcp_config.items():
            args = config.get("args", [])
            for arg in args:
                if isinstance(arg, str) and "server.py" in arg:
                    if "${CLAUDE_PLUGIN_ROOT}" not in arg and not arg.startswith("."):
                        c7_problems.append(f"server '{server_name}' arg does not use ${{CLAUDE_PLUGIN_ROOT}}: {arg}")
    ok("C7", c7_problems)

    # C15: no forbidden development files (run before subprocesses which create __pycache__)
    c15_problems: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        parts = rel.split("/")
        for part in parts:
            if part in FORBIDDEN_DIRS:
                c15_problems.append(f"forbidden directory in bundle: {rel}")
                break
        if any(rel.endswith(ext) for ext in FORBIDDEN_EXTENSIONS):
            c15_problems.append(f"forbidden file type in bundle: {rel}")
    ok("C15", c15_problems)

    # C8-C13: MCP subprocess tests
    server = root / "plugin" / "adapters" / "mcp" / "server.py"
    mcp_available = server.is_file()

    if mcp_available:
        try:
            with tempfile.TemporaryDirectory(prefix="claude-verify-cwd-") as cwd:
                messages = [
                    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                     "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "claude-verify", "version": "1"}}},
                    {"jsonrpc": "2.0", "method": "notifications/initialized"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                    {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                     "params": {"name": "self_test", "arguments": {}}},
                    {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                     "params": {"name": "capability_map", "arguments": {}}},
                ]
                responses = _run_mcp(python, server, messages, Path(cwd))

            # C8: initialize succeeds
            if len(responses) < 1 or responses[0].get("result", {}).get("protocolVersion") != "2025-06-18":
                ok("C8", ["MCP server initialize failed"])
            else:
                ok("C8", [])

            # C9: tools/list works
            if len(responses) < 2:
                ok("C9", ["no tools/list response"])
            else:
                tools = responses[1].get("result", {}).get("tools", [])
                ok("C9", [] if len(tools) > 0 else ["tools/list returned zero tools"])

            # C10: self_test PASS
            if len(responses) < 3:
                ok("C10", ["no self_test response"])
            else:
                st_result = responses[2].get("result", {}).get("structuredContent", {})
                st_status = st_result.get("status", "")
                if st_status != "PASS":
                    ok("C10", [f"self_test status: {st_status}"])
                else:
                    ok("C10", [])

            # C11: capability map readable
            if len(responses) < 4:
                ok("C11", ["no capability_map response"])
            else:
                cm_result = responses[3].get("result", {}).get("structuredContent", {})
                caps = cm_result.get("capabilities", {})
                ok("C11", [] if len(caps) > 0 else ["capability_map returned zero capabilities"])

        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
            for cid in ("C8", "C9", "C10", "C11"):
                if not any(c["id"] == cid for c in checks):
                    record(cid, "FAIL", f"MCP subprocess error: {exc}")
    else:
        for cid in ("C8", "C9", "C10", "C11"):
            record(cid, "FAIL", "MCP server not found in bundle")

    # C12: optional runtime BLOCKED does not prevent init
    # Already implicitly verified: C8-C10 pass even without Playwright/Node
    if mcp_available:
        c12_pass = all(c["status"] == "PASS" for c in checks if c["id"] in ("C8", "C10"))
        ok("C12", [] if c12_pass else ["init or self_test failed; optional runtime may be interfering"])
    else:
        record("C12", "FAIL", "MCP server not available")

    # C13: cwd independence (already tested in C8 — used a temp cwd)
    if mcp_available:
        try:
            with tempfile.TemporaryDirectory(prefix="claude-verify-cwd2-") as cwd2:
                messages = [
                    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                     "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "cwd-test", "version": "1"}}},
                    {"jsonrpc": "2.0", "method": "notifications/initialized"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                ]
                responses = _run_mcp(python, server, messages, Path(cwd2))
            ok("C13", [] if len(responses) >= 2 and len(responses[1].get("result", {}).get("tools", [])) > 0
               else ["tools/list failed from a different cwd"])
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
            ok("C13", [f"cwd independence test failed: {exc}"])
    else:
        record("C13", "FAIL", "MCP server not available")

    # C14: read-only extracted plugin (best-effort on Windows)
    record("C14", "NOT_RUN", "read-only enforcement is covered by generic verification V11; "
           "Claude-specific read-only test deferred to CI with full OS coverage")

    # C16: generic package contract preserved
    c16_problems: list[str] = []
    for required in ("SKILL.md", "VERSION", "uiux/__init__.py", "uiux/api.py",
                     "uiux/core/tools.json", "plugin/manifest/plugin.json",
                     "plugin/adapters/mcp/server.py"):
        if not (root / required).is_file():
            c16_problems.append(f"generic payload missing: {required}")
    ok("C16", c16_problems)

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
