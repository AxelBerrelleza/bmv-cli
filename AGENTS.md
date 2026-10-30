# bmv-cli — agent instructions

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

These gates also run automatically in CI on every push and pull request via `.github/workflows/ci.yml` — when a gate command changes, update **both** this documentation and the workflow together so they stay identical.

**Runner tier**: all Linux GitHub-hosted jobs across `.github/workflows/ci.yml`, `publish.yml`, and `release-please.yml` run on `runs-on: ubuntu-24.04` (pinned OS, not the floating `ubuntu-latest` label, which GitHub repoints to newer Ubuntu versions — e.g. 26.04 in Nov 2026 — silently). Changes to the runner tier must update **all** three workflows and this documentation together. Genuinely lightweight one-off automation jobs may opt into `ubuntu-slim`, but gates and publish jobs must stay on the pinned VM tier.

## Build

- **Canonical build command**: `uv build --no-sources` — produces both a source distribution (`bmv_cli-<version>.tar.gz`) and a wheel (`bmv_cli-<version>-py3-none-any.whl`) in `dist/`.
- **Backend pin maintenance**: The `[build-system]` in `pyproject.toml` pins `uv_build>=0.13.6,<0.14`. When uv releases a new major version, raise the upper bound (e.g., `<0.15` for uv 1.x) to stay compatible. This follows uv's versioning policy where the build backend tracks uv's major releases.

## Releases

Releases are fully automated — never edit the version by hand:

1. Merge `feat:`/`fix:` commits to `main` → `release-please.yml` opens/updates a release PR (bumps `version` in `pyproject.toml`, regenerates `CHANGELOG.md`)
2. Merge the release PR → a `vX.Y.Z` tag + GitHub Release are created
3. The tag triggers `publish.yml`: build job (gates smoke + `uv build --no-sources` + tag↔version guard) → publish job (`uv publish` to PyPI via **Trusted Publishing**, then artifacts attached to the GitHub Release)
4. The publish job pauses in the `pypi` environment until a reviewer approves the deployment

**Hard constraints (PyPI trusted-publisher binding — renaming either breaks publishing authentication):**
- The publish workflow filename must remain exactly `publish.yml`
- The GitHub environment must remain exactly `pypi`
- The registered trusted publisher is: project `bmv-cli`, owner `AxelBerrelleza`, repository `bmv-cli`, workflow `publish.yml`, environment `pypi`

First install from PyPI: `uv tool install bmv-cli` → command `bmv`. No API tokens exist anywhere — publishing authenticates exclusively via OIDC trusted publishing.

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

## OpenSpec Planning (in-repo)

Planning lives in this repo's `openspec/` folder, tracked in git: `openspec/specs/` is the
source of truth, `openspec/changes/` holds in-flight and archived changes, and
`openspec/initiatives/` holds cross-change coordination docs. Change folders ride the code
branch, so every PR reviews the plan and the code together. A plan that emerges from work in
flight may ride that work's PR as a follow-up, even ahead of its own implementation.

Conventions:

1. One change per branch (`change/<name>`, where the branch name is the OpenSpec change name)
   and per worktree; one writer per change folder. Record ownership on the Orca card:
   `orca worktree set --worktree active --comment "change: <name>"`.
2. Cross-worktree context travels through git: commit the change folder to its branch and
   push so other worktrees can see it. To explore or continue an existing change, create the
   worktree from its branch (`orca worktree create --base-branch change/<name> …`).
3. Archive convention: after the change's PR merges, run `openspec archive <name>` on `main`
   as a small follow-up commit.
4. The repo is **public**: never write secrets, tokens, private URLs, personal data, or
   internal-only information into planning artifacts or code. Run `gitleaks detect --no-banner
   --redact` before verification/archive (pre-commit hook + CI enforce this; enable the hook
   once per clone with `git config core.hooksPath .githooks`).
5. If two changes modify the same requirement, re-check it with
   `openspec show <change> --diff` and re-sync before archiving — OpenSpec archive replaces
   whole requirement blocks and can silently revert scenarios.

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