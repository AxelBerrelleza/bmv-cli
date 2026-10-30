# Spec Delta

## Purpose

Defines how OpenSpec changes are started, located, verified, and archived in Orca worktrees
for this project, so parallel changes follow one repeatable workflow.

## ADDED Requirements

### Requirement: Change worktree orchestration

When the user asks to start or continue an OpenSpec change, the workflow SHALL create or
reuse an Orca worktree bound to the change's branch `change/<name>`, brief the agent with the
applicable OpenSpec verb, and record ownership on the Orca card
(`comment: change: <name>`). Worktree names SHALL NOT be relied on for identity.

#### Scenario: Start a new change

- **WHEN** the user asks to start change `add-foo`
- **THEN** an Orca worktree is created on new branch `change/add-foo`, an agent is launched
  with a brief naming the OpenSpec change and the planning conventions, and the card comment
  reads `change: add-foo`

#### Scenario: Continue an existing change

- **WHEN** the user asks to continue change `add-foo` and branch `change/add-foo` exists
- **THEN** a worktree is created from that branch (`--base-branch change/add-foo`) and the
  agent is told to resume from `openspec status` remaining tasks

### Requirement: Change ownership discovery

When the user asks which worktree owns a change or what is in flight, the workflow SHALL
answer from Orca state (card comments and branch selectors) without requiring naming
conventions on worktrees.

#### Scenario: Find the owner of a change

- **WHEN** the user asks to find the worktree working on `add-foo`
- **THEN** the workflow resolves it from the `change: add-foo` card comment or the
  `branch:change/add-foo` selector and reports the owning workspace

### Requirement: Verification gate

Verification of a change SHALL include the OpenSpec verify workflow, the four documented
quality gates, and a secret scan, and SHALL report completion only when all pass.

#### Scenario: Verification passes

- **WHEN** verifying a change whose artifacts, gates, and scan are clean
- **THEN** the workflow reports verification passed and mirrors the state to the Orca card

#### Scenario: Verification fails on a leaked secret

- **WHEN** the secret scan flags a staged or working-tree file during verification
- **THEN** the workflow reports the finding as blocking and does not mark the change verified

### Requirement: Archive discipline

A change SHALL be archived on `main` as a small follow-up commit after its PR merges, and the
archive SHALL first re-check requirements the change modifies against the current main specs.

#### Scenario: Archive after merge

- **WHEN** the change's PR has merged and its tasks are complete
- **THEN** `openspec archive` runs on `main` and the spec delta lands as a follow-up commit

#### Scenario: Same-requirement re-check

- **WHEN** another archived change modified a requirement this change also modifies
- **THEN** the workflow surfaces the divergence (`openspec show <change> --diff`) and
  re-syncs the delta before archiving instead of replacing the requirement wholesale

### Requirement: Skill distribution

The workflow skill SHALL be shareable as an unlisted Orca skill bundle and installable on
another machine such that the same verbs behave identically there.

#### Scenario: Share and install

- **WHEN** the skill is published with `orca skills share` and installed on a second machine
- **THEN** all four verbs are available there and follow the same conventions
