# Beauty & Fashion Domain Design Pack

**Pack ID**: `domain.beauty_fashion`  
**Domain**: `beauty_fashion`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `fashion`, `beauty`, `apparel`, `cosmetics`, `luxury`  

---

## 1. User Types & Operational Context
- **Primary Users**: Visual-first shoppers, trend seekers, lifestyle consumers, repeat brand advocates.
- **Key Psychology**: Imagery-driven, aspirational, highly sensitive to visual fidelity, product color accuracy, fit, and texture details.

## 2. Domain Subtopics
- `editorial_commerce`: Lookbooks, lifestyle hero showcases, curated outfits, seasonal collections.
- `visual_browsing`: Large-format product tiles, hover-to-secondary image reveals, minimal chrome on product imagery.
- `variant_selection`: Swatch pickers for cosmetics/shades, interactive size guides, fit recommenders.
- `product_storytelling`: Model sizing details, fabric/ingredient breakdowns, texture close-ups, application tutorials.
- `recommendations`: "Complete the Look", "Pair with", "You May Also Like" cross-sell carousels.

## 3. Critical Flows
1. **Curated Collection Discovery**: Navigating lookbook/collection -> discovering styled items -> expanding outfit details.
2. **Shade & Sizing Exploration**: Browsing shade swatches with live preview on model imagery -> opening size/fit modal -> confirming selection.
3. **Bag Addition with Cross-Sell**: Adding apparel item -> offering accessory recommendation without interrupting the flow.

## 4. Information Hierarchy & UX Patterns
- **Visual Restraint**: High-end aesthetic with spacious margins and generous whitespace. Decorative elements must never distract from garment or shade photography.
- **Color/Shade Swatches**: Visual color dots or shade swatches with accessible labels (e.g. "Warm Beige 02"), active selection borders, and disabled styling for out-of-stock shades.
- **Fit & Sizing Guidance**: Prominent "Size Guide" or "Find My Fit" link directly adjacent to the size selector.

## 5. Required UI States
- `loading`: Aspect-ratio-preserving skeleton placeholders preventing content shifts as high-res imagery streams in.
- `empty`: Editorial empty state linking to trending collections or new arrivals.
- `sold_out`: Subtle strikethrough or badge on unavailable sizes, offering back-in-stock notification.
- `shade_preview`: Instant dynamic update of the main product image when a shade swatch is tapped.

## 6. Responsive & Accessibility Priorities
- **Responsive**: Full-bleed swipeable product image galleries on mobile with pinch-to-zoom support.
- **Accessibility**:
  - Color swatches must have high-contrast active indicators and descriptive `aria-label` (e.g., `aria-label="Color: Burgundy, in stock"`).
  - Size selectors must be fully operable via keyboard arrows (`role="radiogroup"`).
  - Typography must remain readable over lifestyle imagery (enforce scrim/overlay if text is layered over photos).

## 7. Anti-Patterns to Avoid
- **Unlabeled Color Swatches**: Tiny color circles without text tooltips or accessible names.
- **Hidden Sizing Charts**: Burying measurements in accordion tabs 5 scrolls below the fold.
- **Decorative Clutter**: Excessive gold borders, flashing sale tickers, or heavy visual noise that cheapens brand prestige.

## 8. Workflow Integration & Precedence
- **Greenfield**: Informs editorial typography, large-scale media layout, and clean minimalist aesthetic.
- **Existing UI**: Subordinate to existing brand colors and design systems. Never recolor an existing luxury brand to arbitrary seasonal shades.
