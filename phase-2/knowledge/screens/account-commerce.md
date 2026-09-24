# Account, onboarding and commerce screens

```yaml
id: screen.settings
name: Settings
kind: screen
category: account
phase_1_reference: phase-1/references/settings.md
anatomy: Section navigation, grouped settings with labels and descriptions, save model (auto or explicit), danger zone.
hierarchy: Frequent settings first; dangerous last.
primary_actions: Change settings; save.
secondary_actions: Reset, export.
states: [unsaved-changes, saving, saved, validation-error, permission-limited]
layout: Sidebar section nav plus form column.
interaction: Toggles for immediate effect, forms for batched changes, progressive disclosure for advanced.
motion: Toggle, save feedback; nothing decorative.
responsive: Section list then section page on mobile.
accessibility: Labels, descriptions linked, errors inline.
common_mistakes: Mixed auto-save and explicit save; destructive actions not separated.
variants: Account, workspace, notification preferences.
compatible_layouts: [layout.app-sidebar-workspace]
key_interactions: [interaction.progressive-disclosure, interaction.inline-editing, interaction.focus-management]
key_motion: [motion.m1-toggle, motion.m1-button-feedback]
```

```yaml
id: screen.onboarding
name: Onboarding
kind: screen
category: account
phase_1_reference: phase-1/references/onboarding.md
anatomy: Progress indicator, one task per step, skip/back, value preview, completion.
hierarchy: Current step task; progress secondary.
primary_actions: Complete step.
secondary_actions: Skip, back, get help.
states: [step-active, step-error, skipped, completed]
layout: Centered focused column or split with preview.
interaction: Progressive disclosure, inline validation, sample data.
motion: Step transitions with direction; one celebration at completion.
responsive: Full-screen steps on mobile.
accessibility: Step announced; focus moves to step heading.
common_mistakes: Tours of every feature; blocking modals; no skip.
variants: Account setup, product tour, checklist.
compatible_layouts: [layout.hero-split, layout.hero-centered]
key_interactions: [interaction.progressive-disclosure, interaction.focus-management]
key_motion: [motion.slide, motion.m1-success, motion.m1-progress]
```

```yaml
id: screen.authentication
name: Authentication
kind: screen
category: account
anatomy: Brand, sign-in form (identifier, secret or passwordless), alternative methods, recovery link, sign-up switch.
hierarchy: The form is the only focus.
primary_actions: Sign in or continue.
secondary_actions: Forgot password, other methods, create account.
states: [idle, submitting, invalid-credentials, locked, mfa-required, success]
layout: Centered narrow column; optional brand panel on desktop.
interaction: Password visibility toggle, autofill support, passkeys.
motion: Button feedback, error message appearance; nothing else.
responsive: Single column; keyboard-aware on mobile.
accessibility: Autocomplete attributes, error summary, no CAPTCHA-only paths.
common_mistakes: Placeholder labels; decorative animations; vague errors.
variants: Sign in, sign up, passwordless, SSO.
compatible_layouts: [layout.hero-split, layout.hero-centered]
key_interactions: [interaction.press-feedback, interaction.focus-management]
key_motion: [motion.m1-button-feedback, motion.m1-error]
```

```yaml
id: screen.profile
name: Profile
kind: screen
category: account
anatomy: Identity (avatar, name, role), editable details, activity or content, privacy controls.
hierarchy: Identity then editable details.
primary_actions: Edit profile.
secondary_actions: Change avatar, privacy, share.
states: [viewing, editing, saving, error]
layout: Detail screen with sections.
interaction: Inline editing, upload avatar with crop.
motion: Save feedback; avatar upload progress.
responsive: Stacked sections.
accessibility: Avatar alt text, form labels.
common_mistakes: Public and private fields indistinguishable.
variants: Own profile, public profile, team member profile.
compatible_layouts: [layout.app-master-detail]
key_interactions: [interaction.inline-editing, interaction.drop-zone]
key_motion: [motion.m1-success, motion.m1-progress]
```

```yaml
id: screen.billing
name: Billing
kind: screen
category: commerce
anatomy: Current plan and usage, payment method, invoices, upgrade/downgrade, cancellation.
hierarchy: Plan and next charge first.
primary_actions: Change plan; update payment method.
secondary_actions: Download invoices, cancel.
states: [active, trial, past-due, cancelled, payment-failed]
layout: Settings-style column with summary card.
interaction: Plan comparison, confirmation for changes, proration preview.
motion: Minimal; confirmation feedback.
responsive: Stacked; invoices as list.
accessibility: Amounts formatted for screen readers; tables for invoices.
common_mistakes: Hidden cancellation; unclear proration.
variants: SaaS billing, usage-based billing.
compatible_layouts: [layout.app-sidebar-workspace, layout.story-comparison]
key_interactions: [interaction.progressive-disclosure, interaction.focus-management]
key_motion: [motion.m2-modal, motion.m1-success]
```

```yaml
id: screen.pricing
name: Pricing
kind: screen
category: commerce
anatomy: Billing period toggle, plan tiers with price and key limits, feature comparison, FAQ, contact sales.
hierarchy: Recommended plan justified; price and period clear.
primary_actions: Choose a plan.
secondary_actions: Compare features, contact sales.
states: [monthly, yearly, region-currency, enterprise-contact]
layout: Tier columns plus comparison table.
interaction: Period toggle, expandable comparison, tooltips on limits.
motion: Price change on toggle (short), accordion.
responsive: Tier cards stacked; comparison table scrolls.
accessibility: Table semantics; toggle state announced.
common_mistakes: Fake discounts; hidden fees; decoy tiers.
variants: SaaS tiers, usage pricing, one-time purchase.
compatible_layouts: [layout.story-comparison, layout.grid-card-matrix]
key_interactions: [interaction.progressive-disclosure, interaction.smart-tooltip]
key_motion: [motion.m1-toggle, motion.m2-accordion]
```

```yaml
id: screen.checkout
name: Checkout
kind: screen
category: commerce
phase_1_reference: phase-1/references/checkout.md
anatomy: Order summary, contact/shipping, payment, review, confirmation.
hierarchy: Current step, then summary with total.
primary_actions: Pay or place order.
secondary_actions: Edit cart, apply code, back.
states: [step-error, payment-processing, payment-failed, confirmed]
layout: Two columns (form plus sticky summary) on desktop.
interaction: Inline validation, autofill, address lookup.
motion: Processing indicator; no decorative motion.
responsive: Collapsible summary on mobile; sticky pay button.
accessibility: Error summary; payment fields labelled; no timeouts without warning.
common_mistakes: Surprise fees; distracting animations; lost input on error.
variants: One-page, multi-step, express pay.
compatible_layouts: [layout.hero-split]
key_interactions: [interaction.focus-management, interaction.press-feedback]
key_motion: [motion.m1-button-feedback, motion.m1-error, motion.m1-success]
```

```yaml
id: screen.notifications
name: Notifications
kind: screen
category: account
anatomy: Filter (all/unread/mentions), grouped notification list, mark read, settings link.
hierarchy: Unread and actionable first.
primary_actions: Open notification target.
secondary_actions: Mark read, mute, settings.
states: [empty, unread, all-read, loading]
layout: Panel or page list.
interaction: Swipe actions on touch, bulk mark read, undo.
motion: New items slide in; read state transitions.
responsive: Full-screen list on mobile.
accessibility: New notification announcements polite; badges with counts in text.
common_mistakes: Everything marked important; no grouping.
variants: Inbox panel, activity feed notifications.
compatible_layouts: [layout.app-inbox]
key_interactions: [interaction.swipe-action, interaction.multi-select, interaction.undo]
key_motion: [motion.m2-notification]
```

```yaml
id: screen.activity
name: Activity feed
kind: screen
category: account
anatomy: Chronological events with actor, action, object, time; filters.
hierarchy: Recent and relevant first.
primary_actions: Open referenced object.
secondary_actions: Filter by actor/type.
states: [empty, loading, end-of-feed]
layout: Timeline list.
interaction: Load more, filter, hover preview of objects.
motion: New events fade in at top without shifting reading position.
responsive: Compact entries.
accessibility: Time with machine-readable datetime.
common_mistakes: Feed pushes content while reading.
variants: Audit log, team activity, commit history.
compatible_layouts: [layout.story-timeline, layout.app-master-detail]
key_interactions: [interaction.hover-preview, interaction.keyboard-navigation]
key_motion: [motion.fade]
```
