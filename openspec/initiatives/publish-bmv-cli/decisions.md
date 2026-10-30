# Decisions

## Accepted Decisions

### 2026-10-28: Token for the installed tool is the exported env var, not `.env` discovery

- Decision: For the installed `bmv` command, users set `BMV_API_TOKEN` in their environment (export / shell rc). No `.env` auto-discovery fix (`load_dotenv(usecwd=True)`) for now.
- Why: `load_dotenv()` (no args) searches from the module's directory, so the repo `.env` only works in dev checkouts — but exporting the env var works everywhere and is what the README documents.
- Implications: v0.1.0 is correct as published; the one-line `usecwd=True` fix remains a candidate if `.env` support for installed usage is ever wanted.

### 2026-10-27: Distribution name is `bmv-cli`, command stays `bmv`

- Decision: Publish to PyPI as `bmv-cli`; console script exposed as `bmv`.
- Why: `bmv` is taken on PyPI (Victron BMV monitor, unrelated). `bmv-cli` is available, conventional, and the PyPI distribution name may differ from the console command via `[project.scripts]`.
- Implications: Entry point will be `bmv = "bmv_cli.main:app"`; users run `uv tool install bmv-cli` then use `bmv`.

### 2026-10-27: Single package `src/bmv_cli/` replaces flat layout

- Decision: Restructure `api/`, `commands/`, root `main.py` into one package under `src/bmv_cli/`.
- Why: `uv_build` expects a single module in src layout; flat top-level `api`/`commands` pollute `site-packages` root and risk name collisions. Matches the current Typer packaging tutorial.
- Implications: All imports rewritten (`from commands.price import …` → `from bmv_cli.commands.price import …`), tests/fixtures paths move, AGENTS.md tooling commands updated.

### 2026-10-27: setuptools → uv_build

- Decision: Swap build backend to `uv_build` (pinned with upper bound) in change 2, after the restructure.
- Why: Zero-config, fast, metadata validation, and the repo is already all-in on uv. setuptools kept during change 1 so each change is independently valid.
- Implications: `uv build --no-sources` in CD; bump the pin when uv majors release.

### 2026-10-27: Trusted Publishing (OIDC), no stored tokens

- Decision: Publish via GitHub Actions with PyPI Trusted Publishing; no API tokens in GitHub secrets.
- Why: Current best practice (PyPA + uv docs). PyPI "pending publisher" claims the name on first publish; uv even revokes the short-lived token after uploading.
- Implications: Publish job needs `id-token: write`, `environment: pypi`; build and publish must be separate jobs.

### 2026-10-27: Release Please for release automation

- Decision: Use googleapis/release-please (release-type: python) for version bumps + CHANGELOG; tag `v*` triggers the publish workflow.
- Why: Repo already uses conventional commits. Release PRs keep releases deliberate and generate the changelog. Verified Release Please bumps `[project].version` in pyproject.toml directly.
- Implications: Commit discipline required; two workflows (release-please + publish).

### 2026-10-27: Go straight to PyPI, no TestPyPI staging

- Decision: Skip a TestPyPI staging workflow.
- Why: User preference; quality gates in CI + trusted publishing make the risk acceptable for a small CLI.

### 2026-10-27: Python floor stays >=3.12

- Decision: Keep `requires-python = ">=3.12"`.
- Why: Code targets 3.12+ syntax; honest floor; CI can matrix 3.12–3.14 later if desired.
