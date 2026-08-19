# ADR-0003: Environment-driven, secret-safe configuration

## Status

Accepted — in effect since Step 01.

## Context

The project must support later providers and local services without
embedding credentials in source, logs, tests, or frontend bundles.

## Decision

Validate typed configuration from environment variables, commit only an
example file (`.env.example`), and redact credential-like fields from
structured logs.

## Consequences

- Configuration is validated at process construction — invalid values fail
  clearly rather than being ignored (see [development.md](../development.md)).
- `.env` is never committed; only `.env.example` is tracked.
- Future desktop code must keep this same guarantee — no provider
  credential may reach a frontend bundle (see
  [apps/desktop/README.md](../../apps/desktop/README.md)).
