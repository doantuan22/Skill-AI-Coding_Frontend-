# Accessibility evidence schema

Evidence is stored in `<session>/accessibility/`: `accessibility-manifest.json`, one `<PAGE>__<viewport>__iter-NN__axe.json` per scan, and optional manual review JSON. Scan files use schema v1 and retain violations/incomplete plus bounded, sanitized node excerpts; no full DOM, password, token, cookie, or input values.

Violations preserve rule ID, impact, description, help, help URL, tags, and nodes (target, excerpt, failure summary). Impact is `critical`, `serious`, `moderate`, `minor`, or null/unknown. `incomplete` creates manual follow-up candidates, never silent dismissal.
