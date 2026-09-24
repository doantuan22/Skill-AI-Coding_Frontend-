# Runtime input

The runner accepts JSON with `session_id`, `base_url`, non-empty `routes`, semantic `viewports`, and `iteration >= 1`. Each route has `page_id`, `route`, and optional `expected_selector` or `expected_text`. Optional fields include `output_dir`, finite readiness/navigation/cleanup timeouts, screenshot/console/full-page options, and an explicit `start` block.

`start.command` must be an argv array, not a shell string, and runs only with the runner’s explicit `--allow-start` flag. Command precedence is explicit request → previously detected/documented project command; the runner never infers or executes arbitrary commands. Output defaults to `<project>/.evidence/<session-id>` and must remain under the project root.

Optional design-evidence options (default off, behavior unchanged when absent): `options.reduced_motion` (`reduce` or `no-preference`) emulates the media preference for every capture in the session; `options.motion_probe` (boolean) records a read-only probe per capture after the screenshot (running animations, infinite loops, backdrop/blur/will-change element counts, `transition: all` elements, cumulative layout shift); `options.probe_wait_ms` (0–10000, default 1500) sets the settle time. Reduced-motion captures use the id suffix `:reduced-motion` and file suffix `__reduced-motion`.
