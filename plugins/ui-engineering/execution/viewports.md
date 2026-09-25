# Viewport registry

```yaml
desktop_wide:
  width: 1440
  height: 900
desktop:
  width: 1280
  height: 800
tablet:
  width: 768
  height: 1024
mobile:
  width: 375
  height: 812
```

Normal verification uses `desktop` and `mobile`. Final verification normally uses all four IDs. A task/product may override values in its execution report, but workflows should refer to semantic IDs rather than scattering raw dimensions.
