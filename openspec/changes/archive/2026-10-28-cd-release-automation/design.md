## Context

Changes 1–3 deliver: `src/bmv_cli/` package named `bmv-cli` (entry point `bmv`), `uv_build` backend with `uv build --no-sources` verified, and CI gates on every push/PR. The repo uses conventional commits (verified in git log). PyPI Trusted Publishing lets GitHub Actions authenticate without stored tokens (verified against PyPA and uv docs); a *pending publisher* claims the `bmv-cli` name on first upload. Release Please (release-type `python`) bumps `[project].version` in `pyproject.toml` and writes `CHANGELOG.md` — verified in its Python strategy source.

## Goals / Non-Goals

**Goals:**
- Release PRs with version bump + changelog generated automatically from conventional commits.
- Tag `v*` → automatic build + publish to PyPI with zero stored secrets.
- Dist artifacts attached to the GitHub Release.
- Build and publish as separate jobs (PyPA security guidance: the OIDC-capable job should not run build/test code).
- Tag/version consistency verified before upload.

**Non-Goals:**
- TestPyPI staging (initiative decision: go straight to PyPI).
- PEP 740 attestations / sigstore (can be added later with the pypa action if desired).
- Multi-package/workspace releases (manifest-driven release-please) — single package.
- Docker/homebrew/conda distribution channels.

## Decisions

- **Release Please over python-semantic-release**: two-workflow pattern (release-please PRs → tag-triggered publish) keeps publishing a deliberate, reviewable act; PSR bundles version+build+publish in one tool (more control traded away) — Release Please is the community standard for Python repos on GitHub Actions. Verified: it bumps `[project].version` in pyproject.toml directly.
- **`release-type: python`, no config files**: single-package repo — the workflow alone suffices (no `.release-please-config.json` / manifest needed until monorepo/workspaces appear). `CHANGELOG.md` is bootstrapped once so release-please appends to it.
- **Trigger = tag push `v*` + `workflow_run` on Release Please completion (revised during implementation)**: the original design used only `on: push: tags: v*`, but GitHub suppresses workflow events caused by `GITHUB_TOKEN` (anti-recursion rule) and release-please creates its tags with that token — the tag push never fires `publish.yml`. Fixed with the PyPA-documented dual-trigger pattern: (1) `workflow_run` on "Release Please" completion (fires even for GITHUB_TOKEN events), gated by a resolve step that maps the run's `head_sha` to a `v*` tag and exits cleanly when no release was cut; (2) the original tag-push trigger retained for hand-pushed tags. No double-publish risk: the two paths are mutually exclusive per event.
- **Publish with `uv publish`** (not pypa/gh-action-pypi-publish): native Trusted Publishing support, uniform uv toolchain, and it revokes the short-lived OIDC token after upload. The pypa action is the audited alternative — swap is low-cost if ever needed (same permissions model).
- **Two jobs, not one**: `build` (checkout/sync/build/upload-artifact) and `publish` (download-artifact + `uv publish`, only job with `id-token: write` and `environment: pypi`). Mirrors PyPA's "separate building from publishing" guidance — malicious code in the build environment cannot use the publish credential.
- **Tag↔version guard in the build job**: parse the tag (`vX.Y.Z`) and compare against the built distribution's version; fail on mismatch. Catches accidental hand-typed tags or forgotten bumps.
- **Artifacts attached to the existing GitHub Release**: release-please already creates the Release on tag; `publish.yml` uploads `dist/*` to it (e.g. `gh release upload` with a GITHUB_TOKEN scoped to that job).
- **Publish job does not re-run the full gates**: green CI on `main` is the release's quality gate; the build job does run `uv build --no-sources` which validates metadata. (Optionally a smoke `pytest` in the build job — cheap, keeps zero doubt.)
- **Hard-name constraint**: the workflow file MUST be `publish.yml` and the environment MUST be `pypi` — these strings are part of the user's pending trusted-publisher registration; renaming either breaks authentication silently.
- **Actions pinned by SHA + version comment** (release-please, setup-uv, checkout, upload/download-artifact), per security guidance already adopted in change 3.

## Risks / Trade-offs

- [Trusted publisher misconfiguration blocks first release] → Registration values are pinned in the initiative's manual task ④ (exact strings); publish job failure output names the mismatch; can re-register freely before first release.
- [Repo renamed after registration] → Trusted publisher binds to owner/repo; the initiative's manual task ② forces the rename decision *before* registration.
- [Hand-pushed tag with stale version] → Tag↔version guard fails the build job before any upload.
- [Partial upload failure (some files up)] → `uv publish` retries are idempotent on PyPI (identical files ignored); re-running the failed job is safe.
- [Release Please needs conventional-commit discipline] → CI can't enforce commit style; documented in AGENTS.md release section; mistakes only delay a release PR, never break main.
- [GitHub Release created before publish succeeds] → Release exists with no artifacts until publish completes; acceptable (retry-safe), ordering artifact-upload *after* `uv publish` keeps the release accurate on success.

## Migration Plan

1. Bootstrap `CHANGELOG.md` (Keep a Changelog-style header, 0.1.0 unreleased notes).
2. Add `release-please.yml` (push to `main`).
3. Add `publish.yml` (tag `v*`).
4. User completes manual tasks ②–④ (repo name → GitHub `pypi` environment → PyPI pending publisher) — none of them touch the repo.
5. First release: merge the release-please PR for 0.1.0 → tag `v0.1.0` → publish.yml claims `bmv-cli` on PyPI → manual task ⑤ verifies install.

Rollback: delete both workflows (published PyPI versions are immutable — releases stay, which is expected).

## Open Questions

- None blocking. (Smoke-pytest in build job: implementer's discretion per tasks.)
