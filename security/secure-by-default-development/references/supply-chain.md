# Dependency & Supply-Chain Security Gate

Use this reference whenever adding/updating packages, plugins, themes, SDKs, containers, build tools, CI actions, binaries, scripts, or third-party integrations.

## Before adding anything

- Ask whether an existing framework/stdlib/project dependency can solve the need safely.
- Verify the exact package/plugin/repository identity; watch for typo-squatting and similarly named packages.
- Check maintenance activity, release history, ownership/provenance, license, security posture, and whether the requested permissions are reasonable.
- Prefer mature, narrowly scoped dependencies over obscure packages for trivial functionality.
- Do not install nulled/cracked/pirated plugins, themes, or packages.

## Version and integrity discipline

- Preserve and commit lockfiles where the ecosystem uses them.
- Avoid floating/unpinned production dependencies where reproducibility matters.
- Review major upgrades and security auto-fixes rather than blindly accepting breaking dependency graph changes.
- Use package-manager integrity mechanisms/checksums/signatures when the ecosystem provides them.
- Pin external CI/action/container references appropriately for the project's risk and update strategy.

## Install/build scripts

Treat install hooks, postinstall scripts, binaries, generators, and downloaded executables as code execution.

Review for:

- network downloads;
- shell execution;
- credential reads;
- filesystem writes outside the project;
- telemetry/data collection;
- privilege escalation or broad permissions;
- code generation that enters the production artifact.

Do not run suspicious scripts with production credentials or elevated privileges merely to inspect them.

## Third-party SDK/data boundary

- Determine what data the SDK sends, to which destinations, and whether it collects more than required.
- Keep sensitive/private data separated from analytics/ads/telemetry unless explicitly intended and compliant with the product's privacy obligations.
- Limit API scopes, OAuth scopes, webhook permissions, cloud roles, and tokens to the minimum needed.

## Vulnerability handling

- Run the ecosystem's vulnerability/dependency audit tooling where available.
- New known critical/high vulnerabilities introduced by the change require resolution, replacement, mitigation, or an explicit risk decision.
- Do not treat an audit command returning zero findings as proof that the dependency is trustworthy.

## Adversarial checks

- package name resolves to intended publisher/repository;
- dependency does not require unexpected install-time network/secret access;
- lockfile reflects the intended change only;
- new SDK does not receive sensitive payload fields unnecessarily;
- container/base image is from intended source and not running with needless privilege;
- CI third-party action/tool is pinned/reviewed according to project policy.

## Release blockers

- unknown/typo-squatted dependency used without provenance verification;
- cracked/nulled package/plugin/theme;
- dependency install script unexpectedly accesses secrets or privileged host resources;
- new critical/high vulnerability is knowingly introduced with no mitigation/risk decision;
- third-party SDK receives sensitive data without necessity/approval;
- production build fetches/executes mutable arbitrary remote code without an intentional trust model.
