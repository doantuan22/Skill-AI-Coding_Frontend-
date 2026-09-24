# Playwright resolution

The runner uses the project-local Node module resolution from a temporary helper inside the evidence session. It tries existing `playwright`, then `@playwright/test`, and launches the requested engine (default `chromium`) headlessly. A package declaration is insufficient: import/launch failure becomes `PLAYWRIGHT_IMPORT_FAILURE`, `PLAYWRIGHT_BROWSER_UNAVAILABLE`, or `BROWSER_LAUNCH_FAILURE` without download.

Existing Playwright config, fixtures, e2e directories, `baseURL`, `webServer`, and browser choices are never overwritten. Explicit runtime request values take precedence over project convention for target/viewports only when safe; safety and ownership rules cannot be overridden.
