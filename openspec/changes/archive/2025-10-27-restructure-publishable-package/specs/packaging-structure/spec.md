## ADDED Requirements

### Requirement: Single src-layout package

The repository SHALL contain exactly one top-level Python package, `bmv_cli`, located at `src/bmv_cli/`, holding the `api` and `commands` modules and the CLI `main.py`. The flat top-level `api/` and `commands/` directories and the root `main.py` SHALL NOT remain after the change.

#### Scenario: Package import works after restructure

- **WHEN** the environment is synced (`uv sync --extra dev`) and `import bmv_cli.commands.price` / `import bmv_cli.api` are executed
- **THEN** both imports succeed and no module outside `src/bmv_cli/` is required for them

#### Scenario: No flat leftovers at repo root

- **WHEN** the repository root is inspected after the change
- **THEN** there is no `api/`, `commands/`, `main.py`, `bmv/`, `requirements.txt`, or `bmv.egg-info/` at the root — package code lives only under `src/bmv_cli/`

### Requirement: Console entry point `bmv`

The package SHALL declare `[project.scripts] bmv = "bmv_cli.main:app"` so that installing the distribution provides a `bmv` shell command.

#### Scenario: CLI is runnable after sync

- **WHEN** `uv sync` completes and `bmv --help` is executed in the project environment (e.g. via `uv run bmv --help`)
- **THEN** the command exits 0 and lists the existing subcommands (price, currencies, credits, search, dividend, hello)

#### Scenario: CLI behavior is unchanged

- **WHEN** `bmv price GFNORTEO` is executed with a valid `BMV_API_TOKEN`
- **THEN** output is identical (same commands, arguments, and formatting) to pre-restructure behavior

### Requirement: Distribution named `bmv-cli`

`[project].name` SHALL be `bmv-cli` (the PyPI distribution name; PyPI's `bmv` is taken by an unrelated project).

#### Scenario: Sync shows renamed distribution

- **WHEN** `uv sync --extra dev` runs after the rename
- **THEN** the installed project is reported as `bmv-cli` (e.g. `bmv-cli 0.1.0`), not `bmv`

### Requirement: All quality gates pass after the move

The four project quality gates (ruff format check, ruff check, mypy, pytest) SHALL pass with configuration paths updated to the new layout.

#### Scenario: Full gate run on the restructured tree

- **WHEN** `uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy src/bmv_cli/api src/bmv_cli/commands` (per AGENTS.md), and `uv run pytest` are executed
- **THEN** all four exit 0, including all tests under `src/bmv_cli/commands/tests/` using fixtures from `bmv_cli.commands.tests.fixtures`
