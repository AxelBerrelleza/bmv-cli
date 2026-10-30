# cd-release-automation

Add release-please.yml (conventional commits to release PRs: pyproject version bump + CHANGELOG) and publish.yml (on tag v*: uv build --no-sources in a build job, separate publish job with id-token: write + environment: pypi running uv publish via Trusted Publishing, artifacts attached to the GitHub Release). Workflow filename publish.yml and environment name pypi must match the user's pending trusted-publisher registration. Depends on changes 1-3.
