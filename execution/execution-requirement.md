# Execution requirement decision

```text
Does the task modify rendered UI?
  no  → browser execution optional; artifact-only evidence may be sufficient.
  yes → browser/visual evidence required when capability exists.
```

Frontend implementation, visual redesign, responsive fixes, component polish, and page migrations normally require execution evidence. Skill architecture, Markdown-only updates, design specifications, and audits limited to supplied artifacts do not. If execution is required but no capability exists, report `NOT_EXECUTED`, `LIMITED`, or `BLOCKED`; never claim visual pass.
