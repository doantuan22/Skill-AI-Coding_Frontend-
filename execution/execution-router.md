# Execution strategy router

After detection and requirement decision, select the first viable strategy:

1. Existing agent-provided supported browser/tool capability.
2. Existing project Playwright setup.
3. Existing compatible browser automation dependency.
4. Lightweight locally available mechanism.
5. [Manual fallback](adapters/manual.md).

The router records strategy, confidence, limitations, target routes, semantic viewport IDs, readiness method, evidence plan, and server ownership in `EXECUTION-REPORT.md`. Reuse an already responsive known URL; do not start a duplicate server. A missing tool is not permission to install it.

Target routes come from task scope, Page Specs, and Implementation Map. Do not crawl the whole application. Large migration work names representative form-heavy, data-heavy, and content-heavy routes; targeted recovery recaptures the affected route/viewport plus one regression viewport only when useful.
