# Runtime errors

Each error is a compact record with `code`, `page_id`, `route`, `viewport`, `message`, and `recoverable`. Codes: `RUNTIME_INPUT_INVALID`, `PLAYWRIGHT_IMPORT_FAILURE`, `PLAYWRIGHT_BROWSER_UNAVAILABLE`, `BROWSER_LAUNCH_FAILURE`, `SERVER_START_FAILURE`, `READINESS_TIMEOUT`, `NAVIGATION_FAILURE`, `AUTH_REQUIRED`, `BLANK_RENDER`, `SCREENSHOT_FAILURE`, `EVIDENCE_WRITE_FAILURE`, `CLEANUP_FAILURE`, `PARTIAL_EXECUTION`.

Do not emit passwords, tokens, cookies, authorization headers, or oversized stack traces. A failed route does not receive a fake capture; independent routes may continue when safe.
