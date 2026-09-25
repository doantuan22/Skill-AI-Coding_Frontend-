# Anti-homogenization

Generated interfaces converge on one look. For "tech" products it is:

```text
dark background + purple/blue gradient + glass cards + bento grid + huge centered heading (+ glow, + floating particles)
```

Any of these can be right. The problem is choosing them **by default**, for every product. This rule complements [AI-tell density](../../visual-language/ai-tell-density.md): that file reviews a rendered page for clustered tells; this file prevents the cluster at decision time.

## Pre-design declaration (required before choosing a design language)

Record these in `CAPABILITY-PLAN.md` before styles are ranked:

| Input | Question |
|---|---|
| Brand personality | Which 3–5 attributes, and which attributes must it *not* project? |
| Product type / domain | What category, and what do users do with it? |
| Audience | Who decides and who uses it, and how expert are they? |
| Information density | Low, medium or high? |
| Interaction model | Browse, read, operate, create, transact or converse? |
| Content | What real assets exist (product UI, media, code, data, long-form)? |
| Visual intensity | 1–5 |
| Desired differentiation | How must this look different from its category's defaults and its competitors? |

Without these inputs the resolver cannot rank styles, and the design language is not chosen.

## Default-combination guard

Catalog entries flagged `default_tell: true` (styles: glassmorphism, bento, gradient-heavy, ai-native; layouts: bento grid; effects: glass, glow, mesh gradient, backdrop blur, particles) are overused defaults.

- The resolver penalizes them and allows **at most one** in a composition unless the user explicitly requests them (`explicit_styles`) or the content requires them.
- A composition containing **three or more** default-tell items, or the full combination above without recorded reasons, is `HOMOGENIZED_DESIGN`.
- Differentiation must come from product-specific decisions (content, typography, one signature moment), not from swapping one trend for another.

## Diversity check across projects

When the same agent designs several products, their compositions must differ in primary style, hero/section layout and signature effect. `tests/test_knowledge.py` enforces this for the resolver scenario set: no two scenarios share the same style, layout and effect selection, and the bento + gradient + glass combination may appear in at most one scenario.
