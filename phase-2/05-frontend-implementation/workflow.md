# Frontend implementation workflow

Inspect the project’s current frontend stack, architecture, shared components, utility system, CSS strategy, route conventions, and available browser/QA tooling. Implement only after direction and system decisions exist. Preserve the existing framework and add dependencies only when necessary and authorized.

Build in this order for large work: tokens → base/layout → shared components → representative pages → verified page groups. For migrations, prove the target system on one to three representative form-heavy, data-heavy, or content-heavy pages before broader migration. Record `PAGE ID → component → source file → style source` in `IMPLEMENTATION-MAP.md`.
