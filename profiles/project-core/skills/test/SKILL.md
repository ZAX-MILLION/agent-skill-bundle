---
name: test
description: Select and run the right tests for a project change, from focused regression checks to broader release gates, and report evidence without overstating coverage.
---

# Test workflow

1. Identify the behavior that changed and the failure/regression the test must catch.
2. Prefer the smallest deterministic test that proves that behavior.
3. For bug fixes, reproduce the failure before the fix when practical.
4. Run focused tests first for fast feedback.
5. Expand to type/lint/security/integration/full-suite checks when the change crosses boundaries or is release-sensitive.
6. Test failure paths, permissions, data preservation, localization, and rollback where relevant.
7. Do not replace real runtime/device/browser verification with static tests when the task depends on actual UI/native behavior.
8. Record the exact commands/checks run and their observed result.
9. A passing test is evidence for what it covers, not proof that deployment, migration, release, or production behavior succeeded.
