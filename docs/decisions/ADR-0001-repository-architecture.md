# ADR-0001: Incremental polyglot monorepo

## Decision

Use one Git repository with pnpm, uv, and Cargo owning JavaScript, Python, and
Rust dependencies respectively. Add product workspaces only when their roadmap
milestone starts.

## Rationale

RITRON needs coordinated desktop, core, and future service development without
forcing one ecosystem to own another’s lockfile or build lifecycle.
