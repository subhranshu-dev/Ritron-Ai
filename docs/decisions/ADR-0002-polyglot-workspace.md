# ADR-0002: Native toolchains with pinned versions

## Decision

Use Node 22/pnpm 10, Python 3.13/uv, and Rust 1.97.1. Root Node scripts provide
a single cross-platform command interface.

## Rationale

Native tools support desktop development while keeping Docker optional. Pinned
versions make CI and contributor environments reproducible.
