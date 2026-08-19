# RITRON AI

## Vision

RITRON AI is a local-first, desktop-native personal agentic AI environment.
It is designed to run a user's agents, memory, tools, and knowledge on their
own machine first, treating cloud services as an optional extension rather
than a dependency. The project is built in numbered milestones, and this
repository currently implements only **Step 01: the engineering foundation**.

Step 01 does **not** include the Model Gateway, agents, memory, tools, or the
desktop product. It exists to prove out configuration, HTTP conventions,
health checks, logging, and the cross-language toolchain before any product
surface is built on top of it.

## Current status

The only running capability is a deliberately small Python API bootstrap:

- `GET /health/live`
- `GET /health/ready`

All later product capabilities remain gated behind their corresponding
roadmap milestones. See [docs/architecture.md](docs/architecture.md) for the
full milestone chain.

## Step 1 — Install prerequisites

- Git
- Node 22 LTS and Corepack
- pnpm 10.18.3 (activated by Corepack)
- uv and Python 3.13
- Rust 1.97.1 with `clippy` and `rustfmt`

Install uv and Rust using their official installers.

## Step 2 — Activate toolchains

```bash
corepack enable
corepack prepare pnpm@10.18.3 --activate
uv python install 3.13
rustup toolchain install 1.97.1 --component clippy,rustfmt
```

## Step 3 — Install dependencies

```bash
pnpm install --frozen-lockfile
uv sync --frozen --all-groups
```

`pnpm install --frozen-lockfile` is the installation command. It is not a
package script because package-manager lifecycle scripts must stay explicit.

## Step 4 — Configure environment (optional)

Copy `.env.example` to `.env` only when local overrides are needed. Never
commit `.env`; it may contain secrets in future milestones.

## Step 5 — Run and verify

```bash
pnpm dev     # start the local API on 127.0.0.1:8000
pnpm check   # run the complete local quality gate before committing
```

## Common commands

| Command                 | Purpose                                                |
| ----------------------- | ------------------------------------------------------ |
| `pnpm dev`              | Start the local API on `127.0.0.1:8000`.               |
| `pnpm build`            | Validate TypeScript and build the Python distribution. |
| `pnpm test`             | Run all API tests.                                     |
| `pnpm test:unit`        | Run unit tests.                                        |
| `pnpm test:integration` | Run integration tests.                                 |
| `pnpm test:e2e`         | Run public API contract tests.                         |
| `pnpm lint`             | Run JavaScript, Python, and Rust linters.              |
| `pnpm format`           | Format supported source files.                         |
| `pnpm format:check`     | Verify formatting without changing files.              |
| `pnpm typecheck`        | Run TypeScript and Python type checks.                 |
| `pnpm check`            | Run the complete local quality gate.                   |
| `pnpm clean`            | Remove local build and test artifacts.                 |

## Architecture boundaries

- `apps/api` owns the local core bootstrap and future HTTP/service boundaries.
- `apps/desktop` is reserved for the Step 12 Tauri shell.
- `crates/ritron-foundation` holds the Rust foundation shared by future
  native components.
- Future Core, Model Gateway, Agents, Tools, Memory, Knowledge, Security,
  MCP, Automation, Cloud, and inference components are introduced only at
  their roadmap milestones — not pre-created as empty packages.
- No subsystem outside the future Model Gateway may depend directly on a
  model provider SDK.
- Local data and core operation must remain possible without cloud
  connectivity.
- Platform-specific behavior belongs behind native adapters.

## Where to go next

- [docs/development.md](docs/development.md) — toolchain conventions and
  configuration rules; read before contributing.
- [docs/architecture.md](docs/architecture.md) — the current milestone chain
  and subsystem boundaries.
- [docs/repository.md](docs/repository.md) — what each top-level directory
  is responsible for.
- [docs/testing.md](docs/testing.md) — how the test suites are organized.
- [docs/deployment.md](docs/deployment.md) — deployment posture for this
  step.
- [docs/decisions/](docs/decisions/) — architecture decision records.
