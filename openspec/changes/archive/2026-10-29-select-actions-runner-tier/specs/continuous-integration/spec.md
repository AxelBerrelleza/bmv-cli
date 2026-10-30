## MODIFIED Requirements

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
