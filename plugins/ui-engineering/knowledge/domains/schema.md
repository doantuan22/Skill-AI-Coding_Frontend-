# Knowledge schemas

Every catalog entry is a fenced `yaml` block whose first key is `id`, inside `phase-2/knowledge/`, `phase-2/motion/`, `phase-2/web-patterns/` or `phase-2/05-frontend-implementation/`. `scripts/knowledge_lib.py` parses, validates and indexes them.

## Format rules (YAML subset)

- `key: value`, `key: [a, b]`, nested mappings by two-space indentation, and `- item` sequences.
- Plain values must not start with a YAML indicator character (ampersand, asterisk, exclamation mark, pipe, greater-than, percent, at-sign, backtick, opening brace, question mark, colon, comma, apostrophe, hash) or with `- `, and must not contain `: ` or ` #`. Wrap such a value in double quotes.
- Booleans are written `true`/`false`. Intensity ranges are `[min, max]`.
- Ids are `<kind>.<slug>` (`tech.<slug>` for technologies) and unique across the whole knowledge base.
- References to other entries use ids and are validated. A missing or wrong-kind id fails validation.
- Extra fields are allowed (e.g., `aliases`, `phase_1_reference`) but are not used by the resolver.

## Base schema

```text
id, name, kind, category
```

`kind` ∈ `style | layout | screen | motion | interaction | effect | recipe | technology | graphics`.

## Specialized schemas

### style

`family, character, visual_language, layout, typography, color_behavior, surface, borders, shadows, imagery, iconography, motion, interaction, recommended_effects[effect], avoid_effects[effect], recommended_motion[motion], density[], accessibility_notes, responsive_behavior, good_for, avoid_when, compatible_patterns[layout], compatible_styles[style], implementation_notes, domains[DOMAINS], conveys[ATTRIBUTES], perceived_risks[ATTRIBUTES], intensity[min,max], contexts[CONTEXTS], motion_ceiling(M1–M5), default_tell`

### layout

`purpose, anatomy, hierarchy, grid_behavior, responsive, content_requirements[CONTENT], compatible_styles[style], compatible_motion[motion], interactions[interaction], accessibility, implementation, anti_patterns, good_for, avoid_when, contexts[], density[], motion_cost(low|medium|high), default_tell`

### screen

`anatomy, hierarchy, primary_actions, secondary_actions, states[], layout, interaction, motion, responsive, accessibility, common_mistakes, variants, compatible_layouts[layout], key_interactions[interaction], key_motion[motion]` (+ optional `phase_1_reference`)

### motion

`tier(primitive|M1–M5), purpose, serves[SERVES], trigger, behavior, duration, easing, spring, entrance, exit, interruption, responsive, reduced_motion, performance{cost, notes}, technology{preferred[tech], alternatives[tech]}, intensity(low|medium|high), contexts[], avoid_when, examples`

### interaction

`purpose, flow{input, feedback, state, motion, result}, input_methods{mouse, touch, keyboard}, states[], feedback, motion, error_behavior, accessibility, mobile, desktop, recommended_use, avoid_when, contexts[], min_interaction_intensity(1–5), technology{preferred, alternatives}`

### effect

`visual_purpose, construction, parameters, compatible_styles[style], recommended_contexts[], performance{cost, notes}, accessibility, responsive, implementation, anti_patterns, technology{preferred, alternatives}, default_tell`

### recipe

`domains[], conveys[], styles[style], layouts[layout], typography, surface, color, effects[effect], motion[motion], interactions[interaction], technology[tech], avoid, why`

### technology

`use_for, when_to_use, when_not_to_use, requires_dependency, packages[], cost, fallback, accessibility, responsive, lifecycle`

### graphics

`purpose, when_to_use, when_not_to_use, technology[tech], cost, fallback, accessibility, responsive, lifecycle`

## Vocabularies

Defined once in `scripts/knowledge_lib.py`: `DOMAINS`, `ATTRIBUTES`, `CONTEXTS` (`marketing, application, content, commerce`), `CONTENT`, `DENSITY`, `INTENSITY`, `COST` (`none, low, medium, high, very-high`), `TIERS`, `SERVES` (`feedback, state-change, orientation, continuity, hierarchy, attention, storytelling, delight, brand-expression`). Add a term only when an entry or profile genuinely needs it, and document it in the extension guide.
