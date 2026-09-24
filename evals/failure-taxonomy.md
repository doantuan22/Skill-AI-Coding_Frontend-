# Failure taxonomy

| Code | Meaning |
|---|---|
| `ROUTING_FAILURE` | Wrong phase, mode, path, or rollback target. |
| `CONTEXT_OVERLOAD` | Reads unnecessary levels/references or repeats context. |
| `WRONG_REFERENCE` | Loads irrelevant or omits triggered guidance. |
| `DUPLICATE_ARTIFACT` | Creates uncontrolled duplicate artifact. |
| `STALE_ARTIFACT_USAGE` | Uses an invalidated downstream artifact. |
| `PHASE_BOUNDARY_VIOLATION` | Crosses Phase 1/2 semantic/visual ownership. |
| `STRUCTURE_LOCK_VIOLATION` | Bypasses, edits, or violates locked structure. |
| `BUSINESS_RULE_INVENTION` | Treats an unconfirmed business rule as fact. |
| `SCOPE_CREEP` | Changes outside the explicit task. |
| `LOOP_FAILURE` | Loops without progress or ignores iteration limit. |
| `PREMATURE_DONE` | Marks complete before required gates/evidence. |
| `TRACEABILITY_BREAK` | Required relation cannot be traced through output. |
| `CAPABILITY_MISDETECTION` | Existing or missing capability classified incorrectly. |
| `UNNECESSARY_TOOL_INSTALL` | Installs tool/package without authorization or need. |
| `WRONG_PACKAGE_MANAGER` | Ignores project lockfile/package-manager choice. |
| `DUPLICATE_SERVER` | Starts a server despite an existing target server. |
| `UNSAFE_PROCESS_KILL` | Stops a user-owned or unknown process. |
| `FALSE_READINESS` | Treats spawn/sleep as proof the page is ready. |
| `FAKE_VISUAL_PASS` | Claims visual verification without actual evidence. |
| `MISSING_EVIDENCE` | Route/viewport/session evidence is absent or unlinked. |
| `WRONG_VIEWPORT` | Omits required viewport or performs unnecessary broad sweep. |
| `EXECUTION_LOOP` | Repeats adapter strategy without progress. |
| `CLEANUP_FAILURE` | Owned resource cleanup fails or is unreported. |
| `RUNTIME_RUNNER_FAILURE` | Runtime orchestration fails outside a classified route/capture error. |
| `EVIDENCE_CORRUPTION` | Manifest/report is invalid or incomplete. |
| `EVIDENCE_MISMATCH` | Capture metadata/file does not match requested target. |
| `UNSAFE_SERVER_TERMINATION` | Runner terminates a server it does not own. |
| `AUTO_INSTALL_VIOLATION` | Runner installs Playwright/browser or mutates dependency state. |
| `FALSE_RUNTIME_PASS` | Runner reports completed without required evidence. |
| `PARTIAL_EVIDENCE_LOSS` | Valid capture is discarded after another capture fails. |
| `STALE_EVIDENCE_ACCEPTED` | Old iteration evidence is accepted for changed code. |
| `VISUAL_GRAMMAR_MISSING` | Rendered visual decisions lack an approved/referenced grammar. |
| `AI_TELL_DENSITY_HIGH` | Several unexplained generic signals reinforce each other in a region or page. |
| `BUTTON_GRAMMAR_DRIFT` | Button hierarchy, shape, state, icon, or elevation behavior diverges without rationale. |
| `FEEDBACK_GRAMMAR_DRIFT` | Feedback channel does not match scope, persistence, recovery or accessibility need. |
| `ICONOGRAPHY_DRIFT` | Icon family, semantic role, accessible labeling, or color treatment is inconsistent. |
| `SURFACE_OVERUSE` | Surfaces/cards/elevation are added without grouping or layering purpose. |
| `COLOR_CHARACTER_DRIFT` | Accent, semantic, neutral or surface color distribution obscures hierarchy. |
| `COMPONENT_PERSONALITY_DRIFT` | Components no longer share the approved visual character. |
| `UNNECESSARY_VISUAL_REWRITE` | A coherent existing system is changed without evidence-based need. |
| `REFERENCE_COPYING` | External reference assets, source, pixels, or distinctive identity are copied rather than reinterpreted. |
| `INSPIRATION_DIRECTION_MISSING` | Visual work proceeds without a selected archetype/design DNA where the router required one. |
| `INCOMPATIBLE_REFERENCE_MIX` | Too many or conflicting DNA sources combined (density, surface or motion philosophy clash). |
| `GENERIC_TEMPLATE_COMPOSITION` | Page reduces to interchangeable hero/cards/testimonials/CTA blocks without content-driven reasoning. |
| `PATTERN_MISUSE` | Pattern used without its content requirement or for content it hides/harms. |
| `VISUAL_STORYTELLING_WEAK` | Sections lack narrative progression; claims lack nearby evidence. |
| `TYPOGRAPHY_CHARACTER_MISSING` | No type archetype/decision, or type voice contradicts the product archetype. |
| `WEAK_TYPE_HIERARCHY` | Type roles are too close in size/weight to create order. |
| `EXCESSIVE_FONT_FAMILIES` | More families than justified jobs. |
| `DISPLAY_FONT_MISUSE` | Display face used for body, labels, dense UI or small sizes. |
| `POOR_READING_MEASURE` | Reading line length or line-height outside readable ranges. |
| `MONO_OVERUSE` | Monospace used outside technical content. |
| `TYPE_STYLE_DRIFT` | Ad-hoc sizes/weights/families outside the type system. |
| `MOTION_FOR_DECORATION` | Motion without feedback, orientation, hierarchy, state or story purpose. |
| `EXCESSIVE_ENTRANCE_ANIMATION` | Entrance animation on most elements or repeated triggers. |
| `EVERYTHING_ANIMATED` | No calm regions; intensity budget missing or exceeded. |
| `SLOW_INTERACTION` | Feedback/transition durations delay the task. |
| `SCROLL_JANK_RISK` | Scroll-linked or continuous motion implemented with main-thread/layout-heavy techniques. |
| `MOTION_WITHOUT_REDUCED_MODE` | Non-essential motion lacks a `prefers-reduced-motion` equivalent. |
| `MOTION_STYLE_DRIFT` | Motion timing/easing/character inconsistent or contradicting the archetype; mixed animation systems. |
| `UNJUSTIFIED_PARALLAX` | Parallax without a depth narrative or on text/mobile/multiple sections. |
| `UNNECESSARY_DEPENDENCY` | Animation/font package added when native or existing tooling suffices, or without authorization. |

| `SCROLL_HIJACKING` | Scroll speed/direction overridden or content force-snapped without reason. |
| `MOTION_LAYOUT_INSTABILITY` | Motion animates layout properties or causes layout shift. |
| `COMPETING_MOTION_DIRECTIONS` | Simultaneous motions move in conflicting directions. |
| `CAPABILITY_PLAN_MISSING` | A new build/redesign chose styles, effects or technology without a resolved, explained capability plan. |
| `HOMOGENIZED_DESIGN` | Default tech look (dark + purple gradient + glass + bento + huge heading, glow, particles) chosen without product reasons. |
| `STYLE_INCOHERENCE` | Layers express different styles or mismatched intensities. |
| `PREMIUM_BY_EFFECTS` | "Premium" pursued by adding effects instead of hierarchy, consistency, detail and restraint. |
| `EFFECT_OVERUSE` | Effect budget or single-signature rule exceeded. |
| `INTERACTION_FEEDBACK_MISSING` | Interactive elements lack hover/focus/pressed/loading feedback. |
| `HOVER_ONLY_INTERACTION` | Information or actions reachable only by hover. |
| `HIDDEN_INTERACTION` | Gestures/shortcuts without visible cues or alternatives. |
| `HEAVY_DEPENDENCY_FOR_SIMPLE_EFFECT` | A library is used where native CSS/JS suffices. |
