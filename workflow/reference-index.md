# Reference index

```yaml
references:
  phase_1_forms:
    file: phase-1/references/forms.md
    phase: 1
    triggers: [form, registration, input, validation]
    excludes: [dashboard-only, audit-without-form]
  phase_1_tables:
    file: phase-1/references/tables.md
    phase: 1
    triggers: [data-table, admin-list, sorting, bulk-action]
    excludes: [single-form, marketing-page]
  phase_1_dashboard:
    file: phase-1/references/dashboard.md
    phase: 1
    triggers: [dashboard, monitoring, status-overview]
    excludes: [single-registration, checkout-only]
  phase_1_navigation:
    file: phase-1/references/navigation.md
    phase: 1
    triggers: [multi-page, role-navigation, return-path]
    excludes: [isolated-static-page]
  phase_1_checkout:
    file: phase-1/references/checkout.md
    phase: 1
    triggers: [booking, payment, purchase, confirmation]
    excludes: [dashboard, registration-only]
  phase_2_system:
    file: phase-2/03-design-system/workflow.md
    phase: 2
    triggers: [new-build, visual-redesign, token-inconsistency]
    excludes: [targeted-polish-with-stable-system]
  phase_2_forms:
    file: phase-2/references/forms.md
    phase: 2
    triggers: [form, registration, input-state]
    excludes: [table-only, dashboard-only]
  phase_2_tables:
    file: phase-2/references/tables.md
    phase: 2
    triggers: [data-table, responsive-table, row-action]
    excludes: [single-form, marketing-page]
  phase_2_dashboard:
    file: phase-2/references/dashboard.md
    phase: 2
    triggers: [dashboard, operational-overview, monitoring]
    excludes: [registration-only, checkout-only]
  phase_2_accessibility:
    file: phase-2/08-final-quality-gate/accessibility.md
    phase: 2
    triggers: [interactive-control, final-quality, accessibility-issue]
    excludes: []
  phase_2_visual_language:
    file: phase-2/visual-language/visual-grammar.md
    phase: 2
    triggers: [rendered-ui, visual-redesign, visual-consistency, component-personality]
    excludes: [structure-only, api-only]
  phase_2_button_grammar:
    file: phase-2/visual-language/components/buttons.md
    phase: 2
    triggers: [button, cta, action-hierarchy, icon-button]
    excludes: [text-only, table-only]
  phase_2_feedback_grammar:
    file: phase-2/visual-language/components/feedback.md
    phase: 2
    triggers: [toast, notification, alert, banner, validation, empty-state, error-state]
    excludes: [static-content-only]
  phase_2_icon_grammar:
    file: phase-2/visual-language/components/iconography.md
    phase: 2
    triggers: [icon, icon-button, status-symbol, navigation-icon]
    excludes: [text-only]
  phase_2_craft_review:
    file: phase-2/visual-language/craft-review.md
    phase: 2
    triggers: [generic-ui, ai-slop, visual-polish, craft-review, rendered-redesign]
    excludes: [structure-only, backend-only]
  phase_2_full_visual_redesign:
    file: phase-2/visual-language/adversarial-review.md
    phase: 2
    triggers: [full-redesign, visual-system-replacement, ai-tell-density-high]
    excludes: [targeted-single-component]
  phase_2_design_inspiration:
    file: phase-2/design-inspiration/workflow.md
    phase: 2
    triggers: [landing-page, marketing, product-showcase, launch, make-it-premium, visual-redesign, looks-generic, marketplace-home, editorial]
    excludes: [dashboard-only, small-form, single-component-polish]
  phase_2_reference_extraction:
    file: phase-2/design-inspiration/reference-extraction.md
    phase: 2
    triggers: [screenshot, reference-url, reference-site-name, like-brand-x]
    excludes: [no-reference]
  phase_2_anti_copying:
    file: phase-2/design-inspiration/anti-copying.md
    phase: 2
    triggers: [any-reference, clone-request]
    excludes: [no-reference]
  phase_2_typography_intelligence:
    file: phase-2/typography/README.md
    phase: 2
    triggers: [font, typography, type-hierarchy, readability, new-build, make-it-premium, vietnamese-content]
    excludes: [motion-only, structure-only]
  phase_2_motion_engine:
    file: phase-2/motion/README.md
    phase: 2
    triggers: [animation, motion, transition, interaction, scroll-effect, reduced-motion]
    excludes: [static-content-only, structure-only]
  phase_2_scroll_motion:
    file: phase-2/motion/scroll-motion.md
    phase: 2
    triggers: [scroll-storytelling, parallax, sticky-section, landing-page-motion, scroll-effect]
    excludes: [dashboard, form, app-screen]
  phase_2_web_patterns:
    file: phase-2/web-patterns/README.md
    phase: 2
    triggers: [landing-page, marketing, product-showcase, editorial, marketplace-home, generic-template-composition]
    excludes: [dashboard-only, small-form, single-component]
  phase_2_pattern_selection:
    file: phase-2/design-inspiration/pattern-selection.md
    phase: 2
    triggers: [landing-page, marketing, product-showcase, section-composition, hero, storytelling, generic-template-composition]
    excludes: [dashboard-only, small-form]
  phase_2_capability_resolver:
    file: phase-2/capability-resolver/README.md
    phase: 2
    triggers: [new-build, visual-redesign, landing-page, product-site, make-it-premium, looks-generic, benchmark]
    excludes: [small-form, single-component-polish, audit-only]
  phase_2_design_knowledge:
    file: phase-2/knowledge/retrieval.md
    phase: 2
    triggers: [capability-plan-retrieval, style-selection, screen-pattern, effect, interaction-pattern]
    excludes: [structure-only]
  phase_2_style_catalog:
    file: phase-2/knowledge/styles/README.md
    phase: 2
    triggers: [style-selection, visual-language-choice, homogenized-design]
    excludes: [small-form, targeted-polish-with-stable-system]
  phase_2_screen_library:
    file: phase-2/knowledge/screens/README.md
    phase: 2
    triggers: [dashboard, settings, onboarding, authentication, ai-chat, ai-copilot, kanban, calendar, editor, file-browser]
    excludes: [marketing-only]
  phase_2_interaction_library:
    file: phase-2/knowledge/interactions/README.md
    phase: 2
    triggers: [drag, reorder, inline-edit, command-palette, gesture, undo, optimistic-update, keyboard-navigation]
    excludes: [static-content-only]
  phase_2_effect_library:
    file: phase-2/knowledge/effects/README.md
    phase: 2
    triggers: [glass, glow, gradient, noise, blur, shader, lighting, visual-effect]
    excludes: [dashboard-only, small-form]
  phase_2_composition:
    file: phase-2/knowledge/composition/README.md
    phase: 2
    triggers: [composition, recipe, premium, anti-homogenization]
    excludes: [single-component]
  phase_2_cinematic_motion:
    file: phase-2/motion/cinematic-motion.md
    phase: 2
    triggers: [webgl, three-js, 3d, cinematic-hero, particles, shader-motion]
    excludes: [dashboard, form, app-screen]
  phase_2_technology_resolver:
    file: phase-2/05-frontend-implementation/technology-resolver.md
    phase: 2
    triggers: [animation-library, gsap, framer-motion, rive, lottie, webgl, canvas, view-transitions, new-dependency]
    excludes: []
  phase_2_performance_budget:
    file: phase-2/05-frontend-implementation/performance-budget.md
    phase: 2
    triggers: [visual-effect, continuous-animation, scroll-effect, webgl, backdrop-filter]
    excludes: [static-content-only]
  phase_2_design_quality_evals:
    file: evals/quality/README.md
    phase: 2
    triggers: [design-quality, motion-quality, benchmark, premium-review]
    excludes: [structure-only]
```

This is an index, not an exhaustive catalog. Add entries only when routers need a new deterministic selection rule.
