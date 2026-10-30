# ci-quality-gates

Add .github/workflows/ci.yml: astral-sh/setup-uv (pinned version), uv sync --extra dev, then ruff format --check, ruff check, mypy, pytest on push and pull_request. Written against the final src/bmv_cli paths from restructure-publishable-package.
