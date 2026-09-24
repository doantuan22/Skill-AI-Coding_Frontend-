# Visual Language

This layer translates approved direction and Design System tokens into a coherent rendered visual behavior. It sits after `03-design-system` and before `04-component-realization`; it cannot alter the Structure Lock, product flow, content requirements, API, or component responsibility.

Read [workflow.md](workflow.md), then select only the relevant grammar/reference. Tokens name values; this layer defines their proportion, hierarchy, combination and exceptions. Component specs turn the selected behavior into reusable implementation.

For existing UI, inventory representative patterns first and classify each as `KEEP`, `REFINE`, `NORMALIZE`, or `REPLACE`. Preserve a coherent established language unless evidence ties replacement to the approved direction or an actual usability/quality issue.

## Source-of-truth boundary

| Owner | Owns | Does not own |
|---|---|---|
| Design Inspiration | archetype, reference DNA, pattern candidates | rendered behavior rules |
| Typography Intelligence | type character, families, pairing, rhythm | component behavior |
| Design System | semantic tokens, scales, themes | page-level visual behavior |
| Visual Grammar | visual character, component behavior, composition and exceptions | component API or business semantics |
| Motion System | temporal behavior, intensity budget, reduced motion | static visual behavior |
| Web Patterns | composition vocabulary | which content exists (Phase 1) |
| Component Spec | variants, semantics, states, implementation location | new palette/direction decisions |

Use [craft-review.md](craft-review.md) before browser QA and [adversarial-review.md](adversarial-review.md) for redesigns or suspected generic output.

