# Navigation presentation patterns

Destinations and hierarchy are locked by Phase 1 (`NAVIGATION-MAP.md`). These patterns choose presentation only. Visual behavior of nav items follows [navigation grammar](../../visual-language/components/navigation.md).

| Pattern | When | Requirements | Responsive | Motion | Failure |
|---|---|---|---|---|---|
| **minimal header** | Few destinations (≤ 5), minimal/editorial/portfolio | Logo, links, one action | Collapses to menu button with accessible disclosure | minimal | Hiding the only action behind a menu on mobile |
| **product header** | SaaS/developer/marketplace sites | Product links, docs/pricing, sign-in, primary action | Primary action stays visible on mobile when it is the goal | low | Two competing primary buttons |
| **transparent-to-solid** | Header over immersive/cinematic hero | Contrast guaranteed over media at every scroll position | Solid by default on mobile if contrast is uncertain | low (background fade on scroll via IO sentinel, not scroll handler) | Unreadable links over bright media; jump in height |
| **sticky product nav** | Long single-product pages | Product name, section links, one action (buy/start) | Horizontal scroll for section links | low | Stacking two sticky bars that consume mobile viewport |
| **mega menu** | Large product/catalog breadth (locked IA has groups) | Grouped destinations with labels/descriptions | Becomes nested accordion menu | low–medium (popover) | Mega menu for five links; hover-only opening; no keyboard support |
| **section navigation** | Long docs/technical/editorial pages | Anchored sections with stable IDs | Collapsible "On this page" | minimal; active-section highlight via IO | Scroll-jacking smooth-scroll ignoring reduced motion |

Floating pill nav is not a default; use only when the archetype (e.g., creative tool showcase) and content justify it, with the reason recorded.
