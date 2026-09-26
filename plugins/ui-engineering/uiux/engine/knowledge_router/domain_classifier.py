"""Domain Classifier: Evidence-backed, multi-signal domain intelligence.

Classifies projects and user requests into canonical domains:
- ecommerce
- beauty_fashion
- saas_ai
- developer_tool
- hospitality_travel
- healthcare
- finance_fintech
- portfolio_agency
- general (fallback)

Prevents over-inference by requiring composite evidence across routes, components, and vocabulary.
"""
from __future__ import annotations

import re
from typing import Any

DOMAINS = (
    "ecommerce",
    "beauty_fashion",
    "saas_ai",
    "developer_tool",
    "hospitality_travel",
    "healthcare",
    "finance_fintech",
    "portfolio_agency",
)

DOMAIN_VOCABULARY: dict[str, list[str]] = {
    "ecommerce": [
        "cart", "checkout", "product", "products", "sku", "inventory", "order", "orders",
        "shipping", "billing", "shop", "store", "catalog", "catalogue", "discount", "coupon",
        "giỏ hàng", "thanh toán", "sản phẩm", "đặt hàng", "mua sắm",
    ],
    "beauty_fashion": [
        "fashion", "beauty", "cosmetics", "skincare", "makeup", "apparel", "clothing",
        "garment", "shade", "swatch", "lookbook", "collection", "outfit", "size guide",
        "thời trang", "mỹ phẩm", "son", "quần áo", "bộ sưu tập",
    ],
    "saas_ai": [
        "saas", "dashboard", "workspace", "subscription", "pricing", "plan", "analytics",
        "ai", "prompt", "llm", "generation", "model", "token", "inference", "agent",
        "bảng điều khiển", "gói dịch vụ", "trí tuệ nhân tạo", "không gian làm việc",
    ],
    "developer_tool": [
        "terminal", "cli", "sdk", "api", "console", "log", "logs", "metrics", "debugger",
        "stack trace", "devops", "kubernetes", "docker", "pipeline", "repository", "git",
        "mã nguồn", "nhật ký", "dòng lệnh", "cấu hình",
    ],
    "hospitality_travel": [
        "hotel", "travel", "booking", "reservation", "flight", "room", "rooms", "stay",
        "destination", "check-in", "check-out", "guest", "guests", "resort", "vacation",
        "khách sạn", "du lịch", "đặt phòng", "chỗ ở", "vé máy bay", "nghỉ dưỡng",
    ],
    "healthcare": [
        "health", "medical", "clinic", "patient", "doctor", "practitioner", "appointment",
        "prescription", "dosage", "diagnosis", "records", "hospital", "telehealth", "vitals",
        "y tế", "sức khỏe", "bệnh nhân", "bác sĩ", "lịch hẹn", "đơn thuốc", "bệnh án",
    ],
    "finance_fintech": [
        "fintech", "finance", "banking", "bank", "account", "transfer", "payment",
        "transaction", "balance", "wallet", "crypto", "investment", "currency", "debit", "credit",
        "tài chính", "ngân hàng", "giao dịch", "số dư", "chuyển tiền", "ví điện tử",
    ],
    "portfolio_agency": [
        "portfolio", "case study", "agency", "studio", "freelance", "showcase", "projects",
        "testimonial", "services", "creative", "exhibition",
        "hồ sơ năng lực", "dự án", "thiết kế sáng tạo",
    ],
}

DOMAIN_ROUTES: dict[str, list[str]] = {
    "ecommerce": ["cart", "checkout", "products", "product", "shop", "orders", "catalog"],
    "beauty_fashion": ["lookbook", "collections", "shades", "apparel", "beauty"],
    "saas_ai": ["dashboard", "workspace", "pricing", "billing", "settings", "analytics", "ai"],
    "developer_tool": ["logs", "terminal", "metrics", "api-keys", "config", "debug"],
    "hospitality_travel": ["rooms", "hotels", "booking", "destinations", "reservations", "stay"],
    "healthcare": ["patients", "appointments", "records", "prescriptions", "vitals", "clinic"],
    "finance_fintech": ["transfers", "transactions", "accounts", "cards", "wallet", "pay"],
    "portfolio_agency": ["projects", "case-studies", "work", "services", "about"],
}

DOMAIN_COMPONENTS: dict[str, list[str]] = {
    "ecommerce": ["ProductCard", "CartDrawer", "CheckoutForm", "PriceTag", "VariantSelector", "QuantityPicker"],
    "beauty_fashion": ["ShadeSwatch", "LookbookGallery", "SizeGuideModal", "ProductLook", "SwatchPicker"],
    "saas_ai": ["MetricCard", "PromptInput", "UsageGauge", "StreamingResponse", "PricingTable", "WorkspaceShell"],
    "developer_tool": ["CodeBlock", "LogViewer", "TerminalEmulator", "DiffViewer", "CopyButton", "JsonTree"],
    "hospitality_travel": ["DateRangePicker", "GuestCounter", "RoomCard", "PropertyGallery", "BookingSummary"],
    "healthcare": ["PatientHeader", "VitalSignsCard", "MedicationList", "AppointmentScheduler", "LabResultRow"],
    "finance_fintech": ["BalanceDisplay", "TransferModal", "TransactionList", "MaskedCard", "CurrencyInput"],
    "portfolio_agency": ["ProjectShowcase", "CaseStudyHero", "TestimonialSlider", "ClientLogoGrid"],
}


def classify_domain(
    user_request: str = "",
    repo_profile: dict[str, Any] | None = None,
    explicit_domain: str | None = None,
    requested_scope: str = "global",
) -> dict[str, Any]:
    """Deterministically classify the project and request into primary and secondary domains.
    
    Precedence:
    1. Explicit user domain declaration.
    2. Composite evidence from routes, components, and vocabulary.
    3. Multi-domain detection if strong secondary evidence exists.
    4. Fallback to 'general'.
    """
    evidence: list[str] = []
    conflicts: list[str] = []

    # 1. Check Explicit User Domain
    if explicit_domain and explicit_domain.strip():
        norm_exp = explicit_domain.strip().lower()
        # Handle aliases
        alias_map = {
            "shop": "ecommerce", "store": "ecommerce", "retail": "ecommerce",
            "fashion": "beauty_fashion", "beauty": "beauty_fashion",
            "saas": "saas_ai", "ai": "saas_ai",
            "devtools": "developer_tool", "cli": "developer_tool",
            "travel": "hospitality_travel", "hotel": "hospitality_travel",
            "medical": "healthcare", "health": "healthcare",
            "fintech": "finance_fintech", "banking": "finance_fintech", "finance": "finance_fintech",
            "portfolio": "portfolio_agency", "agency": "portfolio_agency",
        }
        resolved = alias_map.get(norm_exp, norm_exp)
        if resolved in DOMAINS:
            return {
                "primary_domain": resolved,
                "secondary_domains": [],
                "confidence": 1.0,
                "evidence": [f"User explicitly declared domain: '{explicit_domain}'."],
                "conflicts": [],
                "source": "explicit",
            }
        else:
            conflicts.append(f"Explicit domain '{explicit_domain}' is not in the recognized domain catalog.")

    # 2. Check Monorepo Scope
    active_profile = repo_profile or {}
    if "applications" in active_profile and requested_scope in active_profile["applications"]:
        active_profile = active_profile["applications"][requested_scope].get("repo_profile", active_profile)
        evidence.append(f"Scoping domain detection to sub-application '{requested_scope}'.")

    # 3. Gather Signals
    text_corpus = f"{user_request} ".lower()
    routes_list: list[str] = []
    for r in active_profile.get("routes", []):
        if isinstance(r, dict):
            routes_list.append(str(r.get("path") or r.get("route") or "").lower())
        else:
            routes_list.append(str(r).lower())
    for p in active_profile.get("pages", []):
        if isinstance(p, dict):
            routes_list.append(str(p.get("path") or p.get("name") or "").lower())
        else:
            routes_list.append(str(p).lower())
    routes = [r for r in routes_list if r]
    components = [c.get("name", "") if isinstance(c, dict) else str(c) for c in active_profile.get("components", [])]

    scores: dict[str, float] = {d: 0.0 for d in DOMAINS}
    domain_ev: dict[str, list[str]] = {d: [] for d in DOMAINS}

    # Signal A: User request vocabulary
    for domain, words in DOMAIN_VOCABULARY.items():
        matched_words = [w for w in words if re.search(r'\b' + re.escape(w) + r'\b', text_corpus)]
        if matched_words:
            # Vocabulary match contributes up to 0.40
            pts = min(len(matched_words) * 0.15, 0.45)
            scores[domain] += pts
            domain_ev[domain].append(f"Request vocabulary matched: {', '.join(matched_words[:4])}")

    # Signal B: Routes and pages
    for domain, r_list in DOMAIN_ROUTES.items():
        matched_routes = [r for r in routes if any(target in r for target in r_list)]
        if matched_routes:
            pts = min(len(matched_routes) * 0.25, 0.70)
            scores[domain] += pts
            domain_ev[domain].append(f"Matching routes detected: {', '.join(matched_routes[:3])}")

    # Signal C: Component names
    for domain, c_list in DOMAIN_COMPONENTS.items():
        matched_comps = [c for c in components if c in c_list]
        if matched_comps:
            pts = min(len(matched_comps) * 0.20, 0.40)
            scores[domain] += pts
            domain_ev[domain].append(f"Matching domain components: {', '.join(matched_comps[:3])}")

    # 4. Multi-Signal Safeguard (Prevent Over-inference from single weak route)
    # A domain requires at least 2 distinct signals OR strong combined score (>= 0.40) to be considered
    valid_candidates: list[tuple[str, float]] = []
    for domain, score in scores.items():
        signal_count = len(domain_ev[domain])
        if signal_count >= 2 or (signal_count == 1 and round(score, 2) >= 0.40):
            valid_candidates.append((domain, min(round(score, 2), 0.95)))

    valid_candidates.sort(key=lambda x: x[1], reverse=True)

    if not valid_candidates:
        return {
            "primary_domain": "general",
            "secondary_domains": [],
            "confidence": 0.30,
            "evidence": ["No strong domain-specific evidence detected; using general UI guidance."],
            "conflicts": conflicts,
            "source": "inferred",
        }

    primary_domain, primary_score = valid_candidates[0]
    all_evidence = list(domain_ev[primary_domain])

    # Check for Secondary Domain (e.g. Beauty Ecommerce)
    secondary_domains: list[str] = []
    if len(valid_candidates) > 1:
        sec_domain, sec_score = valid_candidates[1]
        # Only accept secondary if its score is substantial (>= 0.40)
        # e.g., Ecommerce (0.80) + Beauty Fashion (0.60)
        if sec_score >= 0.40:
            secondary_domains.append(sec_domain)
            all_evidence.append(f"Secondary domain '{sec_domain}' detected with confidence {sec_score:.2f}")

    return {
        "primary_domain": primary_domain,
        "secondary_domains": secondary_domains,
        "confidence": round(primary_score, 2),
        "evidence": all_evidence,
        "conflicts": conflicts,
        "source": "inferred",
    }
