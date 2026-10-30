# Proposal

## Why

The glue between Orca worktrees and OpenSpec changes — wiring a worktree to a
`change/<name>` branch, recording ownership, running verify + quality gates + secret scan,
and archiving at the right moment — is currently re-told to every agent session in prose.
AGENTS.md holds the conventions, the 12 `openspec-*` skills hold the OpenSpec verbs, and the
`orca-cli` skill holds worktree mechanics, but no single instruction performs the combined
dance. Capturing it as one skill makes the workflow one command and portable to other
machines. This change is deliberately planned now and **deferred**: implement only after the
manual workflow shows which glue is actually missing (per the 2026-10-29 decision).

## What Changes

- New skill `openspec-orca-change` (a `SKILL.md` in `~/.agents/skills/`) encoding four verbs:
  **start** (create change worktree + brief agent + ownership comment), **find** (locate the
  worktree owning a change), **verify** (OpenSpec verify + four quality gates + gitleaks),
  **archive** (post-merge follow-up commit after same-requirement re-check).
- Delivery via `orca skills share` (one unlisted bundle link; installable on other machines).
- One-line pointer in AGENTS.md so sessions know the skill exists.

## Capabilities

- **New Capabilities**:
  - `change-workflow` — how OpenSpec changes are started, located, verified, and archived in
    Orca worktrees for this project.
- **Modified Capabilities**: (none)

## Impact

- Tooling/docs only: no product code, no API, no dependency changes.
- Touches: `~/.agents/skills/openspec-orca-change/` (outside the repo), `AGENTS.md` (pointer
  line). No change to the `openspec-*` skills or the `orca` CLI.
