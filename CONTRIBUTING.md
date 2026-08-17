# Contributing to RITRON AI

RITRON is currently private and accepts changes through reviewed pull requests.

1. Install the pinned tools described in the README.
2. Create a focused branch from `main`.
3. Keep changes within the active roadmap milestone.
4. Run `pnpm check` before opening a pull request.
5. Describe behavior, validation, and any configuration impact in the pull request.

Install local hooks after dependencies are available:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Do not commit secrets, generated artifacts, local databases, or lockfile changes
that were not produced by an intentional dependency update. Do not introduce a
provider SDK outside the future Model Gateway boundary.
