# Existing UI Preservation Invariants & Change Budget

**Knowledge ID**: `preservation.existing_ui_invariants`  
**Category**: `preservation`  
**Priority**: `critical`  
**Status**: Active  

---

## 1. Baseline Invariants (Default Locked/Protected)
In any Existing UI workflow, the following invariants are locked by default:
1. **Color Palette (`color_palette: locked`)**: Primary, secondary, accent, and neutral token values cannot be altered without explicit user permission.
2. **Brand Identity (`brand_identity: locked`)**: Logos, brand typographies, and distinctive theme motifs are locked.
3. **Overall Layout Identity (`overall_layout_identity: protected`)**: Root app shells, header/sidebar navigation models, and global page structures cannot be replaced.
4. **Information Architecture (`information_architecture: protected`)**: Route paths, page inventory, and main content hierarchies cannot be deleted or re-routed.

## 2. Granular Change Budget (L1 / L2 / L3)
- **L1 (Safe Refinement)**: Spacing, responsive adjustments, typography scale tweaks, state handling, micro-interactions, accessibility contrast fixes. Default: **Allowed**.
- **L2 (Local Structural Changes)**: Re-grouping form fields, card internal composition, local tabbed layout. Default: **Requires Justification Trace** (`change_reason`).
- **L3 (Major Redesign / Rebuild)**: Complete site recoloring, changing app navigation, re-architecting global pages. Default: **Requires Explicit User Permission Trace** (`permission_trace`).

## 3. Precedence Hierarchy
When instructions or inspirations conflict:
1. Explicit user instructions (highest precedence within granted scope).
2. Existing brand identity.
3. Existing design system tokens.
4. Existing UX & information architecture.
5. Repository / framework constraints.
6. Domain best practices.
7. Design inspiration (cannot override brand identity or locked palette).
8. AI default preferences.
