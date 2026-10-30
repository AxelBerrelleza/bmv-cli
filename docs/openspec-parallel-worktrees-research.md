# Research: OpenSpec in Orca worktrees — parallel changes with shared context

**Status**: adopted — **in-repo planning** (Option A), 2026-10-29
**Scope**: run several OpenSpec changes at once, each in its own Orca worktree, sharing the
*context* of those changes between worktrees — with a low-friction UX for "create worktree →
explore a new change / apply an existing one / update / verify".

**Sources consulted**

- Local experiments: `openspec` CLI (1.4.1, later upgraded to **1.15.0**), throwaway git
  worktree of this repo, a throwaway store + GitHub repo (created and rolled back, see §4).
- Orca: the `orca-cli` skill's version-matched full guide via `orca-ide skills get orca-cli`,
  the bundled **`orchestration`** skill and its `placement-and-remote.md` /
  `messaging-and-gates.md` references, and the `automations.md` reference.
- Web (OpenSpec upstream, fetched 2026-10-29): README (Stores announcement),
  `docs/stores-beta/user-guide.md`, `docs/team-workflow.md`,
  `openspec-parallel-merge-plan.md`, `docs/cli.md`, `docs/customization.md`,
  `docs/concepts.md`, `docs/workflows.md`, `CHANGELOG.md` (v1.4→1.15 delta).

---

## 1. Findings

### 1.1 OpenSpec planning is checkout-scoped

`openspec status --json` reports `planningHome.root` = the current checkout's root. Each git/
Orca worktree has its own `openspec/` — parallel worktrees never collide **while working**,
but they don't see each other's uncommitted work. Sharing therefore happens through **git**
(committed branches) or through a **registered store** (one absolute path shared by all
worktrees). Those are the only two mechanisms.

### 1.2 Upstream's own answer to parallelism (`docs/team-workflow.md`)

- A change is a folder versioned like code: `git switch -c add-dark-mode` → `/opsx:propose`
  → `/opsx:apply` → **the PR contains the spec delta AND the code** → merge → `/opsx:archive`.
- "Two people, parallel changes": separate change folders don't collide; one change, one
  owner; the one conflict surface is `openspec/specs/` at archive time.
- **Archive after the PR merges** is upstream's recommended convention on teams.

### 1.3 The parallel-archive hazard (`openspec-parallel-merge-plan.md`)

Archive applies *requirement-level replace* semantics: if two archived changes modify the
**same requirement**, the second archive replaces the whole requirement block and **silently
drops** the first one's scenarios. Git does not warn. Upstream's fingerprint/sync remediation
is in flight; interim discipline: `openspec show <change> --diff` before archiving to see what
you replace, and re-sync if the requirement changed since you authored the delta.

### 1.4 Stores (the rejected alternative)

A **store** is a standalone planning git repo registered by name; a `store: <id>` line in
`openspec/config.yaml` routes every command in every worktree to it — **live** cross-worktree
sharing of in-flight changes (one absolute path on disk). Cost: a second repo, and plans
reviewed separately from code. Prototyped (public repo `AxelBerrelleza/bmv-plans`), then
rolled back in favor of in-repo planning — see §4.

### 1.5 Orca (orca-cli + orchestration skills)

- **Worktrees**: `worktree create --name <n> --base-branch <b> --no-parent --agent pi
  --prompt "<brief>" --json`; selectors (`branch:<b>`, `name:<n>`) address worktrees; `--setup
  run` runs repo setup hooks in fresh worktrees.
- **Shared state on the card**: `worktree set --comment "change: <name>"`,
  `--workspace-status todo|in-progress|in-review|completed`, `reference add <PR url>` — the
  live "who is doing what" plane (`worktree list/ps --json`).
- **Orchestration** (supervised coordination): Run/Task/Dispatch, `worker-start --worktree
  new-top-level`, blocking `ask`/`reply`, decision gates, `@worktree:<id>` group messaging.
- **Automations**: scheduled runs with `--precheck` gating.
- **`orca skills share`**: publish selected installed skills behind one unlisted link;
  `orca skills install` on the receiving side. (Delivery vehicle for a future shared UX skill.)

---

## 2. Options considered

| Option | Cross-worktree sharing | History / review | Footprint |
| --- | --- | --- | --- |
| **A. Tracked dir in this repo** ✅ shipped | **Git-mediated**: an in-flight change is visible to other worktrees once committed to a branch (fetch/branch off it) | Plans ride the code branch: one branch carries **change folder + code**, one PR reviews both (upstream's recommended team workflow) | One repo, zero extra machinery |
| **B. Separate planning repo** (store; prototyped, rolled back) | **Live**: one registered absolute path shared by all worktrees | Plans reviewed in their own PRs, separately from code | Second repo to maintain |
| **C. Gitignored dir inside this repo folder**, registered store (`--no-init-git`) | **Live** (registered absolute path) | None — plans have no git history | One folder, no repo |

Decision: **A**. Git-mediated sharing is sufficient (context = committed work), and it keeps
plan + code review in one PR, in one public repo. The live-sharing benefit of B did not
justify a second public repo and a separate review stream.

## 3. Shipped conventions (AGENTS.md)

1. One change per branch (`change/<name>`, branch name == OpenSpec change name) and per
   worktree; one writer per change folder; ownership recorded via
   `orca worktree set --worktree active --comment "change: <name>"` (worktree names are
   irrelevant).
2. Cross-worktree context travels through git: commit the change folder to its branch and
   push. To explore/continue an existing change, create the worktree **from its branch**
   (`orca worktree create --base-branch change/<name> …`).
3. Archive after the change's PR merges: `openspec archive <name>` on `main` as a small
   follow-up commit (upstream's "archive after merge").
4. Public repo: no secrets/private intel in planning artifacts or code; gitleaks before
   verify/archive (enforced by hook + CI).
5. Same-requirement check before archiving (`openspec show <change> --diff`, re-sync) — §1.3.

## 4. The secret/intel guard (note #1)

**Research outcome: OpenSpec has no hard hooks.** `rules`/`operations.*.guidance` are
explicitly "not an enforceable check" (advisory, injected at execution time via
`openspec instructions apply/archive`). Upstream itself points at git pre-commit hooks as the
enforcement pattern. The guard is layered:

- `openspec/config.yaml` — `context` (public-repo constraint, injected into every artifact
  prompt) + `operations.apply/archive.guidance` (gitleaks before verify and archive; archive
  convention; same-requirement re-check)
- `.githooks/pre-commit` (enable once per clone: `git config core.hooksPath .githooks`):
  `gitleaks protect --staged` + `openspec validate --all`
- `.github/workflows/secret-scan.yml`: gitleaks on every push/PR (pinned `ubuntu-24.04` tier)
- Non-secret "intel" cannot be scanned: covered by the `context` constraint + human PR review.

## 5. Rollback note (2026-10-29)

The store prototype was fully undone before adopting A: planning content moved back into the
repo, the two unpushed store-era commits discarded and re-authored to the in-repo convention,
the `bmv-plans` GitHub repo deleted, and the local store deregistered. The `publish-bmv-cli`
initiative docs (from the old 1.4.1 context store) live at
`openspec/initiatives/publish-bmv-cli/`.

## Appendix: verification notes

- Web sources fetched 2026-10-29 via curl (Ollama web tools were unavailable).
- `openspec` upgraded 1.4.1 → 1.15.0 (npm global); skills regenerated to `generatedBy: 1.15.0`
  in `~/.agents/skills/` (global delivery; after future `openspec update` runs, re-sync with
  `rm -rf ~/.agents/skills/openspec-* && mv .agents/skills/openspec-* ~/.agents/skills/`,
  keeping `.agents/skills/.openspec-target` — the shared-skills-root ownership marker, tracked
  in git).
- Workflows installed: `propose, explore, new, continue, apply, update, ff, sync, archive,
  bulk-archive, verify, onboard` (12; `update` added over the old 1.4.1 set).
