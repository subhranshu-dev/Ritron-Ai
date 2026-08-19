# Architecture

## Vision

RITRON AI is layered so that each capability is only introduced once the
layer beneath it is solid. Step 01 defines repository boundaries, not
product implementations — the goal is a foundation that later milestones can
build on without rework, not a scaffold of empty packages.

## Current status: Step 01 — Core API foundation

```text
Desktop (Step 12)
        ↓
UI (Step 13)
        ↓
Core API foundation (Step 01)   <-- we are here
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

## Guiding principles

1. RITRON is provider-agnostic — no subsystem outside the future Model
   Gateway may depend directly on a model provider SDK.
2. RITRON is local-first — core operation must remain possible without
   cloud connectivity; cloud services are optional.
3. RITRON is cross-platform — platform-specific APIs are isolated behind
   native adapters, never called directly from shared code.

## Steps to introduce a new layer

1. Confirm the milestone is next on the roadmap — do not build ahead of
   sequence, even if the code would be simple.
2. Define the subsystem's contract in this document before writing its
   implementation, so the boundary is reviewed independently of the code.
3. Implement only inside the owning directory (see
   [repository.md](repository.md)) — do not let a new layer reach into
   another layer's internals.
4. Record the decision behind any non-obvious boundary choice as a new ADR
   in [docs/decisions/](decisions/).
5. Update the layer diagram above once the milestone lands.
