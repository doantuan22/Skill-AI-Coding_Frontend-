"""Critic Engine – Phase 7.

Produces machine-readable critic_report from a RuntimeValidationSession.

Critic categories:
  VISUAL_REGRESSION        – structural/layout issues detected in after evidence
  PRESERVATION_VIOLATION   – palette, brand, navigation, scope violations
  RESPONSIVE_FAILURE       – overflow, stacking, clipping at specific viewport
  INTERACTION_FAILURE      – form, modal, nav, drawer interaction failures
  ACCESSIBILITY_REGRESSION – new a11y issue introduced by editing
  RUNTIME_ERROR            – console errors, render failures, hydration issues
  PLAN_DRIFT               – change manifest differs from modification plan
  MISSING_REQUIRED_STATE   – required domain UI state absent from implementation

Severity model (deterministic, rule-based; never subjective):
  INFO     – harmless: 1px delta, anti-aliasing
  LOW      – minor: small spacing, non-critical cosmetic
  MEDIUM   – notable: degraded UX but not blocking
  HIGH     – significant: broken component, interaction failure
  CRITICAL – severe: navigation missing, global palette swap, crash

Pre-existing vs New Regression:
  If before evidence also shows the issue → pre_existing (not AI's fault).
  If before passes, after fails → new_regression.
  If before fails, after worse → worsened.

Critic is EVIDENCE-BASED. No subjective design preferences.
"""
from __future__ import annotations

import re
import uuid
from typing import Any

from uiux.engine.runtime_critic.session import RuntimeValidationSession, EVIDENCE_STATUS_VALID, EVIDENCE_STATUS_NO_RUNTIME

# ── Severity levels ──────────────────────────────────────────────────────────
INFO = "INFO"
LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
CRITICAL = "CRITICAL"

SEVERITY_ORDER = {INFO: 0, LOW: 1, MEDIUM: 2, HIGH: 3, CRITICAL: 4}

# ── Issue status ─────────────────────────────────────────────────────────────
NEW_REGRESSION = "new_regression"
PRE_EXISTING = "pre_existing"
WORSENED = "worsened"
RESOLVED = "resolved"

# ── Categories ───────────────────────────────────────────────────────────────
VISUAL_REGRESSION = "visual_regression"
PRESERVATION_VIOLATION = "preservation_violation"
RESPONSIVE_FAILURE = "responsive_failure"
INTERACTION_FAILURE = "interaction_failure"
ACCESSIBILITY_REGRESSION = "accessibility_regression"
RUNTIME_ERROR = "runtime_error"
PLAN_DRIFT = "plan_drift"
MISSING_REQUIRED_STATE = "missing_required_state"

# ── Repair eligibility ───────────────────────────────────────────────────────
# Categories that can be auto-repaired within blast radius
AUTO_REPAIRABLE_CATEGORIES = {VISUAL_REGRESSION, RESPONSIVE_FAILURE, INTERACTION_FAILURE}
# These always require user permission
PERMISSION_REQUIRED_CATEGORIES = {PRESERVATION_VIOLATION}

# Palette-related keywords that signal a preservation violation
PALETTE_VIOLATION_SIGNALS = (
    "primary color", "secondary color", "palette change", "global theme",
    "brand color", "background color", "text color", "unauthorized recolor",
)

# Overflow/stacking signals in visual regression
STRUCTURAL_REGRESSION_SIGNALS = (
    "horizontal overflow", "broken stacking", "clipped content", "missing section",
    "invisible element", "overlapping control", "size collapse", "layout shift",
    "spacing break", "unusable navigation", "missing cta", "content cut off",
    "extends beyond viewport",
)


class CriticEngine:
    """Evidence-based critic: never subjective, always rule-based."""

    def critique(self, session: RuntimeValidationSession) -> dict[str, Any]:
        """Run all critic checks and return a machine-readable critic_report."""
        report_id = f"critic_{uuid.uuid4().hex[:12]}"
        issues: list[dict[str, Any]] = []

        # 1. Plan drift check (always, even without runtime)
        issues.extend(self._check_plan_drift(session))

        # 2. Preservation check (always for existing-ui)
        if session.is_existing_ui():
            issues.extend(self._check_preservation(session))

        # 3. Runtime-based checks (require after_evidence)
        if session.has_runtime():
            issues.extend(self._check_runtime_errors(session))
            issues.extend(self._check_visual_regression(session))
            issues.extend(self._check_responsive(session))
            issues.extend(self._check_interactions(session))
            issues.extend(self._check_accessibility(session))
            issues.extend(self._check_missing_required_states(session))

        # 4. Overall status
        overall_status = self._compute_overall_status(session, issues)

        # 5. Build repair recommendations
        repairable_issues = [i for i in issues if i.get("repairable") and i.get("status") != PRE_EXISTING]
        blocked_issues = [i for i in issues if not i.get("repairable") and i.get("severity") in (HIGH, CRITICAL) and i.get("status") != PRE_EXISTING]

        repair_recommendation = self._build_repair_recommendation(issues, session)

        # 6. Evidence summary
        evidence_summary = self._build_evidence_summary(session)
        preservation_summary = self._build_preservation_summary(session, issues)
        runtime_summary = self._build_runtime_summary(session, issues)

        return {
            "schema_version": 1,
            "report_id": report_id,
            "session_id": session.session_id,
            "plan_id": session.plan_id,
            "workflow": session.workflow,
            "overall_status": overall_status,
            "summary": _build_summary(issues, overall_status),
            "issues": issues,
            "repairable_count": len(repairable_issues),
            "blocked_count": len(blocked_issues),
            "evidence_summary": evidence_summary,
            "preservation_summary": preservation_summary,
            "runtime_summary": runtime_summary,
            "repair_recommendation": repair_recommendation,
        }

    # ── Plan Drift ────────────────────────────────────────────────────────────

    def _check_plan_drift(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        manifest = session.change_manifest
        plan = session.modification_plan

        if not manifest or not plan:
            return issues

        # Reuse Phase 6 drift data if already computed
        drift = manifest.get("drift_detected", False)
        unexpected = manifest.get("unexpected_changes", [])

        blast_radius = plan.get("blast_radius", {})
        allowed_files = set(blast_radius.get("allowed_files", []))
        planned_level = plan.get("change_classification", {}).get("overall_level", "L1")
        actual_levels = manifest.get("actual_change_levels", [])

        for change in unexpected:
            reason = change.get("reason", "unexpected change")
            file_path = change.get("file", change.get("target", ""))
            change_type = change.get("type", "file")

            # Change level escalation detection
            if change_type == "level_escalation":
                actual_level = change.get("actual_level", "L3")
                severity = CRITICAL if actual_level == "L3" else HIGH
                issues.append(_make_issue(
                    category=PLAN_DRIFT,
                    severity=severity,
                    status=NEW_REGRESSION,
                    description=f"Change level escalation: plan={planned_level}, actual={actual_level}. "
                                f"This indicates scope was exceeded during implementation.",
                    affected_file=file_path,
                    evidence=f"Plan allowed {planned_level}; actual change at {actual_level} detected in change manifest.",
                    expected=f"Change level ≤ {planned_level}",
                    actual=f"Change level = {actual_level}",
                    likely_cause="Implementation exceeded authorized change level.",
                    repairable=False,
                    repair_scope=None,
                    permission_required="plan_amendment",
                ))
            elif file_path and file_path not in allowed_files:
                # Unauthorized file edit
                issues.append(_make_issue(
                    category=PLAN_DRIFT,
                    severity=CRITICAL,
                    status=NEW_REGRESSION,
                    description=f"Unauthorized file modification: '{file_path}' is outside the plan's allowed_files.",
                    affected_file=file_path,
                    evidence=f"allowed_files={list(allowed_files)[:5]}; '{file_path}' is not listed.",
                    expected=f"Edits restricted to {list(allowed_files)[:3]}...",
                    actual=f"'{file_path}' was modified.",
                    likely_cause="Implementation touched files outside the approved blast radius.",
                    repairable=False,
                    repair_scope=None,
                    permission_required="plan_amendment",
                ))
            else:
                # Generic drift
                issues.append(_make_issue(
                    category=PLAN_DRIFT,
                    severity=HIGH,
                    status=NEW_REGRESSION,
                    description=f"Plan drift detected: {reason}",
                    affected_file=file_path,
                    evidence=f"Change manifest reports unexpected change: {reason}",
                    expected="Changes within planned scope",
                    actual=reason,
                    likely_cause="Unplanned modification occurred during editing.",
                    repairable=False,
                    repair_scope=None,
                    permission_required=None,
                ))

        # Check for route drift
        planned_routes = set(plan.get("affected_surface", {}).get("routes", []))
        actual_routes = set(manifest.get("changed_routes", []))
        unexpected_routes = actual_routes - planned_routes
        for route in unexpected_routes:
            issues.append(_make_issue(
                category=PLAN_DRIFT,
                severity=CRITICAL,
                status=NEW_REGRESSION,
                description=f"Route '{route}' was touched but not in the modification plan.",
                affected_file=None,
                evidence=f"planned_routes={list(planned_routes)}; actual_routes={list(actual_routes)}.",
                expected=f"Routes modified: {list(planned_routes)}",
                actual=f"Additional route '{route}' was modified.",
                likely_cause="Implementation accidentally touched additional routes.",
                repairable=False,
                repair_scope=None,
                permission_required="plan_amendment",
            ))

        return issues

    # ── Preservation ──────────────────────────────────────────────────────────

    def _check_preservation(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        pres = session.preservation_profile
        if not pres:
            return issues

        # Check palette preservation via code diff signals
        palette_locked = pres.get("granular_permissions", {}).get("palette") == "locked"
        manifest = session.change_manifest
        plan = session.modification_plan

        if palette_locked and manifest:
            changed_tokens = manifest.get("changed_tokens", [])
            protected_tokens = plan.get("blast_radius", {}).get("protected_tokens", [])
            for token in changed_tokens:
                if any(pt in token for pt in (protected_tokens or [])) or _is_color_token(token):
                    issues.append(_make_issue(
                        category=PRESERVATION_VIOLATION,
                        severity=CRITICAL,
                        status=NEW_REGRESSION,
                        description=f"Color token '{token}' was modified despite palette being LOCKED under preservation policy.",
                        affected_file=None,
                        evidence=f"Change manifest reports token '{token}' modified. Preservation profile: palette=locked.",
                        expected="Color tokens unchanged (palette locked).",
                        actual=f"Token '{token}' was modified.",
                        likely_cause="Implementation bypassed palette preservation rules.",
                        repairable=False,
                        repair_scope=None,
                        permission_required="explicit_palette_permission",
                    ))

        # Check navigation preservation
        nav_locked = pres.get("granular_permissions", {}).get("navigation") in ("locked", "protected")
        if nav_locked and manifest:
            deleted_routes = manifest.get("deleted_files", [])
            changed_routes = manifest.get("changed_routes", [])
            protected_routes = plan.get("blast_radius", {}).get("protected_routes", [])
            for route in changed_routes:
                if route in protected_routes:
                    issues.append(_make_issue(
                        category=PRESERVATION_VIOLATION,
                        severity=CRITICAL,
                        status=NEW_REGRESSION,
                        description=f"Protected route '{route}' was modified despite navigation being protected.",
                        affected_file=None,
                        evidence=f"Route '{route}' is in protected_routes. Navigation lock: {nav_locked}.",
                        expected=f"Route '{route}' unchanged.",
                        actual=f"Route '{route}' was modified.",
                        likely_cause="Navigation route modified outside authorized scope.",
                        repairable=False,
                        repair_scope=None,
                        permission_required="explicit_navigation_permission",
                    ))

        # Check protected files
        modified_files = set(manifest.get("modified_files", []) if manifest else [])
        protected_files = set(plan.get("blast_radius", {}).get("protected_files", []))
        for f in modified_files.intersection(protected_files):
            issues.append(_make_issue(
                category=PRESERVATION_VIOLATION,
                severity=CRITICAL,
                status=NEW_REGRESSION,
                description=f"Protected file '{f}' was modified. This file is in the blast radius protected list.",
                affected_file=f,
                evidence=f"protected_files includes '{f}'; change manifest shows it was modified.",
                expected=f"'{f}' unmodified (protected).",
                actual=f"'{f}' was modified.",
                likely_cause="Implementation bypassed the protected file boundary.",
                repairable=False,
                repair_scope=None,
                permission_required="plan_amendment",
            ))

        return issues

    # ── Runtime Errors ────────────────────────────────────────────────────────

    def _check_runtime_errors(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        after_errors = session.get_console_errors()
        before_errors_msgs = {e.get("message", "") for e in session.get_before_console_errors()}

        for err in after_errors:
            msg = err.get("message", "")
            page = err.get("page_id", err.get("route", "/"))
            viewport = err.get("viewport", "unknown")

            is_pre_existing = msg in before_errors_msgs
            status = PRE_EXISTING if is_pre_existing else NEW_REGRESSION

            issues.append(_make_issue(
                category=RUNTIME_ERROR,
                severity=HIGH if not is_pre_existing else LOW,
                status=status,
                description=f"Console error detected: {msg[:200]}",
                page=page,
                viewport=viewport,
                evidence=f"console error: {msg[:300]}",
                expected="No console errors.",
                actual=f"Error: {msg[:200]}",
                likely_cause="JavaScript runtime error introduced or surfaced by edit.",
                repairable=not is_pre_existing,
                repair_scope="affected file if traceable",
                permission_required=None,
            ))

        # Check capture failures in after evidence
        for cap in session.after_evidence.get("captures", []):
            if cap.get("status") == "SCREENSHOT_FAILURE":
                page = cap.get("page_id", cap.get("route", "/"))
                viewport = cap.get("viewport", "unknown")
                issues.append(_make_issue(
                    category=RUNTIME_ERROR,
                    severity=HIGH,
                    status=NEW_REGRESSION,
                    description=f"Page render failure at {page} ({viewport}) – screenshot could not be captured.",
                    page=page,
                    viewport=viewport,
                    evidence=f"capture status=SCREENSHOT_FAILURE for page_id={page}, viewport={viewport}.",
                    expected="Successful page render.",
                    actual="Render failure / blank page.",
                    likely_cause="JavaScript error, missing route handler, or broken component introduced by edit.",
                    repairable=True,
                    repair_scope="affected component or route handler",
                    permission_required=None,
                ))

        return issues

    # ── Visual Regression ─────────────────────────────────────────────────────

    def _check_visual_regression(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        """Structure-aware visual regression check from evidence metadata.

        Relies on runtime probe data and basic_render info from browser.py captures.
        Does NOT do pixel-perfect diff – avoids false positives from subpixel rendering.
        """
        issues: list[dict[str, Any]] = []
        pairs = session.build_evidence_pairs()

        for pair in pairs:
            if pair["status"] == EVIDENCE_STATUS_NO_RUNTIME:
                continue

            after = pair.get("after") or {}
            before = pair.get("before") or {}
            page = pair["page"]
            vp = pair["viewport"]

            # Check basic_render regression
            before_render = before.get("basic_render", {}) if before else {}
            after_render = after.get("basic_render", {}) if after else {}

            if before_render.get("text", 0) > 50 and after_render.get("text", 0) < 10:
                issues.append(_make_issue(
                    category=VISUAL_REGRESSION,
                    severity=CRITICAL,
                    status=NEW_REGRESSION,
                    description=f"Page content collapsed at {page} ({vp}). Before: {before_render.get('text')} chars; After: {after_render.get('text')} chars.",
                    page=page,
                    viewport=vp,
                    evidence=f"basic_render.text: before={before_render.get('text')}, after={after_render.get('text')}. Content may have been removed or page broken.",
                    expected="Meaningful content rendered.",
                    actual="Near-empty page after editing.",
                    likely_cause="Component render failure or conditional rendering bug.",
                    repairable=True,
                    repair_scope="affected component",
                    permission_required=None,
                ))

            # Check for root element presence
            if before_render.get("root") and not after_render.get("root"):
                issues.append(_make_issue(
                    category=VISUAL_REGRESSION,
                    severity=CRITICAL,
                    status=NEW_REGRESSION,
                    description=f"Root element (#root, #app, main) missing at {page} ({vp}).",
                    page=page,
                    viewport=vp,
                    evidence="after evidence: basic_render.root=false; before evidence: basic_render.root=true.",
                    expected="Root element present.",
                    actual="Root element missing – likely app-level crash.",
                    likely_cause="App-level JS error from edit caused root render failure.",
                    repairable=True,
                    repair_scope="affected component or app root",
                    permission_required=None,
                ))

            # Check motion probe for overflow signals
            probe = after.get("motion_probe", {}) if after else {}
            before_probe = before.get("motion_probe", {}) if before else {}
            before_had_overflow = isinstance(before_probe, dict) and before_probe.get("overflow_detected")

            if isinstance(probe, dict) and probe.get("overflow_detected"):
                overflow_detail = probe.get("overflow_detail", f"horizontal overflow detected at {vp}")
                mobile_vp = vp in ("mobile_375", "mobile", "375")
                severity = HIGH if mobile_vp else MEDIUM
                # If before also had overflow, this is pre-existing
                is_pre_existing = before_had_overflow
                issues.append(_make_issue(
                    category=RESPONSIVE_FAILURE if mobile_vp else VISUAL_REGRESSION,
                    severity=LOW if is_pre_existing else severity,
                    status=PRE_EXISTING if is_pre_existing else NEW_REGRESSION,
                    description=f"Layout overflow detected at {page} ({vp}): {overflow_detail}",
                    page=page,
                    viewport=vp,
                    evidence=f"motion_probe reports overflow_detected=true. Detail: {overflow_detail}"
                             f"{' (pre-existing: same issue present in before evidence)' if is_pre_existing else ''}",
                    expected="No overflow at any viewport.",
                    actual=f"Overflow at {vp}: {overflow_detail}",
                    likely_cause="Fixed width, missing max-width, or min-width constraint exceeds viewport.",
                    repairable=True,
                    repair_scope="CSS overflow fix in affected component",
                    permission_required=None,
                ))

        return issues

    # ── Responsive ───────────────────────────────────────────────────────────

    def _check_responsive(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        """Check for responsive-specific failures based on evidence metadata."""
        issues: list[dict[str, Any]] = []
        required_checks = session.get_required_checks()
        viewports = session.get_affected_viewports()

        if "responsive_viewport_matrix" not in required_checks:
            return issues

        mobile_vps = [v for v in viewports if "mobile" in v or "375" in v]
        if not mobile_vps:
            return issues

        pairs = session.build_evidence_pairs()
        for pair in pairs:
            if pair["viewport"] not in mobile_vps:
                continue
            if pair["status"] == EVIDENCE_STATUS_NO_RUNTIME:
                continue

            after = pair.get("after") or {}
            before = pair.get("before") or {}
            page = pair["page"]
            vp = pair["viewport"]

            # Capture failures on mobile = responsive failure
            if after.get("status") == "SCREENSHOT_FAILURE" and (not before or before.get("status") == "CAPTURED"):
                issues.append(_make_issue(
                    category=RESPONSIVE_FAILURE,
                    severity=HIGH,
                    status=NEW_REGRESSION,
                    description=f"Mobile capture failure at {page} ({vp}) – page not renderable at this viewport.",
                    page=page,
                    viewport=vp,
                    evidence="after capture: status=SCREENSHOT_FAILURE; before capture was successful.",
                    expected="Successful render at mobile viewport.",
                    actual="Capture failure at mobile.",
                    likely_cause="Fixed-width layout, viewport-breaking CSS, or component not responsive.",
                    repairable=True,
                    repair_scope="responsive CSS in affected component",
                    permission_required=None,
                ))

        return issues

    # ── Interaction Scenarios ─────────────────────────────────────────────────

    def _check_interactions(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        """Check interaction scenario results from after evidence."""
        issues: list[dict[str, Any]] = []
        interaction_results = session.after_evidence.get("interaction_results", [])
        before_interaction_results = session.before_evidence.get("interaction_results", [])

        before_failures = {r.get("scenario_id") for r in before_interaction_results if r.get("status") == "FAILED"}

        for result in interaction_results:
            if result.get("status") == "FAILED":
                scenario_id = result.get("scenario_id", "unknown")
                page = result.get("page", "/")
                is_pre_existing = scenario_id in before_failures

                issues.append(_make_issue(
                    category=INTERACTION_FAILURE,
                    severity=HIGH if not is_pre_existing else MEDIUM,
                    status=PRE_EXISTING if is_pre_existing else NEW_REGRESSION,
                    description=f"Interaction scenario '{scenario_id}' failed at {page}. {result.get('error', '')}",
                    page=page,
                    viewport=result.get("viewport", "desktop_1440"),
                    scenario=scenario_id,
                    evidence=f"Interaction result: {result.get('error', 'no details')}",
                    expected=result.get("expected", "Interaction completes successfully."),
                    actual=result.get("actual", f"Scenario '{scenario_id}' failed."),
                    likely_cause=result.get("likely_cause", "Component interaction broken by edit."),
                    repairable=not is_pre_existing,
                    repair_scope="affected component interaction handler",
                    permission_required=None,
                ))

        return issues

    # ── Accessibility ─────────────────────────────────────────────────────────

    def _check_accessibility(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        """Check for accessibility regressions from axe scan results."""
        issues: list[dict[str, Any]] = []
        a11y_checks = session.get_accessibility_checks()

        if not a11y_checks:
            return issues

        after_scans = session.after_evidence.get("accessibility_scans", [])
        before_scans = session.before_evidence.get("accessibility_scans", [])

        # Build before violation index by (page, viewport, rule)
        before_violations: set[tuple[str, str, str]] = set()
        for scan in before_scans:
            for v in scan.get("violations", []):
                before_violations.add((scan.get("route", "/"), scan.get("viewport", ""), v.get("id", "")))

        for scan in after_scans:
            page = scan.get("route", scan.get("page", "/"))
            vp = scan.get("viewport", "desktop_1440")
            for violation in scan.get("violations", []):
                rule_id = violation.get("id", "")
                is_pre_existing = (page, vp, rule_id) in before_violations

                issues.append(_make_issue(
                    category=ACCESSIBILITY_REGRESSION,
                    severity=HIGH if not is_pre_existing else LOW,
                    status=PRE_EXISTING if is_pre_existing else NEW_REGRESSION,
                    description=f"Accessibility violation: rule '{rule_id}' at {page} ({vp}). {violation.get('description', '')}",
                    page=page,
                    viewport=vp,
                    evidence=f"axe violation: rule={rule_id}, impact={violation.get('impact', 'unknown')}. "
                             f"{'Pre-existing issue.' if is_pre_existing else 'New regression introduced by edit.'}",
                    expected="No accessibility violations.",
                    actual=f"axe rule '{rule_id}' fails.",
                    likely_cause="Edit removed aria attribute, label, or changed DOM structure breaking a11y.",
                    repairable=not is_pre_existing,
                    repair_scope="add missing aria/label attribute",
                    permission_required=None,
                ))

        return issues

    # ── Missing Required States ───────────────────────────────────────────────

    def _check_missing_required_states(self, session: RuntimeValidationSession) -> list[dict[str, Any]]:
        """Check domain pack required states are present in implementation."""
        issues: list[dict[str, Any]] = []
        required_states = session.get_required_states()
        if not required_states:
            return issues

        implemented_states = set(session.after_evidence.get("implemented_states", []))
        pages = session.get_affected_pages()

        for state in required_states:
            if state not in implemented_states:
                # Only report for pages in affected surface
                issues.append(_make_issue(
                    category=MISSING_REQUIRED_STATE,
                    severity=MEDIUM,
                    status=NEW_REGRESSION,
                    description=f"Required UI state '{state}' is missing from the implementation. "
                                f"Domain pack requires this state to be handled.",
                    page=pages[0] if pages else "/",
                    viewport="desktop_1440",
                    evidence=f"Domain pack required_states includes '{state}'; not found in after evidence implemented_states.",
                    expected=f"State '{state}' handled in UI.",
                    actual=f"State '{state}' not implemented.",
                    likely_cause="Implementation did not add the required domain UI state pattern.",
                    repairable=True,
                    repair_scope=f"add UI state '{state}' to affected component",
                    permission_required=None,
                ))

        return issues

    # ── Status Resolution ─────────────────────────────────────────────────────

    def _compute_overall_status(
        self, session: RuntimeValidationSession, issues: list[dict[str, Any]]
    ) -> str:
        new_issues = [i for i in issues if i.get("status") in (NEW_REGRESSION, WORSENED)]

        if not new_issues:
            return "pass"

        max_severity = max((SEVERITY_ORDER.get(i.get("severity", INFO), 0) for i in new_issues), default=0)

        if not session.has_runtime():
            # No browser runtime – can only verify code-level checks
            critical = any(i.get("severity") == CRITICAL for i in new_issues)
            if critical:
                return "blocked"
            return "warn"

        if max_severity >= SEVERITY_ORDER[CRITICAL]:
            return "fail"
        if max_severity >= SEVERITY_ORDER[HIGH]:
            return "fail"
        if max_severity >= SEVERITY_ORDER[MEDIUM]:
            return "warn"
        return "warn"

    # ── Summary builders ──────────────────────────────────────────────────────

    def _build_repair_recommendation(
        self, issues: list[dict[str, Any]], session: RuntimeValidationSession
    ) -> dict[str, Any]:
        new_issues = [i for i in issues if i.get("status") in (NEW_REGRESSION, WORSENED)]
        repairable = [i for i in new_issues if i.get("repairable")]
        not_repairable = [i for i in new_issues if not i.get("repairable")]

        if not new_issues:
            decision = "PASS"
        elif not_repairable:
            decision = "BLOCKED" if any(
                i.get("permission_required") for i in not_repairable
            ) else "BLOCKED"
            if all(i.get("permission_required") for i in not_repairable):
                decision = "NEEDS_USER_PERMISSION"
        elif repairable:
            decision = "REPAIRABLE"
        else:
            decision = "PASS"

        return {
            "decision": decision,
            "repairable_issues": [i["issue_id"] for i in repairable],
            "blocked_issues": [i["issue_id"] for i in not_repairable],
            "repair_priority": _compute_repair_priority(repairable),
        }

    def _build_evidence_summary(self, session: RuntimeValidationSession) -> dict[str, Any]:
        pairs = session.build_evidence_pairs()
        return {
            "runtime_available": session.has_runtime(),
            "baseline_available": session.has_baseline(),
            "evidence_pairs": len(pairs),
            "valid_pairs": sum(1 for p in pairs if p["status"] == EVIDENCE_STATUS_VALID),
            "affected_pages": session.get_affected_pages(),
            "affected_viewports": session.get_affected_viewports(),
        }

    def _build_preservation_summary(
        self, session: RuntimeValidationSession, issues: list[dict[str, Any]]
    ) -> dict[str, Any]:
        pres_issues = [i for i in issues if i.get("category") == PRESERVATION_VIOLATION]
        pres = session.preservation_profile
        return {
            "preservation_required": session.is_existing_ui(),
            "palette_status": pres.get("granular_permissions", {}).get("palette", "unknown"),
            "navigation_status": pres.get("granular_permissions", {}).get("navigation", "unknown"),
            "violations_found": len(pres_issues),
            "all_pass": len(pres_issues) == 0,
        }

    def _build_runtime_summary(
        self, session: RuntimeValidationSession, issues: list[dict[str, Any]]
    ) -> dict[str, Any]:
        runtime_issues = [i for i in issues if i.get("category") == RUNTIME_ERROR]
        new_runtime = [i for i in runtime_issues if i.get("status") == NEW_REGRESSION]
        return {
            "runtime_available": session.has_runtime(),
            "total_runtime_issues": len(runtime_issues),
            "new_regressions": len(new_runtime),
            "pre_existing": len(runtime_issues) - len(new_runtime),
        }


# ── Issue factory ─────────────────────────────────────────────────────────────

def _make_issue(
    category: str,
    severity: str,
    status: str,
    description: str,
    evidence: str,
    expected: str,
    actual: str,
    likely_cause: str,
    repairable: bool,
    page: str = "/",
    viewport: str = "desktop_1440",
    scenario: str = "default",
    affected_file: str | None = None,
    affected_component: str | None = None,
    repair_scope: str | None = None,
    permission_required: str | None = None,
) -> dict[str, Any]:
    """Build a standardized, evidence-based issue dict."""
    return {
        "issue_id": f"issue_{uuid.uuid4().hex[:8]}",
        "category": category,
        "severity": severity,
        "status": status,
        "description": description,
        "page": page,
        "viewport": viewport,
        "scenario": scenario,
        "affected_file": affected_file,
        "affected_component": affected_component,
        "evidence": evidence,
        "expected": expected,
        "actual": actual,
        "likely_cause": likely_cause,
        "repairable": repairable,
        "repair_scope": repair_scope,
        "permission_required": permission_required,
    }


def _build_summary(issues: list[dict[str, Any]], overall_status: str) -> str:
    new_issues = [i for i in issues if i.get("status") in (NEW_REGRESSION, WORSENED)]
    pre_existing = [i for i in issues if i.get("status") == PRE_EXISTING]
    critical = [i for i in new_issues if i.get("severity") == CRITICAL]
    high = [i for i in new_issues if i.get("severity") == HIGH]

    parts = [f"Overall: {overall_status.upper()}"]
    if critical:
        parts.append(f"{len(critical)} CRITICAL issue(s)")
    if high:
        parts.append(f"{len(high)} HIGH issue(s)")
    if new_issues and not critical and not high:
        parts.append(f"{len(new_issues)} new issue(s)")
    if pre_existing:
        parts.append(f"{len(pre_existing)} pre-existing (not attributed to current edit)")
    if not new_issues:
        parts.append("No new regressions detected.")
    return ". ".join(parts) + "."


def _compute_repair_priority(repairable: list[dict[str, Any]]) -> list[str]:
    """Order repair priority by severity then category."""
    order = {
        RUNTIME_ERROR: 0,
        PRESERVATION_VIOLATION: 1,
        PLAN_DRIFT: 2,
        INTERACTION_FAILURE: 3,
        RESPONSIVE_FAILURE: 4,
        ACCESSIBILITY_REGRESSION: 5,
        VISUAL_REGRESSION: 6,
        MISSING_REQUIRED_STATE: 7,
    }
    sorted_issues = sorted(
        repairable,
        key=lambda i: (
            -SEVERITY_ORDER.get(i.get("severity", INFO), 0),
            order.get(i.get("category", ""), 99),
        )
    )
    return [i["issue_id"] for i in sorted_issues]


def _is_color_token(token: str) -> bool:
    """Heuristic check if a token name relates to colors."""
    return bool(re.search(r"\b(color|palette|brand|primary|secondary|background|foreground|text|border|fill)\b", token, re.I))
