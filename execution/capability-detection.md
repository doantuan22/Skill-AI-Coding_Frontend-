# Capability detection

Detection is read-only. Inspect available Node/Python commands, package manager lockfiles, project package/config files, frontend framework signals, dev/build/test scripts, browser/automation packages, Playwright package/config, known URL, existing server response, screenshot/headless-browser capability, and any agent-provided browser tool.

Report each capability as `AVAILABLE`, `AVAILABLE_WITH_LIMITATIONS`, `NOT_AVAILABLE`, or `UNKNOWN`, with confidence `confirmed`, `inferred`, or `unknown`. A package declaration confirms package presence but not a browser binary/runtime. Use [scripts/detect_capabilities.py](../scripts/detect_capabilities.py) for a standard-library, read-only manifest; it must not become an installation step.
