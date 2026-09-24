# Evidence storage

Storage is a local, session-scoped evidence inventory—not a test-result database. [evidence-layout.md](evidence-layout.md) defines deterministic paths, [manifest-schema.md](manifest-schema.md) defines machine-readable integrity, and [retention.md](retention.md) defines conservative retention. Validate with `python scripts/validate_runtime_evidence.py <session-dir>`.
