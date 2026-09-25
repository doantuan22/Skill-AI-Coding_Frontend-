# Feedback states

For important interactions, identify default, loading, empty, error, success, disabled, partial, permission-denied, no-match, and cancellation states as relevant. Each state needs a trigger, meaning, allowed action, and recovery/next path.

An empty state is not an error; a permission-denied state is not a missing-data state. Keep these distinctions in `STATE-MAP.md` and linked flows.
