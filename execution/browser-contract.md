# Browser adapter contract

The core contract is API-neutral. A selected adapter supports the applicable operations:

```text
open(url)
navigate(route)
set_viewport(width, height)
wait_ready()
capture()
inspect_basic_state()
close()
```

`inspect_basic_state()` checks route reached, non-blank root/main content, target UI presence, and obvious fatal render state. A route/render failure is a `BLOCKER`; do not continue visual-polish evaluation. Adapters may collect console observations when available, but the core does not depend on a console API.

Execution defaults to read/render/navigate. Safe interactions may open menus, modals, tabs, or sections for needed state evidence. Do not trigger destructive/external side effects, payment, cancellation, deletion, or submission unless an explicit scenario authorizes it.
