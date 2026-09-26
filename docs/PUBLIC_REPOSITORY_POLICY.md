# Public repository policy

This repository is public. Only generic, legally reusable skills and authorized examples belong here.

Never publish QA passwords, session cookies, tokens, private keys, real account identifiers, private administrative endpoints, network maps, raw environment files, user data, or live security assessment details. Store these in separate private workspaces or a credential manager.

Before each release:
1. Run python3 scripts/public_repo_gate.py . and perform a manual diff review.
2. For owner-specific names/domains, run the same command with --private-denylist pointing at a file outside this repository (one marker per line). Never commit or print that list.
3. Vet any external dependency, script, browser access, network destination, license and provenance. The pinned documentation exceptions in registry/approved-public-examples.json apply only to exact reviewed Git blob SHAs.
4. Enable branch protection and require the public-content CI check using GitHub settings; this workflow by itself cannot force review or stop administrator bypasses.

Deleting a file from main does not clean historical commits, PR diffs, forks, clones, or search caches. For a real exposure, revoke/rotate credentials, review application access, notify the affected owner, make the repository private if feasible, then coordinate a deliberate Git history rewrite and cache cleanup. Rewriting public history can break clones, branches and PRs; never claim complete erasure of copies outside your control.

The scanner is heuristic, checks tracked HEAD files rather than all past revisions, and cannot inspect secret data inside screenshots or opaque binaries. Manual and historical reviews remain necessary.