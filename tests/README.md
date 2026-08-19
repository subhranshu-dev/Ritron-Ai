# Cross-Cutting Test Boundaries

## Vision

Tests that exercise a single component live beside that component — for
example, the API foundation's suite lives in `apps/api/tests`. This
top-level directory is reserved for tests that cross component boundaries,
so that cross-cutting coverage has one obvious home instead of being
scattered or duplicated per component.

## Current status

No subdirectory here is populated yet. A directory is added only together
with a real test suite or a boundary-specific test harness — no placeholder
or empty test directories. See [docs/testing.md](../docs/testing.md) for the
overall testing strategy.

## Reserved boundaries

| Directory      | Covers                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `unit/`        | Pure cross-component behavior.                                                                                                              |
| `integration/` | Interactions between installed services.                                                                                                    |
| `e2e/`         | User-visible flows across process boundaries.                                                                                               |
| `agent-evals/` | Agent correctness, tool selection, hallucination, planning, recovery, safety, latency, and cost — arrives with the agent runtime milestone. |
| `security/`    | Adversarial and security-regression coverage.                                                                                               |

## Steps to add a suite to one of these boundaries

1. Confirm the behavior genuinely crosses component ownership — if it
   belongs to one component, put it in that component's own `tests/`
   directory instead (e.g. `apps/api/tests`).
2. Create the boundary directory only when you're adding its first real
   test file, not in advance.
3. Wire the new suite into the relevant `pnpm test:*` script so it runs in
   the standard quality gate.
4. Keep `agent-evals/` empty until the agent runtime milestone begins;
   metrics defined in [docs/testing.md](../docs/testing.md) apply once it
   does.
