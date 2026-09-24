# Runtime output

Session output lives at `.evidence/<session-id>/` by default:

```text
manifest.json              # evidence inventory
execution-report.json      # run/session outcome
pages/PAGE-ID__mobile__iter-01.png
logs/console.json          # optional console.error/pageerror observations
```

Both JSON files use UTF-8, `schema_version: 1`, and atomic replace writes. `COMPLETED` means every requested capture is `CAPTURED`; `PARTIAL` preserves completed captures while recording failed ones; `FAILED` has no successful capture; `BLOCKED` did not pass capability/preflight.
