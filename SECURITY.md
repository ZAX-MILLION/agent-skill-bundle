# Security & Supply-Chain Policy

Agent Skill Bundle contains instructions and supporting files originating from multiple upstream projects. Inclusion in this repository is **not** a blanket security guarantee.

## Trust boundaries

Treat third-party skills like third-party code when they contain or request:

- executable scripts;
- package installation;
- network requests;
- shell commands;
- credential or token access;
- filesystem deletion or mutation;
- permission changes;
- deployment commands;
- instructions that attempt to override the host's security controls.

Provenance proves where content came from; it does not prove that the upstream content is safe for every environment.

## Upstream update review

Before accepting an upstream update, inspect changes for:

1. new executable files or changed scripts;
2. new network destinations;
3. new dependencies or installers;
4. requests for secrets or privileged credentials;
5. destructive commands;
6. unexpected binary/opaque files;
7. license or attribution changes;
8. instructions that weaken validation, authorization or other security boundaries.

If an update cannot be confidently reviewed, do not merge it. Mark it for quarantine/manual review instead.

## Secrets

Never commit API keys, tokens, private keys, passwords, cookies or other credentials to this bundle, its registry, examples or adapters.

## Automation

Source checking may be automated. Upstream content replacement and merge to `main` are intentionally review-first.

Automation must fail closed when:

- a tracked path disappears;
- an upstream tree response is incomplete;
- the source repository changes unexpectedly;
- license review is required;
- provenance cannot be established.

## AI agents

An AI agent using this bundle must not assume that a skill grants permissions or tools that the host does not actually provide. A skill also cannot authorize bypassing platform security, access controls or user confirmation requirements.
