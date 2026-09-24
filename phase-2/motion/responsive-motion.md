# Responsive motion

Responsive design covers motion as well as layout. Every motion decision states its behavior at each of the five levels below. Levels are cumulative: each one applies everything above it plus its own reductions.

| Level | Signal | Motion behavior |
|---|---|---|
| **Desktop full** | `(hover: hover) and (pointer: fine)`, wide viewport | All selected tiers up to the style's ceiling, within the page budget |
| **Tablet** | Coarse pointer or medium viewport | No hover-dependent motion; pinned sections shortened; parallax off; M5 only if lightweight |
| **Mobile** | Narrow viewport, coarse pointer | M1–M3 kept; M4 reduced to reveals and native scroll-snap; M5 replaced by poster/video; entrance distances halved |
| **Low-power** | `prefers-reduced-data`/`save-data`, `navigator.hardwareConcurrency <= 4` or `deviceMemory <= 4` as hints, or measured jank | No continuous loops, no shaders or particles, static effects, pre-blurred images instead of live blur |
| **Reduced motion** | `prefers-reduced-motion: reduce` | Per-entry `reduced_motion` fallback; essential feedback kept; see [reduced-motion.md](reduced-motion.md) |

## Transformation examples

| Desktop | Mobile | Reduced motion |
|---|---|---|
| Pinned 3D product sequence (M5) | Short muted video with poster, or stacked exploded-view images | Static labelled images |
| Sticky storytelling (M4) | Stacked steps with inline visuals | Stacked steps |
| Parallax hero layers | Static composition | Static composition |
| Cursor-reactive light | Static light | Static light |
| Card → modal morph (M3) | Full-screen sheet slide-up | Fade |
| Hover lift on cards | No lift; press feedback | Color change only |

## Rules

- Decide mobile motion explicitly. It is not whatever the desktop animation happens to do on a phone.
- Treat hardware hints (`deviceMemory`, `hardwareConcurrency`, connection) as hints. Degrade progressively and never block content.
- Gate heavy motion behind `matchMedia` checks that also listen for changes (a user can toggle reduced motion mid-session).
- Test motion at the `mobile` and `desktop` viewports of [execution/viewports.md](../../execution/viewports.md). The E78 Responsive Motion eval uses runtime probes at both.
