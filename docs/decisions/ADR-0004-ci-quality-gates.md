# ADR-0004: Linux CI quality gate first

## Status

Accepted — in effect since Step 01.

## Context

Linux gives meaningful, cost-effective validation before a desktop shell
exists. Cross-platform packaging validation starts when Tauri is
introduced.

## Decision

Run formatting, linting, type checking, builds, tests, audits, secret
scanning, and API health smoke tests on Linux GitHub Actions.

## Consequences

- `pnpm check` mirrors the CI gate locally, so failures surface before a
  push (see [development.md](../development.md)).
- Cross-platform (macOS/Windows) validation is deliberately out of scope
  until the Tauri shell milestone (see
  [apps/desktop/README.md](../../apps/desktop/README.md) and
  [deployment.md](../deployment.md)).
