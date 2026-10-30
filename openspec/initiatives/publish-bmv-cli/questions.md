# Questions

## Open Questions

- TBD

## Open Questions

- TBD

## Resolved Questions

### How do releases get triggered given GITHUB_TOKEN event suppression? (resolved 2026-10-28)

Tags created by release-please (via GITHUB_TOKEN) do not emit workflow events, so a tag-push-only trigger never fires. Solved with the PyPA-documented dual-trigger: `workflow_run` on Release Please completion (tag resolved from the run's head_sha) + hand-pushed `v*` tag trigger. Captured in the archived change's design.md and the `package-publishing` main spec.
