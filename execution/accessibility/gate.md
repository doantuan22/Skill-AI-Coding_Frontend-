# Accessibility gate

States: `PASS`, `FAIL`, `LIMITED`, `BLOCKED`, `NOT_APPLICABLE`. PASS requires required automated scans, required manual checks, no unresolved critical issue, no serious issue affecting primary task, and no manual blocker. A successful axe scan alone cannot pass the gate.

`LIMITED` applies when automation runs but required manual verification is limited/not executed; it is not full production PASS by default. `BLOCKED` applies when required capability/auth is unavailable. Final Quality Gate must not allow DONE when accessibility is required and this gate is not policy-permitted.
