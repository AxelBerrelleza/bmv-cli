## Context

Post-restructure, the project builds via setuptools with a src-layout `[tool.setuptools.packages.find]`. The initiative targets a uv-native toolchain end-to-end: `uv_build` is Astral's build backend — fast, validating, zero-config for a single `src/<pkg>` module — and is the same backend the Typer packaging tutorial and the uv publishing guide assume. CD (change 4) will invoke `uv build --no-sources` to cut release artifacts.

## Goals / Non-Goals

**Goals:**
- `[build-system]` uses `uv_build` pinned with an upper bound.
- Zero build configuration (delete setuptools config entirely).
- `uv build --no-sources` produces a valid, installable sdist + wheel.
- Gates stay green; lock refreshed.

**Non-Goals:**
- Any code/module change.
- Publishing anywhere (change 4).
- Excluding co-located tests from the wheel (uv_build packages the module; shipping tests is acceptable — noted, not solved).
- CI wiring of the build (change 3/4).

## Decisions

- **uv_build over setuptools**: same toolchain as the rest of the project, metadata validation catches packaging mistakes early, no `[tool.*]` build config to maintain. Alternative kept on the table: hatchling — only needed if flexible layouts/build hooks ever appear; a plain-module CLI does not need it.
- **Pinned with upper bound** `uv_build>=0.13.6,<0.14`: uv's documented policy is that the backend follows uv's major-version releases; the bound protects future builds from breaking majors. Maintenance rule goes in AGENTS.md.
- **No `module-name`/`module-root` config needed**: the package is `bmv-cli` → uv_build's default module discovery expects `src/bmv_cli/__init__.py`, which the restructure provides. Zero config is the goal.
- **`--no-sources` as canonical build command**: uv's publishing guide recommends it so the artifact builds without uv-specific `tool.uv.sources` overrides — exactly what CD will run. Verified locally in this change.
- **Refresh `uv.lock`** after the backend swap so CI and CD resolve the new build dependency.

## Risks / Trade-offs

- [uv_build major releases force pin bumps] → Documented maintenance rule in AGENTS.md; minor bump cost, explicit.
- [Tests ship inside the wheel] → Accepted (uv_build packages the whole module); harmless for a small CLI; revisit only if wheel size/composition ever matters.
- [uv_build only supports pure Python] → Fine: this project is pure Python; if extension modules ever appear, migrate to hatchling.
- [Bundled-backend behavior: uv uses its embedded backend when version-compatible] → Deterministic as long as the pin range covers it; `uv.lock` pins `uv_build` for other frontends.

## Migration Plan

1. Edit `[build-system]`; delete `[tool.setuptools.packages.find]`.
2. `uv sync --extra dev` (rebuilds the editable install under the new backend); `uv lock` refresh.
3. `uv build --no-sources` → inspect `dist/` (sdist + wheel), sanity-install the wheel into a scratch venv and run `bmv --help`.
4. Run all four gates.
5. Single commit — revert restores setuptools.

## Open Questions

- None blocking.
