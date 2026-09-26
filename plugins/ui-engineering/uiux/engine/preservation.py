"""Preservation policy, Change Budget (L1/L2/L3) and Permission Model.

This module implements the hard preservation rules and granular permissions required
by the UI Orchestrator:
- PRESERVE FIRST -> IMPROVE SECOND -> REDESIGN ONLY WHEN EXPLICITLY REQUESTED
- Granular permission model: layout permission != palette permission, palette != architecture rebuild
- L1 (Safe Refinement): Allowed by default
- L2 (Local Structural Change): Justified only by default
- L3 (Major Redesign): Denied by default, requires explicit user permission
- Vague enhancement phrases ("modernize", "làm đẹp", "make it professional") DO NOT grant L3
- Strict Precedence Hierarchy (1..8)
"""
from __future__ import annotations

import re
from typing import Any

# Change budget levels
L1 = "L1"  # Safe refinement (spacing, typography scale, responsive, states, a11y, consistency)
L2 = "L2"  # Local structural change (component layout, section arrangement, form flow)
L3 = "L3"  # Major redesign (global palette, branding, page architecture, rebuild)

# Precedence hierarchy: 1 has the highest priority, 8 has the lowest
PRECEDENCE_HIERARCHY = [
    "1. Explicit user instruction",
    "2. Existing brand identity",
    "3. Existing design system",
    "4. Existing UX / information architecture",
    "5. Repository/framework constraints",
    "6. Domain best practices",
    "7. Design inspiration",
    "8. AI preference",
]

# Regex patterns for vague enhancement phrases (CANNOT grant L3, CANNOT unlock palette/branding)
VAGUE_ENHANCEMENT_PATTERNS = [
    r"\bmodernize\b",
    r"\blàm đẹp\b",
    r"\bnâng cấp\b",
    r"\bđồng bộ giao diện\b",
    r"\bmake\s+it\s+(?:look\s+)?(?:more\s+)?(?:professional|clean|modern|better|pretty)\b",
    r"\brefresh\s+(?:the\s+)?(?:ui|look|design)\b",
    r"\bimprove\s+(?:the\s+)?(?:ui|ux|interface|look|appearance)\b",
    r"\bclean\s+up\s+(?:the\s+)?ui\b",
    r"\btút\s+tát\b",
]

# Regex patterns indicating explicit L3 permissions in prompt text
EXPLICIT_REDESIGN_PATTERNS = [
    r"\bredesign\s+toàn\s+bộ\b",
    r"\bthay\s+(?:đổi\s+)?(?:toàn\s+bộ\s+)?brand\b",
    r"\bthay\s+đổi\s+bản\s+sắc\s+thương\s+hiệu\b",
    r"\bđược\s+phép\s+thay\s+đổi\s+(?:navigation|kiến\s+trúc)\b",
    r"\bxây\s+lại\s+(?:ui|giao\s+diện)\s+từ\s+đầu\b",
    r"\brebuild\s+(?:the\s+)?(?:ui|interface)\s+from\s+scratch\b",
    r"\bfull\s+redesign\b",
    r"\boverhaul\s+(?:the\s+)?(?:ui|branding)\b",
    r"\bcomplete\s+redesign\b",
]

# Patterns for explicit palette change permission
PALETTE_CHANGE_PATTERNS = [
    r"\b(?:đổi|thay\s+đổi|thay)\s+(?:toàn\s+bộ\s+)?(?:palette|bảng\s+màu|tông\s+màu|màu(?:\s+sắc)?)\b",
    r"\bthay\s+màu\b",
    r"\bchange\s+(?:the\s+)?(?:palette|colors?|color\s+scheme|theme)\b",
    r"\bnew\s+color\s+palette\b",
    r"\bsang\s+tông\b",
]

# Patterns for explicit layout / architecture permission
LAYOUT_CHANGE_PATTERNS = [
    r"\bđược\s+phép\s+thay\s+đổi\s+layout\b",
    r"\bthay\s+đổi\s+bố\s+cục\b",
    r"\bchange\s+(?:the\s+)?layout\b",
    r"\brestructure\s+(?:the\s+)?layout\b",
    r"\breorganize\s+(?:the\s+)?sections?\b",
]

# Patterns for local component scope
LOCAL_SCOPE_PATTERNS = [
    r"\b(?:chỉ\s+)?(?:sửa|chỉnh|thay|cải\s+thiện)\s+(?:nút|button|form|input|modal|dialog|card|header|footer)\b",
    r"\b(?:fix|update|style|refine)\s+(?:the\s+)?(?:button|form|input|modal|card|dropdown)\b",
    r"\bsingle\s+component\b",
]


def is_vague_enhancement(text: str) -> bool:
    """Return True if text only contains generic/vague improvement requests."""
    t = text.lower()
    return any(re.search(pat, t) for pat in VAGUE_ENHANCEMENT_PATTERNS)


def extract_explicit_permissions(
    user_request: str,
    explicit_permissions: dict[str, Any] | None = None,
) -> dict[str, bool]:
    """Parse explicit user permissions from structured dictionary or textual prompt.

    Ensures permissions are strictly granular:
    - allow_palette_change does NOT imply allow_architecture_change.
    - allow_layout_change does NOT imply allow_palette_change.
    - Vague enhancement phrases do NOT imply any L3 permission.
    """
    req_lower = user_request.lower()
    perms: dict[str, bool] = {
        "allow_palette_change": False,
        "allow_branding_change": False,
        "allow_layout_change": False,
        "allow_navigation_change": False,
        "allow_architecture_change": False,
        "allow_rebuild": False,
        "explicit_l3_granted": False,
    }

    # 1. Text heuristics for explicit permission phrasing
    has_explicit_redesign = any(re.search(p, req_lower) for p in EXPLICIT_REDESIGN_PATTERNS)
    if has_explicit_redesign:
        perms["explicit_l3_granted"] = True
        if any(term in req_lower for term in ("từ đầu", "from scratch", "redesign toàn bộ", "full redesign")):
            perms["allow_rebuild"] = True
            perms["allow_architecture_change"] = True

    # Granular check for palette
    if any(re.search(p, req_lower) for p in PALETTE_CHANGE_PATTERNS):
        perms["allow_palette_change"] = True
        perms["explicit_l3_granted"] = True

    # Granular check for layout
    if any(re.search(p, req_lower) for p in LAYOUT_CHANGE_PATTERNS):
        perms["allow_layout_change"] = True

    # 2. Structured input strictly overrides text heuristics (highest precedence)
    if explicit_permissions and isinstance(explicit_permissions, dict):
        for key in (
            "allow_palette_change", "allow_branding_change", "allow_layout_change",
            "allow_navigation_change", "allow_architecture_change", "allow_rebuild"
        ):
            if key in explicit_permissions:
                perms[key] = bool(explicit_permissions[key])
        allowed_levels = explicit_permissions.get("allowed_levels", [])
        if "L3" in allowed_levels:
            perms["explicit_l3_granted"] = True
        elif allowed_levels and "L3" not in allowed_levels and not perms["allow_palette_change"] and not perms["allow_rebuild"]:
            perms["explicit_l3_granted"] = False

    # Granular check for palette
    if any(re.search(p, req_lower) for p in PALETTE_CHANGE_PATTERNS):
        perms["allow_palette_change"] = True

    # Granular check for layout
    if any(re.search(p, req_lower) for p in LAYOUT_CHANGE_PATTERNS):
        perms["allow_layout_change"] = True

    return perms


def infer_requested_scope(user_request: str, requested_scope: str = "unspecified") -> str:
    """Classify the scope (component, local, page, global) from input or text."""
    if requested_scope != "unspecified":
        return requested_scope
    req_lower = user_request.lower()
    if any(re.search(p, req_lower) for p in LOCAL_SCOPE_PATTERNS):
        return "component"
    if any(term in req_lower for term in ("toàn bộ", "all pages", "global", "entire app", "hệ thống")):
        return "global"
    if any(term in req_lower for term in ("trang", "page", "screen", "view")):
        return "page"
    return "unspecified"


def evaluate_preservation_policy(
    workflow: str,
    ui_state: str,
    user_request: str,
    explicit_permissions: dict[str, Any] | None = None,
    requested_scope: str = "unspecified",
) -> dict[str, Any]:
    """Evaluate hard preservation rules, L1/L2/L3 change budget, and granular permissions.

    Machine-readable output matching Orchestrator contract.
    """
    scope = infer_requested_scope(user_request, requested_scope)
    perms = extract_explicit_permissions(user_request, explicit_permissions)

    # Greenfield workflow:
    # No existing UI to preserve by default, full design freedom unless user specified constraints
    if workflow == "greenfield" or ui_state == "GREENFIELD":
        return {
            "preservation_required": False,
            "design_freedom": "high",
            "protected_properties": {
                "color_palette": "unlocked",
                "brand_identity": "unlocked",
                "overall_layout_identity": "unprotected",
                "navigation_model": "unprotected",
                "information_architecture": "unprotected",
                "component_structure": "uncontrolled",
            },
            "allowed_change_level": {
                "safe_refinement": True,
                "local_structural_change": "allowed",
                "major_redesign": "granted",
                "max_level": L3,
            },
            "permissions_detail": {
                "palette_editable": True,
                "branding_editable": True,
                "layout_editable": True,
                "navigation_editable": True,
                "architecture_editable": True,
                "rebuild_allowed": True,
            },
            "precedence_order": PRECEDENCE_HIERARCHY,
            "scope": scope,
            "notes": [
                "Greenfield project: AI may establish design direction, tokens, and IA.",
                "Explicit user instructions (palette, style, framework) take precedence over AI defaults.",
            ],
        }

    # Unknown workflow: safe fallback
    if workflow == "unknown" or ui_state == "UNKNOWN":
        return {
            "preservation_required": True,
            "design_freedom": "constrained",
            "protected_properties": {
                "color_palette": "locked",
                "brand_identity": "locked",
                "overall_layout_identity": "protected",
                "navigation_model": "protected",
                "information_architecture": "protected",
                "component_structure": "controlled",
            },
            "allowed_change_level": {
                "safe_refinement": True,
                "local_structural_change": "justified_only",
                "major_redesign": "denied",
                "max_level": L1,
            },
            "permissions_detail": {
                "palette_editable": False,
                "branding_editable": False,
                "layout_editable": False,
                "navigation_editable": False,
                "architecture_editable": False,
                "rebuild_allowed": False,
            },
            "precedence_order": PRECEDENCE_HIERARCHY,
            "scope": scope,
            "notes": [
                "UI State is UNKNOWN: conservative preservation applied.",
                "Inspection required before proceeding with any structural or visual modification.",
            ],
        }

    # EXISTING_UI or PARTIAL_UI: HARD PRESERVATION RULES APPLY
    # HARD RULE: PRESERVE FIRST -> IMPROVE SECOND -> REDESIGN ONLY WHEN EXPLICITLY REQUESTED
    color_palette_state = "unlocked" if perms["allow_palette_change"] else "locked"
    brand_identity_state = "unlocked" if perms["allow_branding_change"] else "locked"
    layout_identity_state = "unprotected" if perms["allow_layout_change"] else "protected"
    navigation_state = "unprotected" if perms["allow_navigation_change"] else "protected"
    architecture_state = "unprotected" if perms["allow_architecture_change"] else "protected"

    # Local scope restriction (Case 6)
    is_local_scope = scope in ("component", "local", "section")

    # Determine max change level
    if perms["explicit_l3_granted"] and not is_local_scope:
        max_level = L3
        major_redesign_status = "granted"
        design_freedom = "medium"
    elif is_local_scope:
        max_level = L2  # Local component scope cannot perform global redesign
        major_redesign_status = "denied"
        design_freedom = "constrained"
    elif perms["allow_layout_change"] or "responsive" in user_request.lower():
        max_level = L2
        major_redesign_status = "explicit_user_permission_only"
        design_freedom = "constrained"
    else:
        # Default for existing UI: L1 safe refinement only
        max_level = L1
        major_redesign_status = "explicit_user_permission_only"
        design_freedom = "constrained"

    notes = [
        "Existing UI detected: Hard preservation rules active.",
        "Color palette & brand identity are LOCKED unless explicitly granted by user.",
        "Precedence hierarchy strictly enforced: Existing brand identity and design system defeat inspiration or AI preference.",
    ]

    if is_vague_enhancement(user_request):
        notes.append(
            "Vague enhancement prompt detected ('modernize/làm đẹp'): L3 redesign and palette change remain DENIED."
        )

    if is_local_scope:
        notes.append("Local/component scope active: changes are confined; global architecture remains untouched.")

    return {
        "preservation_required": True,
        "design_freedom": design_freedom,
        "protected_properties": {
            "color_palette": color_palette_state,
            "brand_identity": brand_identity_state,
            "overall_layout_identity": layout_identity_state,
            "navigation_model": navigation_state,
            "information_architecture": architecture_state,
            "component_structure": "controlled",
        },
        "allowed_change_level": {
            "safe_refinement": True,
            "local_structural_change": "allowed" if perms["allow_layout_change"] else "justified_only",
            "major_redesign": major_redesign_status,
            "max_level": max_level,
        },
        "permissions_detail": {
            "palette_editable": perms["allow_palette_change"],
            "branding_editable": perms["allow_branding_change"],
            "layout_editable": perms["allow_layout_change"],
            "navigation_editable": perms["allow_navigation_change"],
            "architecture_editable": perms["allow_architecture_change"],
            "rebuild_allowed": perms["allow_rebuild"],
        },
        "precedence_order": PRECEDENCE_HIERARCHY,
        "scope": scope,
        "notes": notes,
    }


def resolve_precedence(
    explicit_user: str | None = None,
    existing_brand: str | None = None,
    existing_design_system: str | None = None,
    existing_ux: str | None = None,
    repo_constraints: str | None = None,
    domain_best_practice: str | None = None,
    design_inspiration: str | None = None,
    ai_preference: str | None = None,
) -> dict[str, Any]:
    """Resolve conflicting design directions according to the Precedence Hierarchy (1..8)."""
    candidates = [
        (1, "Explicit user instruction", explicit_user),
        (2, "Existing brand identity", existing_brand),
        (3, "Existing design system", existing_design_system),
        (4, "Existing UX / information architecture", existing_ux),
        (5, "Repository/framework constraints", repo_constraints),
        (6, "Domain best practices", domain_best_practice),
        (7, "Design inspiration", design_inspiration),
        (8, "AI preference", ai_preference),
    ]
    for rank, label, val in candidates:
        if val is not None:
            return {"chosen": val, "winner_rank": rank, "winner_label": label}
    return {"chosen": None, "winner_rank": 8, "winner_label": "None"}
