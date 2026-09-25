# Accessibility gate

Check semantic HTML, keyboard operation, visible focus, labels, contrast, text alternatives, appropriate ARIA, touch targets, reduced motion, and error semantics. Use automated tools such as axe when available, but complement them with manual keyboard, focus, and semantic checks.

For rendered UI work, apply the shared [Accessibility Gate](../../execution/accessibility/gate.md). Automated axe findings are evidence, not a full pass; manual checks must be passed or honestly limited/not executed.

Contrast review includes text/background, button/background, badge/background, disabled state, and focus state. Do not communicate essential meaning by color alone. Target roughly 44px touch targets when appropriate for mobile interaction.
