# Development Guide

Use the tool versions pinned by `package.json`, `pyproject.toml`, and
`rust-toolchain.toml`. Dependency managers have separate responsibilities:
pnpm manages JavaScript tooling, uv manages Python, and Cargo manages Rust.

After installation, run `pnpm check`. Start the local foundation with
`pnpm dev`, then query `/health/live` and `/health/ready`. Future business API
routes will use the `/api/v1` version prefix; operational health routes remain
unversioned.

The API accepts configuration only through `RITRON_API_*` environment variables.
Future global boundaries use the `RITRON_*` prefix. Configuration is validated
at process construction; invalid values fail clearly rather than being ignored.
