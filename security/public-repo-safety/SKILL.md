---
name: public-repo-safety
description: Protect public skill repositories against leaked secrets, project-specific operational details and unreviewed supply-chain imports.
---
# Public repository safety

1. Assume all tracked files, PR diffs and prior public commits may be copied. Only generic authorized content belongs here.
2. Run scripts/public_repo_gate.py before release, and the private owner-denylist check when available. Do not echo matched values. Review added binaries, images and third-party scripts manually.
3. Keep QA accounts, production incidents, security findings, private endpoints, server topology and user data in a restricted project workspace or vault.
4. Preserve upstream authorship and license; review dependency/network/dangerous-command changes before import.
5. Existing approved upstream documentation examples are pinned by exact blob hashes. Any change loses approval until reviewed again.
6. On an exposure revoke/rotate credentials, assess access and notify the affected owner. Deletion commits do not erase history or outside copies.
7. A skill does not grant root, SSH, social, browser, database or Cloudflare access.
