# Missing reduced-motion fixture

Locked product page with purposeful motion: modal scale-in (250ms), drawer slide (300ms), one sticky storytelling section with image scale on scroll, section fade-up via IntersectionObserver, and a hero headline word reveal. Durations are tokenized and the budget is reasonable, but there is **no** `prefers-reduced-motion` handling, and `.reveal` elements start at `opacity: 0` in plain CSS (content invisible without JS).
