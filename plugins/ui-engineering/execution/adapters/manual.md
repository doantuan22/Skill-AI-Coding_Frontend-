# Manual evidence fallback

When no usable automation exists, produce a truthful manual execution request: target route, required viewport IDs, expected target UI/root content, visual dimensions to inspect, safe interactions needed, and evidence expected from a human or agent-provided browser tool.

Status is `NOT_EXECUTED`, `LIMITED`, or `BLOCKED` until evidence is actually supplied. Manual fallback never implies that a page was opened, rendered, or passed visual QA.
