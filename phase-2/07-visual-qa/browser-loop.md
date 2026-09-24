# Browser and visual QA loop

```text
Implement → self review → run application → open/inspect rendered page
→ capture or inspect → classify issue → fix → verify again
```

For rendered UI changes, follow [execution requirement](../../execution/execution-requirement.md), then route through the [execution layer](../../execution/README.md): detect capability → select strategy → reuse/start runtime safely → readiness → target route/viewport → capture evidence → review. Playwright is an existing-setup adapter, not a default dependency. Normal checks use `desktop` and `mobile`; final checks normally use all semantic viewport IDs from [viewports](../../execution/viewports.md). Do not capture every viewport after every minor change.

When no usable browser capability exists, record `NOT_EXECUTED`, `LIMITED`, or `BLOCKED` and issue a manual evidence request; never report visual success without evidence. After a targeted fix, recapture the affected route/viewport and one regression viewport only when needed.

The maximum automatic visual-refinement loop is three iterations. If a blocker remains afterward, enter `BLOCKED` with evidence, affected pages/components, and a rollback target.
