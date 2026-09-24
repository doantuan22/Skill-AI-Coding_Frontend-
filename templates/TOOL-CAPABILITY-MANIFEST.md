# Tool Capability Manifest

```yaml
runtime:
  node: {status: UNKNOWN, version: null, confidence: unknown}
  python: {status: UNKNOWN, version: null, confidence: unknown}
package_manager: {detected: null, command: null, confidence: unknown}
project:
  framework: {value: null, confidence: unknown}
  dev_command: null
  build_command: null
  test_command: null
browser: {status: UNKNOWN, strategy: null, confidence: unknown}
playwright:
  package_present: {status: UNKNOWN, confidence: unknown}
  config_present: {status: UNKNOWN, confidence: unknown}
  browser_ready: {status: UNKNOWN, confidence: unknown}
application:
  known_url: null
  already_running: {status: UNKNOWN, confidence: unknown}
execution_strategy: null
limitations: []
```

_Persist only for complex work or execution debugging. Detection is read-only._

