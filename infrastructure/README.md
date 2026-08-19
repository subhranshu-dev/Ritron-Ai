# Infrastructure

## Vision

This directory will hold every tracked infrastructure artifact RITRON AI
needs to build, run, deploy, and observe itself — but only once each
capability is real. Empty subdirectories are not pre-created, because a
placeholder folder implies an architecture that doesn't exist yet and
misleads contributors.

## Current status

Step 01 requires none of this. CI runs on GitHub Actions directly, and no
Docker container, database, Redis instance, model runtime, or cloud service
is started to build, test, or run the local API. See
[docs/deployment.md](../docs/deployment.md) for the full deployment posture.

## Reserved subdirectories

| Directory     | Will hold                                             | Arrives at |
| -------------- | ------------------------------------------------------ | ---------- |
| `docker/`      | Container definitions for development/server infra.    | When a real server-infrastructure need exists — not a desktop requirement. |
| `ci/`          | CI configuration beyond the default GitHub Actions setup. | When CI needs outgrow inline workflow files. |
| `deployment/`  | Deployment manifests and environment configuration.    | With the Tauri shell / server milestone. |
| `monitoring/`  | Observability and monitoring configuration.             | Once a running service exists to observe. |

## Steps to populate a subdirectory (when its milestone arrives)

1. Confirm the roadmap milestone that requires it is active (check
   [docs/architecture.md](../docs/architecture.md)).
2. Add only the files needed for that milestone's real capability — no
   speculative scaffolding.
3. Document the new capability's purpose in this README, replacing its
   "reserved" row above.
4. Wire any new automation into `pnpm check` or CI so it is enforced, not
   just present.
