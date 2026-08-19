# Test Boundaries

Tests that exercise a component live beside that component. The API foundation
uses `apps/api/tests`. This top-level directory reserves the cross-cutting
boundaries that later milestones will populate:

- `unit/`: pure cross-component behavior.
- `integration/`: interactions between installed services.
- `e2e/`: user-visible flows across process boundaries.
- `agent-evals/`: agent correctness, safety, recovery, latency, and cost.
- `security/`: adversarial and security-regression coverage.

No placeholder tests are stored here. A directory is added only with a real
test suite or a boundary-specific test harness.
