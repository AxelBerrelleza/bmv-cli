## Why

The repository currently lacks unified configuration, automated linting, formatting, and static type analysis. Agent instructions are absent, and the project metadata in `pyproject.toml` uses placeholder values. As AI agents execute workflows, the absence of fast, automated quality gates leads to stylistic drift, untyped data structures, and undetected regressions.

Modernizing this infrastructure according to current Python Enhancement Proposals (PEPs) and high-performance tooling (`uv`, `ruff`, `mypy`, `pytest`) provides a sub-second, deterministic quality feedback loop essential for spec-driven development with AI agents.

## What Changes

- **Update `pyproject.toml` project metadata**: Correct project name from `typer-migration-and-uv-implement` to `bmv`, add proper description, license, and authors fields per PEP 621.
- **Add development dependencies**: Introduce `[project.optional-dependencies]` with `dev` group containing `pytest`, `ruff`, `mypy`, `requests-mock`, and `types-requests` for comprehensive quality tooling.
- **Configure `ruff` for formatting and linting**: Add `[tool.ruff]` configuration targeting Python 3.12+ (PEP 8, line-length 100, isort import sorting, pyupgrade, bugbear, simplify rules), matching conventions from reference project `axl-uti`.
- **Configure `mypy` for static type analysis**: Add `[tool.mypy]` baseline configuration with gradual typing (PEP 484, PEP 585, PEP 604) and appropriate overrides for test files.
- **Configure `pytest` test runner**: Add `[tool.pytest.ini_options]` with test paths, verbosity, and traceback settings.
- **Modernize existing code**: Apply automated formatting and safe lint fixes to existing modules (`api/client.py`, `commands/price.py`, `commands/hello.py`) — replace deprecated `typing.List` with built-in `list`, simplify if/else to ternary expressions, ensure trailing newlines.
- **Create test infrastructure**: Establish `commands/tests/` directory structure with `__init__.py` and `conftest.py` containing shared fixtures (e.g., `cli_runner`).
- **Document project conventions**: Create `AGENTS.md` with setup instructions, run commands, quality gates, architecture overview, testing conventions, and current project status (noting DataBursatil API is broken, out of scope).
- **Configure build system**: Add `[build-system]` and `[tool.setuptools.packages.find]` for proper packaging.

## Capabilities

### New Capabilities
- `python-project-standards`: Standardized `pyproject.toml` project packaging, dependency definitions, and tool configuration compliant with PEP 517/518/621/735 using `uv`.
- `code-formatting-and-linting`: Automated, sub-second code formatting and rule enforcement via `ruff` adhering to PEP 8 and modern Python conventions.
- `static-type-analysis`: Static type checking baseline via `mypy` supporting PEP 484, 585, 604 with gradual typing.
- `test-infrastructure`: Pytest configuration and test scaffolding for future test development.

### Modified Capabilities
(none — no existing specs are modified; this introduces development infrastructure)

## Impact

- **Configuration files**: Updated `pyproject.toml` with complete project metadata, dev dependencies, and tool configurations for ruff, mypy, and pytest.
- **Codebase changes**: Applied automated formatting and safe lint fixes to `api/client.py`, `commands/price.py`, `commands/hello.py` — modernized type annotations, simplified control flow, ensured PEP 8 compliance.
- **Test infrastructure**: Created `commands/tests/__init__.py` and `commands/tests/conftest.py` with `cli_runner` fixture.
- **Documentation**: Created `AGENTS.md` with comprehensive project instructions, setup, quality gates, architecture, and current status (API broken).
- **Workflow**: Established four quality gates: `ruff format --check`, `ruff check`, `mypy`, `pytest`.
- **Non-Goals & Follow-up Changes**:
  - *Test Coverage*: Writing actual tests for existing commands is out of scope and deferred to follow-up (`add-test-coverage`).
  - *API Integration Fix*: DataBursatil API breaking changes are out of scope and deferred to follow-up (`fix-databursatil-api`).
  - *CI/CD*: GitHub Actions or similar CI pipeline is out of scope.
