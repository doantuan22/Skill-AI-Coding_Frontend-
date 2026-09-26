# Developer Tool Domain Design Pack

**Pack ID**: `domain.developer_tool`  
**Domain**: `developer_tool`  
**Version**: `1.0.0`  
**Status**: Stable  
**Aliases**: `devtools`, `cli`, `sdk`, `infra`, `api`, `monitoring`  

---

## 1. User Types & Operational Context
- **Primary Users**: Software engineers, DevOps, SREs, technical architects.
- **Key Psychology**: Information-density driven, keyboard-first, highly pragmatic, impatient with decorative animations, intolerant of concealed technical details.

## 2. Domain Subtopics
- `dense_information`: Log viewers, metrics dashboards, server health grids, execution graphs.
- `code_terminal`: Syntax-highlighted code blocks, CLI terminal emulators, copy-to-clipboard widgets, diff viewers.
- `diagnostics_logs`: Real-time streaming log tables, log level filtering (INFO, WARN, ERROR), stack trace drawers.
- `configuration`: Environment variable editors, YAML/JSON schema validators, webhook settings, API key management.
- `docs_integration`: Side-by-side interactive API explorers, request/response payload sandboxes.

## 3. Critical Flows
1. **API Key Generation & Copy**: Generating key -> one-time reveal modal -> instant copy confirmation -> security guidance.
2. **Log Triage & Diagnosis**: Filtering logs by severity -> expanding stack trace -> copying error context -> navigating to source line.
3. **Environment Configuration**: Editing config keys -> syntax validation check -> diff preview -> safe deployment trigger.

## 4. Information Hierarchy & UX Patterns
- **Information Density**: High density by default. Minimized row padding, compact typography, monospaced fonts for technical data (`font-mono`).
- **Code Snippet Ergonomics**:
  - Always include a persistent or hover-triggered "Copy" button with visual feedback ("Copied!").
  - Multi-language tab switchers (cURL, JavaScript, Python, Go) that remember the developer's language preference across pages.
- **Diff & Status Visuals**: Standardized green (`+`) and red (`-`) background highlights for code and configuration changes.

## 5. Required UI States
- `streaming`: Live log viewer autoscroll indicator with "Pause auto-scroll" toggle.
- `empty`: Code snippet placeholders with sample CLI commands (`curl -X GET ...`) rather than generic empty illustrations.
- `error_diagnostic`: Formatted error messages with expandable raw stack traces and direct links to documentation.
- `masked_secret`: Concealed API secrets (`sk_live_••••••••`) with explicit "Reveal" and "Rotate" actions.

## 6. Responsive & Accessibility Priorities
- **Responsive**: Horizontal scroll with visible scrollbars on wide code blocks and data tables; touch-friendly copy buttons.
- **Accessibility**:
  - Code syntax themes must pass 4.5:1 contrast against the editor background (avoid ultra-dim pastel colors).
  - Terminal output and logs must support keyboard scrolling and screen reader announcements for critical runtime failures.

## 7. Anti-Patterns to Avoid
- **Decorative Slowness**: Adding 400ms transition delays on code block expansion or log tab switching.
- **Truncated Errors without Full Copy**: Cutting off error messages with ellipsis without providing a way to inspect the full stack trace.
- **Missing Copy Feedback**: Providing a copy button that leaves the developer wondering whether the clipboard was updated.

## 8. Workflow Integration & Precedence
- **Greenfield**: Establishes dark/light theme code blocks, high-density data tables, and keyboard command palettes.
- **Existing UI**: Respects existing technical design tokens. Never replace clean utilitarian typography with decorative display fonts.
