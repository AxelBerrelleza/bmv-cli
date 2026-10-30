# package-publishing Specification

## Purpose

Automatic, secret-free publication of releases to PyPI via Trusted Publishing (OIDC) — triggered by release-please completions or hand-pushed tags, with tag/version guarding and release assets.

## Requirements

### Requirement: Releases are built and published to PyPI automatically

The `publish.yml` workflow SHALL be triggered by completion of the Release Please workflow (`workflow_run`, since tags created with `GITHUB_TOKEN` do not emit workflow events) and by hand-pushed `v*` tags, and SHALL produce the distributions with `uv build --no-sources`. The publish step SHALL upload to PyPI using Trusted Publishing — the publish job is the only job granted `id-token: write` and runs in the GitHub environment `pypi`. Runs that correspond to no release SHALL exit cleanly without publishing.

#### Scenario: Release-please release publishes a new version

- **WHEN** a Release Please run completes after creating a release (tag `vX.Y.Z` pointing at the run's commit)
- **THEN** the build job resolves the tag, produces sdist + wheel for that version, and the publish job uploads them to https://pypi.org/project/bmv-cli/

#### Scenario: Non-release Release Please run publishes nothing

- **WHEN** a Release Please run completes without cutting a release (e.g. it only updated a release PR)
- **THEN** publish.yml runs, finds no `v*` tag at the run's commit, and exits successfully without uploading anything

#### Scenario: No stored credentials are used

- **WHEN** the publish workflow is inspected and run
- **THEN** no PyPI API token appears in the repo, workflow, or GitHub secrets — authentication is exclusively via the OIDC trusted publisher registered for this repo, workflow `publish.yml`, and environment `pypi`

#### Scenario: Build and publish are separate jobs

- **WHEN** the publish workflow executes
- **THEN** building (checkout, sync, `uv build --no-sources`, artifact upload) happens in one job, and only the separate publish job holds `id-token: write` + `environment: pypi` and performs the upload

### Requirement: Tag and package version must match

The build job SHALL verify that the pushed tag's version equals the project version being built, failing before any upload on mismatch.

#### Scenario: Mismatched tag fails safely

- **WHEN** a hand-pushed tag `v9.9.9` does not match the `[project].version` being built
- **THEN** the build job exits non-zero and nothing is published

### Requirement: Dist artifacts are attached to the GitHub Release

After a successful publish, the workflow SHALL upload the `dist/` files (sdist + wheel) as assets of the tag's GitHub Release.

#### Scenario: Release assets present after publish

- **WHEN** a release completes successfully
- **THEN** the GitHub Release for `vX.Y.Z` lists the sdist (`.tar.gz`) and wheel (`.whl`) as downloadable assets
