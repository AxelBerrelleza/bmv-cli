## 1. Create the workflow file

- [x] 1.1 Create `.github/workflows/ci.yml`: triggers on `push` (all branches) + `pull_request`, `permissions: contents: read`, one job on `ubuntu-latest`
- [x] 1.2 Add steps: checkout (action pinned by SHA + version comment), `astral-sh/setup-uv` (pinned by SHA, `version:` pinned to local tooling version, uv cache enabled), `uv python install` (respects `.python-version`), `uv sync --extra dev`
- [x] 1.3 Add the four gate steps in fail-fast order, commands exactly matching AGENTS.md: `uv run ruff format --check .` → `uv run ruff check .` → `uv run mypy src/bmv_cli/api src/bmv_cli/commands` → `uv run pytest`

## 2. Verify

- [x] 2.1 Push a branch and confirm the workflow triggers and goes green end-to-end on the restructured codebase
- [x] 2.2 Confirm the run requires no secrets (no `BMV_API_TOKEN` in the environment) and all tests pass via mocks

## 3. Docs

- [x] 3.1 Add a CI note to AGENTS.md (Quality Gates section): gates run automatically on push/PR via ci.yml — gate-command changes must update both the docs and the workflow together
- [x] 3.2 Note the recommended manual follow-up in the initiative tasks: protect `main` and require the CI status check (user-side GitHub setting) — completed by the user via branch ruleset `default-branch-ruleset` (see initiative task ②★)
