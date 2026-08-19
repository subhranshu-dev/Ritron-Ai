# Deployment

## Vision

RITRON AI must stay easy to run locally and cheap to validate in CI at every
step, without forcing infrastructure that later milestones don't need yet.
Deployment complexity is added only when a real target — a server, a
packaged desktop app — exists to deploy.

## Current status: Step 01

- Docker is a future development/server-infrastructure option, not a
  desktop installation requirement.
- No database, Redis, model runtime, or cloud service is started by
  Step 01.
- CI validates the foundation on Linux only.
- Desktop packaging and OS matrix validation begin with the Tauri shell
  milestone (Step 12).

## Steps to extend deployment for a new milestone

1. Confirm the milestone genuinely needs new infrastructure — check
   [architecture.md](architecture.md) before adding anything.
2. Add configuration under `infrastructure/` following its
   [README](../infrastructure/README.md), not ad hoc at the root.
3. Extend CI incrementally: keep Linux validation passing before adding a
   new OS or platform target.
4. Document the new deployment shape here, replacing the relevant bullet
   under "Current status."
5. Record any non-obvious infrastructure choice as an ADR in
   [docs/decisions/](decisions/).
