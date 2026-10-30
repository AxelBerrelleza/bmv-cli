## Why

The `Quality gates` CI job currently runs on `runs-on: ubuntu-latest` (4 vCPU VM). That label has two problems:

- **Silent OS migration**: `ubuntu-latest` will be repointed from Ubuntu 24.04 to Ubuntu 26.04 in November 2026 (per the `actions/runner-images` announcements), changing the OS our gates run on without any workflow change.
- **No right-sizing**: GitHub now offers a spectrum of Linux runner tiers — the standard VMs (`ubuntu-24.04`, `ubuntu-26.04`, `-arm` variants) and the official `ubuntu-slim` container runner (1 vCPU / 5 GB, GA Jan 2026, optimized for lightweight jobs like linting, formatting, and small test suites). Our CI job completes in ~16 s end-to-end with only a few seconds of actual compute, so it is exactly the profile `ubuntu-slim` targets — but `ubuntu-slim` brings constraints (15-minute job cap, unprivileged container) that need an explicit evaluation, not a blind switch.

`cd-release-automation` (change 4) will add a publish job that depends on these same conventions; picking and pinning the runner tier now gives that change a decided baseline instead of inheriting `ubuntu-latest` by default.

## What Changes

- **Evaluate the candidate runner tiers** for this repo's Linux CI jobs on a documented decision matrix:
  - `ubuntu-slim` — 1 vCPU/5 GB container, smallest and cheapest model, 15-min job timeout, unprivileged container (no Docker-in-Docker), image ships Python 3.12 + Git
  - `ubuntu-latest` — status quo (4 vCPU VM), but subject to silent OS bumps (24.04 → 26.04 in Nov 2026)
  - `ubuntu-24.04` — pinned 4 vCPU VM, immune to `-latest` repointing
  - `ubuntu-26.04` — newest GA x64 VM image
  - `ubuntu-24.04-arm` — free arm64 VM (image managed by Arm); adds arm architecture coverage but different CPU arch (prebuilt wheels, `uv` availability consistent; recompilation performance differs)
- **Selection criteria**: compute fit (no timeout/1-vCPU starvation risk), stability (no silent OS/arch changes), job latency, isolation constraints (container vs VM), and forward-compatibility with the `publish.yml` build+publish job from `cd-release-automation`.
- **Update every Linux GitHub-hosted job to the selected tier** across all three workflows: `.github/workflows/ci.yml` (`Quality gates` job), `.github/workflows/publish.yml` (build + publish jobs — already live from `cd-release-automation`), and `.github/workflows/release-please.yml` (release PR automation). One tier for all Linux jobs keeps the environment surface the gates must validate green to a single BOSS.
- **Update docs** (AGENTS.md CI note and the main `continuous-integration` spec) so the runner tier is a declared, reviewable property of CI rather than an accident of the `ubuntu-latest` default.

## Capabilities

### New Capabilities
<!-- None — this change refines an existing capability. -->

### Modified Capabilities
- `continuous-integration`: the runner-tier requirement — CI jobs SHALL run on a pinned/selected GitHub-hosted runner tier recorded in the workflow (replacing the implicit `ubuntu-latest` default introduced by `ci-quality-gates`), with the choice justified and documented so follow-on workflows (publish) use the same policy.

## Impact

- **Files**: all three workflow files get their `runs-on` lines pinned (`.github/workflows/ci.yml`, `.github/workflows/publish.yml`, `.github/workflows/release-please.yml`), AGENTS.md CI note, `openspec/specs/continuous-integration/spec.md` (runner requirement delta).
- **Risk**: all `ubuntu-slim`/`arm`/new-OS options change the execution environment (container vs VM, OS version, CPU arch) — gates must be re-verified green after the switch; the 15-min cap of `ubuntu-slim` must be shown to have wide headroom over actual run duration.
- **Cost**: none — this repo is public, so all standard GitHub-hosted runners (including `ubuntu-slim`) are free and unlimited; the decision is about fit and stability, not billing.
- **Downstream**: none remaining — `cd-release-automation` has already shipped; the policy applies to its already-live `publish.yml` jobs directly in this change.
