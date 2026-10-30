## Why

The repo is a functional Typer CLI but is not an installable package: it has no `[project.scripts]` entry point, a flat multi-package layout (`api/`, `commands/`, root `main.py`), no LICENSE file, and a README that only covers dev setup. This is the foundational change of the `publish-bmv-cli` initiative — PyPI publication (as `bmv-cli`) and CI/CD cannot be built on the current shape.

## What Changes

- **Restructure to src layout**: move `api/` and `commands/` (with its `tests/`) into a single package `src/bmv_cli/`; move root `main.py` to `src/bmv_cli/main.py`; rewrite all internal imports (`from commands.price import …` → `from bmv_cli.commands.price import …`, `from api…` → `from bmv_cli.api…`).
- **Rename the distribution** to `bmv-cli` in `pyproject.toml` (the PyPI name `bmv` is taken by an unrelated project).
- **Add a console entry point**: `[project.scripts] bmv = "bmv_cli.main:app"` so installed users get a `bmv` command.
- **Add LICENSE** file (MIT) and declare it via PEP 639 metadata (`license = "MIT"`).
- **Rewrite README.md** as the PyPI landing page: what it is, install (`uv tool install bmv-cli` / `pipx install bmv-cli`), token setup (`BMV_API_TOKEN`), usage examples for every command.
- **Add trove classifiers** (License :: OSI Approved :: MIT License, Environment :: Console, Programming Language :: Python :: 3.12–3.14, etc.).
- **Cleanup**: delete the leftover empty `bmv/` directory and the stale `requirements.txt` (uv.lock is the lock of record).
- Keep the **setuptools** backend for this change (it supports src layouts); the swap to `uv_build` is a separate change.
- Update **AGENTS.md** tooling paths (run/test/lint commands reference the new module paths).

## Capabilities

### New Capabilities
- `packaging-structure`: The repository is laid out as an installable Python package — single `src/bmv_cli/` package, correct imports, console entry point `bmv`, distribution named `bmv-cli`.
- `package-metadata`: Complete, publishable project metadata — LICENSE (MIT), README serving as the package landing page, trove classifiers, PEP 639 license expression.

### Modified Capabilities
<!-- No existing specs to modify — this repo has no openspec/specs/ yet. -->

## Impact

- **Moved/rewritten code**: every module in `api/` and `commands/` (import rewrites), `main.py`, all files under `commands/tests/` (imports + fixture paths + pytest `testpaths`).
- **Config**: `pyproject.toml` (name, scripts, license, classifiers, `[tool.setuptools.packages.find]` pointed at `src/`), `uv.lock`, `[tool.pytest.ini_options]`, `[tool.ruff.lint.isort] known-first-party`, `[tool.mypy]` overrides for the moved test paths.
- **Docs**: `AGENTS.md` (dev commands), `README.md` (rewritten), new `LICENSE`.
- **Deleted**: `bmv/` (empty leftover), `requirements.txt`, stale `bmv.egg-info/` if regenerated.
- No behavior change to any CLI command; all four quality gates (ruff format, ruff check, mypy, pytest) must stay green after the move.
