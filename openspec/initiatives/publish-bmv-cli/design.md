# Design

## Context

The repo (github.com/AxelBerrelleza/cli-finance-py) is a uv-managed Typer CLI for Mexican stock market data. It is not yet installable as a package: no `[project.scripts]` entry point, flat multi-package layout, no LICENSE file, README is dev-only notes. The PyPI name `bmv` is taken; `bmv-cli` is verified available.

## Approach

Four sequential changes, each independently valid and reviewable:

1. **restructure-publishable-package** — move to `src/bmv_cli/` (api/ and commands/ become submodules), add `main.py` with the app, add `[project.scripts] bmv = "bmv_cli.main:app"`, rename project to `bmv-cli`, add LICENSE (MIT), rewrite README as PyPI landing page, add classifiers, delete `bmv/` leftover dir and `requirements.txt`. Stays on setuptools (which supports src layouts) so the intermediate state is green.
2. **adopt-uv-build-backend** — swap `[build-system]` to `uv_build` (pinned `>=0.13.6,<0.14`), verify `uv build --no-sources` produces sdist+wheel, update lock.
3. **ci-quality-gates** — `.github/workflows/ci.yml`: astral-sh/setup-uv (pinned SHA), `uv sync --extra dev`, then the 4 gates on push/PR.
4. **cd-release-automation** — `.github/workflows/release-please.yml` (release-type: python) + `.github/workflows/publish.yml` (on tag `v*`: build job → separate publish job with `id-token: write`, `environment: pypi`, `uv publish`, GitHub Release with artifacts).

Publishing auth uses PyPI Trusted Publishing (OIDC): no API tokens stored in GitHub. PyPI "pending publisher" claims the `bmv-cli` name on first release.

## Affected Areas

- Package structure: `main.py`, `api/`, `commands/`, `commands/tests/` → `src/bmv_cli/…`
- `pyproject.toml` (name, scripts, license, classifiers, build-system, setuptools config → uv_build)
- `uv.lock`, `.gitignore`, `README.md`, new `LICENSE`
- `.github/workflows/` (new ci.yml, release-please.yml, publish.yml)
- Tooling paths in AGENTS.md (mypy targets, test paths, run commands)

## Dependencies

- Change 2 requires the src layout from change 1 (uv_build expects a single module).
- Change 3 is written against the final paths from change 1.
- Change 4 requires 1+2 (uv build) and 3 (gates gate the release).
- User-owned: PyPI account, trusted publisher registration, GitHub `pypi` environment (see tasks.md).

## Risks

- Import rewrite across all modules/tests during restructure (mechanical, but broad — tests + mypy must stay green).
- Trusted publisher binds to the GitHub repo name: renaming the repo after registering requires re-registering on PyPI.
- Release Please expects conventional commits — repo already uses them; discipline must continue.
- `uv_build` upper-bound pin must be bumped when uv releases new majors (documented versioning policy).
