# Desktop Application (Reserved)

## Vision

RITRON AI's desktop shell will be a Tauri 2 application with a Rust backend
and a React/TypeScript frontend, giving users a native, local-first UI over
the agentic core. It is planned as **Step 12** on the roadmap and is
intentionally not implemented in Step 01.

## Current status

This directory is a reservation only. No Tauri, Rust, React, or TypeScript
application code exists here yet. Building it out now, ahead of its
milestone, would create a false architecture that Step 01 explicitly avoids
(see [docs/repository.md](../../docs/repository.md)).

## Constraints for when this milestone begins

1. Keep provider credentials and other secrets outside frontend bundles —
   nothing sent to a browser/webview process may hold a raw API key.
2. Communicate with the local core only through documented adapters, never
   by reaching into core internals directly from the UI layer.
3. Isolate platform-specific capabilities (filesystem, notifications, OS
   integrations) behind native adapters so the core stays cross-platform.
4. Follow the dependency rule in the root [README.md](../../README.md): no
   subsystem outside the future Model Gateway may depend directly on a
   model provider SDK.

## Steps to begin this milestone

1. Confirm Step 12 is active on the roadmap in
   [docs/architecture.md](../../docs/architecture.md).
2. Scaffold the Tauri 2 project inside this directory, pinning Rust,
   Node, and pnpm versions consistent with the rest of the repo.
3. Wire the desktop `pnpm` scripts into the root quality gate (`pnpm
check`, `pnpm lint`, `pnpm test`) rather than introducing a parallel
   toolchain.
4. Replace this README with real setup and architecture documentation for
   the shipped shell.
