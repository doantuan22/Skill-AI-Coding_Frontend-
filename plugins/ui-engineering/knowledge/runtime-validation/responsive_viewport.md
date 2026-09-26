# Responsive Viewport Validation Knowledge

**Knowledge ID**: `runtime.responsive_viewport`  
**Category**: `runtime`  
**Priority**: `medium`  
**Status**: Active  

---

## 1. Viewport Matrix
Verify the UI layout against standard responsive viewports:
- Mobile: `375 x 812` (iPhone X/12)
- Tablet: `768 x 1024` (iPad Portrait)
- Desktop: `1440 x 900` (MacBook Standard)
- Ultrawide: `1920 x 1080` (FHD Monitor)

## 2. Validation Checks
- **No Horizontal Scroll**: Ensure `window.innerWidth >= document.documentElement.scrollWidth`.
- **Text Wrapping**: Confirm text does not clip or overflow container boundaries.
- **Touch Target Size**: Interactive targets must be at least `44x44px` on mobile screens.
- **Stacking Behavior**: Verify multi-column layouts gracefully collapse into single columns on mobile.
