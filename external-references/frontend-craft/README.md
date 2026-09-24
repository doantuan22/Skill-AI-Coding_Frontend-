# Frontend Craft

An agent skill that keeps AI coding agents from shipping generic, AI-looking frontend design, and that can unslop a frontend that already shipped that way.

AI-generated frontends converge on the same defaults: the same fonts, the same purple CTA, the same three identical feature cards. The look is recognizable enough that people call it slop and catalog its tells. This skill merges that research, along with established interface craft and visual design fundamentals, into one skill a coding agent can actually follow. For a new build: commit to a design direction, build a real system, implement with craft, and audit the result before delivering. For an existing codebase: inventory what's already there, audit it against the same catalog, and fix in place without a wasteful rebuild.

> "Colored left borders are almost as reliable a sign of AI-generated design as em-dashes for text."
>
> A designer, quoted in the Show HN analysis listed below.

## What's inside

The skill lives in `skills/frontend-craft/`:

- [`SKILL.md`](skills/frontend-craft/SKILL.md): the core. The workflow, rules by dimension, and a quick tell check with frequency data.
- [`references/slop-tells.md`](skills/frontend-craft/references/slop-tells.md): ~45 deduplicated AI-design tells with code signals and fixes.
- [`references/craft-checklist.md`](skills/frontend-craft/references/craft-checklist.md): interaction, form, typography, accessibility, and performance rules with exact values.
- [`references/design-foundations.md`](skills/frontend-craft/references/design-foundations.md): visual principles and how to build the type, color, spacing, and motion systems.

The skill is anchored on three findings that show up independently across the sources:

- **Slop is the absence of decisions, not a particular style.** Every visual choice should be explainable in terms of the product and its audience. A choice you cannot explain is a default someone else set.
- **The tells migrate.** The 2022 default was purple gradients and glassmorphism on near-black. The 2026 default is warm cream and an editorial serif. Both read as generated for the same reason. Avoid-lists rot, so the skill teaches the structural reasoning first and treats the concrete catalog as perishable.
- **Density is the signal.** Automated detectors pass pages with 1 or 2 tells and flag pages with 5 or more. No single pattern is banned; unexamined accumulation is.

## Installation

Clone the repo and copy `skills/frontend-craft` into the skills directory of whatever harness you use:

```bash
git clone https://github.com/nattergabriel/frontend-craft
```

- Claude Code: `.claude/skills/` in the project, or `~/.claude/skills/` for all projects
- Codex and other `.agents`-based setups: `.agents/skills/`
- Anything else that supports agent skills: its skills directory

The skill is a plain `SKILL.md` with YAML frontmatter plus reference files, no harness-specific machinery, so it works anywhere the skill format is supported.

> [!NOTE]
> Once installed, the skill triggers on its own whenever the agent builds, styles, or audits web UI, so there's usually nothing to invoke manually. If it doesn't fire on its own, just tell the agent to use it (e.g. "use the frontend-craft skill on this").

## How this skill was made

The content is aggregated, not invented. Eight curated resources, spanning slop catalogs, quantitative measurement, interface guidelines, accessibility, and visual design fundamentals, were each read in full and distilled into structured findings: every rule, pattern, threshold, and explanation the source had to offer.

Those findings were then merged and deduplicated. The slop catalogs overlap heavily (the card accent stripe appears in all four), so overlapping tells became single entries that keep the sharpest explanation, the exact code signals, and the measured frequency where one exists. General quality rules such as contrast floors and line length apply to any frontend, AI-made or not, so they were folded into the craft checklist rather than the tell catalog.

The result is organized for progressive disclosure: a lean `SKILL.md` that always loads, plus three reference files an agent reads when it needs them.

## Sources

All credit for the underlying research goes to these authors.

- [Anthropic: Prompting for Frontend Aesthetics](https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics). Why models converge on generic output, and prompt guidance for typography, color, motion, and backgrounds.
- [Kill AI Slop](https://killaislop.com). 33 AI-UI tells across color, typography, copy, components, motion, and layout, each with a before/after and why it fails.
- [Impeccable: Slop](https://impeccable.style/slop/). 46 patterns that mark an interface as AI-generated, including the 2022 vs 2026 era comparison showing how the tells migrate.
- [Scoring Show HN Submissions for AI Design Patterns](https://www.adriankrebs.ch/blog/design-slop/). Recurring AI design patterns measured across 1,590 Show HN sites. Source of the frequency data.
- [Design Slop Cop](https://github.com/AdrianKrebs/design-slop-cop). Open-source deterministic detector for 14 AI design patterns. Source of the exact thresholds and the density-based scoring.
- [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines). Practical rules for usable, accessible, polished web interfaces.
- [Accessibility for Visual Designers (digital.gov)](https://digital.gov/guides/accessibility-for-teams/visual-design). Concrete numbers for contrast, typography, forms, touch targets, and mobile layouts.
- [Nielsen Norman Group: Principles of Visual Design](https://media.nngroup.com/media/articles/attachments/Principles_Visual_Design-A4.pdf). Scale, visual hierarchy, balance, contrast, and Gestalt grouping.

## Updates

The tell catalog describes a moving target. Today's tasteful default is tomorrow's cliché, and the sources document this themselves: Space Grotesk went from a recommended distinctive choice to a slop-list entry within two years. This repo will be updated as the defaults shift: new tells added, stale ones retired, frequencies refreshed when new measurements exist. The structural principles are the stable part.
