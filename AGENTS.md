# cli-finance-py — agent instructions

## Setup

```bash
uv sync --extra dev
cp .env.sample .env  # then set BMV_API_TOKEN
```

## Run

```bash
uv run bmv --help
uv run bmv price GFNORTEO WALMEX
uv run bmv currencies
uv run bmv credits
uv run bmv search WALMEX
uv run bmv dividend FMTY14
```

## Test & Quality Gates

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src/bmv_cli/api src/bmv_cli/commands
uv run pytest
```

## Architecture

- **CLI framework**: [Typer](https://typer.tiangolo.com/) — sub-commands registered in `src/bmv_cli/main.py` from `bmv_cli.commands.hello`, `bmv_cli.commands.price`, `bmv_cli.commands.currencies`, `bmv_cli.commands.credits`, `bmv_cli.commands.search`, and `bmv_cli.commands.dividend`
- **API**: [DataBursatil](https://www.databursatil.com/docs.html) v2 (`token` from `BMV_API_TOKEN` env var, loaded via `dotenv` in `bmv_cli.api.client`). Base URL: `https://api.databursatil.com/v2/`
  - Endpoints used: `cotizaciones`, `divisas`, `creditos`, `emisoras`
  - Auth: token query parameter (`?token=...`)
  - Docs: <https://www.databursatil.com/docs.html>
- **Display**: Rich tables for terminal output
- **Package structure**:
  - `src/bmv_cli/api/` — HTTP client for DataBursatil API
  - `src/bmv_cli/commands/` — Typer sub-command modules (one `app = typer.Typer()` per file)
  - `src/bmv_cli/commands/tests/` — pytest test suite (co-located with commands)
  - `src/bmv_cli/main.py` — CLI entry point, registers all sub-command apps

## Testing Conventions

- Uses `requests-mock` and `typer.testing.CliRunner`
- Test fixtures live in `src/bmv_cli/commands/tests/fixtures/`
- Test files follow `test_<module>.py` naming

### Using Test Fixtures

Fixtures provide mock API responses for testing. Import from `bmv_cli.commands.tests.fixtures`:

```python
from bmv_cli.commands.tests.fixtures import (
    prices_response,
    currencies_response,
    credits_response,
    emisoras_response,
    emisoras_error_response,
)
```

### Mocking API Responses with requests-mock

Use `requests_mock` fixture to mock API endpoints:

```python
@pytest.fixture
def mock_prices_api(requests_mock):
    """Mock the cotizaciones API endpoint."""
    response = prices_response()
    requests_mock.get(
        "https://api.databursatil.com/v2/cotizaciones",
        json=response,
    )
    return response
```

### Testing CLI Commands with CliRunner

Use `typer.testing.CliRunner` to invoke commands and verify output:

```python
from typer.testing import CliRunner
from bmv_cli.commands.price import app

runner = CliRunner()


def test_single_symbol_price(mock_prices_api):
    result = runner.invoke(app, ["GFNORTEO"], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "GFNORTEO" in result.stdout
    assert "213.5" in result.stdout
```

**Important**: Set `env={"COLUMNS": "200"}` to prevent Rich from truncating table output with `…`.

### Test Structure Pattern

```python
import pytest
from typer.testing import CliRunner
from bmv_cli.commands.mycommand import app
from bmv_cli.commands.tests.fixtures import my_fixture

runner = CliRunner()


@pytest.fixture
def mock_api(requests_mock):
    response = my_fixture()
    requests_mock.get("https://api.databursatil.com/v2/endpoint", json=response)
    return response


def test_my_command(mock_api):
    result = runner.invoke(app, ["arg1"], env={"COLUMNS": "200"})
    assert result.exit_code == 0
    assert "expected_output" in result.stdout
```

## Quality Standards

- **Formatting**: `uv run ruff format .` (enforces PEP 8, line length 100)
- **Linting**: `uv run ruff check --fix .` (safe auto-fixes enabled)
- **Static Typing**: `uv run mypy src/bmv_cli/api src/bmv_cli/commands`
- **Testing**: `uv run pytest`
- Always verify all four quality gates pass cleanly before finishing any task.

## Conventions

- Python 3.12+ with `uv` for dependency management
- Double quotes, 100-char line length
- `from __future__ import annotations` not required (3.12+ has modern syntax)
- Imports sorted via ruff/isort; first-party groups: `bmv_cli`
- Typer argument defaults with `typer.Option(...)` are excluded from B008