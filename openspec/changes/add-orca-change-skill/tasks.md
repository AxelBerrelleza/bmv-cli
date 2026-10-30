# Tasks

## 1. Skill authoring

- [ ] 1.1 Write `~/.agents/skills/openspec-orca-change/SKILL.md` with the four verbs
  (start/find/verify/archive) as concrete `orca` + `openspec` command recipes, and verify the
  skill loads in a pi session (appears in the skill list with a routable description)
- [ ] 1.2 Verify each verb against reality: run `start` for a throwaway change and observe the
  worktree + branch + card comment; run `find` and get the owning worktree back

## 2. Delivery

- [ ] 2.1 Publish the skill with `orca skills share --skill openspec-orca-change
  --bundle-name "OpenSpec x Orca"` from an Orca terminal on this machine, and verify the
  command returns an unlisted bundle link
- [ ] 2.2 Install the bundle on a second machine (or agent) and verify all four verbs resolve
  there with the same behavior

## 3. Integration

- [ ] 3.1 Add the one-line AGENTS.md pointer to the skill, and verify a fresh session
  mentions/loads the skill when asked to start a change
- [ ] 3.2 Trial one real change end-to-end (start -> apply -> verify -> archive) using only
  the skill, and verify the archive lands as the post-merge follow-up commit per convention

## Workflow follow-up

- Archive the change after the project's review requirements are satisfied.
- Verify the archived result (`openspec validate --archived`).
