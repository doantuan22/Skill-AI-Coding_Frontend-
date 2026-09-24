# Accessibility runtime

Accessibility runtime reuses browser execution sessions, routes, viewports, evidence roots, and server ownership. Read-only detection chooses local `@axe-core/playwright`, local `axe-core` injection, or manual fallback; it never installs packages, uses a CDN, or bypasses auth.

Each route/viewport scan writes separate axe JSON and a session accessibility manifest. Violations/incomplete results are structured evidence; incomplete becomes manual follow-up. Manual review covers keyboard/focus, form errors, responsive/touch/motion and color-only communication. The gate distinguishes PASS, FAIL, LIMITED, BLOCKED, and NOT_APPLICABLE; zero axe violations never proves full accessibility.

Use targeted rescans after a fix and treat pre-change evidence as stale. Validate evidence with [validate_accessibility_evidence.py](../scripts/validate_accessibility_evidence.py); actual scan requires project-local Playwright and axe capability.
