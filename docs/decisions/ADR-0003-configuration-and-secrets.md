# ADR-0003: Environment-driven, secret-safe configuration

## Decision

Validate typed configuration from environment variables, commit only an example
file, and redact credential-like fields from structured logs.

## Rationale

The project must support later providers and local services without embedding
credentials in source, logs, tests, or frontend bundles.
