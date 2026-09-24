# Artifact contract

Artifact templates use a simple `Status` and `Version` field. The active artifact is the latest version explicitly referenced by the active structure lock; a superseded artifact is retained for traceability but is not an input to new work.

| Artifact | Created by | Read by | Editable by | Locked / completion point |
|---|---|---|---|---|
| `REQUIREMENT-SPEC.md` | Phase 1 | Phase 1, reviews | Phase 1 | Referenced at review / lock when in scope |
| `CURRENT-UX-MAP.md` | Phase 1 | Phase 1, reviews | Phase 1 | Referenced at review / lock when existing UI is in scope |
| `ACTOR-MAP.md`, `USE-CASE-MAP.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` when in scope |
| `INFORMATION-ARCHITECTURE.md`, `NAVIGATION-MAP.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` when in scope |
| `UX-FLOW.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` |
| `PAGE-MAP.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` |
| `PAGE-SPEC.md`, `COMPONENT-MAP.md`, `STATE-MAP.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` when in scope |
| `WIREFRAME-SPEC.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` |
| `TRACEABILITY-MATRIX.md`, `PHASE-1-REVIEW.md` | Phase 1 / review | Phase 1, reviews | Phase 1 / review | Complete at passing Phase 1 review |
| `DESIGN-BRIEF.md` | Phase 1 | Phase 1, Phase 2, reviews | Phase 1 | Locked at `STRUCTURE_LOCKED` |
| `STRUCTURE-LOCK.md` | Structure-lock transition | Phase 2 and all reviews | Phase 1 / authorized structural transition | Active from `STRUCTURE_LOCKED`; superseded only by a later valid lock |
| `DESIGN-SYSTEM.md` | Phase 2 | Phase 2 and final review | Phase 2 | Baseline complete at `PHASE_2_REVIEW` pass |
| `DESIGN-DIRECTION.md`, `REFERENCE-ANALYSIS.md`, `DESIGN-INSPIRATION.md`, `CURRENT-DESIGN-SYSTEM.md` | Phase 2 | Phase 2, reviews | Phase 2 | Complete at the relevant direction/system decision |
| `DESIGN-TOKENS.md`, `MOTION-SYSTEM.md`, `COMPONENT-SPEC.md`, `IMPLEMENTATION-MAP.md` | Phase 2 | Phase 2, reviews | Phase 2 | Complete at `PHASE_2_REVIEW` pass when in scope |
| `VISUAL-REVIEW.md`, `ACCESSIBILITY-REVIEW.md`, `PHASE-2-REVIEW.md`, `FINAL-QUALITY-REPORT.md` | Phase 2 / review | Phase 2, final review | Phase 2 / review | Complete at the associated passing gate |
| `FINAL-REVIEW.md` | Final review | All states after final review | Final review | Complete at `DONE` when status is `passed` |

The router selects a minimum sufficient set. The baseline handoff is `UX-FLOW.md`, `PAGE-MAP.md`, `WIREFRAME-SPEC.md`, `DESIGN-BRIEF.md`, and a passing review; it also includes whichever supporting artifacts are necessary to make the selected scope unambiguous. Small projects may merge compatible artifacts while retaining their fields and traceability.

Dependencies flow one way: requirements → Phase 1 artifacts → Structure Lock → Phase 2 direction/system/components/implementation → Phase 2 reviews/quality gate → Final Review. Review records assess their inputs but do not replace or silently modify artifacts owned by another phase. This prevents dependency cycles.
