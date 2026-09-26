"""Domain Registry: Machine-readable registry and subtopic query surface for Domain Design Packs.

Exposes domain metadata, critical flows, required states, anti-patterns,
and task-aware subtopic resolution to ensure strict context efficiency.
"""
from __future__ import annotations

import re
from typing import Any

DOMAIN_PACKS: dict[str, dict[str, Any]] = {
    "domain.ecommerce": {
        "id": "domain.ecommerce",
        "domain": "ecommerce",
        "name": "E-Commerce UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["shop", "store", "retail", "marketplace"],
        "subtopics": {
            "discovery": "Category hierarchy, promotional banners, search suggestions, visual recommendations.",
            "listing": "Product grid/list, facets, multi-attribute filtering, sorting, pagination.",
            "product_detail": "Image galleries, pricing/promotions, variant selectors (size/color/quantity), stock indicators.",
            "cart": "Line items, item modification, shipping estimates, coupon redemption, cart drawer.",
            "checkout": "Multi-step vs one-page checkout, address validation, shipping method, payment integration, order summary.",
            "order_state": "Order tracking, receipt confirmation, fulfillment timeline.",
            "trust": "Payment security badges, customer reviews, clear return policies, delivery guarantees.",
        },
        "critical_flows": [
            "Category browse to product detail view",
            "Variant selection and real-time add-to-cart",
            "Cart review to multi-step checkout and confirmation",
        ],
        "required_states": ["loading", "empty", "out_of_stock", "validation_error", "payment_pending", "confirmation"],
        "trust_patterns": ["Accepted payment provider badges", "Verified buyer reviews", "Return policy guarantee next to CTA"],
        "anti_patterns": [
            "Hidden fees revealed only at final checkout step",
            "Ambiguous variant selection adding unselected sizes to cart",
            "Equal visual weight given to secondary and primary purchase CTAs",
            "Direct imitation or cloning of proprietary marketplace assets",
        ],
        "responsive_priorities": ["Mobile-first bottom filter drawer", "Sticky purchase action bar on mobile viewports"],
        "accessibility_priorities": ["Accessible variant radio groups", "aria-live announcement of cart updates", "4.5:1 badge contrast"],
        "recommended_runtime_validation": ["runtime.form_interaction", "runtime.responsive_viewport"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/ecommerce.md",
    },
    "domain.beauty_fashion": {
        "id": "domain.beauty_fashion",
        "domain": "beauty_fashion",
        "name": "Beauty & Fashion UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["fashion", "beauty", "apparel", "cosmetics", "luxury"],
        "subtopics": {
            "editorial_commerce": "Lookbooks, lifestyle hero showcases, curated outfits, seasonal collections.",
            "visual_browsing": "Large-format product tiles, hover image reveals, minimal chrome on photography.",
            "variant_selection": "Cosmetic shade swatches, interactive size guides, fit recommenders.",
            "product_storytelling": "Model sizing details, fabric/ingredient breakdowns, texture close-ups.",
            "recommendations": "Complete the look and curated accessory cross-sell carousels.",
        },
        "critical_flows": [
            "Lookbook curated collection discovery",
            "Shade swatch switching with live preview update",
            "Size guide comparison and addition to bag",
        ],
        "required_states": ["loading", "empty", "sold_out", "shade_preview"],
        "trust_patterns": ["Ingredient transparency", "Material & fabric origin notes", "Ethical production badges"],
        "anti_patterns": [
            "Unlabeled color circles without text or accessible tooltips",
            "Hiding sizing charts 5 scrolls below the fold",
            "Decorative clutter or neon sale tickers cheapening brand luxury",
        ],
        "responsive_priorities": ["Swipeable touch galleries with pinch-to-zoom", "Clean mobile swatch grids"],
        "accessibility_priorities": ["Color swatch aria-labels with stock status", "High contrast active borders on swatches"],
        "recommended_runtime_validation": ["runtime.responsive_viewport", "runtime.smoke_test"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/beauty_fashion.md",
    },
    "domain.saas_ai": {
        "id": "domain.saas_ai",
        "domain": "saas_ai",
        "name": "SaaS & AI Product UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["saas", "ai", "b2b", "cloud", "platform", "workspace"],
        "subtopics": {
            "public_surfaces": "Value proposition hero, feature breakdowns, transparent pricing tiers, documentation.",
            "dashboard": "Key metric cards, recent activity streams, quick action shortcuts, personalized feeds.",
            "workspace": "Multi-pane layouts, persistent sidebars, collaborative canvases, resource tables.",
            "onboarding": "Multi-step progress wizards, interactive product tours, sample data presets.",
            "settings_billing": "Team permissions, API keys, usage meter gauges, subscription tiers.",
            "ai_interaction": "Prompt input bars, streaming token responses, response citations/sources, feedback controls.",
        },
        "critical_flows": [
            "Onboarding to first meaningful value delivery",
            "Dashboard metric triage and table drill-down",
            "AI prompt submission, streaming generation, and citation inspection",
        ],
        "required_states": ["loading", "empty", "error", "plan_limit", "streaming"],
        "trust_patterns": ["Transparent quota usage meters", "Clear AI citation sources", "Auditable change history"],
        "anti_patterns": [
            "Applying dark neon gradients indiscriminately to enterprise tools",
            "Cramming 25 unrelated widgets onto home screen without visual hierarchy",
            "Concealing AI hallucination risks without source review tools",
        ],
        "responsive_priorities": ["Collapsible multi-pane navigation into drawers", "Horizontally scrollable data tables"],
        "accessibility_priorities": ["Keyboard shortcuts for command palettes (Cmd+K)", "aria-live for streaming generation"],
        "recommended_runtime_validation": ["runtime.smoke_test", "runtime.responsive_viewport"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/saas_ai.md",
    },
    "domain.developer_tool": {
        "id": "domain.developer_tool",
        "domain": "developer_tool",
        "name": "Developer Tool UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["devtools", "cli", "sdk", "infra", "api", "monitoring"],
        "subtopics": {
            "dense_information": "Log viewers, metrics dashboards, server health grids, execution graphs.",
            "code_terminal": "Syntax-highlighted code blocks, CLI terminal emulators, copy widgets, diff viewers.",
            "diagnostics_logs": "Real-time streaming log tables, log level filtering (INFO, WARN, ERROR), stack traces.",
            "configuration": "Environment variable editors, YAML/JSON schema validators, API key management.",
            "docs_integration": "Side-by-side interactive API explorers, payload request/response sandboxes.",
        },
        "critical_flows": [
            "One-time secure API key generation and copying",
            "Log filtering by severity and expanding stack trace line",
            "Configuration editing, diff verification, and deployment trigger",
        ],
        "required_states": ["streaming", "empty", "error_diagnostic", "masked_secret"],
        "trust_patterns": ["Explicit copy feedback confirmation", "Masked secrets with reveal toggles", "Diff preview before mutation"],
        "anti_patterns": [
            "Slow decorative animations on log expansion",
            "Truncating stack traces without full copy action",
            "Unclear copy buttons leaving user uncertain if clipboard updated",
        ],
        "responsive_priorities": ["Visible horizontal scrollbars on code blocks", "Touch-friendly copy buttons on mobile"],
        "accessibility_priorities": ["Syntax theme contrast >= 4.5:1", "Keyboard-accessible code blocks and terminal output"],
        "recommended_runtime_validation": ["runtime.smoke_test"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/developer_tool.md",
    },
    "domain.hospitality_travel": {
        "id": "domain.hospitality_travel",
        "domain": "hospitality_travel",
        "name": "Hospitality & Travel UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["travel", "hotel", "booking", "hospitality", "resort", "tourism", "vacation"],
        "subtopics": {
            "search": "Sticky search bar with destination, check-in/out dates, and guest counters.",
            "date_guest": "Dual-month interactive calendar date range picker, room occupancy counters.",
            "property_detail": "Categorized photo galleries, amenities list, neighborhood map, guest reviews.",
            "room_selection": "Room cards, bed types, cancellation policy badges, nightly vs total pricing.",
            "booking": "Guest details, arrival time estimates, payment method, itemized stay summary.",
            "confirmation": "Printable booking voucher, check-in instructions, trip cancellation controls.",
        },
        "critical_flows": [
            "Destination and date availability search",
            "Room comparison and rate tier selection (refundable vs non-refundable)",
            "Reservation review with itemized stay breakdown to confirmation",
        ],
        "required_states": ["loading", "unavailable", "booking_summary", "confirmed"],
        "trust_patterns": ["Itemized nightly and total price breakdown", "Prominent cancellation terms", "Verified guest reviews"],
        "anti_patterns": [
            "Concealing resort fees or cleaning charges until final payment step",
            "Ambiguous date context displaying days without month or night count",
            "Fabricating fake urgency countdown timers",
            "Direct imitation of Airbnb or Booking.com proprietary layouts",
        ],
        "responsive_priorities": ["Full-screen mobile search modal with touch-friendly date selection", "Sticky booking CTA"],
        "accessibility_priorities": ["Keyboard navigation across calendar dates", "Descriptive aria-labels on guest counters"],
        "recommended_runtime_validation": ["runtime.form_interaction", "runtime.responsive_viewport"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/hospitality_travel.md",
    },
    "domain.healthcare": {
        "id": "domain.healthcare",
        "domain": "healthcare",
        "name": "Healthcare Domain Design Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["health", "medical", "clinic", "patient", "telehealth", "doctor", "hospital"],
        "subtopics": {
            "patient_practitioner": "Practitioner profiles, specialties, hospital affiliations, patient records.",
            "appointments": "Real-time slot booking, consultation mode (in-person vs video), reminders.",
            "medical_records": "Lab results, prescription lists, immunization records, clinical history.",
            "structured_data": "Vital signs cards, reference ranges, blood pressure/glucose tracking.",
            "status_actions": "Prescription refill requests, emergency contacts, preparation checklists.",
        },
        "critical_flows": [
            "Practitioner condition search to appointment slot confirmation",
            "Lab result inspection against normal reference ranges",
            "Prescription refill request with pharmacy selection",
        ],
        "required_states": ["loading", "empty", "abnormal_flag", "emergency_notice"],
        "trust_patterns": ["Doctor credentials and hospital affiliations", "Standard reference ranges for metrics", "Prominent emergency hotline"],
        "anti_patterns": [
            "Using color alone (green/red) to indicate normal/abnormal medical status",
            "Displaying dosages or metrics without explicit measurement units",
            "Concealing emergency contact notices behind navigation menus",
        ],
        "responsive_priorities": ["Clear stacked forms on mobile", "Large touch targets (>= 48px) for vulnerable patients"],
        "accessibility_priorities": ["Strict WCAG AA/AAA contrast", "Minimum 16px body font size", "Unambiguous form field labels"],
        "recommended_runtime_validation": ["runtime.accessibility_audit", "runtime.form_interaction"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/healthcare.md",
    },
    "domain.finance_fintech": {
        "id": "domain.finance_fintech",
        "domain": "finance_fintech",
        "name": "Finance & Fintech UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["fintech", "finance", "banking", "crypto", "payments", "investment", "wallet"],
        "subtopics": {
            "account_overview": "Total balance cards, multi-currency accounts, quick transfer buttons.",
            "transaction_history": "Date-grouped transaction feeds, category icons, statement exports.",
            "transfer_payment": "Recipient selector, amount input, real-time fee calculation, memo field.",
            "confirmation_audit": "Two-step review modal, itemized transfer details, irreversible action warnings.",
            "risk_security": "Session timeout alerts, 2FA screens, card freeze/unfreeze toggles.",
        },
        "critical_flows": [
            "Recipient selection and fund transfer with two-step review",
            "Transaction feed inspection and statement download",
            "Debit/credit card limit adjustment and temporary freeze toggle",
        ],
        "required_states": ["loading", "masked", "destructive_confirm", "transaction_status"],
        "trust_patterns": ["Two-step confirmation modal with exact amount on button", "Explicit fee transparency before execution", "Masked balance toggles"],
        "anti_patterns": [
            "Generic confirmation button saying 'Submit' instead of 'Transfer $150.00'",
            "Concealing transfer or foreign exchange fees",
            "Using low-contrast or gradient text on monetary amounts",
        ],
        "responsive_priorities": ["Sticky transfer review CTA on mobile", "Responsive numerical PIN entry pad"],
        "accessibility_priorities": ["Tabular monospaced figures (tabular-nums)", "Descriptive currency announcements for screen readers"],
        "recommended_runtime_validation": ["runtime.form_interaction", "runtime.accessibility_audit"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/finance_fintech.md",
    },
    "domain.portfolio_agency": {
        "id": "domain.portfolio_agency",
        "domain": "portfolio_agency",
        "name": "Portfolio & Agency UI Engineering Pack",
        "version": "1.0.0",
        "status": "stable",
        "aliases": ["portfolio", "agency", "studio", "creative", "freelance", "showcase"],
        "subtopics": {
            "narrative_structure": "Hero statement, positioning tagline, studio about section, philosophy.",
            "project_showcase": "Featured project grid/cards, hover reveals, client tags, discipline badges.",
            "case_study": "Challenge, solution, architecture diagrams, before/after comparisons, measurable KPIs.",
            "services_outcomes": "Service offerings, engagement models, client logos, testimonials.",
            "contact_conversion": "Project inquiry form, budget tier selectors, consultation booking links.",
        },
        "critical_flows": [
            "Showcase card browse to in-depth case study and metric review",
            "Service exploration to project inquiry submission",
        ],
        "required_states": ["loading", "empty", "interactive_preview", "inquiry_success"],
        "trust_patterns": ["Client logo wall", "Measurable project KPI metrics", "Verified client testimonials"],
        "anti_patterns": [
            "Scrolljacking that hijacks standard wheel scrolling or breaks keyboard navigation",
            "Uncompressed massive media files creating sluggish rendering",
            "Vague project descriptions without business problem or measurable outcome",
        ],
        "responsive_priorities": ["Single-column case study reflow on mobile", "Responsive optimized image srcset"],
        "accessibility_priorities": ["Descriptive alt text on project imagery", "Accessible carousel controls with pause"],
        "recommended_runtime_validation": ["runtime.smoke_test", "runtime.responsive_viewport"],
        "weight": "medium",
        "priority": "high",
        "source": "knowledge/domain-packs/portfolio_agency.md",
    },
}


def get_domain_pack(domain_id_or_name: str) -> dict[str, Any] | None:
    """Retrieve domain pack metadata by full ID (domain.ecommerce) or short name (ecommerce)."""
    clean = domain_id_or_name.strip().lower()
    if clean in DOMAIN_PACKS:
        return dict(DOMAIN_PACKS[clean])
    pack_id = f"domain.{clean}"
    if pack_id in DOMAIN_PACKS:
        return dict(DOMAIN_PACKS[pack_id])

    # Check aliases
    for pack in DOMAIN_PACKS.values():
        if clean in pack.get("aliases", []):
            return dict(pack)
    return None


def list_domain_packs() -> list[dict[str, Any]]:
    """Return a list of all 8 domain pack metadata objects."""
    return [dict(p) for p in DOMAIN_PACKS.values()]


def resolve_domain_pack(domain_name: str, context: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Extension resolver interface: resolves domain pack or returns None cleanly."""
    return get_domain_pack(domain_name)


def query_domain_subtopics(domain_name: str, user_request: str = "", task_intent: str = "") -> list[str]:
    """Deterministically select only the relevant subtopics of a domain pack based on task intent and request text.
    
    Prevents context bloat: a button alignment task on ecommerce does NOT load checkout, cart, or discovery!
    A checkout task only loads checkout, cart, and trust.
    """
    pack = get_domain_pack(domain_name)
    if not pack:
        return []

    # Handle argument order flexibility
    known_intents = {
        "create_ui", "improve_ui", "redesign", "full_redesign", "page_redesign",
        "component_refactor", "visual_polish", "consistency_fix", "responsive_fix",
        "accessibility_fix", "form_ux", "navigation_ux", "motion", "audit_only",
        "general_ui", "runtime_validation", "design_system_work",
    }
    if user_request in known_intents and task_intent not in known_intents:
        task_intent, user_request = user_request, task_intent

    subtopics = pack.get("subtopics", {})
    all_subtopic_keys = list(subtopics.keys())
    text_lower = (user_request or "").lower()

    # If task is generic / create_ui / page_redesign and mentions whole page:
    if task_intent in ("page_redesign", "full_redesign", "create_ui") and any(w in text_lower for w in ("toàn bộ", "full", "all", "entire", "landing", "home")):
        return all_subtopic_keys[:3]  # Return primary top 3 subtopics to respect context budget

    # Match specific subtopics by keywords in request or task intent
    selected: list[str] = []
    
    # E-Commerce subtopic matching
    if domain_name == "ecommerce":
        if any(w in text_lower for w in ("order_state", "tracking", "fulfillment", "order status")):
            selected.extend(["order_state", "trust"])
        elif any(w in text_lower for w in ("checkout", "thanh toán", "pay", "payment", "order")):
            selected.extend(["checkout", "cart", "trust"])
        elif any(w in text_lower for w in ("cart", "giỏ hàng", "bag")):
            selected.extend(["cart", "trust"])
        elif any(w in text_lower for w in ("filter", "sort", "lọc", "sắp xếp", "listing", "danh sách")):
            selected.extend(["listing", "discovery"])
        elif any(w in text_lower for w in ("detail", "chi tiết", "pdp", "variant", "size", "color")):
            selected.extend(["product_detail", "trust"])

    # Hospitality subtopic matching
    elif domain_name == "hospitality_travel":
        if any(w in text_lower for w in ("room", "phòng", "select", "rate", "bed")):
            selected.extend(["room_selection", "booking"])
        elif any(w in text_lower for w in ("date", "calendar", "guest", "ngày", "khách")):
            selected.extend(["date_guest", "search"])
        elif any(w in text_lower for w in ("book", "booking", "đặt", "voucher", "confirm")):
            selected.extend(["booking", "confirmation"])

    # SaaS subtopic matching
    elif domain_name == "saas_ai":
        if any(w in text_lower for w in ("ai", "prompt", "stream", "generate", "llm")):
            selected.extend(["ai_interaction", "workspace"])
        elif any(w in text_lower for w in ("price", "pricing", "plan", "bảng giá", "gói")):
            selected.extend(["public_surfaces", "settings_billing"])
        elif any(w in text_lower for w in ("dashboard", "metric", "chart", "bảng điều khiển")):
            selected.extend(["dashboard", "workspace"])

    # Developer Tool subtopic matching
    elif domain_name == "developer_tool":
        if any(w in text_lower for w in ("code", "syntax", "terminal", "copy")):
            selected.extend(["code_terminal", "dense_information"])
        elif any(w in text_lower for w in ("log", "logs", "error", "stack trace", "nhật ký")):
            selected.extend(["diagnostics_logs", "dense_information"])

    # Ensure any explicitly named subtopic key is included
    for st_key in all_subtopic_keys:
        if st_key in text_lower and st_key not in selected:
            selected.append(st_key)

    # Generic subtopic scanning based on subtopic names if still empty
    if not selected:
        for st_key in all_subtopic_keys:
            if any(word in text_lower for word in st_key.split("_") if len(word) > 2):
                selected.append(st_key)

    # If still empty (e.g. minor local fix like "button alignment"), return minimal relevant subtopic or empty list
    # so we do not dump unrelated flows into context!
    return list(dict.fromkeys(selected))
