# Vue UI Engineering Knowledge Pack

**Pack ID**: `framework.vue`  
**Category**: `framework`  
**Version**: `1.0.0`  
**Status**: Active  

---

## 1. Single File Component (SFC) Discipline
- **Structure**: Maintain standard order `<script setup lang="ts">`, `<template>`, `<style scoped>`.
- **Composition API**: Use `<script setup>` with `ref`, `computed`, and `watch` for modern reactive UI logic.
- **Props & Emits**:
  - Declare typed props with `defineProps<{ modelValue: string; disabled?: boolean }>()`.
  - Declare typed emits with `defineEmits<{ (e: 'update:modelValue', value: string): void }>()`.
  - Use `v-model` bindings for reusable form controls.

## 2. Slots & Reusable UI Composition
- **Named & Scoped Slots**: Use `<slot name="header" />` and `<slot :item="item" />` to give consumers layout and rendering flexibility without prop drilling.
- **Template Cleanliness**: Keep templates focused on UI markup; extract complex logic into `computed` properties.

## 3. Preservation & Styling
- **Scoped Styles**: Prefer `<style scoped>` or Tailwind utility classes to avoid leaking styles to parent or child components.
- **Preserve Existing Component Architecture**: Keep existing Vue component folder hierarchy (`src/components/`).
