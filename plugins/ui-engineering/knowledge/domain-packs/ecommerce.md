# E-Commerce Domain Design Pack

**Pack ID**: `domain.ecommerce`  
**Domain**: `ecommerce`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `shop`, `store`, `retail`, `marketplace`  

---

## 1. User Types & Operational Context
- **Primary Users**: Shoppers, casual browsers, repeat customers, mobile shoppers.
- **Key Psychology**: Friction-sensitive, speed-demanding, seeking price transparency, high need for reassurance and validation.

## 2. Domain Subtopics
- `discovery`: Category trees, promotional banners, search suggestions, visual recommendations.
- `listing`: Product grid/list, facets, multi-attribute filtering, sorting, pagination/infinite scroll.
- `product_detail`: Image galleries, pricing/promotions, variant selectors (size/color/quantity), stock indicators, specifications.
- `cart`: Line items, item modification, shipping estimates, coupon redemption, cart drawer vs cart page.
- `checkout`: Multi-step vs one-page checkout, address validation, shipping method selection, payment integration, order summary.
- `order_state`: Order tracking, receipt confirmation, fulfillment timeline.
- `trust`: Payment security badges, customer reviews, clear return policies, delivery guarantees.

## 3. Critical Flows
1. **Browse to PDP**: Category navigation -> faceted search -> product card click -> Product Detail Page.
2. **Variant Selection & Add-to-Cart**: Selecting size/color -> real-time stock feedback -> Add to Cart CTA -> persistent cart drawer feedback.
3. **Cart to Checkout**: Reviewing item quantities/totals -> initiating checkout -> entering shipping/payment details -> order confirmation.

## 4. Information Hierarchy & UX Patterns
- **Product Cards**: Primary product image (consistent aspect ratio) -> brand/title -> clear price (with strikethrough original if discounted) -> stock/rating summary -> primary Add to Cart / View action.
- **Price Transparency**: Always display total cost clearly. Never hide shipping fees, processing charges, or taxes until the final step.
- **Sticky Actions**: On mobile viewports, keep the primary "Add to Cart" or "Buy Now" button anchored at the bottom of the viewport when scrolling past the main product header.

## 5. Required UI States
- `loading`: Skeleton loaders for product cards and checkout payment gateways.
- `empty`: Helpful empty cart with direct link to popular collections; empty search with spelling suggestions and trending categories.
- `out_of_stock`: Clear disabled variant buttons with option for "Notify me when available".
- `validation_error`: Inline form errors on checkout address fields with explicit aria associations.
- `payment_pending`: Unclosable processing overlay with clear progress spinner.
- `confirmation`: Order reference number, delivery address breakdown, and receipt download.

## 6. Trust & Reassurance Patterns
- Prominently position accepted payment logos (Visa, Mastercard, PayPal, Apple Pay).
- Display verified buyer ratings and return policy duration ("30-day free returns") right near the primary checkout or PDP CTA.

## 7. Responsive & Accessibility Priorities
- **Responsive**: Mobile-first bottom drawer for filters (`lg:hidden`), responsive image srcset, sticky purchase bar on small viewports.
- **Accessibility**:
  - Variant pickers must use accessible radio groups (`role="radiogroup"`) or `<select>` with clear keyboard navigation.
  - Announce cart total updates via `aria-live="polite"`.
  - Contrast ratios for discount tags and badges must satisfy WCAG AA (4.5:1).

## 8. Anti-Patterns to Avoid
- **Hidden Fees**: Revealing surprise handling charges only at the payment step.
- **Ambiguous Variant Selection**: Adding items to cart without explicitly verifying that the required size/color is selected.
- **Competing CTAs**: Equal visual weight given to "Add to Wishlist" and "Add to Cart" causing user hesitation.
- **Product Cloning**: No attempt to reproduce proprietary layouts or brand assets of Amazon, Shopee, or Apple.

## 9. Workflow Integration & Precedence
- **Greenfield**: Guides information architecture, product catalog layout, and checkout steps.
- **Existing UI**: Domain pack strictly sits at **Level 6** in the Precedence Hierarchy. It **NEVER** overrides the existing brand identity, locked color palette, or established app navigation. It operates solely to improve domain UX flows and missing state coverage.
