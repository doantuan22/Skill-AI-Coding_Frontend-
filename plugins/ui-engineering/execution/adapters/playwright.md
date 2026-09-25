# Playwright adapter

Use only when existing project capability detection confirms compatible Playwright package/setup. Reuse `playwright.config.*`, existing tests/e2e directory, fixtures, and browser configuration; never overwrite them. Do not install Playwright, modify package scripts, or download browser binaries in detection.

Adapter responsibilities: detect/confirm setup, launch or connect according to the project’s existing convention, navigate, wait for readiness, set semantic viewport dimensions, capture evidence, collect basic page state/optional console observations, close owned browser/session, and report limitations. Its implementation must satisfy [browser contract](../browser-contract.md), not define the core API.

If package configuration is present but runtime/browser readiness cannot be confirmed, report `AVAILABLE_WITH_LIMITATIONS` or `PLAYWRIGHT_RUNTIME_FAILURE`, not success.

For a confirmed project-local runtime, use [runtime runner](../runtime/README.md). It writes session evidence under a separate namespace and does not alter existing tests/configuration.
