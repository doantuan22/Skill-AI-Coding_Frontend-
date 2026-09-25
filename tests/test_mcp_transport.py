"""Shared MCP stdio transport: lifecycle, public-API boundary, protocol safety and real subprocess integration."""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _paths
from adapters.mcp import protocol, server
from uiux import api

ROOT = _paths.PACKAGE_ROOT
SERVER = ROOT / "adapters/mcp/server.py"


def message(identifier: int, method: str, params: dict | None = None) -> dict:
    value = {"jsonrpc": "2.0", "id": identifier, "method": method}
    if params is not None:
        value["params"] = params
    return value


def initialize(target: server.McpServer) -> None:
    response = target.handle(message(1, "initialize", {"protocolVersion": protocol.MCP_PROTOCOL_VERSION,
                                                         "capabilities": {},
                                                         "clientInfo": {"name": "test", "version": "1"}}))
    assert response and response["result"]["protocolVersion"] == protocol.MCP_PROTOCOL_VERSION
    assert target.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


class ProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = server.McpServer()

    def test_initialize_ping_and_lifecycle(self) -> None:
        before = self.server.handle(message(1, "tools/list"))
        self.assertEqual(before["error"]["code"], protocol.NOT_INITIALIZED)
        initialize(self.server)
        ping = self.server.handle(message(2, "ping"))
        self.assertEqual(ping, {"jsonrpc": "2.0", "id": 2, "result": {}})

    def test_tools_list_is_registry_derived_and_annotations_are_preserved(self) -> None:
        initialize(self.server)
        response = self.server.handle(message(2, "tools/list"))
        tools = response["result"]["tools"]
        registry = [tool for tool in api.list_tools() if tool["visibility"] == "public"]
        self.assertEqual([tool["name"] for tool in tools], [tool["id"] for tool in registry])
        self.assertEqual(len(tools), len({tool["name"] for tool in tools}))
        for actual, expected in zip(tools, registry):
            with self.subTest(tool=expected["id"]):
                self.assertEqual(actual["inputSchema"], expected["input"])
                self.assertEqual(actual["annotations"]["readOnlyHint"], expected["annotations"]["read_only"])
                self.assertEqual(actual["_meta"]["uiux.dev/annotations"]["filesystem_read"],
                                 expected["annotations"]["filesystem_read"])
                self.assertEqual(actual["_meta"]["uiux.dev/annotations"]["filesystem_write"],
                                 expected["annotations"]["writes_to"])

    def test_tool_invocation_preserves_public_validation_and_errors(self) -> None:
        initialize(self.server)
        success = self.server.handle(message(2, "tools/call", {"name": "retrieve_knowledge",
                                                                  "arguments": {"ids": ["style.swiss"]}}))
        self.assertFalse(success["result"]["isError"])
        self.assertEqual(success["result"]["structuredContent"]["entries"][0]["id"], "style.swiss")
        for identifier, name, arguments, code in (
            (3, "resolve_capabilities", {}, "MISSING_REQUIRED_ARGUMENT"),
            (4, "retrieve_knowledge", {"ids": "style.swiss"}, "INVALID_ARGUMENT_TYPE"),
            (5, "does_not_exist", {}, "UNKNOWN_TOOL"),
        ):
            with self.subTest(code=code):
                response = self.server.handle(message(identifier, "tools/call", {"name": name, "arguments": arguments}))
                result = response["result"]
                self.assertTrue(result["isError"])
                self.assertEqual(result["structuredContent"]["error_code"], code)
                self.assertTrue(result["structuredContent"]["remediation"])

    def test_blocked_runtime_is_a_valid_tool_result(self) -> None:
        initialize(self.server)
        request = {"session_id": "mcp-blocked", "base_url": "http://127.0.0.1:9",
                   "routes": [{"page_id": "P", "route": "/"}], "viewports": ["desktop"], "iteration": 1}
        with tempfile.TemporaryDirectory() as project:
            response = self.server.handle(message(2, "tools/call", {"name": "run_runtime",
                                                                        "arguments": {"request": request, "project": project}}))
        result = response["result"]
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"]["summary"]["status"], "BLOCKED")

    def test_protocol_errors_and_internal_error_do_not_leak_tracebacks(self) -> None:
        malformed = self.server.handle({"jsonrpc": "2.0", "id": 1, "method": 2})
        self.assertEqual(malformed["error"]["code"], protocol.INVALID_REQUEST)
        self.assertEqual(self.server.handle(message(2, "not/a/method"))["error"]["code"], protocol.METHOD_NOT_FOUND)
        initialize(self.server)
        bad_shape = self.server.handle(message(3, "tools/call", {"name": "retrieve_knowledge", "arguments": []}))
        self.assertEqual(bad_shape["error"]["code"], protocol.INVALID_PARAMS)

        def broken_validate_skill() -> dict:
            raise RuntimeError("secret traceback content")

        broken_validate_skill.__name__ = "validate_skill"
        with mock.patch.dict(api._DISPATCH, {"validate_skill": broken_validate_skill}):
            internal = self.server.handle(message(4, "tools/call", {"name": "validate_skill", "arguments": {}}))
        self.assertEqual(internal["error"]["code"], protocol.INTERNAL_ERROR)
        self.assertNotIn("secret", json.dumps(internal))

    def test_malformed_json_does_not_stop_following_messages_and_eof_is_clean(self) -> None:
        input_stream = io.StringIO("{bad json\n" + json.dumps(message(1, "ping")) + "\n")
        output_stream = io.StringIO()
        self.assertEqual(server.serve(input_stream, output_stream), 0)
        replies = [json.loads(line) for line in output_stream.getvalue().splitlines()]
        self.assertEqual([reply["error"]["code"] if "error" in reply else reply["result"] for reply in replies],
                         [protocol.PARSE_ERROR, {}])


class SubprocessIntegrationTests(unittest.TestCase):
    def test_stdio_server_works_from_an_unrelated_directory_with_clean_stdout(self) -> None:
        transcript = [
            message(1, "initialize", {"protocolVersion": protocol.MCP_PROTOCOL_VERSION, "capabilities": {},
                                        "clientInfo": {"name": "subprocess", "version": "1"}}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            message(2, "tools/list"),
            message(3, "tools/call", {"name": "retrieve_knowledge", "arguments": {"ids": ["style.swiss"]}}),
            message(4, "tools/call", {"name": "nope", "arguments": {}}),
            message(5, "tools/call", {"name": "self_test", "arguments": {}}),
        ]
        with tempfile.TemporaryDirectory() as cwd:
            process = subprocess.run([sys.executable, str(SERVER)], input="\n".join(json.dumps(item) for item in transcript) + "\n",
                                     capture_output=True, text=True, encoding="utf-8", cwd=cwd, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr)
        replies = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual(len(replies), 5)  # initialized is a notification, so has no response
        self.assertEqual(replies[0]["result"]["serverInfo"]["version"], api.version())
        self.assertEqual([item["name"] for item in replies[1]["result"]["tools"]],
                         [item["id"] for item in api.list_tools() if item["visibility"] == "public"])
        self.assertEqual(replies[2]["result"]["structuredContent"]["entries"][0]["id"], "style.swiss")
        self.assertEqual(replies[3]["result"]["structuredContent"]["error_code"], "UNKNOWN_TOOL")
        self.assertEqual(replies[4]["result"]["structuredContent"]["status"], "PASS")
        self.assertEqual(process.stderr, "")


if __name__ == "__main__":
    unittest.main()
