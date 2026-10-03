---
name: task-to-pr
description: Turn an approved project task into a small, verified branch and pull request without silently merging or deploying. Use when ADMIN wants implementation delivered through Git/GitHub.
---

# Task to PR

1. Inspect the current branch, project rules, active work, and the files/tests relevant to the task.
2. Preserve stacked branch dependencies and working configuration.
3. If a new branch is appropriate, create a focused branch from the intended base; do not silently change the target branch.
4. Implement only the requested scope and avoid unrelated cleanup.
5. Run the smallest relevant tests, then the project's required quality/security gates.
6. Review the diff for secrets, generated junk, accidental files, data-loss risk, and unrelated changes.
7. Commit with a clear message and open/update a PR with:
   - what changed
   - why
   - verification evidence
   - deployment/migration/build state stated separately
8. Do not merge, deploy, publish, apply migrations, or release unless ADMIN explicitly authorizes that action.
9. Never claim success from an attempted command alone; verify the resulting branch/PR/state.
