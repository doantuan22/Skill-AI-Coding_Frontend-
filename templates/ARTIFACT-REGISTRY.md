# Artifact Registry

```yaml
artifacts:
  REQUIREMENT-SPEC:
    version: v1
    status: draft # draft | active | validated | locked | needs_review | stale | invalid | superseded
    phase: 1
    path: templates/REQUIREMENT-SPEC.md
    depends_on: []
    last_validated:
```

One artifact type has one active version. Resolution precedence is `LOCKED > ACTIVE > DRAFT > SUPERSEDED`; `VALIDATED`, `NEEDS_REVIEW`, `STALE`, and `INVALID` describe reuse safety. The Structure Lock names the source-of-truth versions for Phase 2.
