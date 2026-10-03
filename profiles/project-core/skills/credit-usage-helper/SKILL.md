---
name: credit-usage-helper
description: Keep Project Core agent credit and context use efficient. Use for long tasks, multi-file exploration, skill loading, or deciding whether specialist retrieval or repo-wide analysis is justified.
---

# Project Core credit / context efficiency

1. Use the installed core skills first.
2. Retrieve a specialist only when the current task clearly needs it.
3. Read the smallest useful file/range before broad repository scans.
4. Batch related searches and checks; do not repeatedly read the same large output.
5. Use Graphify/Graft only when they save meaningful exploration work.
6. Prefer focused tests first; use broader suites when scope/risk justifies them.
7. Avoid speculative refactors, decorative docs, and reinstalling healthy tooling.
8. Keep human-facing responses action-first and concise; keep detailed evidence in commits/tests/PRs when useful.
9. Security and verification gates are never skipped to save credits.
10. Do not load the complete vault into native discovery or active context "just in case".
