# Browser execution layer

This layer turns Phase 2 visual QA into an agent-agnostic execution request. It separates read-only capability detection, execution contracts, optional [Playwright runtime](runtime/README.md), local [evidence storage](storage/README.md), and evaluation. It never installs tooling, edits project configuration, downloads browsers, or assumes Playwright.

Load [capability-detection.md](capability-detection.md), [execution-requirement.md](execution-requirement.md), and [execution-router.md](execution-router.md) first. Then load runtime, browser, viewport, evidence, and adapter contracts only for the selected strategy. Execution supports render/navigation/inspection/capture—not a complete end-to-end test framework.
