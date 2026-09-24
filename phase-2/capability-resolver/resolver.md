# Resolver rules

Reference implementation: `scripts/resolve_capabilities.py`. The rules below are the contract. If code and document disagree, fix the code or update both deliberately.

## Profile

```json
{
  "id": "premium-ai-saas",
  "intent": "Futuristic AI product; premium, technical, impressive, not flashy.",
  "domain": ["ai", "saas"],
  "brand_attributes": ["premium", "technical", "futuristic", "impressive", "calm"],
  "avoid_attributes": ["flashy", "noisy"],
  "visual_intensity": 3,
  "interaction_intensity": 3,
  "density": "medium",
  "contexts": ["marketing"],
  "screens": [],
  "content": ["product-ui", "metrics"],
  "platform": ["desktop", "mobile"],
  "existing_dependencies": [],
  "allow_new_dependencies": false,
  "explicit_styles": [],
  "exclude_styles": []
}
```

| Field | Values |
|---|---|
| `domain` | Controlled vocabulary `DOMAINS` in `scripts/knowledge_lib.py` |
| `brand_attributes`, `avoid_attributes` | Controlled vocabulary `ATTRIBUTES` ("not flashy" → `avoid_attributes: [flashy]`) |
| `visual_intensity` | 1 restrained … 5 spectacle |
| `interaction_intensity` | 1 read/click … 5 direct manipulation and play |
| `density` | `low`, `medium`, `high` |
| `contexts` | `marketing`, `application`, `content`, `commerce` |
| `screens` | Screen ids from locked page types (e.g., `screen.dashboard`) |
| `content` | Real content that exists: `product-ui`, `product-media`, `code`, `data`, `long-form`, … |
| `existing_dependencies` | Package names detected by `scripts/detect_capabilities.py` (`design_runtime.packages`) |

## Style ranking

Rejected when contexts do not overlap, density is outside the style's range, or visual intensity is more than one level outside the style's `intensity`.

| Signal | Score |
|---|---|
| Each matching domain | +3 |
| Each brand attribute the style conveys | +2 |
| Each avoided attribute the style conveys or risks | −4 |
| Each conveyed attribute that conflicts with a brand attribute (e.g., calm vs energetic) | −2 |
| Visual intensity inside range / one level outside | +2 / −1 |
| Explicitly requested | +10 |
| `default_tell` style not requested | −2 |

The **primary** is the top score. The **secondary** is the best-scoring entry from the primary's `compatible_styles` with a positive score (never two default-tell styles). The secondary is scoped to a region or layer.

## Layout ranking

Rejected for missing required content, density more than one level off, or `motion_cost: high` below visual intensity 4. Scores: +4 compatible with primary, +2 with secondary, +3 listed in the primary's `compatible_patterns`, +3 fits a requested screen, −1 per density level off, −1 medium motion cost below intensity 3, −2 default tell. Selection: marketing/content/commerce → one hero plus up to three grid/storytelling layouts (max two per category); application → up to two application shells plus one grid.

## Motion gating

| Tier | Allowed when |
|---|---|
| primitive, M1, M2 | Always (up to the style's `motion_ceiling`) |
| M3 | Interaction intensity ≥ 3 or application context |
| M4 | Marketing or content context and visual intensity ≥ 2 |
| M5 | Visual intensity ≥ 4, desktop platform, marketing context |

Maximum motion intensity: `high` at visual intensity ≥ 4; `medium` at visual ≥ 2 or interaction ≥ 3; otherwise `low`. Only one `high` motion per plan. Baseline feedback (press, focus, hover) comes first; plans are capped at 12 motion patterns. Candidates come from the primary/secondary `recommended_motion`, selected layouts' `compatible_motion` and screens' `key_motion`.

## Interaction selection

Baseline: press feedback, focus management, keyboard navigation. Then screens' `key_interactions` and layouts' `interactions`, filtered by `min_interaction_intensity` and context, capped at 10.

## Effect budget

Points: none 0, low 1, medium 2, high 4, very-high 6. Budget by visual intensity: 1→2, 2→3, 3→5, 4→8, 5→12. High-cost effects need visual intensity ≥ 4; one signature (high-cost) effect per page, and it may come only from the primary style. The primary style's `avoid_effects` are enforced. The secondary style may add low/medium supporting effects.

## Anti-homogenization guard

At most one `default_tell` item among the secondary style, layouts and effects unless the style was explicitly requested. Three or more default-tell items mark the plan `homogenized`.

## Technology resolution

For each selected motion, effect and interaction, candidates are `technology.preferred` then `alternatives`:

1. an option already installed in the project (reuse; never add a second library for the same job);
2. otherwise the first **native** option among `preferred` (`requires_dependency: false`);
3. otherwise, only if `allow_new_dependencies`, the first preferred library, recorded as a new dependency;
4. otherwise the first native option among `alternatives`, recorded as a fallback;
5. otherwise the capability is **degraded** (removed with a reason).

## Composition anchor

Recipes score +3 per domain, +4 if they contain the primary style, +2 the secondary, +1 per shared layout/effect, +1 per shared conveyed attribute. The top recipe is the anchor. Items it contains that the plan did not adopt are listed, not silently added.
