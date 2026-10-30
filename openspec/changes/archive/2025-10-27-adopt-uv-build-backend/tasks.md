## 1. Swap the build backend

- [x] 1.1 Replace `[build-system]` in `pyproject.toml` with `requires = ["uv_build>=0.13.6,<0.14"]` / `build-backend = "uv_build"`
- [x] 1.2 Delete the `[tool.setuptools.packages.find]` section (and any remaining `[tool.setuptools.*]` config)

## 2. Refresh lock and environment

- [x] 2.1 Run `uv sync --extra dev` and `uv lock` so the editable install and lockfile reflect the new backend dependency

## 3. Verify the build

- [x] 3.1 Run `uv build --no-sources` and confirm `dist/` contains both the sdist (`bmv_cli-<version>.tar.gz`) and the wheel (`bmv_cli-<version>-py3-none-any.whl`)
- [x] 3.2 Install the wheel into a clean scratch venv and run `bmv --help` (all subcommands listed)

## 4. Docs

- [x] 4.1 Add a build section to AGENTS.md: canonical build command `uv build --no-sources`, and the pin-maintenance rule (raise the `uv_build` upper bound when uv majors)

## 5. Gates

- [x] 5.1 Run all four quality gates green with zero source-file changes: `uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy src/bmv_cli/api src/bmv_cli/commands`, `uv run pytest`
