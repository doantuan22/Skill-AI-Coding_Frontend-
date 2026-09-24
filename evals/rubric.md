# Evaluation rubric

| Criterion | Pass evidence | Fail signal |
|---|---|---|
| Routing accuracy | Correct phase/mode, fast/full path, and rollback | Wrong phase/mode or bypassed route |
| Context efficiency | Core + selected files only; exclusions respected | Unrelated references/phase loaded or repeated reads |
| Requirement fidelity | Request represented without invention | Required behavior omitted or invented |
| Scope discipline | Only requested scope changed; impact noted | Unrelated redesign or scope creep |
| Phase separation | Phase 1/2 boundary preserved | Styling in Phase 1 or semantic redesign in Phase 2 |
| Artifact reuse | Active/locked artifact reused or permitted update | Random duplicate or stale artifact used |
| Structure Lock compliance | Lock located, validated, immutable in Phase 2 | Missing/bypassed/edited lock |
| Business rule safety | Unknowns/assumptions explicit | Invented payment, approval, permission, backend rule |
| Review effectiveness | Issues classified; targeted delta reviewed | Review ignores blocker/regression |
| Loop stability | Progress recorded; no-progress blocks | Infinite/repeated identical loop |
| Traceability | Required chain is linkable when scope needs it | Required item cannot reach output |
| Completion correctness | Gates/evidence and no blocker before DONE | Premature DONE |
| Capability detection | Existing tooling/runtime correctly identified without mutation | Misdetected capability or unsolicited install |
| Execution strategy | Highest safe existing strategy selected | Wrong adapter/package manager or unnecessary server |
| Runtime safety | Readiness and process ownership evidenced | Duplicate server, false readiness, unsafe kill |
| Evidence integrity | Route/viewport/session evidence exists and is linked | Fake pass or missing/ambiguous evidence |
| Viewport coverage | Required semantic viewports, targeted rerun | Wrong/unnecessary viewport sweep |
| Fallback honesty | Limited/no-browser state is explicit | Claims inspection without capability/evidence |
| Cleanup safety | Owned resources cleaned; user resources left alone | Unsafe kill or unreported cleanup failure |
| Runtime execution correctness | Runner validates, launches only confirmed local runtime, and records result | Bypassed detector, wrong status, or auto-install |
| Screenshot coverage | Requested captures are present with deterministic metadata | Missing/mislabeled capture |
| Partial-failure honesty | Successful evidence retained and failures explicit | Lost evidence or false completed result |
| Targeted recapture | New iteration captures only requested targets | Stale evidence accepted or needless full sweep |
