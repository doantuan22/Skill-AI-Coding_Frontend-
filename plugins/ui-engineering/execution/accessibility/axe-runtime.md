# axe runtime adapter

`run_accessibility_scan.py` requires detector-confirmed project-local Playwright plus either `@axe-core/playwright` or `axe-core`. It launches its own owned browser/context but reuses the existing execution session’s server/base URL and never manages the server. It first tries `@axe-core/playwright`; local `axe-core` source injection is the compatible fallback. No CDN is used.
