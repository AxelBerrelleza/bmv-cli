## Why

The initiative's first three changes make the repo a correctly structured, uv_build-packaged project with CI keeping it green — but releases are still manual copy-paste work, and the package has never reached PyPI. This change closes the loop: conventional commits (already the repo's habit) automatically produce versioned, changelogged releases that publish to PyPI with zero stored secrets, via PyPI Trusted Publishing (OIDC).

## What Changes

- **Add `.github/workflows/release-please.yml`**: on push to `main`, googleapis/release-please (release-type: `python`) maintains a running release PR that bumps `[project].version` in `pyproject.toml` and regenerates `CHANGELOG.md` from conventional commits. Merging that PR cuts a `vX.Y.Z` tag and creates the GitHub Release.
- **Add `.github/workflows/publish.yml`**: triggered on tag push `v*`. Two separate jobs:
  1. **build**: checkout, pinned `astral/sh/setup-uv`, `uv sync --extra dev`, gates smoke (rely on green CI), `uv build --no-sources`, verify tag↔version match, upload `dist/` as workflow artifact
  2. **publish**: download the artifact, `uv publish` authenticated by Trusted Publishing (`id-token: write`, `environment: pypi`), then attach `dist/` files to the GitHub Release
- **Bootstrap `CHANGELOG.md`** (initial content) so release-please has its anchor file.
- **No stored credentials anywhere**: no PyPI API tokens; the trusted publisher is registered user-side (see initiative manual tasks) against exactly `publish.yml` + environment `pypi` on this repo.
- **AGENTS.md**: document the release process (merge release PR → tag → publish is automatic; manual task checklist link).

## Capabilities

### New Capabilities
- `release-automation`: Conventional commits on `main` automatically produce release PRs (version bump + changelog); merging one creates the tag and GitHub Release — no manual version editing.
- `package-publishing`: A `v*` tag automatically builds and publishes the distribution to PyPI using Trusted Publishing (no secrets), with artifacts attached to the GitHub Release.

### Modified Capabilities
<!-- None — CI and build-backend specs are untouched; this change only adds workflows and CHANGELOG. -->

## Impact

- **New files**: `.github/workflows/release-please.yml`, `.github/workflows/publish.yml`, `CHANGELOG.md`; docs update in `AGENTS.md`.
- **User-side prerequisites** (cannot be done by the agent — tracked in the initiative's manual tasks): PyPI account + 2FA, pending trusted-publisher registration for `bmv-cli` (owner `AxelBerrelleza`, repo, workflow `publish.yml`, environment `pypi`), GitHub `pypi` environment, repo-name decision (before registration).
- **Dependencies**: requires changes 1–3 applied (src layout + uv_build for `uv build`, green CI as the release's quality gate).
- **First release**: after this change lands, the first release-please PR merges to publish `bmv-cli 0.1.0`, claiming the PyPI name.
