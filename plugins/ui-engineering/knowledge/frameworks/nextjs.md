# Next.js UI Engineering Knowledge Pack

**Pack ID**: `framework.nextjs`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. App Router vs Pages Router Architecture
- **Respect Detected Router**:
  - If the repository uses `app/`, follow Next.js App Router conventions.
  - If the repository uses `pages/`, follow Next.js Pages Router conventions.
  - **CRITICAL**: Never initiate an unsolicited migration between App Router and Pages Router.
- **App Router UI File Conventions**:
  - `layout.tsx`: Shared UI shell, does not re-render on navigation.
  - `page.tsx`: Unique UI for a route.
  - `loading.tsx`: Instant loading skeleton wrapped in React Suspense.
  - `error.tsx`: Error boundary UI, must be a Client Component (`"use client"`).
  - `not-found.tsx`: 404 UI for the route segment.

## 2. Server vs Client Component Boundaries
- **Server by Default**: In App Router, components are Server Components by default. Keep data-fetching, heavy static rendering, and layout shells on the server.
- **Push `"use client"` to the Leaves**: Only mark components with `"use client"` when they use state (`useState`), effects (`useEffect`), browser APIs, or event handlers (`onClick`, `onChange`).
- **Do not convert parent layouts or pages to `"use client"`** just to handle a single interactive button or modal; extract the interactive element into a dedicated client leaf component.

## 3. Navigation, Images & Fonts
- **Navigation**: Always use `next/link` for internal transitions (`<Link href="...">`) to enable prefetching and client-side transitions.
- **Images**: Use `next/image` with explicit `width`, `height`, and responsive `sizes` attribute or `fill` with parent container positioning to prevent Layout Shift (CLS).
- **Typography & Fonts**: Use `next/font/google` or `next/font/local` with CSS variables (`className={inter.variable}`) to preserve zero-runtime font loading.

## 4. Preservation & Scope
- **Preserve existing layout structure**: Keep root layout providers (`ThemeProvider`, `QueryClientProvider`) intact.
- **Preserve route structure**: Do not alter URL paths, route groups `(group)`, or dynamic segments `[id]` without explicit user permission.
