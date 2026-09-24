# Application runtime and readiness

Resolve command priority: documented project command → declared package script → existing framework configuration → safe low-confidence inference. Inspect `package.json`, README, Makefile, build files, and framework configuration; record `UNKNOWN` instead of guessing when evidence is insufficient.

Before starting, check whether the known target URL already responds. If it does, reuse it and set `server_owned: false`; never terminate it. When this layer starts a process, record command, PID/process handle, base URL, readiness evidence, and `server_owned: true`.

Readiness is a successful HTTP response, a known page/root, or another explicit project signal—not process spawn or a fixed sleep alone. A timeout may bound the check but cannot prove readiness. If the expected port is occupied, do not kill it; distinguish a known target server from an unrelated process or report `BLOCKED`.

Authenticated routes report `AUTH_REQUIRED` when no existing fixture/session exists. Dynamic data must use existing fixtures/dev data/test environment or report `LIMITED`/`BLOCKED`; never invent data.
