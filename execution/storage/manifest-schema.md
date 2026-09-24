# Manifest and report schema

`manifest.json` is an evidence inventory:

```json
{"schema_version":1,"session_id":"visual-001","strategy":"playwright","base_url":"http://localhost:3000","iteration":1,"status":"COMPLETED","captures":[{"id":"PAGE-LOGIN:mobile:1","page_id":"PAGE-LOGIN","route":"/login","viewport":"mobile","width":375,"height":812,"iteration":1,"status":"CAPTURED","file":"pages/PAGE-LOGIN__mobile__iter-01.png"}]}
```

`execution-report.json` records run status, counts, errors, server ownership/readiness, and cleanup. Evidence is valid only when capture status is `CAPTURED`, file exists, route/viewport/iteration match the requested capture, and schema version is supported. Evidence predating a code-change iteration is stale for new verification; targeted recapture requests only changed routes/viewports.

Captures may carry optional `reduced_motion` and `motion_probe` fields when the request enabled them; validators ignore unknown optional fields, and `scripts/analyze_design_quality.py --manifest` consumes them for E67, E68 and E78.
