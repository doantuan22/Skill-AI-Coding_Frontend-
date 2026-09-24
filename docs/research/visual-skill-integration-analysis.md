# Visual skill integration analysis

## Scope and method

This is a research record, not a runtime dependency. The four local repositories were inspected in this order: `frontend-craft`, `unslop-ui`, `Anti-AI-UI`, then `ui-ux-kit`. Readmes, skill definitions, references and licences were reviewed; package folders, generated imagery, source code, CSV datasets and example assets were intentionally excluded. Ideas below are independently paraphrased. No source code, design assets, screenshots, vendor names, or source text are imported into the core skill.

The core already had useful direction, token, component, responsive and QA modules plus a short anti-generic reference. Its gap was a layer between tokens and realized components: it did not make button, feedback, icon, surface, color, type, or motion behavior an explicit, reviewable contract. The old reference also treated tells as a flat list, without a density or preserve-existing-system decision.

## Repository analysis

| Repository | Useful concepts and unique techniques | Existing overlap / gap | Worth adapting and suggested destination | Do not integrate / duplication risk |
|---|---|---|---|---|
| `frontend-craft` | Product/audience-led visual direction; audit live UI before changing it; treat clustered visual tells as more meaningful than one style choice; root-cause token fixes; explicit craft details such as states, nested radii and purposeful motion. | Direction, tokens and existing anti-slop already overlap. Missing: explicit extraction classification and density-based review. | Adapt decision rationale to `visual-language/visual-grammar.md`, `ai-tell-density.md`, `craft-review.md`, and the current-system workflow. | Do not preserve its frequency claims or recreate its catalogue verbatim. A static blacklist would duplicate and age poorly. Licence not present in this local checkout: concepts only, no copying. |
| `unslop-ui` | Restraint checks for hue overload, decorative icon containers, emoji misuse, gratuitous glass/gradients, nested cards and ornamental animation; a quick visual “squint” test. | The old anti-slop reference mentions most categories, but lacks component-specific grammar and exceptions. | Adapt as review signals in `anti-slop/global.md`, `color.md`, `icons.md`, `surfaces.md`, and component rules. | MIT licence was reviewed. Do not copy its wording, examples or image assets. Avoid turning its style preferences into universal bans. |
| `Anti-AI-UI` | Filter → constructive palette → contextual research sequence; component negative review; deliberate visual rhythm; semantic HTML and reduced-motion quality bar; scope-aware system choices. | Existing design-intelligence and accessibility already own contextual strategy and accessibility. Missing: constructive craft/adversarial review before browser QA. | Adapt the three-part review sequence into `craft-review.md` and `adversarial-review.md`; add character docs for type, motion and surfaces. | MIT licence was reviewed. Do not reuse component recipes, data CSVs, scripts, library/vendor catalogues, branded exemplars, or hard bans. Those would duplicate existing Intelligence and Accessibility modules. |
| `ui-ux-kit` | A written visual profile, surface hierarchy, component reuse, interaction-state completeness, and preserving a coherent existing system; clear separation of experiential work from normal product UI. | Existing Design System has tokens and Component Realization has contracts, but neither owns rendered visual behavior. | Adapt profile fields into `VISUAL-GRAMMAR.md`; route only approved experiential direction through existing motion decisions; use review gates for state completeness. | MIT licence was reviewed. Do not copy its template, package recommendations, animation/3D toolkit lists or quality checklist. Avoid making the Visual Language module a second Design System. |

## Integration decisions

1. **Source of truth remains separated:** Design System owns named tokens; Visual Grammar owns how visual choices behave and combine; Component Spec owns realized component APIs, semantics and implementation.
2. **Preserve before polish:** existing UI patterns are classified `KEEP`, `REFINE`, `NORMALIZE`, or `REPLACE`; a coherent system is not rewritten merely to look newer.
3. **Density, not dogma:** a pattern becomes a concern when several unexplained tells reinforce one another. Product-, brand-, or task-justified exceptions are recorded in the grammar.
4. **No external runtime coupling:** every operational link points within this repository. `external-references/` stays research-only.

## License and provenance note

`unslop-ui`, `Anti-AI-UI`, and `ui-ux-kit` declare MIT licences in their local `LICENSE` files. `frontend-craft` had no licence file in the local checkout. Regardless of licence, this integration paraphrases principles and creates original, repository-native guidance only. Before any future literal reuse, verify upstream licence, attribution, and scope separately.
