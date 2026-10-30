## 1. Project Configuration & Metadata

- [x] 1.1 Update `pyproject.toml` with correct project name (`bmv`), description, license, and authors fields
- [x] 1.2 Add `[build-system]` and `[tool.setuptools.packages.find]` for proper packaging
- [x] 1.3 Add `[project.optional-dependencies]` dev group with pytest, ruff, mypy, requests-mock, types-requests

## 2. Tool Configuration

- [x] 2.1 Add `[tool.ruff]` configuration (target Python 3.12, line-length 100, select E/W/F/I/UP/B/SIM/RUF/TCH rules, appropriate ignores)
- [x] 2.2 Add `[tool.ruff.lint.isort]` with known-first-party = ["commands", "api"]
- [x] 2.3 Add `[tool.ruff.format]` (double quotes, space indent, auto line-ending)
- [x] 2.4 Add `[tool.mypy]` configuration (Python 3.12, check_untyped_defs, warn settings, test overrides)
- [x] 2.5 Add `[tool.pytest.ini_options]` (testpaths, minversion, addopts)

## 3. Code Modernization

- [x] 3.1 Run `uv run ruff format .` to format entire codebase
- [x] 3.2 Run `uv run ruff check --fix .` for safe automated lint fixes
- [x] 3.3 Replace deprecated `typing.List` with built-in `list` in `api/client.py` and `commands/price.py`
- [x] 3.4 Simplify if/else block to ternary in `commands/price.py`
- [x] 3.5 Ensure trailing newlines in all Python files
- [x] 3.6 Verify all quality gates pass: `ruff format --check`, `ruff check`, `mypy`, `pytest`

## 4. Test Infrastructure

- [x] 4.1 Create `commands/tests/` directory structure
- [x] 4.2 Create `commands/tests/__init__.py`
- [x] 4.3 Create `commands/tests/conftest.py` with `cli_runner` fixture

## 5. Documentation

- [x] 5.1 Create `AGENTS.md` with setup, run, test, and quality gate commands
- [x] 5.2 Document architecture (CLI framework, API provider, package structure)
- [x] 5.3 Document current project status (DataBursatil API broken, out of scope)
- [x] 5.4 Document testing conventions and quality standards

## 6. Follow-up Scope Tracking

- [x] 6.1 Create follow-up OpenSpec change for `add-test-coverage` (writing actual tests)
- [x] 6.2 Create follow-up OpenSpec change for `fix-databursatil-api` (API integration)
