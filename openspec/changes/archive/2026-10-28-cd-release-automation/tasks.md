## 1. Release Please workflow

- [x] 1.1 Create `.github/workflows/release-please.yml`: on push to `main`, `googleapis/release-please` action (pinned by SHA + version comment) with `release-type: python`, `token` = default GITHUB_TOKEN (`permissions` limited to what release-please needs: contents/PR write on that job only)
- [x] 1.2 Bootstrap `CHANGELOG.md` (Keep a Changelog-style header + Unreleased 0.1.0 notes) so release-please appends from the first release PR — adjusted: header-only bootstrap (with maintenance comment); release-please generates the initial [0.1.0] section from commit history itself, avoiding a stale hand-written Unreleased section

## 2. Publish workflow

- [x] 2.1 Create `.github/workflows/publish.yml` triggered on tag push `v*` with two jobs:
- [x] 2.2 **build job**: checkout (pinned), `astral-sh/setup-uv` (pinned, as in ci.yml), `uv sync --extra dev`, `uv build --no-sources`, tag↔version check (compare `github.ref` tag with the project version — fail on mismatch), upload `dist/` via actions/upload-artifact; optionally smoke-run `uv run pytest` (implementer's discretion) — included
- [x] 2.3 **publish job** (needs build, no checkout of the source tree beyond what `uv publish` requires): download the `dist/` artifact, `uv publish` with `permissions: id-token: write` and `environment: pypi`; then attach `dist/*` to the `vX.Y.Z` GitHub Release (e.g. `gh release upload` with the job's GITHUB_TOKEN) — release upload skips gracefully when no GitHub Release exists (hand-pushed tags)
- [x] 2.4 Verify no token/password inputs or repo secrets are referenced anywhere in the workflow (Trusted Publishing only) — verified: only `id-token: write` and auto-provisioned `github.token`; all workflows parse as valid YAML

## 3. Docs

- [x] 3.1 Add a Release section to AGENTS.md: the release flow (conventional commit → release PR → merge → auto tag/build/publish), the hard constraint that the workflow filename stays `publish.yml` and environment stays `pypi` (trusted-publisher binding), and a pointer to the initiative's manual tasks ②–⑤
- [x] 3.2 Update the initiative `tasks.md` coordination checklist: confirm manual tasks ②–④ are listed and unchanged (repo-name decision, GitHub `pypi` environment, PyPI pending trusted publisher: `bmv-cli` / `AxelBerrelleza` / repo / `publish.yml` / `pypi`) — all three verified done and checked off; checklist updated with archive statuses

## 4. First-release dry run (after user manual tasks ②–④ are done)

- [x] 4.1 Merge the first release-please PR (v0.1.0) and confirm: tag created → publish.yml green → `bmv-cli` claimed on PyPI at https://pypi.org/project/bmv-cli/ → GitHub Release lists sdist+wheel assets — DONE: PR #5 merged, tag v0.1.0 cut, publish run 40639768101 green after user approved the `pypi` environment deployment; release assets `bmv_cli-0.1.0-py3-none-any.whl` + `bmv_cli-0.1.0.tar.gz` attached
- [x] 4.2 Verify installability from PyPI (`uv tool install bmv-cli` → `bmv --help`) — also checks initiative manual task ⑤ — DONE: installed from PyPI; `bmv --help` lists all commands; live `price`/`credits` calls work with `BMV_API_TOKEN` exported. Note: `.env` auto-discovery does not work for the installed tool (python-dotenv searches from the module's directory, not the cwd) — documented as a follow-up fix candidate (usecwd=True in client.py) to ship as 0.1.1
