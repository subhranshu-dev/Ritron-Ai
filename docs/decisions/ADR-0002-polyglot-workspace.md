# ADR-0002: Native toolchains with pinned versions

## Status

Accepted — in effect since Step 01.

## Context

Native tools support desktop development while keeping Docker optional.
Pinned versions make CI and contributor environments reproducible.

## Decision

Use Node 22/pnpm 10, Python 3.13/uv, and Rust 1.97.1. Root Node scripts
provide a single cross-platform command interface (see
[development.md](../development.md)).

## Consequences

- Contributors install native toolchains directly rather than relying on
  Docker for local development (see
  [ADR-0001](ADR-0001-repository-architecture.md)).
- Version drift is caught early because `package.json`,
  `pyproject.toml`, and `rust-toolchain.toml` are the single source of
  truth for pinned versions.
