# Product showcase and interaction patterns

Use only when the interaction fits the content. Each must be keyboard and screen-reader operable and have a static reduced-motion state.

| Pattern | Use when | Don't use when | Requirements | Motion |
|---|---|---|---|---|
| **tabs** | 2–6 parallel views of the same object/topic; users compare by switching | Content is sequential or all needed at once; > 6 tabs | ARIA tabs pattern or links; visible selected state; content not critical to SEO/reading hidden forever | low content crossfade |
| **accordion** | Optional detail, FAQ, specs | Critical info (price, terms, required steps) | Button semantics, `aria-expanded`; multiple open allowed unless reason | low expand |
| **carousel** | Many equivalent items where browsing is the task (gallery, related items) | Hero messaging, key features, testimonials that must be read | Visible controls, swipe, no auto-advance (or pause control), items reachable by keyboard | low–medium slide; reduced → no animation |
| **gallery** | Visual products, travel/property, portfolio | Few images | Consistent aspect ratios, lightbox with focus management, alt text | medium spatial (thumbnail → full) |
| **comparison slider** | Honest before/after of the same frame | Different compositions; accessibility-critical comparisons | Keyboard-operable slider (`role=slider` or range input), labels, equal crop | none beyond drag |
| **product configurator** | Real options affect appearance/price | Options are not visual | State in URL or form; price/summary updates live (`aria-live` polite) | soft state transitions |
| **feature switcher** | One visual area shows different features selected from a list | Features unrelated to one visual | Selection list + visual; mobile stacks as accordion or inline visuals | medium crossfade |
| **interactive demo** | Product is best understood by trying | Demo is slow/heavy or requires sign-up | Lightweight, sensible defaults, reset action, non-interactive fallback | snappy |

Failures → `PATTERN_MISUSE`: carousel for critical messages, tabs hiding content users need simultaneously, auto-rotating content without pause, interactive demos that block the page.
