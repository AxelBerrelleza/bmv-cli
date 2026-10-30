## 1. Pin the runner tier in workflows

- [x] 1.1 Change `runs-on: ubuntu-latest` → `runs-on: ubuntu-24.04` in `.github/workflows/ci.yml` (`Quality gates` job)
- [x] 1.2 Apply the same `runs-on: ubuntu-24.04` pin to every Linux job in `.github/workflows/publish.yml` (build + publish jobs) and `.github/workflows/release-please.yml`

## 2. Verify

- [x] 2.1 Push a verification branch, confirm all touched workflows trigger and go green end-to-end (same step layout, only `runs-on` differs; check queue/latency shows no regression acceptable for ±few seconds) — PR #9: push + PR runs green on `ubuntu-24.04` (runner label confirmed, all steps ✅, ~11s vs 16s baseline)

## 3. Docs

- [x] 3.1 Update the AGENTS.md CI note to declare the pinned runner tier (`ubuntu-24.04` for all Linux jobs) — runner-tier changes must update both the docs and the workflows together
- [x] 3.2 Confirm the delta spec's scenarios match the implemented state (no workflow uses `ubuntu-latest`; the runner policy is declared in AGENTS.md and the workflows) — grep: 0 occurrences of `ubuntu-latest`, 4× `runs-on: ubuntu-24.04`, policy noted in AGENTS.md
