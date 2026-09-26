# Angular UI Engineering Knowledge Pack

**Pack ID**: `framework.angular`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Component Architecture & Templates
- **Standalone Components**: Follow modern Angular standalone component conventions (`standalone: true`, explicit `imports: [...]`) when present in the repo, or NgModule structure if legacy.
- **Control Flow**: Use modern `@if`, `@for`, `@switch` block syntax when Angular 17+ is detected, otherwise `*ngIf`, `*ngFor`.
- **Forms**: Use Reactive Forms (`FormGroup`, `FormControl`, `formControlName`) for complex validated inputs, ensuring validation feedback is accessible.

## 2. Preservation & Project Architecture
- **Preserve CLI & Module Structure**: Keep component selector prefixes (`app-*`) and file organization (`component.ts`, `component.html`, `component.scss`).
- **No Unsolicited Architecture Rewrites**: Do not convert legacy NgModules to standalone components unless explicitly instructed by the user.
