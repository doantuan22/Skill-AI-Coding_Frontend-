"""Runtime Validation Session – immutable context for a Phase 7 critic run.

Holds all inputs the critic needs:
  - modification_plan (from Phase 6)
  - change_manifest  (from Phase 6 ControlledEditingEngine)
  - before_evidence  (runtime captures before editing)
  - after_evidence   (runtime captures after editing)
  - preservation_profile (from modification_plan if not supplied separately)

Key principle: session is IMMUTABLE after creation. Repair loop creates new
sessions derived from the original.
"""
from __future__ import annotations

import uuid
from typing import Any

# Evidence pair status values
EVIDENCE_STATUS_VALID = "valid"
EVIDENCE_STATUS_MISSING_BASELINE = "missing_baseline"
EVIDENCE_STATUS_MISSING_AFTER = "missing_after"
EVIDENCE_STATUS_NO_RUNTIME = "no_runtime"


class RuntimeValidationSession:
    """Immutable container for all runtime critic inputs."""

    def __init__(
        self,
        modification_plan: dict[str, Any] | None = None,
        change_manifest: dict[str, Any] | None = None,
        before_evidence: dict[str, Any] | None = None,
        after_evidence: dict[str, Any] | None = None,
        workflow: str = "existing-ui",
        session_id: str | None = None,
    ) -> None:
        self.session_id = session_id or f"session_{uuid.uuid4().hex[:12]}"
        self.modification_plan: dict[str, Any] = modification_plan or {}
        self.change_manifest: dict[str, Any] = change_manifest or {}
        self.before_evidence: dict[str, Any] = before_evidence or {}
        self.after_evidence: dict[str, Any] = after_evidence or {}
        self.workflow = workflow

        # Derived from modification_plan
        self.plan_id: str = self.modification_plan.get("plan_id", "")
        self.preservation_profile: dict[str, Any] = self.modification_plan.get("preservation", {})
        self.blast_radius: dict[str, Any] = self.modification_plan.get("blast_radius", {})
        self.validation_handoff: dict[str, Any] = self.modification_plan.get("validation", {})
        self.affected_surface: dict[str, Any] = self.modification_plan.get("affected_surface", {})
        self.change_classification: dict[str, Any] = self.modification_plan.get("change_classification", {})
        self.domain_pack: dict[str, Any] = self.modification_plan.get("knowledge", {})
        self.request: dict[str, Any] = self.modification_plan.get("request", {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RuntimeValidationSession":
        return cls(
            modification_plan=data.get("modification_plan"),
            change_manifest=data.get("change_manifest"),
            before_evidence=data.get("before_evidence"),
            after_evidence=data.get("after_evidence"),
            workflow=data.get("workflow", "existing-ui"),
            session_id=data.get("session_id"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "plan_id": self.plan_id,
            "workflow": self.workflow,
            "modification_plan": self.modification_plan,
            "change_manifest": self.change_manifest,
            "before_evidence": self.before_evidence,
            "after_evidence": self.after_evidence,
        }

    def has_runtime(self) -> bool:
        """True if any after-evidence was provided (browser runtime was available)."""
        return bool(self.after_evidence and self.after_evidence.get("captures"))

    def has_baseline(self) -> bool:
        """True if before-evidence was provided (Existing UI baseline available)."""
        return bool(self.before_evidence and self.before_evidence.get("captures"))

    def is_greenfield(self) -> bool:
        return self.workflow == "greenfield"

    def is_existing_ui(self) -> bool:
        return self.workflow == "existing-ui"

    def is_runtime_required(self) -> bool:
        """True if the validation contract mandates runtime/browser evidence.

        Evaluated from:
          1. Explicit flag in validation handoff: requires_runtime (bool).
          2. Explicit flag in validation handoff: requires_browser (bool).
          3. Required checks demanding runtime: responsive viewport, accessibility axe audit,
             browser runtime, form/modal/interaction testing, visual regression.
          4. Presence of interaction scenarios or accessibility checks.
          5. Existing UI workflows with visual preservation or responsive/interaction requirements.
        """
        if "requires_runtime" in self.validation_handoff:
            return bool(self.validation_handoff["requires_runtime"])
        if "requires_browser" in self.validation_handoff:
            return bool(self.validation_handoff["requires_browser"])

        if self.workflow in ("code-only", "static-analysis", "code-level"):
            return False

        req_checks = self.get_required_checks()
        runtime_keywords = (
            "responsive", "viewport", "interaction", "accessibility", "axe",
            "browser", "visual_regression", "runtime", "console_error", "state_verification"
        )
        if any(any(kw in str(c).lower() for kw in runtime_keywords) for c in req_checks):
            return True

        if self.get_interaction_scenarios() or self.get_accessibility_checks():
            return True

        if self.validation_handoff.get("affected_viewports"):
            return True

        if self.is_existing_ui() and self.preservation_profile:
            return True

        return False

    def get_missing_evidence_pairs(self) -> list[tuple[str, str]]:
        """Return list of (page, viewport) pairs required by handoff but missing from after captures."""
        if not self.after_evidence:
            return [(page, vp) for page in self.get_affected_pages() for vp in self.get_affected_viewports()]

        after_index = _index_captures(self.after_evidence.get("captures", []))
        missing = []
        for page in self.get_affected_pages():
            for vp in self.get_affected_viewports():
                if (page, vp) not in after_index:
                    missing.append((page, vp))
        return missing

    def has_complete_evidence(self) -> bool:
        """True if after-evidence exists and covers all affected pages and viewports."""
        if not self.has_runtime():
            return False
        return len(self.get_missing_evidence_pairs()) == 0

    def has_partial_evidence(self) -> bool:
        """True if some after captures exist but do not cover all required pages/viewports."""
        if not self.has_runtime():
            return False
        return len(self.get_missing_evidence_pairs()) > 0

    def get_affected_pages(self) -> list[str]:
        """Return pages/routes from validation handoff or affected surface."""
        handoff_pages = self.validation_handoff.get("affected_pages", [])
        if handoff_pages:
            return handoff_pages
        routes = self.affected_surface.get("routes", [])
        return routes if routes else ["/"]

    def get_affected_viewports(self) -> list[str]:
        """Return viewports from validation handoff."""
        return self.validation_handoff.get("affected_viewports", ["desktop_1440"])

    def build_evidence_pairs(self) -> list[dict[str, Any]]:
        """Build before/after evidence pairs with stable identity.

        Each pair: {evidence_pair_id, page, viewport, scenario, before, after, status}
        Only pairs where both before and after are captured are fully valid.
        """
        pairs: list[dict[str, Any]] = []
        pages = self.get_affected_pages()
        viewports = self.get_affected_viewports()

        # Index captures by (page, viewport)
        before_index = _index_captures(self.before_evidence.get("captures", []))
        after_index = _index_captures(self.after_evidence.get("captures", []))

        for page in pages:
            for vp in viewports:
                key = (page, vp)
                before_cap = before_index.get(key)
                after_cap = after_index.get(key)

                if before_cap and after_cap:
                    status = EVIDENCE_STATUS_VALID
                elif not before_cap and after_cap:
                    status = EVIDENCE_STATUS_MISSING_BASELINE
                elif before_cap and not after_cap:
                    status = EVIDENCE_STATUS_MISSING_AFTER
                else:
                    status = EVIDENCE_STATUS_NO_RUNTIME

                pairs.append({
                    "evidence_pair_id": f"pair_{_safe_id(page)}_{vp}",
                    "page": page,
                    "viewport": vp,
                    "scenario": "default",
                    "before": before_cap,
                    "after": after_cap,
                    "status": status,
                })

        return pairs

    def get_console_errors(self) -> list[dict[str, Any]]:
        """Return after-evidence console errors (introduced during editing)."""
        return self.after_evidence.get("console_errors", [])

    def get_before_console_errors(self) -> list[dict[str, Any]]:
        """Return before-evidence console errors (pre-existing)."""
        return self.before_evidence.get("console_errors", [])

    def get_required_states(self) -> list[str]:
        """Return required UI states from domain pack."""
        selected_packs = self.domain_pack.get("selected_packs", {})
        required_states: list[str] = []
        for _domain, pack_data in selected_packs.items():
            if isinstance(pack_data, dict):
                required_states.extend(pack_data.get("required_states", []))
        return list(dict.fromkeys(required_states))  # deduplicate maintaining order

    def get_required_checks(self) -> list[str]:
        return self.validation_handoff.get("required_checks", [])

    def get_interaction_scenarios(self) -> list[str]:
        return self.validation_handoff.get("interactions", [])

    def get_accessibility_checks(self) -> list[str]:
        return self.validation_handoff.get("accessibility", [])

    def get_preservation_checks(self) -> list[str]:
        return self.validation_handoff.get("preservation", [])


def _index_captures(captures: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    """Index captures by (page/route, viewport) key."""
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for cap in captures:
        page = cap.get("route", cap.get("page", cap.get("page_id", "/")))
        vp = cap.get("viewport", "desktop_1440")
        if isinstance(vp, dict):
            viewport = vp.get("name") or f"{vp.get('width', 1280)}x{vp.get('height', 800)}"
        else:
            viewport = str(vp)
        index[(str(page), viewport)] = cap
    return index


def _safe_id(text: str) -> str:
    """Convert text to a safe identifier fragment."""
    import re
    return re.sub(r"[^A-Za-z0-9_-]", "_", text).strip("_") or "page"
