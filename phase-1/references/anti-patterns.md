# Structural anti-patterns

| Area | Avoid | Structural response |
|---|---|---|
| Navigation | Duplicate or dead-end navigation | Define one source of movement and a return path. |
| Forms | Unrelated field groups; all fields at once; placeholder-only labels | Group by task; establish labels and field necessity. |
| Flows | Unnecessary steps or unmodelled failure | Remove unjustified transitions; model branches and recovery. |
| Page architecture | One page mixes unrelated goals | Split or establish progressive disclosure. |
| Actions | Main action hidden; destructive action easy to trigger | State hierarchy and safeguards. |
| Content | Database structure exposed as page hierarchy | Organize around user goal and decision. |
| Modals | Complex multi-step workflow in a modal | Use an appropriate page or explicit step flow. |
| Tables | Important business actions/columns left implicit | Specify columns, actions, state, search/filter, and pagination needs. |
| Dashboards | Charts added without a decision purpose | Tie each region to awareness, attention, change, or action. |
