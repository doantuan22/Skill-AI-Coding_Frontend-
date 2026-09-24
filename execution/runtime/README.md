# Playwright runtime

The runtime runner is an optional Playwright adapter implementation, not a replacement for capability detection or browser contracts. It accepts a validated JSON request, runs only after read-only detector confirmation, launches an isolated headless context through project-local Playwright, captures target routes/viewports, stores structured evidence, and cleans up owned resources.

Read [runtime-input.md](runtime-input.md), [runner-contract.md](runner-contract.md), and [session-lifecycle.md](session-lifecycle.md) before use. Run `python scripts/run_browser_execution.py --input <request.json> --project <project-root>`; use `--dry-run` to validate/plan without server or browser launch.
