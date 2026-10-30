# continuous-integration Specification

## Purpose
TBD - created by archiving change ci-quality-gates. Update Purpose after archive.
## Requirements
### Requirement: CI runs on every push and pull request

The repository SHALL have a GitHub Actions workflow (`.github/workflows/ci.yml`) triggered on `push` (all branches) and `pull_request` events, with workflow-level permissions limited to `contents: read`.

#### Scenario: Workflow triggers on a new branch push

- **WHEN** any branch is pushed to GitHub
- **THEN** the CI workflow runs on that branch's HEAD commit

#### Scenario: Workflow triggers on pull requests

- **WHEN** a pull request is opened or updated against `main`
- **THEN** the CI workflow runs against the pull request's merge state

#### Scenario: Least-privilege permissions

- **WHEN** the workflow file is inspected
- **THEN** it declares `permissions: contents: read` (or stricter) and references no secrets

### Requirement: All four quality gates run in CI

The CI workflow SHALL execute, in order, the four project quality gates exactly as documented in AGENTS.md: `uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy src/bmv_cli/api src/bmv_cli/commands`, and `uv run pytest`. The job SHALL fail if any gate exits non-zero.

#### Scenario: Green run on a healthy commit

- **WHEN** CI runs on a commit where all gates pass locally
- **THEN** the workflow job completes successfully (all four steps green)

#### Scenario: Failing gate fails the job

- **WHEN** a pushed commit introduces a lint or test failure
- **THEN** the workflow job fails at the first failing gate (format/lint failing before mypy/pytest) and the commit shows a red status check

### Requirement: Pinned, reproducible toolchain

CI SHALL install a specific pinned uv version via `astral-sh/setup-uv` (action referenced by SHA with a version comment, uv `version:` pinned) and SHALL set up Python by respecting the repository's `.python-version` pin, followed by `uv sync --extra dev`. Additionally, every Linux job across all repository workflows (`ci.yml`, `publish.yml`, `release-please.yml`) SHALL run on a pinned GitHub-hosted runner tier (`runs-on: ubuntu-24.04`) rather than the `ubuntu-latest` floating label, so the OS version executing the jobs cannot change silently. The remaining `ubuntu-slim`, `ubuntu-26.04`, and arm64 tiers are explicitly evaluated alternatives; `ubuntu-slim` MAY be used by genuinely lightweight automation jobs (e.g. scheduled lints, issue operations), but MUST NOT be the default tier for gates or publish jobs because its 15-minute job ceiling and unprivileged container model are standing constraints. OS upgrades (e.g. to `ubuntu-26.04`) SHALL be deliberate, reviewed workflow changes.

#### Scenario: Runner tier is pinned

- **WHEN** any of the repository's workflow files is inspected
- **THEN** each Linux job's `runs-on` is `ubuntu-24.04` (not `ubuntu-latest`), matching the documented runner policy

#### Scenario: Silent OS migration is excluded

- **WHEN** GitHub repoints the `ubuntu-latest` label to a newer OS version (e.g. 26.04 in November 2026)
- **THEN** the repository's CI environment is unaffected because no workflow uses the floating label

#### Scenario: Toolchain is pinned

- **WHEN** the workflow file is inspected
- **THEN** `astral-sh/setup-uv` is pinned to a SHA and a `version:` of uv is specified, and Python setup honors `.python-version` (3.12)

#### Scenario: Environment is synced before gates

- **WHEN** the job executes
- **THEN** `uv sync --extra dev` runs successfully before the gate steps, installing the project (`bmv-cli`) and dev dependencies

### Requirement: No secrets or real API access in CI

The CI workflow SHALL NOT require `BMV_API_TOKEN` or any other secret; all tests SHALL pass using the existing requests-mock fixtures, keeping the workflow fully public-repo compatible.

#### Scenario: Green run without any token

- **WHEN** the CI workflow runs on the public repository with no secrets configured
- **THEN** `uv run pytest` passes (API calls are mocked via fixtures and requests-mock)

