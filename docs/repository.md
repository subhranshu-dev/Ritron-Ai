# Repository Layout

| Location         | Responsibility                                                     |
| ---------------- | ------------------------------------------------------------------ |
| `apps/api`       | Python FastAPI core bootstrap and future local service boundary.   |
| `apps/desktop`   | Reserved Tauri/React desktop shell workspace.                      |
| `infrastructure` | Development container, CI, deployment, and monitoring conventions. |
| `scripts`        | Cross-platform root command orchestration.                         |
| `tests`          | Future cross-cutting test-boundary documentation.                  |
| `docs/decisions` | Architecture decision records.                                     |

Future code is added when its roadmap step begins, not pre-created as empty
packages. This prevents false architecture and keeps ownership meaningful.
