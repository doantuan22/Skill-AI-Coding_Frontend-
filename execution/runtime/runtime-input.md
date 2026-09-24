# Runtime input

The runner accepts JSON with `session_id`, `base_url`, non-empty `routes`, semantic `viewports`, and `iteration >= 1`. Each route has `page_id`, `route`, and optional `expected_selector` or `expected_text`. Optional fields include `output_dir`, finite readiness/navigation/cleanup timeouts, screenshot/console/full-page options, and an explicit `start` block.

`start.command` must be an argv array, not a shell string, and runs only with the runner’s explicit `--allow-start` flag. Command precedence is explicit request → previously detected/documented project command; the runner never infers or executes arbitrary commands. Output defaults to `<project>/.evidence/<session-id>` and must remain under the project root.
