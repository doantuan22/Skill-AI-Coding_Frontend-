# Change impact analysis

Before changing a requirement, flow, page, lock, design system, or other important artifact, record:

1. What changed and why?
2. Which active/locked artifacts depend on it?
3. Which phase owns the change?
4. Does the active Structure Lock become invalid?
5. Which review and quality gate must rerun?

Use this dependency order: requirement → actors/use cases → IA/navigation/flows → page specs/components/states/wireframes → Structure Lock → direction/system/tokens/components/implementation → reviews. An impacted downstream artifact becomes `NEEDS_REVIEW`; it becomes `STALE` when its dependency is superseded/invalid and cannot safely be reused. Do not activate downstream work until required upstream dependencies are valid.
