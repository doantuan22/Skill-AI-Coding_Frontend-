---
id: E46
name: button grammar drift
category: visual-language
project_state: existing product has inconsistent radii, CTA gradients, icon placement and primary hierarchy
user_request: Normalize buttons on the checkout pages.
expected_route: Phase 2 → button grammar → component spec → representative implementation → QA
required_artifacts: [VISUAL-GRAMMAR, COMPONENT-SPEC, IMPLEMENTATION-MAP]
forbidden_behavior: [change-checkout-flow, make-every-action-primary, replace-coherent-variants-without-reason]
expected_context: [visual-language/components/buttons, current-design-system, checkout]
success_conditions: [document-variants-and-states, preserve-semantic-actions, fix-drift-at-root, verify-representative-route]
failure_conditions: [button-grammar-drift, primary-everywhere, gradient-cta-by-default]
---
