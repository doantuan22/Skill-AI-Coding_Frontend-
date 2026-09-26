"""UX Flow Analyzer: Identifies recognized user flows and flags missing states or friction signals."""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def analyze_ux_flows(
    repo_profile: dict[str, Any],
    snapshot: RepositorySnapshot | None = None,
) -> dict[str, Any]:
    """Examine routes, pages, and components for UX flows and state completeness."""
    routes = repo_profile.get("routes", [])
    pages = repo_profile.get("pages", [])

    flows: list[str] = []
    detected_states: list[str] = []
    missing_states: list[str] = []
    friction_signals: list[str] = []
    evidence: list[str] = []

    all_route_paths = [r.get("path", "").lower() for r in routes]

    # 1. Identify recognized flows by routes and page names
    for p in all_route_paths:
        if any(term in p for term in ("login", "signin", "auth", "register", "signup")):
            if "authentication" not in flows:
                flows.append("authentication")
                evidence.append(f"Identified authentication flow at route '{p}'")
        elif "dashboard" in p or "overview" in p or "analytics" in p:
            if "dashboard" not in flows:
                flows.append("dashboard")
                evidence.append(f"Identified dashboard/metrics flow at route '{p}'")
        elif "search" in p or "explore" in p or "filter" in p:
            if "search_and_browse" not in flows:
                flows.append("search_and_browse")
        elif any(term in p for term in ("checkout", "cart", "payment", "order")):
            if "checkout" not in flows:
                flows.append("checkout")
        elif "settings" in p or "profile" in p or "account" in p:
            if "account_settings" not in flows:
                flows.append("account_settings")
        elif any(term in p for term in ("new", "edit", "create", "manage", "items", "users")):
            if "crud_management" not in flows:
                flows.append("crud_management")

    if not flows and routes:
        flows.append("content_presentation")

    # 2. Inspect component/page markup for state handling
    if snapshot:
        sample_files = [p.get("file") for p in pages[:8] if p.get("file")]
        combined_text = "\n".join(snapshot.read_text(f, max_chars=12_000) for f in sample_files)

        # Check for loading state handling
        has_loading = bool(re.search(r'\b(?:isLoading|loading|pending|skeleton|spinner|fallback)\b', combined_text, re.I))
        if has_loading:
            detected_states.append("loading")
        else:
            missing_states.append("loading_state_coverage")
            friction_signals.append("No loading or skeleton state handling detected in examined page components.")

        # Check for error state handling
        has_error = bool(re.search(r'\b(?:isError|error|errorMessage|alert|toast\.error)\b', combined_text, re.I))
        if has_error:
            detected_states.append("error")
        else:
            missing_states.append("error_state_feedback")
            friction_signals.append("No explicit error banner or form error state handling detected.")

        # Check for empty state handling
        has_empty = bool(re.search(r'\b(?:empty|no\s+results|length\s*===?\s*0|not\s+found)\b', combined_text, re.I))
        if has_empty:
            detected_states.append("empty")
        else:
            missing_states.append("empty_state_handling")

        # Check for destructive confirmation
        has_destructive_action = bool(re.search(r'\b(?:delete|remove|destroy)\b', combined_text, re.I))
        has_dialog_confirm = bool(re.search(r'\b(?:confirm|dialog|alertdialog|modal)\b', combined_text, re.I))
        if has_destructive_action and not has_dialog_confirm:
            friction_signals.append("Destructive actions present without explicit confirmation dialog pattern.")

    conf = 0.85 if routes or pages else 0.40

    return {
        "flows": flows,
        "states": detected_states or ["standard_display"],
        "missing_states": missing_states,
        "friction_signals": friction_signals,
        "confidence": conf,
        "evidence": evidence or ["UX flows evaluated from page entry points and route structures."],
    }
