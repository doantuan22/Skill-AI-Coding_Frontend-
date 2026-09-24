# Session lifecycle

States: `CREATED → VALIDATED → RUNNING → CAPTURING → COMPLETED|PARTIAL|FAILED|BLOCKED → CLEANED`.

A session records strategy, start time, base URL, routes, viewports, iteration, owned resources, evidence, structured errors, and cleanup status. On normal completion, interruption, or exception, the runner closes owned page/context/browser resources. It terminates a server only if it started it. Interrupted sessions retain valid captures and mark report/manifest status accurately.
