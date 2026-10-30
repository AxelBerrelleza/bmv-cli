# Tasks

## Coordination Tasks

Implementation changes (in this order, each its own OpenSpec change):

- [x] 1. `restructure-publishable-package` — src/bmv_cli layout, entry point `bmv`, rename to bmv-cli, LICENSE, README, classifiers, cleanup (archived 2025-10-27)
- [x] 2. `adopt-uv-build-backend` — drop setuptools, `[build-system]` → uv_build pinned, verify `uv build --no-sources` (archived 2025-10-27)
- [x] 3. `ci-quality-gates` — `.github/workflows/ci.yml` with the four gates on push/PR (archived 2026-10-28; branch ruleset active, see ②★)
- [x] 4. `cd-release-automation` — release-please.yml + publish.yml (trusted publishing, environment: pypi) — DONE & archived 2026-10-28: **v0.1.0 published to PyPI** after fixing two real issues discovered in-flight (GITHUB_TOKEN event suppression → workflow_run dual-trigger; git context before ls-remote). Specs synced to `openspec/specs/` (release-automation, package-publishing).

## Manual Tasks (user-owned — cannot be done by the agent)

Preferred order: ① now → ② before change 4 → ③④ during change 4 → ⑤ after first release.

### ① Create PyPI account (do it now — takes 5 minutes) — DONE

- [x] Register at https://pypi.org/account/register/ (use a professional username; it becomes your publisher identity)
- [x] Verify the email
- [x] Enable 2FA (Account settings → Two-factor authentication) — required to manage projects and register publishers

### ② Decide on the GitHub repo name (before change 4 is applied) — DONE

- [x] Decide: keep `cli-finance-py` or rename to `bmv-cli` (recommended, for consistency).
- [x] Rename done (2026-10-27): renamed on GitHub to `bmv-cli`; local remote updated (`git remote set-url origin git@github.com:AxelBerrelleza/bmv-cli.git` — verified with `git ls-remote`); stale repo-name references fixed in `pyproject.toml` (`[project.urls]`), `README.md` (clone URL), and `AGENTS.md` (title).
  - ⚠️ Must happen BEFORE registering the trusted publisher (it binds to owner/repo name). If done later, the publisher must be re-registered on PyPI. — RESOLVED: rename completed before registration; when registering the pending publisher (task ④), use **Repository: `bmv-cli`**.

### ②★ Protect `main` and require the CI status check (after change 3 `ci-quality-gates` ships) — DONE

- [x] Branch ruleset `default-branch-ruleset` (active) on `~DEFAULT_BRANCH`: deletion + non-fast-forward blocked, `pull_request` rule (CI merge only), `required_status_checks` = `Quality gates` (CI from `.github/workflows/ci.yml`), bypass actor `RepositoryAdmin` with `bypass_mode: pull_request` (bypass only for PR merges; direct pushes still require the check).

### ③ Create GitHub `pypi` environment (during change 4, after publish.yml design is known) — DONE

- [x] GitHub repo → Settings → Environments → New environment → name it `pypi` — created with **1 required reviewer (owner)**, so every publish from `publish.yml` needs a manual approval.
- [x] (Optional, recommended) Add required reviewers — done (see above).

### ④ Register pending Trusted Publisher on PyPI (during change 4, before the first release) — DONE

- [x] Registered on PyPI (pending publisher) with:
  - PyPI project name: `bmv-cli`
  - Owner: `AxelBerrelleza`
  - Repository: `bmv-cli` (renamed on 2026-10-27, before registration — see ②)
  - Workflow name: `publish.yml`
  - Environment name: `pypi`
- [x] This claims the name when the first `uv publish` runs from that workflow.

### ⑤ Verify the first release (after change 4 ships v0.1.0) — DONE

- [x] `uv tool install bmv-cli` (or `pipx install bmv-cli`) and run `bmv --help` with `BMV_API_TOKEN` set — done 2026-10-28: installed from PyPI; live `price GFNORTEO` + `credits` verified with the token exported (249k credits remaining)
- [x] Check https://pypi.org/project/bmv-cli/ renders the README and shows correct metadata/license — package claimed via pending publisher; visible under "Projects with active publishers"
