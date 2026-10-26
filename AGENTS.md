# cli-finance-py — agent instructions

## ⚠️ Current Status: BROKEN (out of scope)

The BMV CLI tool is **currently non-functional** because the DataBursatil API provider released breaking changes to its API. **Updating the API integration is out of scope for this session.** Do not attempt to fix the API calls — focus only on project scaffolding, conventions, linting, and testing infrastructure.

## Setup

```bash
uv sync --extra dev
cp .env.sample .env  # then set BMV_API_TOKEN
```

## Run

```bash
uv run python main.py --help
uv run python main.py price AAPL
uv run python main.py currencies
```

## Test & Quality Gates

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy commands api
uv run pytest
```

## Architecture

- **CLI framework**: [Typer](https://typer.tiangolo.com/) — sub-commands registered in `main.py` from `commands/hello`, `commands/price`, and `commands/currencies`
- **API**: DataBursatil (`token` from `BMV_API_TOKEN` env var, loaded via `dotenv` in `api/client.py`). Base URL: `https://api.databursatil.com/v2/`
- **Display**: Rich tables for terminal output
- **Package structure**:
  - `api/` — HTTP client for DataBursatil API
  - `commands/` — Typer sub-command modules (one `app = typer.Typer()` per file)
  - `commands/tests/` — pytest test suite (co-located with commands)
  - `main.py` — CLI entry point, registers all sub-command apps

## Testing Conventions

- Uses `requests-mock` and `typer.testing.CliRunner`
- Test fixtures live in `commands/tests/fixtures/`
- Test files follow `test_<module>.py` naming

## Quality Standards

- **Formatting**: `uv run ruff format .` (enforces PEP 8, line length 100)
- **Linting**: `uv run ruff check --fix .` (safe auto-fixes enabled)
- **Static Typing**: `uv run mypy commands api`
- **Testing**: `uv run pytest`
- Always verify all four quality gates pass cleanly before finishing any task.

## Conventions

- Python 3.12+ with `uv` for dependency management
- Double quotes, 100-char line length
- `from __future__ import annotations` not required (3.12+ has modern syntax)
- Imports sorted via ruff/isort; first-party groups: `commands`, `api`
- Typer argument defaults with `typer.Option(...)` are excluded from B008
