# Text motion

Text motion is justified only for a rare headline moment or a metric that gains meaning from change. Reading must never wait on animation.

| Pattern | Purpose | Good | Bad | Intensity | Perf | A11y | Implementation |
|---|---|---|---|---|---|---|---|
| **line reveal** | Pace a multi-line hero statement | Premium/editorial hero, once | Body copy; every section heading | medium | Wrap lines in spans with overflow clip; transform only | Screen readers must read the full string once (no split per character in the accessibility tree); reduced → static | Split by lines at render, not per frame |
| **word reveal** | Emphasis on a short statement | 3–8 word hero | Long headlines; dense UI | medium | fine for few elements | `aria-label` on container or visually-hidden full text + `aria-hidden` spans | Stagger 30–60ms, total < ~800ms |
| **character reveal** | Signature typographic moment | Portfolio/expressive single word | Anything read by users to act | high | many elements; keep very short | Same as above; high vestibular/cognitive cost | Avoid unless the archetype demands it |
| **mask reveal** | Editorial reveal of headline | Chapter openers | Repeated use | medium | clip-path on a block | reduced → static | `clip-path: inset()` |
| **headline transition** (rotating words) | Show breadth of use cases | Rarely; with pause control if auto-rotating | Hiding the actual value proposition in rotation | medium | trivial | Auto-rotation > 5s needs pause/stop (WCAG 2.2.2); reduced → static first variant | Prefer static list |
| **counter / metric reveal** | Emphasize magnitude when it enters view | Real metrics in proof sections | Fake stats; counting on every revisit | low–medium | rAF limited to few numbers; tabular numerals to prevent jitter | Final value must be in DOM/announced; reduced → final value immediately | IO trigger once; `font-variant-numeric: tabular-nums` |

Rules: never split text in ways that change reading order or break Vietnamese diacritics (split by grapheme cluster, not code unit — `Intl.Segmenter` if splitting characters); first meaningful text is readable within ~1s.
