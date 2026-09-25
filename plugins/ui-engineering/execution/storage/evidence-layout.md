# Evidence layout

Default evidence root is `<project>/.evidence/`; a request may choose another directory only within project root. Session IDs and page IDs are sanitized to avoid traversal. Screenshots live under `pages/` and use `PAGE-ID__viewport__iter-NN.png`; optional console evidence lives under `logs/`.

The runner never writes screenshots into application source files or mixes them with project Playwright test output. `.evidence/` is normally a local artifact; projects may add it to `.gitignore` by their own policy—the runner does not edit `.gitignore`.
