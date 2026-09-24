# AI interface grammar

AI components make model work legible: what the AI is doing, what it produced, where it came from, and how the user stays in control. Reserve the AI accent color for AI states; do not use sparkle icons or purple gradients as a substitute for showing capability.

| Component | Design rules | States | Implementation guidance |
|---|---|---|---|
| **Prompt input** | Multi-line field that grows to a max height; clear send button; attachments shown as removable chips; model/tool options secondary; hint for Enter vs Shift+Enter | empty, typing, attachment uploading, sending, disabled (with reason), rate-limited | Pinned above the mobile keyboard; `interaction.drop-zone` for files; never lose the draft on error |
| **Thinking state** | Compact indicator in the response slot with honest text (e.g., "Searching documents"), not a fake progress bar | thinking, tool running (named), waiting for user permission | `motion.m1-loading`; announce state changes politely; show elapsed time for long runs |
| **Streaming state** | Text appears progressively in the final layout; a visible **Stop** control; cursor or caret subtle | streaming, stopped (partial kept), complete, error mid-stream | Append text without per-token layout animation (`motion.m3-layout-reflow` for block insertion only); screen readers get the completed answer, not every token; auto-scroll only if the user is at the bottom |
| **AI response** | Clear separation from user messages by alignment/spacing rather than heavy bubbles; readable body type; code blocks with copy; citations/sources inline and listed; actions (copy, regenerate, rate) quiet until hover/focus | complete, with sources, with tool results, edited, regenerated, flagged | Markdown rendering with safe HTML; long answers get headings; tables/charts use data-display grammar |
| **Inline suggestion / apply** | Proposed changes shown as a diff or highlight with Accept / Reject; applied changes briefly highlighted | proposed, accepted, rejected, reverted | `interaction.undo` after apply; focus stays in the user's work |

Anti-patterns: no stop control; streaming that jumps the page; AI output indistinguishable from verified content; typing animations that slow real output; generic "AI magic" decoration.
