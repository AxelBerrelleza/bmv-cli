# release-automation Specification

## Purpose

Automated release PRs from conventional commits via Release Please — version bumps, changelog generation, and tag/release creation happen without manual version editing.

## Requirements

### Requirement: Release PRs are generated from conventional commits

The repository SHALL run a release-please workflow (`.github/workflows/release-please.yml`, release-type `python`) on pushes to `main` that maintains a release pull request bumping `[project].version` in `pyproject.toml` and regenerating `CHANGELOG.md`. Merging the release PR SHALL create a `vX.Y.Z` tag and a GitHub Release.

#### Scenario: Conventional commits accumulate into a release PR

- **WHEN** `feat:` or `fix:` commits land on `main`
- **THEN** release-please opens/updates a single release PR containing the next version bump in `pyproject.toml` and the corresponding CHANGELOG entries

#### Scenario: Merging the release PR creates tag and release

- **WHEN** the release PR is merged
- **THEN** a `vX.Y.Z` tag matching the bumped version is created and a GitHub Release is published with the generated notes

#### Scenario: Non-release commits do not trigger releases

- **WHEN** only `chore:`, `docs:`, or `test:` commits land on `main`
- **THEN** no new release PR or version bump is produced

### Requirement: Release process is documented

AGENTS.md SHALL document the release workflow: conventional-commit → release PR → merge → automatic tag/build/publish, the hard constraint that the publish workflow filename stays `publish.yml` and environment name stays `pypi` (trusted-publisher binding), and the link to the initiative's manual tasks.

#### Scenario: Docs describe the release flow

- **WHEN** a maintainer reads AGENTS.md after this change
- **THEN** they can release a new version without editing any version number manually and know the trusted-publisher constraints on renaming the workflow or environment
