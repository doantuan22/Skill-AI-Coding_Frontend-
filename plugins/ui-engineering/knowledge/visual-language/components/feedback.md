# Feedback grammar

Choose feedback by scope, persistence and recoverability.

| Pattern | Use when | Avoid when |
|---|---|---|
| inline validation | error/action belongs to a field | global result or unrelated field |
| local feedback | outcome belongs to a nearby control/section | user may navigate away before seeing it |
| toast | brief, non-blocking outcome with no immediate decision | critical error, field correction or durable status |
| alert/banner | persistent page/system condition affects next actions | a transient success message |
| status panel | data view has loading/empty/error/permission state | simple confirmation |
| dialog | a decision, acknowledgement or recovery must block progress | routine success or passive information |

Every message states what happened, impact and next action when one exists. Pair semantic color with text/icon; manage announcement and focus through accessibility guidance.

