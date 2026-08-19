# RITRON AI

RITRON AI is a local-first, desktop-native personal agentic AI environment.
This repository currently contains **Step 01: the engineering foundation**—not
the Model Gateway, agents, memory, tools, or desktop product.

## Status

The only running capability is a deliberately small Python API bootstrap:

- `GET /health/live`
- `GET /health/ready`

All later product capabilities remain gated by their corresponding milestones.

## Prerequisites

- Git
- Node 22 LTS and Corepack
- pnpm 10.18.3 (activated by Corepack)
- uv and Python 3.13
- Rust 1.97.1 with `clippy` and `rustfmt`

Install uv and Rust using their official installers, then activate pnpm:

```bash
corepack enable
corepack prepare pnpm@10.18.3 --activate
uv python install 3.13
rustup toolchain install 1.97.1 --component clippy,rustfmt
pnpm install --frozen-lockfile
uv sync --frozen --all-groups
```

Copy `.env.example` to `.env` only when local overrides are needed. Never
commit `.env`; it may contain secrets in future milestones.

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

`pnpm install --frozen-lockfile` is the installation command. It is not a
package script because package-manager lifecycle scripts must stay explicit.

## Architecture boundaries

`apps/api` owns the local core bootstrap and future HTTP/service boundaries.
`apps/desktop` is reserved for the Step 12 Tauri shell. Future Core, Model
Gateway, Agents, Tools, Memory, Knowledge, Security, MCP, Automation, Cloud,
and inference components will be introduced only at their roadmap milestones.

No subsystem outside the future Model Gateway may depend directly on a model
provider SDK. Local data and core operation must remain possible without cloud
connectivity. Platform-specific behavior belongs behind native adapters.

Read [the development guide](docs/development.md) before contributing and
[the architecture guide](docs/architecture.md) for the current boundaries.
