# ADR-0004: Linux CI quality gate first

## Decision

Run formatting, linting, type checking, builds, tests, audits, secret scanning,
and API health smoke tests on Linux GitHub Actions.

## Rationale

Linux gives meaningful, cost-effective validation before a desktop shell exists.
Cross-platform packaging validation starts when Tauri is introduced.
