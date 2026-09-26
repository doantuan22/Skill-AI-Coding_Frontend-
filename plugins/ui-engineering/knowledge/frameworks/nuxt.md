# Nuxt UI Engineering Knowledge Pack

**Pack ID**: `framework.nuxt`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Directory Structure & Conventions
- **Routing**: Respect file-system routing in `pages/` (e.g. `pages/index.vue`, `pages/dashboard.vue`).
- **Layouts**: Use `layouts/default.vue` with `<slot />` or named layouts referenced via `definePageMeta({ layout: 'admin' })`.
- **Auto-Imports**: Rely on Nuxt's auto-imported composables (`useRoute`, `useRouter`, `useFetch`, `useState`) and components without redundant manual imports.

## 2. Navigation & Media
- **Navigation**: Always use `<NuxtLink to="...">` for internal routing to gain prefetching and accessibility advantages.
- **Images**: Use `@nuxt/image` (`<NuxtImg>` / `<NuxtPicture>`) if installed, or standard semantic responsive `<img>` with proper dimensions.

## 3. Preservation & Boundary Rules
- **Preserve route architecture**: Do not change page file names or route parameters without explicit instruction.
- **Preserve Nuxt configuration**: Maintain existing modules and configuration in `nuxt.config.ts`.
