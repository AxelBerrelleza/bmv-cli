## Context

The repo works as a dev checkout (`uv run python main.py price …`) but cannot be pip/uv-installed: flat layout with two top-level packages (`api/`, `commands/`) plus a root `main.py`, no entry point, no LICENSE, README is dev-only. The PyPI name `bmv` is taken; `bmv-cli` is verified available. This is change 1 of 4 in the `publish-bmv-cli` initiative; changes 2–4 (uv_build backend, CI, CD) depend on the structure produced here.

## Goals / Non-Goals

**Goals:**
- Single importable package `src/bmv_cli/` containing `api/`, `commands/`, and `main.py`.
- A `bmv` console command after install (`[project.scripts] bmv = "bmv_cli.main:app"`).
- Distribution renamed to `bmv-cli`; complete publishable metadata (LICENSE, README, classifiers).
- All four quality gates green after the move.

**Non-Goals:**
- Swapping the build backend to `uv_build` (change 2 — setuptools stays here, it supports src layouts).
- CI/CD workflows (changes 3–4).
- Any behavior change to commands, arguments, output, or the API client.
- Widening Python support below 3.12.

## Decisions

- **Single package `bmv_cli` under `src/`** (vs. keeping flat multi-package, vs. multiple packages). `uv_build` (change 2) expects one module in src layout; flat top-level `api`/`commands` also risk collisions in `site-packages/`. All internal imports become `bmv_cli.…`. This also matches the current Typer packaging tutorial.
- **Command name `bmv`, distribution name `bmv-cli`.** PyPI's `[project]` name and `[project.scripts]` key are independent; users install `bmv-cli` but type `bmv`.
- **Keep setuptools for this change.** setuptools >= 77 supports src layouts and PEP 639. Doing the layout move and the backend swap in separate changes keeps each bisectable; the intermediate state is fully valid.
- **PEP 639 license metadata**: replace `license = { text = "MIT" }` with `license = "MIT"` (SPDX expression) + add `LICENSE` file; bump build requires to `setuptools>=77`. Newer form, no deprecation warnings, classifiers for license become optional/forbidden-with-expression — we rely on the expression and drop the license classifier.
- **Tests stay co-located**: `commands/tests/` moves to `src/bmv_cli/commands/tests/`, preserving the repo's testing convention (fixtures importable via `bmv_cli.commands.tests.fixtures`). Whether test files are excluded from the wheel is deferred to change 2 (backend-dependent); shipping them is harmless.
- **Tooling config follows the move**: `testpaths = ["src/bmv_cli/commands/tests"]`, `known-first-party = ["bmv_cli"]`, mypy override `module = "bmv_cli.commands.tests.*"`, `[tool.setuptools.packages.find] where = ["src"]`.
- **README becomes the product page**: what it is, install via `uv tool install bmv-cli` / `pipx install bmv-cli`, getting a DataBursatil token (`BMV_API_TOKEN` env var or `.env`), usage examples for all commands, development section pointing at AGENTS.md. `.env`/dotenv behavior is unchanged — installed users simply export the env var.
- **Delete legacy artifacts**: empty `bmv/` dir, `requirements.txt`, and stale `bmv.egg-info/` (git-ignored if it regenerates).

## Risks / Trade-offs

- [Broad mechanical import rewrite may miss a reference] → All four gates are the safety net: mypy catches bad imports, pytest catches bad test imports; run them before finishing any task.
- [Dotted-module test imports could change fixture behavior] → Fixtures already import via package path (`commands.tests.fixtures`); rewrite is mechanical (`commands` → `bmv_cli.commands`); pytest run confirms.
- [PEP 639 needs setuptools >= 77; older tooling may reject the SPDX string] → Acceptable: uv.lock pins build deps; CI (change 3) will exercise the same gates.
- [Co-located tests may ship in the wheel] → Deferred to change 2; harmless for a small CLI.
- [`.python-version` (3.12) vs newer dev interpreters] → No change; requires-python stays `>=3.12`.

## Migration Plan

1. Create `src/bmv_cli/` (with `__init__.py`), `git mv api src/bmv_cli/api` and `git mv commands src/bmv_cli/commands`, `git mv main.py src/bmv_cli/main.py` (preserve history).
2. Rewrite imports across all moved files (`api`, `commands`, `main.py`, tests, fixtures).
3. Update `pyproject.toml` (name, scripts, license, classifiers, packages.find, pytest, isort, mypy override).
4. Add `LICENSE`, rewrite `README.md`, update `AGENTS.md` paths/commands.
5. Remove `bmv/`, `requirements.txt`, `bmv.egg-info/`; `uv sync` to refresh the editable install; run all gates.

Rollback: single commit move — `git revert` restores the flat layout.

## Open Questions

- None blocking. (Wheel test exclusion is explicitly deferred to change 2.)
