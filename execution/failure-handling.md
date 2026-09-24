# Execution failure handling

| Failure | Ownership | Result / response |
|---|---|---|
| Capability/browser unavailable | Environment | `NOT_EXECUTED`, `LIMITED`, or `BLOCKED`; use manual fallback if appropriate. |
| Server start/readiness/route failure | Project runtime | Record evidence; stop visual review as blocker. |
| Blank/fatal render | UI implementation | `BLOCKER`; return to Phase 2 implementation. |
| Capture/viewport/adapter failure | Execution adapter | Record attempt and limitation; retry only with a changed strategy. |
| Auth/data unavailable | Environment/project setup | `AUTH_REQUIRED`, `LIMITED`, or `BLOCKED`; do not fake verification. |
| Cleanup failure | Execution ownership | Record owned process/session and cleanup state; never kill user-owned process. |

Taxonomy: `SERVER_START_FAILURE`, `READINESS_TIMEOUT`, `ROUTE_FAILURE`, `BROWSER_UNAVAILABLE`, `PLAYWRIGHT_UNAVAILABLE`, `PLAYWRIGHT_RUNTIME_FAILURE`, `BLANK_RENDER`, `SCREENSHOT_FAILURE`, `VIEWPORT_FAILURE`, `PROCESS_CLEANUP_FAILURE`.

On interruption, record last successful step, owned processes, cleanup status, and evidence captured. Follow the global blocked contract and rollback only to the phase that owns the issue.
