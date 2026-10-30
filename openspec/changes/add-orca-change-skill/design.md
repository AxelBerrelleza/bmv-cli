# Design

## Context

Conventions live in AGENTS.md (branch-per-change `change/<name>`, one writer per change,
ownership via card comment, archive-after-merge, gitleaks discipline, same-requirement
re-check). The 12 `openspec-*` skills (global `~/.agents/skills/`) cover the OpenSpec verbs;
the bundled `orca-cli` skill covers worktree/terminal mechanics. The gap is only the glue:
the combined "worktree + branch + brief + ownership + gates + scan + archive timing" dance.
See proposal.md - Why.

## Goals / Non-Goals

**Goals:**
- One `SKILL.md` that a session can load to perform start/find/verify/archive correctly
- Recipes reference AGENTS.md as the single source of truth for conventions (no duplicated
  rules to drift)
- Shareable via `orca skills share` so another machine gets identical behavior

**Non-Goals:**
- No code, scripts, or dependencies; no changes to `openspec-*` or `orca` skills
- No worktree-naming enforcement (names are irrelevant; identity is the card comment)
- Not a replacement for the OpenSpec skills — this skill only orchestrates around them

## Decisions

- **Skill id `openspec-orca-change`, single file.** Four verb sections with concrete
  `orca`/`openspec` command lines. Alternative: multi-file skill with references — rejected
  for now; the content fits one file and stays reviewable.
- **Identity via card comment `change: <name>` and branch selector `branch:change/<name>`.**
  Alternative: worktree naming convention — rejected (user preference, 2026-10-29).
- **Delivery via `orca skills share`.** Requires the default-off Settings → Share Skills
  permission and must run from an Orca terminal on the machine whose skills are shared (WSL
  wrinkle observed 2026-10-29). Alternative: commit the skill to this repo — rejected for now
  (it is cross-repo glue, not project code); revisit if sharing friction appears.
- **Implement only after real friction.** This change is the plan; the task list is executed
  when the manual workflow reveals which glue is genuinely missing.

## Risks / Trade-offs

- [Conventions drift between AGENTS.md and the skill] → the skill references AGENTS.md by
  pointer and repeats only command lines, never rules
- [Share/install skips user-edited copies silently at update time] → keep skill edits in this
  change's PR history; re-share intentionally
- [orca CLI flags change between releases] → recipes cite `orca ... --help` recovery in each
  verb instead of relying on memorized flags
