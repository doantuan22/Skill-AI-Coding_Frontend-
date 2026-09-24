---
id: E47
name: feedback grammar misuse
category: visual-language
project_state: registration flow uses toasts for field errors and blocking dialogs for routine success
user_request: Fix the confusing feedback behavior.
expected_route: Phase 2 → feedback grammar → state/component realization → accessibility and QA
required_artifacts: [VISUAL-GRAMMAR, COMPONENT-SPEC, STATE-MAP]
forbidden_behavior: [change-validation-business-rules, communicate-state-by-color-alone, replace-all-feedback-with-toasts]
expected_context: [visual-language/components/feedback, forms, accessibility]
success_conditions: [scope-based-feedback-selection, actionable-copy, inline-field-validation, accessible-status-treatment]
failure_conditions: [feedback-grammar-drift, modal-for-routine-success, toast-for-required-correction]
---
