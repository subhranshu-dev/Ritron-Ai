# Development Guide

## Vision

Contributing to RITRON AI should feel the same regardless of which
language you're touching — one set of pinned tool versions, one root
command interface, and one validated configuration convention across
Python, Rust, and TypeScript.

## Step 1 — Use the pinned tool versions

Use the tool versions pinned by `package.json`, `pyproject.toml`, and
`rust-toolchain.toml`. Dependency managers have separate responsibilities:

- **pnpm** manages JavaScript tooling.
- **uv** manages Python.
- **Cargo** manages Rust.

## Step 2 — Validate your setup

```bash
pnpm check
```

## Step 3 — Run the foundation locally

```bash
pnpm dev
```

Then query:

- `GET /health/live`
- `GET /health/ready`

Future business API routes will use the `/api/v1` version prefix;
operational health routes remain unversioned.

## Step 4 — Configure through environment variables only

The API accepts configuration only through `RITRON_API_*` environment
variables. Future global boundaries use the `RITRON_*` prefix.
Configuration is validated at process construction; invalid values fail
clearly rather than being ignored.

## Step 5 — Before opening a PR

1. Run `pnpm check` and confirm it passes.
2. Confirm no `.env` or credential-like value is staged for commit.
3. If your change alters an architecture boundary, add or update an ADR in
   [docs/decisions/](decisions/) rather than only updating code comments.
4. Confirm your change matches the current roadmap step in
   [architecture.md](architecture.md) — do not implement ahead of
   milestone.
