## Why

The project has four local quality gates (ruff format check, ruff check, mypy, pytest) that protect main only by developer discipline — nothing runs automatically. Every change in this initiative touches code or config that must stay green, and CD (change 4) will gate releases on these same checks. A CI workflow on push/PR is the safety net that makes the whole pipeline trustworthy.

## What Changes

- **Add `.github/workflows/ci.yml`** triggered on `push` (all branches) and `pull_request`:
  - Check out code (action pinned by SHA + version comment, per GitHub security best practice)
  - Install uv via `astral-sh/setup-uv` (pinned version + SHA)
  - Set up Python from `.python-version` (respecting the project pin)
  - `uv sync --extra dev`
  - Run the four gates in order: `uv run ruff format --check .` → `uv run ruff check .` → `uv run mypy src/bmv_cli/api src/bmv_cli/commands` → `uv run pytest`
- **Least-privilege permissions** (`contents: read` only; no write scopes).
- **Job-level step ordering matters**: fail fast — format/lint before mypy/pytest.

## Capabilities

### New Capabilities
- `continuous-integration`: Automated execution of the four project quality gates on every push and pull request, with a pinned uv toolchain and least-privilege permissions.

### Modified Capabilities
<!-- None — no spec-level behavior of the CLI changes; this is pure pipeline infrastructure. -->

## Impact

- **New files only**: `.github/workflows/ci.yml` (+ possibly a CI note in AGENTS.md's Quality Gates section).
- **Runtime**: GitHub-hosted `ubuntu-latest` runner; zero secrets required; the `BMV_API_TOKEN`-dependent code paths are covered by mocked tests (requests-mock), so no secret handling in CI.
- Downstream: change 4's release path assumes green CI on `main`.
- Requires the restructure change to be applied first (gates run against `src/bmv_cli/…` paths).
