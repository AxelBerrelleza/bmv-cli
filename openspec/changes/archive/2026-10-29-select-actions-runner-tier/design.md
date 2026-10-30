## Context

`ci-quality-gates` (archived 2026-10-28) added `.github/workflows/ci.yml` with a single `Quality gates` job on `runs-on: ubuntu-latest`. The job's observed profile: ~16 s wall time end-to-end, with the four gates (ruff format check, ruff check, mypy, pytest-8-tests) contributing only a few seconds of compute; `uv sync` dominates the rest. No Docker, no elevated-privilege steps, no `macos`/`windows` needs.

GitHub now offers a wider runner spectrum than when that change landed:

- `ubuntu-slim` — official GA (Jan 2026): 1 vCPU / 5 GB **container** (not a VM), aimed at "automation tasks, issue operations, linting and formatting, short-running jobs"; hard **15-minute job timeout**; unprivileged container (no Docker-in-Docker/kernel features); image: Ubuntu 24.04 base with Python 3.12.3, Git, uv-compatible tooling.
- `ubuntu-latest` — today: 4 vCPU / 16 GB VM; **announced to repoint from Ubuntu 24.04 to 26.04 in November 2026**, i.e. the OS under our gates will silently change.
- `ubuntu-24.04` / `ubuntu-26.04` — same 4 vCPU / 16 GB VM specs, pinned OS version.
- `ubuntu-24.04-arm` / `ubuntu-26.04-arm` — 4 vCPU / 16 GB **arm64** VMs, free in public repos, images managed by Arm.

The repo is **public** → all of the above standard tiers are free and unlimited, so billing is not a decision factor; fit, stability, and latency are.

Resource ceiling check for the gates job on `ubuntu-slim`: current total run is ~16 s including provisioning; the 15-min cap leaves ~98% headroom — not marginal today. The real constraint differences are the 15-min ceiling (creeps in if the suite ever grows, or if other jobs are moved onto the tier) and the unprivileged container model.

## Goals / Non-Goals

**Goals:**
- Pick the runner tier(s) for `ci.yml`'s `Quality gates` job on a scored, documented matrix — replacing the accidental `ubuntu-latest` default with a deliberate choice.
- Eliminate silent environment changes: no OS repointing under our feet (the `ubuntu-latest` → 26.04 November 2026 migration must not happen invisibly).
- Fix the runner policy for `cd-release-automation`'s future `publish.yml` build+publish job so change 4 doesn't inherit an ambiguous default.
- Verify the gates remain green after any switch.

**Non-Goals:**
- Self-hosted runners, larger runners (Team/Enterprise-Gated), or GPU runners — unsuitable scale-wise for this repo.
- Windows/macOS jobs (no cross-plat artifacts planned for publish; `bmv-cli` is pure-Python).
- Cost optimization — every candidate is free for public repos.
- Re-running the publish job on multiple architectures to ship arm wheels (pure-Python wheel is `py3-none-any`).

## Decisions

### Decision: `Quality gates` job runs on `runs-on: ubuntu-24.04` (pinned x64 VM)

**Decision matrix** (scored against this repo's actual profile, 1 = poor, 5 = excellent):

| Criterion | weight | `ubuntu-slim` (1 vCPU container) | `ubuntu-24.04` (pinned VM) | `ubuntu-26.04` (newest VM) | `ubuntu-latest` (4-core VM, will repoint) | `ubuntu-24.04-arm` |
|---|---|---|---|---|---|---|
| Compute fit / growth headroom | high | 4 (fast enough today; **15-min hard cap** is the growth ceiling) | 5 (4 vCPU, no cap) | 5 | 5 | 5 |
| Stability (no silent env change) | high | 4 (pinned container image, but image model younger) | **5 (pinned OS, standard belt-and-suspenders VM)** | 5 (pinned) | **1 (repoints to 26.04 Nov 2026 silently)** | 4 (pinned) |
| Job latency | medium | 4 (container start can be faster than VM boot; 1 vCPU slightly slower gates; net near-parity) | 4 (observed: green in ~16 s) | 4 | 4 | 3 (often longer queue times in peaks, historically preview) |
| Isolation / compatibility | medium | 3 (unprivileged container: no Docker-in-Docker, no sudo-level ops; 15-min cap complicates job reuse) | 5 (full VM, everything available) | 5 | 5 | 4 (arm caveats: nonetheless standard-supported) |
| Forward-fit for `publish.yml` (build+publish via uv + OIDC) | high | 3 (fine now, but any future heavier publish steps inherit the same cap) | 5 (no cap, standard parity with docs/Astral examples) | 5 | 4 | 4 |
| **Weighted result** | | **3.4** | **4.9** | **4.9** | **2.9** | **4.0** |
| **+ qualitative verdict** | | Viable, smallest blast radius machine, but ceiling-constrained | **Selected: pinned, standard, headroom** | Equal score but no added value for gates | Rejected: silent OS migration | Rejected: arch is a non-requirement for pure-Python CI |

**Rationale for `ubuntu-24.04` over `ubuntu-slim`, given the numbers are close:**
- `ubuntu-slim` saves nothing that matters here (cost: nil on a public repo; latency: near-parity with 1 vCPU partly offsetting faster container startup) while introducing two standing constraints: the **15-minute hard cap** and the **unprivileged container**. CI jobs tend to accrete steps (release-please, publish, coverage) — a tier with a hard timeout ceiling is the wrong default for the *shared* runner policy even if the gates job fits comfortably.
- `ubuntu-24.04` is strictly the status quo minus the `latest` footgun: same specs, same observed ~16 s green runs, no migration to prepare for, and parity with the Astral/uv documentation examples that `publish.yml` will follow in change 4.
- Pinning also makes the eventual 26.04 upgrade a **deliberate, reviewable diff** (change `ubuntu-24.04` → `ubuntu-26.04` when motivated) rather than an automatic surprise.

### Decision: all Linux hosted-runner jobs across the repo run on `ubuntu-24.04`

`cd-release-automation` has already shipped: `publish.yml` (build + publish jobs, trusted publishing via `uv publish`) and `release-please.yml` are live on `ubuntu-latest`. All of those Linux jobs are pinned to `ubuntu-24.04` here — release-critical jobs especially benefit from the VM tier (no 15-min cap) and a single declared tier keeps the repo's Actions convention simple.

### Decision: keep x64, keep one pinned OS across all Linux jobs

Not going `arm`, not going `26.04` now, not going `ubuntu-slim` — all documented above. A single tier across all Linux workflows minimizes the environment surface the gates must be green on, matching the "reproducible toolchain" spirit already established (pinned uv, pinned action SHAs).

## Risks / Trade-offs

- [Pinned OS drifts from newest stack] → 24.04 is the LTS repo targets anyway (`.python-version` 3.12 is the image's native Python); upgrade to 26.04 is one reviewable line when motivated.
- [We're trading away the free "extra arm coverage" the arm tier could give] → Rejected deliberately: pure-Python package, no arm consumers; can be added later as an additional job if arm validation ever matters.
- [Gates don't exercise 1-vCPU/container paths we might encounter later] → If a future job (e.g. scheduled lint, issue automation) is genuinely tiny, it can still opt into `ubuntu-slim` explicitly per the documented policy — this change just sets the **default** tier.
- [Runner-image deprecation policy exists (2 GA images max)] → Pinning to 24.04 means a future deprecation deadline must be honored with an explicit line-change; acceptable and visible.
- [Switching runner tier could expose network/cache behavior differences] → Mitigation: single verification run (task 2.1) on the branch before merge — same step layout, only `runs-on` differs.

## Migration Plan

1. Change `runs-on: ubuntu-latest` → `runs-on: ubuntu-24.04` in `.github/workflows/ci.yml` `Quality gates` job.
2. Verification branch: push, confirm workflow triggers and goes green end-to-end (steps layout unchanged).
3. Docs: update the AGENTS.md CI note to declare the pinned runner tier; update the main `continuous-integration` spec requirements at archive-time via the delta spec.
4. `publish.yml` and `release-please.yml` get the same `runs-on: ubuntu-24.04` pin in the same sweep (all three workflows change together so the policy is applied atomically).

Rollback: revert the `runs-on` line.
