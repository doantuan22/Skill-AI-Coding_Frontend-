# Text motion (M4 typography)

Realizations of [text reveal](scroll-motion.md) and metric motion. Text motion is justified only for a rare headline moment or a metric that gains meaning from change. Reading must never wait on animation: first meaningful text is readable within ~1s.

Rules: never split text in ways that change reading order or break Vietnamese diacritics (split by grapheme cluster with `Intl.Segmenter`, not code units). Screen readers must read the full string once: keep the real text on the container (`aria-label` or visually hidden text) and `aria-hidden` the animated spans.

```yaml
id: motion.text-line-reveal
name: Line reveal
kind: motion
category: text
tier: M4
purpose: Pace a multi-line hero statement.
serves: [hierarchy, brand-expression]
trigger: Page load (hero) or viewport entry, once.
behavior: Each line rises from an overflow-clipped mask.
duration: 400-800ms total, 60-100ms line stagger
easing: cubic-bezier(0.16, 1, 0.3, 1)
spring: none
entrance: Top line first.
exit: None.
interruption: Completes.
responsive: Re-split lines after resize (debounced) or animate the block as one on mobile.
reduced_motion: Static.
performance:
  cost: low
  notes: Few elements; split once at render.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: medium
contexts: [marketing, content]
avoid_when: Body copy or every section heading.
examples: Editorial hero headline.
```

```yaml
id: motion.text-word-reveal
name: Word reveal
kind: motion
category: text
tier: M4
purpose: Emphasize a short statement word by word.
serves: [hierarchy, brand-expression]
trigger: Viewport entry once.
behavior: Words fade/rise in sequence.
duration: 30-60ms per word, under 800ms total
easing: ease-out
spring: none
entrance: Reading order.
exit: None.
interruption: Completes instantly on user scroll past.
responsive: Line reveal instead on mobile.
reduced_motion: Static.
performance:
  cost: low
  notes: Suitable for 3-8 words.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap, tech.motion]
intensity: medium
contexts: [marketing]
avoid_when: Long headlines; dense UI.
examples: Three-word product claim.
```

```yaml
id: motion.text-character-reveal
name: Character reveal
kind: motion
category: text
tier: M4
purpose: Signature typographic moment for expressive brands.
serves: [brand-expression]
trigger: Load or viewport entry once.
behavior: Characters animate individually (rise, scramble, weight change).
duration: Under 1000ms total
easing: ease-out or steps for scramble
spring: none
entrance: Reading order.
exit: None.
interruption: Completes.
responsive: Disabled on mobile.
reduced_motion: Static.
performance:
  cost: medium
  notes: Many elements; keep to one short word or phrase.
technology:
  preferred: [tech.css]
  alternatives: [tech.gsap]
intensity: high
contexts: [marketing]
avoid_when: Anything users read to act; non-expressive brands.
examples: Portfolio name assembling on load.
```

```yaml
id: motion.text-rotating-headline
name: Rotating headline
kind: motion
category: text
tier: M4
purpose: Show breadth of use cases in one slot.
serves: [attention]
trigger: Timer.
behavior: One word/phrase cycles through variants.
duration: Each variant visible 2-3s, transition 300ms
easing: ease-in-out
spring: none
entrance: Slide or fade.
exit: Slide or fade.
interruption: Pauses on hover/focus; stop control if over 5s total.
responsive: Static first variant on mobile.
reduced_motion: Static first variant.
performance:
  cost: low
  notes: Trivial.
technology:
  preferred: [tech.css]
  alternatives: [tech.native-js]
intensity: medium
contexts: [marketing]
avoid_when: The actual value proposition would be hidden in rotation.
examples: Built for designers / engineers / teams.
```

```yaml
id: motion.text-counter
name: Counter / metric reveal
kind: motion
category: text
tier: M4
purpose: Emphasize the magnitude of a real metric or value change.
serves: [attention, state-change]
trigger: Metric enters the viewport once, or value changes in an app.
behavior: Number counts or rolls to its value with tabular numerals.
duration: 600-1200ms marketing; 200-400ms app value change
easing: ease-out
spring: none
entrance: From a nearby value, not always zero.
exit: None.
interruption: Jumps to final value.
responsive: Same.
reduced_motion: Final value immediately.
performance:
  cost: low
  notes: rAF limited to a few numbers; font-variant-numeric tabular-nums prevents jitter.
technology:
  preferred: [tech.native-js]
  alternatives: [tech.motion, tech.gsap]
intensity: low
contexts: [marketing, application]
avoid_when: Invented stats; counting on every revisit.
examples: Portfolio balance updating after a trade.
```
