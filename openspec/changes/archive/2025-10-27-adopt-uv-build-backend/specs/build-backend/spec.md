## ADDED Requirements

### Requirement: Build backend is uv_build

`[build-system]` SHALL use `build-backend = "uv_build"` with `requires = ["uv_build>=0.13.6,<0.14"]` (pinned with an upper bound per uv's versioning policy), and no `[tool.setuptools.*]` build configuration SHALL remain.

#### Scenario: pyproject declares uv_build with no legacy build config

- **WHEN** `pyproject.toml` is inspected after the change
- **THEN** `[build-system]` shows `uv_build` with a version range (lower and upper bound) and there is no `[tool.setuptools…]` section

#### Scenario: Zero build configuration for default layout

- **WHEN** `uv build` runs with only the default `src/bmv_cli/` structure (no `tool.uv.build-backend` options)
- **THEN** the build succeeds by auto-discovering the module — no build-specific configuration file or section is required

### Requirement: Canonical release build command

The project SHALL use `uv build --no-sources` as the canonical command for producing release distributions, and it SHALL output both a source distribution and a wheel to `dist/`.

#### Scenario: uv build produces sdist and wheel

- **WHEN** `uv build --no-sources` is executed from the repository root
- **THEN** `dist/` contains both `bmv_cli-<version>.tar.gz` (sdist) and `bmv_cli-<version>-py3-none-any.whl` (wheel) for the current project version

#### Scenario: Built wheel is installable and functional

- **WHEN** the wheel from `dist/` is installed into a clean virtual environment and `bmv --help` is executed
- **THEN** installation succeeds and the `bmv` command lists all subcommands

### Requirement: Backend pin maintenance documented

AGENTS.md SHALL document that `uv_build`'s upper bound must be raised when uv releases a new major version, as part of the project's build/backend guidance.

#### Scenario: Maintenance rule present in docs

- **WHEN** AGENTS.md is read after the change
- **THEN** it contains a note to bump the `uv_build` pin upper bound when uv's major version changes

### Requirement: Quality gates unaffected by backend swap

The four quality gates SHALL pass identically before and after the swap (no code changes are part of this change).

#### Scenario: Gates green with new backend

- **WHEN** the four gates (`uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy src/bmv_cli/api src/bmv_cli/commands`, `uv run pytest`) run after the swap
- **THEN** all four exit 0 with no changes to any source file
