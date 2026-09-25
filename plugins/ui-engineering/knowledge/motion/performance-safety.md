# Motion performance safety

| Rule | Why | Do |
|---|---|---|
| Animate `transform` and `opacity` | Compositor-only; no layout/paint | Replace `top/left/width/height/margin` animation with transforms or grid-rows techniques |
| Avoid layout thrashing | Interleaved read/write forces sync layout | Batch DOM reads then writes; no measurements inside scroll handlers |
| No uncontrolled scroll handlers | Fire at high frequency on main thread | Use `IntersectionObserver`, native scroll-driven animations, or a passive listener + rAF throttle |
| Avoid heavy continuous animation | Drains battery, competes with interaction | Loops only with rationale; pause when off-screen (`IntersectionObserver`) and when tab hidden (`visibilitychange`) |
| Limit blur/filter/backdrop-filter animation | Expensive repaint per frame | Animate opacity of a pre-blurred layer; never animate blur radius on large areas |
| Don't animate large backgrounds without reason | Full-viewport repaints | Keep animated area small; use static gradients/images |
| `will-change` sparingly | Each promoted layer costs memory | Apply just before animating and remove after, or only on the few elements that animate continuously |
| Avoid layout shift from motion | CLS | Reserve space; entrance transforms must not change layout size |
| Video/Lottie/canvas | Large payload and CPU | Lazy-load, poster frames, pause off-screen; only when the content needs it |
| Budget per page | Compounding cost | ≤ 1 continuous animation visible at a time; ≤ 1 scroll-linked region active |

Risk signals → `SCROLL_JANK_RISK`: scroll listeners doing work per event, animated layout properties, many simultaneous transforms on large images, pinned sections with heavy media, parallax on mobile.

Verify in browser QA when capability exists (scroll through the page at desktop and mobile viewports and note dropped-frame symptoms). This milestone does not require Lighthouse or profiling tools; do not install them.
