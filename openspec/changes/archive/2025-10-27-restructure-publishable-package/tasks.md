## 1. Scaffold the new package structure

- [x] 1.1 Create `src/bmv_cli/__init__.py` and `git mv api src/bmv_cli/api`, `git mv commands src/bmv_cli/commands`, `git mv main.py src/bmv_cli/main.py` (preserve history)
- [x] 1.2 Rewrite all internal imports in moved files: `from api…` / `from commands…` → `from bmv_cli.api…` / `from bmv_cli.commands…` (including `commands/tests/**` and fixture imports)

## 2. Update pyproject.toml metadata

- [x] 2.1 Rename `[project] name` to `bmv-cli`; add `[project.scripts] bmv = "bmv_cli.main:app"`; add `[project.urls]` (GitHub repo + issues)
- [x] 2.2 Replace `license = { text = "MIT" }` with `license = "MIT"` (PEP 639); add LICENSE classifier set per spec (omit license classifier if using the SPDX expression); add Environment/Topic/Python 3.12–3.14 classifiers
- [x] 2.3 Update `[build-system]` requires to `setuptools>=77` (PEP 639 support) and `[tool.setuptools.packages.find]` to `where = ["src"]`
- [x] 2.4 Update tooling paths: pytest `testpaths = ["src/bmv_cli/commands/tests"]`, ruff isort `known-first-party = ["bmv_cli"]`, mypy override `module = "bmv_cli.commands.tests.*"`

## 3. Package assets

- [x] 3.1 Add `LICENSE` file (MIT, copyright Axel Berrelleza)
- [x] 3.2 Rewrite `README.md` as the package landing page per spec: intro, install (uv tool / pipx / pip), `BMV_API_TOKEN` setup, usage examples for all subcommands, development section
- [x] 3.3 Update `AGENTS.md` — run commands (`uv run bmv …`), quality-gate paths (`mypy src/bmv_cli/api src/bmv_cli/commands`, pytest), import examples from `bmv_cli…`

## 4. Cleanup legacy artifacts

- [x] 4.1 Delete leftover `bmv/` directory and `requirements.txt`; remove stale `bmv.egg-info/` if present

## 5. Verify

- [x] 5.1 `uv sync --extra dev` — project installs as `bmv-cli`; `uv run bmv --help` lists all subcommands
- [x] 5.2 Run all four quality gates green: `uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy src/bmv_cli/api src/bmv_cli/commands`, `uv run pytest`
- [x] 5.3 Smoke-test one command with the real token (e.g. `uv run bmv price GFNORTEO`) to confirm behavior is unchanged
