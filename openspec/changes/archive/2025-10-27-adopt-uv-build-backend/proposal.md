## Why

After `restructure-publishable-package`, the repo builds with setuptools — a working but legacy choice that we keep no configuration for beyond path discovery. The project is all-in on uv; the `uv_build` backend (same toolchain as the docs and the future CD pipeline) offers zero-config builds, metadata validation, and faster builds. This must happen before CD (change 4), which runs `uv build --no-sources` to produce release artifacts.

## What Changes

- **Swap `[build-system]`** from `setuptools.build_meta` to `uv_build`, pinned with an upper bound per uv's versioning policy (`requires = ["uv_build>=0.13.6,<0.14"]`).
- **Remove setuptools-specific config**: `[tool.setuptools.packages.find]` (uv_build auto-discovers `src/bmv_cli` — zero config needed).
- **Verify `uv build`** produces both a valid sdist and wheel in `dist/`; establish `uv build --no-sources` as the canonical build command for releases (it is what CD will run).
- **Refresh `uv.lock`** so the build dependency graph reflects the new backend.
- Document the backend pin maintenance rule (bump the upper bound when uv releases a major) in AGENTS.md.

## Capabilities

### New Capabilities
- `build-backend`: The project builds its distributions with the `uv_build` backend — pinned `[build-system]`, no build config, reproducible sdist+wheel via `uv build --no-sources`.

### Modified Capabilities
<!-- None: packaging-structure and package-metadata specs from the restructure change are unaffected (they specify layout/metadata, not the backend). -->

## Impact

- **Config**: `pyproject.toml` `[build-system]` and removal of `[tool.setuptools.*]`; `uv.lock`.
- **Docs**: `AGENTS.md` (build section: `uv build`, pin maintenance note).
- **No code changes** — no module, import, or behavior changes; all four quality gates must remain green.
- Downstream: `cd-release-automation` (change 4) will rely on `uv build --no-sources` + `uv publish`.
