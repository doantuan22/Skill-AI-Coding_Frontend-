# Accessibility execution contract

Rendered UI changes that are accessibility relevant require the gate. Reuse the execution request’s base URL, target routes, viewport IDs, iteration, session directory, and server ownership; do not start a duplicate server. Default scan scope is document/root; rule include/exclude must be explicit and exclusions require reasons.

The runner supports initial rendered state only. Auth redirects become `AUTH_REQUIRED`; it does not enter credentials or invent data. Targeted re-scan uses only affected route/viewport/rules; shared-component changes use existing change-impact to select representative pages.
