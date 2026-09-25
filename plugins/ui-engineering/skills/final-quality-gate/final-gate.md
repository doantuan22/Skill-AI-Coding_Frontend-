# Final quality gate

Create `FINAL-QUALITY-REPORT.md` and pass only when:

- Structure Lock and Page Specs are respected.
- The Design System and tokens are respected or documented exceptions exist.
- The Visual Grammar is respected; any exception, density risk, or necessary replacement is documented and reviewed.
- Responsive behavior works at selected viewports.
- Required states are implemented.
- Visual QA passes with no blocker.
- There is no blocker accessibility issue, major cross-page inconsistency, or unresolved design drift.
- When the task modified rendered UI and execution capability was available, the required route/viewport execution evidence exists and is linked to review.

If required execution was not completed, `DONE` is forbidden unless the task is artifact-only or a documented limitation changes the state to `NOT_EXECUTED`, `LIMITED`, or `BLOCKED`. If an implementation/visual issue remains, return to `PHASE_2`. If a semantic or business mismatch exists, create a rollback request and return to `PHASE_1`. A pass feeds final review; it does not change the lock.
