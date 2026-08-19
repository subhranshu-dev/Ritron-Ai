# Repository Layout

## Vision

Every top-level directory should have one clear owner and one clear
responsibility, so a contributor can find where new code belongs without
guessing. Future code is added when its roadmap step begins, not
pre-created as empty packages — this prevents false architecture and keeps
ownership meaningful.

## Current layout

| Location          | Responsibility                                                    |
| ------------------ | -------------------------------------------------------------------- |
| `apps/api`          | Python FastAPI core bootstrap and future local service boundary.     |
| `apps/desktop`       | Reserved Tauri/React desktop shell workspace.                        |
| `crates/ritron-foundation` | Rust foundation shared by future native components.           |
| `infrastructure`     | Development container, CI, deployment, and monitoring conventions.   |
| `scripts`            | Cross-platform root command orchestration.                           |
| `tests`              | Cross-cutting test-boundary documentation and future suites.         |
| `docs`               | Guides and architecture documentation (this directory).              |
| `docs/decisions`     | Architecture decision records.                                       |

## Steps to add a new top-level location

1. Check whether the responsibility already fits an existing directory
   above — most new code belongs inside `apps/api`, not at the root.
2. Confirm the roadmap milestone that needs the new location is active
   (see [architecture.md](architecture.md)).
3. Add the directory together with real, working content — never as an
   empty placeholder.
4. Add a row to the table above describing its responsibility in one
   sentence.
5. If the addition changes an architecture boundary, record it as an ADR in
   [docs/decisions/](decisions/).
