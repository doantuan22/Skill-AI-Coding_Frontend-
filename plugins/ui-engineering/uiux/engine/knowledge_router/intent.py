"""Task Intent Classifier: Deterministic classification of user requests into canonical UI engineering intents.

Supports 15 canonical intent categories used for fine-grained knowledge routing, with compound intent support.
"""
from __future__ import annotations

import re
from typing import Any

# Canonical Intents
CREATE_UI = "create_ui"
IMPROVE_UI = "improve_ui"
RESPONSIVE_FIX = "responsive_fix"
ACCESSIBILITY_FIX = "accessibility_fix"
COMPONENT_REFACTOR = "component_refactor"
PAGE_REDESIGN = "page_redesign"
FULL_REDESIGN = "full_redesign"
DESIGN_SYSTEM_WORK = "design_system_work"
CONSISTENCY_FIX = "consistency_fix"
FORM_UX = "form_ux"
NAVIGATION_UX = "navigation_ux"
MOTION = "motion"
VISUAL_POLISH = "visual_polish"
RUNTIME_VALIDATION = "runtime_validation"
AUDIT_ONLY = "audit_only"
GENERAL_UI = "general_ui"

CANONICAL_INTENTS = {
    CREATE_UI, IMPROVE_UI, RESPONSIVE_FIX, ACCESSIBILITY_FIX, COMPONENT_REFACTOR,
    PAGE_REDESIGN, FULL_REDESIGN, DESIGN_SYSTEM_WORK, CONSISTENCY_FIX, FORM_UX,
    NAVIGATION_UX, MOTION, VISUAL_POLISH, RUNTIME_VALIDATION, AUDIT_ONLY, GENERAL_UI,
}

INTENT_PATTERNS = [
    # Full Redesign / Rebuild
    (FULL_REDESIGN, re.compile(r"\b(?:rebuild|toàn\s+bộ|from\s+scratch|từ\s+đầu|full\s+redesign|overhaul\s+all)\b", re.I)),
    # Page Redesign
    (PAGE_REDESIGN, re.compile(r"\b(?:page\s+redesign|redesign\s+page|thiết\s+kế\s+lại\s+trang|redesign\s+dashboard|redesign\s+landing)\b", re.I)),
    # Navigation UX
    (NAVIGATION_UX, re.compile(r"\b(?:navbar|sidebar|navigation|menu|drawer|breadcrumb|header\s+nav|điều\s+hướng)\b", re.I)),
    # Form UX
    (FORM_UX, re.compile(r"\b(?:form|input|validation|submit|login\s+form|checkout\s+form|đăng\s+nhập|biểu\s+mẫu)\b", re.I)),
    # Accessibility Fix
    (ACCESSIBILITY_FIX, re.compile(r"\b(?:a11y|accessibility|contrast|trợ\s+năng|screen\s+reader|aria|keyboard\s+nav|wcag)\b", re.I)),
    # Responsive Fix
    (RESPONSIVE_FIX, re.compile(r"\b(?:responsive|mobile|tablet|viewport|co\s+giãn|tràn\s+màn\s+hình|break\s+on\s+mobile|overflow)\b", re.I)),
    # Component Refactor
    (COMPONENT_REFACTOR, re.compile(r"\b(?:refactor\s+component|sửa\s+button|button\s+component|card\s+component|tách\s+component)\b", re.I)),
    # Consistency Fix
    (CONSISTENCY_FIX, re.compile(r"\b(?:consistency|đồng\s+bộ|inconsistent|không\s+đồng\s+nhất|duplicate\s+styles|lệch\s+chuẩn)\b", re.I)),
    # Design System Work
    (DESIGN_SYSTEM_WORK, re.compile(r"\b(?:design\s+system|tokens|color\s+palette|typography\s+scale|spacing\s+scale|theme)\b", re.I)),
    # Motion (covers all required keywords: animate, animated, animation, animations, transition, transitions, motion, stagger, reveal, scroll reveal, entrance, exit, page transition, layout animation, micro-interaction)
    (MOTION, re.compile(r"\b(?:animate|animated|animation|animations|transition|transitions|motion|stagger|reveal|scroll\s+reveal|entrance|exit|page\s+transition|layout\s+animation|micro-interaction|keyframes|hiệu\s+ứng)\b", re.I)),
    # Visual Polish
    (VISUAL_POLISH, re.compile(r"\b(?:polish|modernize|làm\s+đẹp|clean\s+up|tinh\s+chỉnh|làm\s+mới|refresh)\b", re.I)),
    # Runtime Validation
    (RUNTIME_VALIDATION, re.compile(r"\b(?:validate|kiểm\s+tra\s+runtime|smoke\s+test|run\s+evals|test\s+render)\b", re.I)),
    # Audit Only
    (AUDIT_ONLY, re.compile(r"\b(?:audit|đánh\s+giá|review|kiểm\s+tra\s+toàn\s+bộ|inspect\s+ui)\b", re.I)),
    # Create UI
    (CREATE_UI, re.compile(r"\b(?:tạo|create|xây|build|implement|thêm|add\s+new|new\s+page|new\s+component)\b", re.I)),
    # Improve UI
    (IMPROVE_UI, re.compile(r"\b(?:improve|cải\s+thiện|nâng\s+cấp|enhance|update)\b", re.I)),
]


def classify_task_intents(task_text: str, user_intent: str | None = None) -> dict[str, Any]:
    """Classify user request into primary and secondary canonical intents.

    Returns:
        dict with keys:
            - primary_intent: canonical intent string
            - secondary_intents: list of complementary intent strings (max 3)
            - all_intents: list containing primary + secondary intents
            - compound: bool indicating if secondary intents were detected
    """
    text = (task_text or "").strip()
    matched_intents: list[str] = []

    if text:
        for intent, pattern in INTENT_PATTERNS:
            if pattern.search(text) and intent not in matched_intents:
                matched_intents.append(intent)

    # 1. Resolve Primary Intent
    explicit_primary = None
    if user_intent and user_intent.strip():
        canonical = user_intent.strip().lower()
        if canonical in CANONICAL_INTENTS:
            explicit_primary = canonical

    if explicit_primary:
        primary_intent = explicit_primary
    elif matched_intents:
        primary_intent = matched_intents[0]
    else:
        primary_intent = GENERAL_UI

    # 2. Resolve Secondary Intents (deterministic, capped at 3, no uncontrolled explosion)
    secondary_intents = [
        intent for intent in matched_intents
        if intent != primary_intent
    ][:3]

    all_intents = [primary_intent] + [i for i in secondary_intents if i != primary_intent]

    return {
        "primary_intent": primary_intent,
        "secondary_intents": secondary_intents,
        "all_intents": all_intents,
        "compound": len(secondary_intents) > 0,
    }


def classify_task_intent(task_text: str, user_intent: str | None = None) -> str:
    """Classify user request into a canonical task intent (backward-compatible single return)."""
    return classify_task_intents(task_text, user_intent)["primary_intent"]
