## Context

The repo (github.com/AxelBerrelleza/cli-finance-py) currently has no `.github/` directory — zero CI. The four quality gates exist and are documented in AGENTS.md. uv is the package manager; `astral-sh/setup-uv` is the official action for it (per uv's GitHub integration guide, which also recommends pinning uv to a specific version). Tests are fully mocked (requests-mock + fixtures), so CI needs no API token or secrets.

## Goals / Non-Goals

**Goals:**
- One workflow file: `.github/workflows/ci.yml` running all four gates on `push` and `pull_request`.
- Reproducible toolchain: uv version pinned in the workflow; Python resolved from `.python-version`.
- Least privilege: read-only permissions, no secrets.
- Fail fast: cheap checks (format, lint) run before expensive ones (mypy, pytest).

**Non-Goals:**
- Python version matrix (3.12–3.14) — the project pins one interpreter; can be added later without config churn.
- Publishing or release jobs (change 4).
- Test coverage reporting/coverage badges.
- Branch protection rules (user-side GitHub setting, noted in the change's docs).

## Decisions

- **Single workflow, four steps, one job**: the gates are sequential steps, not a matrix of jobs — they share the same synced environment, finish in ~1–2 min, and a matrix adds runner startup overhead for zero isolation benefit at this size. Alternative (job per gate) rejected: each job re-runs `uv sync`, tripling setup time.
- **`astral-sh/setup-uv` pinned by version** (e.g. `version: "0.12.10"` to match local tooling) and the action itself pinned by SHA + `# vX.Y.Z` comment, per the security guidance in uv's docs and the pypa action README.
- **Python from `.python-version` via `setup-uv`'s `uv python install`** (respects the project pin, per uv's GitHub guide) rather than hardcoding `python-version: "3.12"` in two places.
- **Explicit gate commands matching AGENTS.md verbatim** (including mypy's scoped paths `src/bmv_cli/api src/bmv_cli/commands`) — CI is the enforcement of the documented gates, so commands must be identical.
- **`permissions: contents: read`** at workflow level; workflow needs no write scopes.
- **Order: format → lint → mypy → pytest**: fail on the cheapest signal first.
- **Push on all branches + PR events**: keeps feature branches honest before the PR even opens; no downside at this scale.

## Risks / Trade-offs

- [CI drift from local gates] → Commands copy AGENTS.md exactly; any gate-command change must update both (noted in AGENTS.md).
- [uv version pin goes stale] → Acceptable: deliberate upgrades, same policy as `uv_build` backend pin.
- [Runner Python cache vs `uv python install`] → `uv python install` may download an interpreter on first run (slower than `actions/setup-python`); mitigated by uv's cache (`enable-cache: true` on setup-uv) — worth enabling for the uv cache at minimum.
- [No branch protection means a red main is still possible via direct push] → User-side setting: recommend requiring the CI check on `main` (noted as a manual follow-up in the initiative).

## Migration Plan

1. Create `.github/workflows/ci.yml` with the job described above.
2. Push to a branch, watch the run go green on the restructured codebase.
3. (User, recommended) GitHub → Settings → Branches → protect `main`, require the CI status check.

Rollback: delete the workflow file.

## Open Questions

- None blocking. Python matrix deferred (goal-level non-goal).
