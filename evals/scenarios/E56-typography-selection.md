---
id: E56
name: Typography selection
category: inspiration
project_state: fixture inspiration/vietnamese-typography
user_request: Create a typography system that feels premium but trustworthy.
expected_route: Phase 2 / typography intelligence → font selection → pairing → rhythm → design system typography section → typography review
required_artifacts: [DESIGN-SYSTEM, VISUAL-REVIEW]
forbidden_behavior: [unverified-vietnamese-coverage, vendor-font-files, font-chosen-by-trend, more-than-two-families]
expected_context: [typography/README, typography-archetypes, font-selection, font-pairing, typography-rhythm, technical-type]
success_conditions: [archetype-with-reasoning, license-and-coverage-recorded, diacritic-test-string-verified, tabular-numerals-for-prices, fallback-stack-defined]
failure_conditions: [typography-character-missing, excessive-font-families, unnecessary-dependency]
---

Fixture: [`fixtures/inspiration/vietnamese-typography`](../fixtures/inspiration/vietnamese-typography/README.md).

Teammate-suggested trendy fonts must be verified for Vietnamese before use; if coverage is missing, a covered alternative with similar character is chosen.
