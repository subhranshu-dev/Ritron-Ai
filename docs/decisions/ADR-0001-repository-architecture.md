# ADR-0001: Incremental polyglot monorepo

## Status

Accepted — in effect since Step 01.

## Context

RITRON needs coordinated desktop, core, and future service development
without forcing one ecosystem to own another's lockfile or build lifecycle.

## Decision

Use one Git repository with pnpm, uv, and Cargo owning JavaScript, Python,
and Rust dependencies respectively. Add product workspaces only when their
roadmap milestone starts.

## Consequences

- A single repository gives one place for cross-language history and
  review, but requires each ecosystem's tooling to stay independently
  correct (see [ADR-0002](ADR-0002-polyglot-workspace.md)).
- No workspace is pre-created for a future milestone — see
  [repository.md](../repository.md) for the steps to add one when its
  milestone begins.
