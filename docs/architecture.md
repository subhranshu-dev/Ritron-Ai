# Architecture Foundation

Step 01 defines repository boundaries, not product implementations.

```text
Desktop (Step 12)
        ↓
UI (Step 13)
        ↓
Core API foundation (Step 01)
        ↓
Model Gateway | Agent Runtime | Tool Runtime (later milestones)
        ↓
Context / Memory / Knowledge (later milestones)
        ↓
Local storage / optional cloud (later milestones)
```

The current API owns configuration, HTTP conventions, request correlation,
health, safe errors, logging, and lifecycle. It must not acquire business
routes before their milestone. Future subsystem contracts are introduced in
Step 02; implementations follow the roadmap.

RITRON is provider-agnostic, local-first, and cross-platform. Cloud services
are optional; platform APIs are isolated in native adapters.
