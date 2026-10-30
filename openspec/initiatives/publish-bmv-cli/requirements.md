# Requirements

## Product Intent

Coordinate four changes to make cli-finance-py a publishable PyPI package (bmv-cli, command bmv): 1) restructure to src/bmv_cli layout with entry point/LICENSE/README, 2) adopt uv_build backend dropping setuptools, 3) CI quality gates, 4) CD release automation with Release Please + trusted publishing. Includes user-owned manual tasks (PyPI account, trusted publisher registration).

## Accepted Requirements

- Publish to PyPI as distribution name `bmv-cli` (the name `bmv` is taken on PyPI by an unrelated Victron project).
- Expose the CLI command as `bmv` via `[project.scripts] bmv = "bmv_cli.main:app"`.
- Restructure the flat layout (`api/`, `commands/`, root `main.py`) into a single `src/bmv_cli/` package.
- Use the `uv_build` build backend (drop setuptools) once the src layout exists.
- CI runs the four existing quality gates (ruff format, ruff check, mypy, pytest) on every push/PR.
- CD: Release Please generates release PRs (version bump + CHANGELOG) from conventional commits; a tag `v*` triggers build + publish via Trusted Publishing (OIDC, no stored secrets).
- Python floor stays `>=3.12`.
- Go straight to PyPI — no TestPyPI staging workflow.

## Out Of Scope

- Publishing to any registry other than PyPI.
- Widening Python support below 3.12.
- Changes to CLI features, commands, or API behavior.
- Renaming the GitHub repository (optional, user decision — see tasks).
