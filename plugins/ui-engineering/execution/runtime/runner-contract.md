# Runner contract

1. Validate input, paths, viewport IDs, and session ID.
2. Invoke read-only capability detection; require project-local Playwright package and Node before runtime launch.
3. Preflight output location and, if necessary, browser import/launch. No installation, download, package/config/lockfile mutation, or config overwrite is permitted.
4. Reuse a responding base URL or, only with explicit `--allow-start`, start the exact argv command and mark it owned.
5. Poll HTTP readiness at 500 ms until a finite timeout. Spawn/sleep alone is never readiness.
6. For each requested route/viewport, create isolated browser context, navigate with `domcontentloaded`, perform a basic render check, capture PNG, and preserve partial evidence.
7. Atomically write `manifest.json` and `execution-report.json`; clean browser and owned server; print a short JSON result.

Exit codes: `0` completed, `1` execution failed, `2` blocked capability/preflight, `3` invalid input, `4` partial execution. Runner stdout is one summary JSON; runtime errors are structured in the report and concise on stderr.
