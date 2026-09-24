"""MCP Server test harness (Smoke test)."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def clean_env(**extra: str) -> dict:
    """Provide a clean environment for MCP subprocess without testing artifacts."""
    env = {k: v for k, v in os.environ.items()
           if k not in {"PYTHONPATH", "UIUX_ROOT", "UIUX_CONFIG", "UIUX_TEST_ROOT"}}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}, **extra)
    return env


def run_mcp_raw(python: str, server: Path, messages: list[dict], cwd: Path) -> list[dict]:
    """Send JSON-RPC messages to the MCP server and return parsed responses."""
    stdin_data = "\n".join(json.dumps(m) for m in messages) + "\n"
    result = subprocess.run(
        [python, str(server)], input=stdin_data,
        capture_output=True, text=True, encoding="utf-8",
        cwd=str(cwd), env=clean_env(), timeout=60
    )
    responses = []
    for line in result.stdout.splitlines():
        if line.strip():
            try:
                responses.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return responses


def run_mcp_smoke_test(python: str, server: Path, cwd: Path) -> dict:
    """Run common MCP sanity checks (C8-C13).
    
    Args:
        python: Python executable path.
        server: Path to the MCP server script.
        cwd: Working directory to run the server from.
        
    Returns:
        Dictionary of checks formatted for the verify report.
    """
    checks: list[dict] = []
    
    def record(cid: str, name: str, status: str, detail: str = "") -> None:
        checks.append({"id": cid, "name": name, "status": status, "detail": detail})

    def ok(cid: str, name: str, problems: list[str]) -> None:
        record(cid, name, "FAIL" if problems else "PASS", "; ".join(problems) if problems else "")

    if not server.is_file():
        for cid, name in (
            ("C8", "MCP server initializes from bundle (subprocess)"),
            ("C9", "tools/list works"),
            ("C10", "self_test PASS"),
            ("C11", "capability map readable"),
            ("C12", "optional runtime BLOCKED does not prevent init"),
            ("C13", "cwd independence"),
        ):
            record(cid, name, "FAIL", "MCP server not found in bundle")
        return {"checks": checks}

    try:
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                        "clientInfo": {"name": "common-verify", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "self_test", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "capability_map", "arguments": {}}},
        ]
        responses = run_mcp_raw(python, server, messages, cwd)
        
        # C8: initialize succeeds
        if len(responses) < 1 or responses[0].get("result", {}).get("protocolVersion") != "2025-06-18":
            ok("C8", "MCP server initializes from bundle (subprocess)", ["MCP server initialize failed"])
        else:
            ok("C8", "MCP server initializes from bundle (subprocess)", [])

        # C9: tools/list works
        if len(responses) < 2:
            ok("C9", "tools/list works", ["no tools/list response"])
        else:
            tools = responses[1].get("result", {}).get("tools", [])
            ok("C9", "tools/list works", [] if len(tools) > 0 else ["tools/list returned zero tools"])

        # C10: self_test PASS
        if len(responses) < 3:
            ok("C10", "self_test PASS", ["no self_test response"])
        else:
            st_result = responses[2].get("result", {}).get("structuredContent", {})
            st_status = st_result.get("status", "")
            if st_status != "PASS":
                ok("C10", "self_test PASS", [f"self_test status: {st_status}"])
            else:
                ok("C10", "self_test PASS", [])

        # C11: capability map readable
        if len(responses) < 4:
            ok("C11", "capability map readable", ["no capability_map response"])
        else:
            cm_result = responses[3].get("result", {}).get("structuredContent", {})
            caps = cm_result.get("capabilities", {})
            ok("C11", "capability map readable", [] if len(caps) > 0 else ["capability_map returned zero capabilities"])

    except FileNotFoundError as exc:
        for cid, name in (
            ("C8", "MCP server initializes from bundle (subprocess)"),
            ("C9", "tools/list works"),
            ("C10", "self_test PASS"),
            ("C11", "capability map readable"),
        ):
            record(cid, name, "FAIL", f"Python executable '{python}' not found (Missing Python runtime)")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        for cid, name in (
            ("C8", "MCP server initializes from bundle (subprocess)"),
            ("C9", "tools/list works"),
            ("C10", "self_test PASS"),
            ("C11", "capability map readable"),
        ):
            record(cid, name, "FAIL", f"MCP subprocess error: {exc}")

    # C12: optional runtime BLOCKED does not prevent init
    c12_pass = all(c["status"] == "PASS" for c in checks if c["id"] in ("C8", "C10"))
    ok("C12", "optional runtime BLOCKED does not prevent init", 
       [] if c12_pass else ["init or self_test failed; optional runtime may be interfering"])

    # C13: cwd independence
    import tempfile
    try:
        with tempfile.TemporaryDirectory(prefix="common-verify-cwd2-") as cwd2:
            messages_cwd = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                 "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                            "clientInfo": {"name": "cwd-test", "version": "1"}}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            ]
            responses_cwd = run_mcp_raw(python, server, messages_cwd, Path(cwd2))
        ok("C13", "cwd independence", 
           [] if len(responses_cwd) >= 2 and len(responses_cwd[1].get("result", {}).get("tools", [])) > 0
           else ["tools/list failed from a different cwd"])
    except FileNotFoundError as exc:
        ok("C13", "cwd independence", [f"cwd independence test failed: Python executable '{python}' not found"])
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        ok("C13", "cwd independence", [f"cwd independence test failed: {exc}"])
        
    return {"checks": checks}
