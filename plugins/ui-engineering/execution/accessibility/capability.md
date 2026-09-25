# Accessibility capability

Detection is read-only and reports local `@axe-core/playwright`, `axe-core`, Playwright, browser runtime, and project tooling as available/limited/unavailable/unknown. Strategy priority is `@axe-core/playwright` → local `axe-core` injection → existing project adapter → manual fallback. Never install axe, download from CDN, or modify dependencies.
