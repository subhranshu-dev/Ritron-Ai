# Testing Strategy

## Vision

Every component owns tests that prove its own behavior, while cross-cutting
concerns get a single shared home in [tests/](../tests/README.md). The
strategy scales from Step 01's small API surface up to future agent
evaluations without needing a rewrite.

## Current status: Step 01 API suite

Component tests live with their component — the API foundation's suite is
in `apps/api/tests`:

- **Unit tests** — pure configuration and logging behavior.
- **Integration tests** — application lifecycle and health.
- **End-to-end contract tests** — externally visible error behavior.

## Future: agent evaluations

Once the agent runtime milestone begins, agent evaluations must measure:

1. Correctness
2. Tool selection
3. Hallucination
4. Planning
5. Recovery
6. Safety
7. Latency
8. Cost

These are not implemented before that milestone.

## Steps to add a new test

1. Decide the scope: single component → put it beside that component
   (e.g. `apps/api/tests`); crosses components → use the matching
   boundary in [tests/](../tests/README.md).
2. Write the test against real behavior — no placeholder or empty test
   files.
3. Register it with the matching `pnpm test:*` script so it runs in
   `pnpm check`.
4. For agent evaluations specifically, wait for the agent runtime
   milestone and score against all eight dimensions above, not a subset.
