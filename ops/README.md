# Server-side updater

This repository does not require GitHub Actions to monitor upstream skill changes. A Linux server can run the included systemd timer instead.

## Safety model

- The timer never merges to `main`.
- Only canonical entries already classified `UPDATE_AVAILABLE` are selected automatically.
- Exact upstream copies are prepared on a new `upstream-sync/...` review branch.
- Pushing that review branch is disabled by default.
- Baseline differences, legacy-derived skills, local skills, reference specs and collections requiring manual handling are never silently selected.

## Initial setup

Recommended checkout: `/srv/agent-skill-bundle` owned by a dedicated unprivileged user named `agent-skill-bundle`.

Before enabling the timer, create and review the initial audit baseline once:

```bash
cd /srv/agent-skill-bundle
python3 scripts/check_upstreams.py --write
python3 scripts/audit_skills.py --write
git diff -- registry/
```

Review the output before committing registry metadata. An initial `DIFFERS_FROM_UPSTREAM` state is intentionally not treated as permission to overwrite a skill.

## Install timer

```bash
sudo cp ops/systemd/agent-skill-bundle-update.service /etc/systemd/system/
sudo cp ops/systemd/agent-skill-bundle-update.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now agent-skill-bundle-update.timer
```

Check it with:

```bash
systemctl status agent-skill-bundle-update.timer
journalctl -u agent-skill-bundle-update.service
```

## Optional review-branch push

By default the updater only prepares a local review branch. To publish review branches to GitHub, configure a scoped deploy key or other repository credential for the dedicated service user and create:

`/etc/agent-skill-bundle/update.env`

```text
PUSH_UPDATES=1
```

Do not put private keys, tokens or passwords in this repository. Test `git push` interactively as the service user before enabling automatic review-branch pushes.

Even with `PUSH_UPDATES=1`, the updater does not merge the branch.

## Main branch protection

For a production distribution repository, protect `main` with a GitHub ruleset/branch protection rule: require pull requests/review for changes, disallow force pushes, and disallow branch deletion. This is a repository setting, not something the updater can enforce from inside the repository.
