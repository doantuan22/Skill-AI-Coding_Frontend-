"""Component Consistency Analyzer: Evaluates component variants, consistency, and detects anomalies/duplicates."""
from __future__ import annotations

import re
from typing import Any

from uiux.engine.repo_intelligence.scanner import RepositorySnapshot


def analyze_component_consistency(
    repo_profile: dict[str, Any],
    snapshot: RepositorySnapshot | None = None,
) -> dict[str, Any]:
    """Inspect component inventory to detect canonical patterns, variants, and inconsistencies."""
    comp_data = repo_profile.get("components", {})
    shared = comp_data.get("shared", [])
    primitives = comp_data.get("primitives", [])
    duplicates = comp_data.get("possible_duplicates", [])

    evidence: list[str] = []
    anomalies: list[str] = []
    severity = "info"

    # 1. Canonical primitive detection
    button_files = [f for f in [*primitives, *shared] if "button" in f.lower()]
    input_files = [f for f in [*primitives, *shared] if "input" in f.lower()]
    modal_files = [f for f in [*primitives, *shared] if any(k in f.lower() for k in ("modal", "dialog"))]

    variants: dict[str, list[str]] = {}
    canonical_patterns: dict[str, str | None] = {
        "button": button_files[0] if button_files else None,
        "input": input_files[0] if input_files else None,
        "modal": modal_files[0] if modal_files else None,
    }

    if button_files:
        evidence.append(f"Canonical button component detected at '{button_files[0]}'")
    if input_files:
        evidence.append(f"Canonical input component detected at '{input_files[0]}'")

    # 2. Inspect button source code for variant consistency if snapshot available
    if snapshot and button_files:
        btn_text = snapshot.read_text(button_files[0], max_chars=15_000)
        # Find variants (cva, switch, or props)
        found_variants = re.findall(r'(?:variant|intent)\s*[:=]\s*\{([^}]+)\}', btn_text)
        if found_variants:
            v_keys = re.findall(r'(\w+)\s*:', found_variants[0])
            variants["button"] = v_keys
            evidence.append(f"Button component exports variants: {', '.join(v_keys)}")
        else:
            variants["button"] = ["default", "primary", "secondary"]

    # 3. Inconsistency & Anomaly Detection
    # Case: Multiple duplicate button files across different subdirectories
    if len(button_files) > 1:
        anomalies.append(f"Multiple button implementations detected: {', '.join(button_files)}. Risk of inconsistent styling.")
        severity = "medium"

    # Check for duplicate names from Phase 2
    if duplicates:
        for d in duplicates:
            anomalies.append(f"Duplicated component name across paths: {d}")
        if severity == "info":
            severity = "low"

    # Check for hardcoded button styling in other components bypassing canonical button
    if snapshot and button_files:
        other_files = [f for f in snapshot.files if f.endswith((".tsx", ".jsx", ".vue")) and f != button_files[0]][:10]
        ad_hoc_button_count = 0
        for of in other_files:
            txt = snapshot.read_text(of, max_chars=10_000)
            if re.search(r'<button\s+[^>]*class(?:Name)?=[\'"][^\'"]*(?:bg-|p-\d|rounded)[^\'"]*[\'"]', txt):
                ad_hoc_button_count += 1
        if ad_hoc_button_count >= 2:
            anomalies.append(f"Detected {ad_hoc_button_count} occurrences of raw <button> tags with custom classes bypassing canonical Button component.")
            severity = "medium"

    # Consistency classification
    if not anomalies:
        consistency = "high" if len(primitives) >= 2 else "moderate"
        evidence.append("No component styling anomalies or duplicate conflicts detected.")
    elif len(anomalies) <= 1:
        consistency = "moderate"
    elif len(anomalies) <= 3:
        consistency = "low"
    else:
        consistency = "inconsistent"

    conf = 0.85 if shared or primitives else 0.50

    return {
        "variants": variants,
        "consistency": consistency,
        "shared_patterns": [f for f in shared if f not in duplicates],
        "anomalies": anomalies,
        "canonical_patterns": canonical_patterns,
        "duplicate_signals": duplicates,
        "severity": severity,
        "confidence": conf,
        "evidence": evidence,
    }
